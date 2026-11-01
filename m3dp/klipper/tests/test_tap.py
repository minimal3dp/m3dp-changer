"""TAP gates run real macro code; no physical probe or homing is connected."""
import pytest
from extras.gcode_macro import TemplateWrapper
from klipper_harness import CommandError
from test_toolchange import make_printer


def activate_probe(p):
    # Run the exact [probe] activate_gcode template Klipper would execute.
    template=TemplateWrapper(p,p.objects['gcode_macro'].env,'probe:activate_gcode',
                             p.sections['probe']['activate_gcode'])
    template.run_gcode_from_command()

@pytest.mark.parametrize('tool',[-1,1,5])
@pytest.mark.parametrize('command',['G28','G28 Z','QUAD_GANTRY_LEVEL','BED_MESH_CALIBRATE'])
def test_homing_and_bed_probing_reject_missing_or_wrong_reference_tool(tool,command):
    p=make_printer(tool)
    with pytest.raises(CommandError,match='TAP requires'):
        p.run(command)
    assert not p.hardware_events
    assert not p.moves
    assert not p.waits

@pytest.mark.parametrize('command',['G28','G28 Z','QUAD_GANTRY_LEVEL','BED_MESH_CALIBRATE'])
def test_live_reference_sensor_must_be_present_before_native_probe_or_home(command):
    p=make_printer(0)
    p.objects['filament_switch_sensor cx_tool_sensor'].data['filament_detected']=False
    with pytest.raises(CommandError,match='not detected'):p.run(command)
    assert not p.hardware_events
    assert not p.moves

@pytest.mark.parametrize('command',['G28 Z','QUAD_GANTRY_LEVEL','BED_MESH_CALIBRATE'])
def test_verified_t0_allows_native_homing_and_probing(command):
    p=make_printer(0)
    p.run(command)
    assert len(p.hardware_events)==1
    assert p.objects['extruder'].heater.target==150
    assert p.objects['extruder1'].heater.target==220


def test_unverified_tap_mount_blocks_homing():
    p=make_printer(0)
    p.macro('_CX_TAP_CONFIG')['mount_verified']=False
    with pytest.raises(CommandError,match='mounting'):p.run('G28 Z')
    assert not p.hardware_events

@pytest.mark.parametrize('target,temperature,expected_target,expected_temperature',[
    (220.,220.,150.,150.),(0.,220.,0.,155.),(150.,151.,150.,151.)
])
def test_actual_probe_activation_controls_t0_temperature_only(target,temperature,expected_target,expected_temperature):
    p=make_printer(0)
    p.objects['extruder'].heater.target=target
    p.objects['extruder'].heater.temperature=temperature
    before=[(p.objects[f'extruder{n}'].heater.target,p.objects[f'extruder{n}'].heater.temperature) for n in range(1,6)]
    activate_probe(p)
    assert p.objects['extruder'].heater.target==expected_target
    assert p.objects['extruder'].heater.temperature==expected_temperature
    after=[(p.objects[f'extruder{n}'].heater.target,p.objects[f'extruder{n}'].heater.temperature) for n in range(1,6)]
    assert after==before
    assert all('T0' in line for line in p.trace if line.startswith('M109 '))
    assert all(sensor=='extruder' for sensor,_,_ in p.waits)


def test_probe_activation_rejects_active_virtual_heater_other_than_t0():
    p=make_printer(0)
    p.run('ACTIVATE_EXTRUDER EXTRUDER=extruder5')
    with pytest.raises(CommandError,match='reference heater'):activate_probe(p)
    assert not p.waits
    assert all(p.objects['extruder' if n==0 else f'extruder{n}'].heater.target==220 for n in range(6))


def test_tap_rechecks_reference_sensor_after_cooling_wait():
    p=make_printer(0)
    original=p.before_command
    def switch_changes_during_cooling(gcmd):
        original(gcmd)
        if gcmd.get_command()=='M109':
            p.objects['filament_switch_sensor cx_tool_sensor'].data['filament_detected']=False
    p.before_command=switch_changes_during_cooling
    with pytest.raises(CommandError,match='not detected'):p.run('G28 Z')
    assert not p.hardware_events

@pytest.mark.parametrize('tool',[-1,1])
def test_print_start_requires_t0_before_any_motion_or_heating(tool):
    p=make_printer(tool)
    command='PRINT_START INITIAL_TOOL=5 T5_USED=1 T5_TEMP=225'
    with pytest.raises(CommandError):p.run(command)
    assert p.trace==[command]
    assert not p.hardware_events
    assert not p.moves


def test_job_without_t0_still_probes_with_t0_then_turns_it_off():
    p=make_printer(0)
    observed=[]
    original=p.before_command
    def observe_native_operation(gcmd):
        original(gcmd)
        if gcmd.get_command() in ('G9928','CX_BASE_QUAD_GANTRY_LEVEL','CX_BASE_BED_MESH_CALIBRATE'):
            observed.append((p.macro('_CX_STATE')['current_tool'],p.toolhead.active,
                             p.objects['filament_switch_sensor cx_tool_sensor'].data['filament_detected']))
    p.before_command=observe_native_operation
    p.run('PRINT_START INITIAL_TOOL=5 T5_USED=1 T5_TEMP=225 BED=65')
    assert len(observed)==4
    assert all(state==(0,'extruder',True) for state in observed)
    assert p.objects['extruder'].heater.target==0
    assert p.objects['extruder5'].heater.target==225
    assert p.macro('_CX_STATE')['current_tool']==5
    assert len(p.extrusions)==2
    assert all(e['active']=='extruder5' and e['physical'] for e in p.extrusions)
