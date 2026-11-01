from pathlib import Path
import pytest
from klipper_harness import Printer, CommandError

STAGE=Path(__file__).resolve().parent.parent


def make_printer(tool=0, pickup=True, release=True, extra_paths=()):
    p=Printer([STAGE/'toolchange.cfg',STAGE/'print.cfg',STAGE/'tap.cfg',*extra_paths])
    p.macro('_CX_TAP_CONFIG')['mount_verified']=True
    p.macro('_CX_CONFIG').update(commissioned=True,docks={n:[232.-n*30,-20.] for n in range(6)})
    for n in range(6):
        name='extruder' if n==0 else f'extruder{n}'
        p.objects['configfile'].data['settings'][name]['min_extrude_temp']=180.
        p.objects[name].heater.min_extrude_temp=180.
        for axis,value in zip('xyz',[n*.1,-n*.2,n*.03]):
            p.objects['save_variables'].data['variables'][f't{n}_offset_{axis}']=value
    sensor=p.objects['filament_switch_sensor cx_tool_sensor']
    sensor.data['filament_detected']=tool>=0
    p.run(f'CX_CONFIRM_TOOL TOOL={tool}')
    p.run('G90\nG1 X150 Y150 Z20 F6000')
    p.trace.clear();p.moves.clear()
    def hardware_result(gcmd):
        name=gcmd.get_command()
        if name in ('_CX_AFTER_RELEASE','_CX_VERIFY_PICKUP'):
            # Inject a physical switch outcome only at a completed/settled move.
            # This does not alter the actual verification macro or its decision.
            assert p.trace[-3].startswith('M400')
            assert p.trace[-2].startswith('G4 ')
            sensor.data['filament_detected']=(not release) if name=='_CX_AFTER_RELEASE' else pickup
    p.before_command=hardware_result
    return p

@pytest.mark.parametrize('tool',range(6))
def test_all_six_tools_activate_matching_heater_and_shared_motor(tool):
    p=make_printer(-1)
    p.run(f'T{tool}\nM83\nG1 E1 F60')
    name='extruder' if tool==0 else f'extruder{tool}'
    assert p.macro('_CX_STATE')['current_tool']==tool
    assert p.toolhead.active==p.motor_queue==name
    assert p.extrusions[-1]['physical']
    assert p.extrusions[-1]['active']==name
    assert not p.macro('_CX_STATE')['busy']


def test_failed_pickup_aborts_enclosing_priming_macro_and_caller():
    p=make_printer(-1,pickup=False)
    with pytest.raises(CommandError,match='Pickup failed'):
        p.run('_CX_PRIME TOOL=1 LINE=0\nCX_TEST_MARKER')
    assert 'CX_TEST_MARKER' not in p.trace
    assert not p.extrusions
    assert p.macro('_CX_STATE')['current_tool']==-2
    assert p.macro('_CX_STATE')['faulted']
    assert all(p.objects['extruder' if n==0 else f'extruder{n}'].heater.target==0 for n in range(6))
    assert p.objects['heater_bed'].data['target']==0
    assert p.objects['pause_resume'].is_paused
    assert p.motor_queue==''
    with pytest.raises(CommandError):p.run('RESUME')


def test_failed_release_does_not_attempt_pickup():
    p=make_printer(0,release=False)
    with pytest.raises(CommandError,match='release did not clear'):
        p.run('T1\nCX_TEST_MARKER')
    assert not any(x.startswith('_CX_PICKUP ') for x in p.trace)
    assert 'CX_TEST_MARKER' not in p.trace
    assert p.macro('_CX_STATE')['faulted']
    assert all(p.objects['extruder' if n==0 else f'extruder{n}'].heater.target==0 for n in range(6))
    assert p.objects['heater_bed'].data['target']==0


def test_hot_t1_can_extrude_when_t0_is_cold():
    p=make_printer(-1)
    p.objects['extruder'].heater.temperature=25
    p.run('T1\nM83\nG1 E1 F60')
    assert p.extrusions[-1]['active']=='extruder1'
    assert p.extrusions[-1]['physical']


def test_cold_t1_cannot_extrude_even_when_t0_is_hot():
    p=make_printer(-1)
    p.objects['extruder1'].heater.temperature=25
    p.objects['extruder1'].heater.target=0
    p.run('T1')
    assert not p.extrusions  # Dry change must not make a hidden retract/prime.
    with pytest.raises(CommandError,match='minimum temp'):
        p.run('M83\nG1 E1 F60')

@pytest.mark.parametrize('relative',[False,True])
@pytest.mark.parametrize('g92',[False,True])
def test_round_trip_preserves_logical_xyz_modes_e_and_global_adjustment(relative,g92):
    p=make_printer(1)
    p.run('SET_GCODE_OFFSET Z_ADJUST=0.17 MOVE=0\nM83\nG1 E2 F300')
    if g92:p.run('G92 X50 Y70 Z10 E100')
    if relative:p.run('G91')
    baseline=p.motion.get_status()
    original_machine=list(p.toolhead.position)
    for tool in (5,2,0,1):
        p.run(f'T{tool}')
        state=p.motion.get_status()
        assert state['gcode_position'][:3]==pytest.approx(baseline['gcode_position'][:3])
        assert state['gcode_position'].e==pytest.approx(baseline['gcode_position'].e)
        assert state['absolute_coordinates']==baseline['absolute_coordinates']
        assert state['absolute_extrude']==baseline['absolute_extrude']
        expected=[original_machine[i]+[.1,-.2,.03][i]*(tool-1) for i in range(3)]
        assert p.toolhead.position[:3]==pytest.approx(expected)
        assert state['homing_origin'].z==pytest.approx(.17+tool*.03)
        assert p.toolhead.max_accel==3000


def test_z_hop_fits_below_machine_maximum():
    p=make_printer(0)
    p.run('G1 Z347 F600')
    p.moves.clear()
    p.run('T5')
    assert max(m['end'][2] for m in p.moves)<=350
    assert p.motion.get_status()['gcode_position'].z==pytest.approx(347)


def test_compensated_return_outside_limits_is_rejected_before_docking():
    p=make_printer(0)
    p.run('G1 Z350 F600');p.moves.clear()
    with pytest.raises(CommandError,match='return position exceeds'):
        p.run('T5')
    assert not p.moves
    assert p.macro('_CX_STATE')['current_tool']==0


def test_untool_leaves_machine_frame_at_safe_exit_without_descent():
    p=make_printer(1)
    before=p.toolhead.position[2]
    p.run('UNTOOL')
    assert p.macro('_CX_STATE')['current_tool']==-1
    assert p.motor_queue==''
    assert all(m['end'][2]>=m['start'][2] for m in p.moves)
    assert p.toolhead.position[2]>=before
    assert p.motion.get_status()['homing_origin'][:3]==(0.,0.,0.)
    assert p.motion.get_status()['gcode_position'][:3]==pytest.approx(p.toolhead.position[:3])

@pytest.mark.parametrize('command',[
    'CX_CHANGE_TOOL TOOL=-2','CX_CHANGE_TOOL TOOL=6','CX_CHANGE_TOOL TOOL=abc',
    'CX_CHANGE_TOOL TOOL=1.5','CX_CHANGE_TOOL TOOL=1 RETURN=2',
    'CX_CHANGE_TOOL TOOL=1 RETURN=abc','CX_CONFIRM_TOOL TOOL=1.5',
])
def test_invalid_tool_parameters_rejected_without_child_commands(command):
    p=make_printer(0)
    with pytest.raises(CommandError):p.run(command)
    assert p.trace==[command]
    assert not p.moves


def test_uncommissioned_and_unknown_state_cannot_move():
    p=make_printer(0)
    p.macro('_CX_CONFIG')['commissioned']=False
    with pytest.raises(CommandError,match='not commissioned'):p.run('T1')
    assert not p.moves
    p.macro('_CX_CONFIG')['commissioned']=True
    p.macro('_CX_STATE')['current_tool']=-2
    with pytest.raises(CommandError,match='uncertain'):p.run('T1')
    assert not p.moves


def test_return_zero_allows_uncalibrated_dry_selection_in_machine_frame():
    p=make_printer(-1)
    p.objects['save_variables'].data['variables']={}
    p.objects['extruder5'].heater.target=0
    p.run('CX_CHANGE_TOOL TOOL=5 RETURN=0')
    assert p.macro('_CX_STATE')['current_tool']==5
    assert p.motion.get_status()['homing_origin'][:3]==(0.,0.,0.)
    assert not p.extrusions


def test_print_end_switches_off_all_heaters_before_docking_and_never_descends():
    p=make_printer(5)
    p.run('G1 Z340 F600');p.moves.clear();p.trace.clear()
    p.run('PRINT_END')
    assert p.trace.index('TURN_OFF_HEATERS')<p.trace.index('UNTOOL')
    assert all(p.objects['extruder' if n==0 else f'extruder{n}'].heater.target==0 for n in range(6))
    assert all(m['end'][2]>=m['start'][2] for m in p.moves)
    assert p.macro('_CX_STATE')['current_tool']==-1

@pytest.mark.parametrize('first',[0,5])
def test_print_start_heats_and_primes_six_tools_with_initial_tool_last(first):
    p=make_printer(0)
    p.run('M82\nG92 E42')
    params=' '.join(f'T{n}_USED=1 T{n}_TEMP={220+n}' for n in range(6))
    p.run(f'PRINT_START INITIAL_TOOL={first} BED=65 {params}')
    assert p.macro('_CX_STATE')['current_tool']==first
    assert p.toolhead.active==('extruder' if first==0 else f'extruder{first}')
    primed=[int(line.split('TOOL=')[1].split()[0]) for line in p.trace if line.startswith('_CX_PRIME ')]
    assert primed==[n for n in range(6) if n!=first]+[first]
    assert len(p.extrusions)==12
    assert all(e['physical'] for e in p.extrusions)
    assert p.motion.get_status()['gcode_position'].e==pytest.approx(42)
    assert p.motion.get_status()['absolute_extrude']
    assert p.objects['heater_bed'].data['target']==65
    for n in range(6):
        assert p.objects['extruder' if n==0 else f'extruder{n}'].heater.target==(220+n if n==first else 0)


def test_failed_pickup_during_print_start_stops_later_tools_and_extrusion():
    p=make_printer(0,pickup=False)
    with pytest.raises(CommandError,match='Pickup failed'):
        p.run('PRINT_START INITIAL_TOOL=0 T0_USED=1 T0_TEMP=220 T1_USED=1 T1_TEMP=220\nCX_TEST_MARKER')
    assert not p.extrusions
    assert len([line for line in p.trace if line.startswith('_CX_PRIME ')])==1
    assert 'CX_TEST_MARKER' not in p.trace
    assert p.macro('_CX_STATE')['faulted']
    assert all(p.objects['extruder' if n==0 else f'extruder{n}'].heater.target==0 for n in range(6))
    assert p.objects['heater_bed'].data['target']==0


def test_print_start_rechecks_t0_sensor_before_homing():
    p=make_printer(0)
    # Physical T0 was removed after the operator's earlier confirmation.
    p.objects['filament_switch_sensor cx_tool_sensor'].data['filament_detected']=False
    with pytest.raises(CommandError):
        p.run('PRINT_START INITIAL_TOOL=0 T0_USED=1 T0_TEMP=220')
    assert not any(line.startswith('G28') for line in p.trace)
    assert not any(line.startswith(('M140','M190','M104','M109')) for line in p.trace)


@pytest.mark.parametrize('height',[348.01,349.8,350.])
def test_toolchange_rejects_insufficient_z_clearance_before_any_motion(height):
    p=make_printer(0)
    p.objects['save_variables'].data['variables']['t5_offset_z']=0.
    p.run(f'G1 Z{height} F600');p.moves.clear()
    with pytest.raises(CommandError,match='clearance'):
        p.run('T5')
    assert not p.moves
    assert p.macro('_CX_STATE')['current_tool']==0
    assert not p.macro('_CX_STATE')['busy']


def test_print_end_still_shuts_down_if_required_z_clearance_is_unavailable():
    p=make_printer(0)
    p.run('G1 Z350 F600');p.moves.clear()
    with pytest.raises(CommandError,match='clearance'):
        p.run('PRINT_END')
    assert not p.moves
    assert all(p.objects['extruder' if n==0 else f'extruder{n}'].heater.target==0 for n in range(6))
    assert p.objects['heater_bed'].data['target']==0
