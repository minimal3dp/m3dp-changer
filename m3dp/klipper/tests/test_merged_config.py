"""Audit the real deployed include layout and exercise its final macro bodies."""
from pathlib import Path
import os
import shutil
import pytest
from klipper_harness import Printer, CommandError, Coord
from config_audit import read_active_config,audit_pins

STAGE=Path(__file__).resolve().parent.parent
REPO=Path(os.environ.get('CXCHANGER_SOURCE',str(Path(__file__).resolve().parents[3])))

@pytest.fixture
def merged_tree(tmp_path):
    target=tmp_path/'m3dp'/'klipper';target.mkdir(parents=True)
    shutil.copytree(REPO/'m3dp'/'voron',target.parent/'voron')
    for path in STAGE.glob('*.cfg'):
        shutil.copy2(path,target/path.name)
    for name in ('printer.cfg','hardware.cfg','hotends.cfg'):
        shutil.copy2(STAGE/(name+'.example'),target/name)
    # Preserve all deliberate placeholders: this is structural/macro validation,
    # not a claim that the uncommissioned draft can start a connected printer.
    return read_active_config(target/'printer.cfg')

@pytest.fixture
def merged_printer(merged_tree):
    config,_=merged_tree
    p=Printer(fileconfig=config)
    p.macro('_CX_CONFIG').update(commissioned=True,docks={n:[300.-n*30,10.] for n in range(6)})
    p.macro('_CX_TAP_CONFIG')['mount_verified']=True
    minimum=[config.getfloat('stepper_'+a,'position_min',fallback=0.) for a in 'xyz']
    maximum=[config.getfloat('stepper_'+a,'position_max') for a in 'xyz']
    p.toolhead.axis_minimum=Coord(minimum);p.toolhead.axis_maximum=Coord(maximum)
    for n in range(6):
        name='extruder' if n==0 else f'extruder{n}'
        p.objects['configfile'].data['settings'][name]['min_extrude_temp']=config.getfloat(name,'min_extrude_temp')
        p.objects[name].heater.min_extrude_temp=config.getfloat(name,'min_extrude_temp')
        for axis,value in zip('xyz',[n*.1,-n*.2,n*.03]):
            p.objects['save_variables'].data['variables'][f't{n}_offset_{axis}']=value
    p.objects['filament_switch_sensor cx_tool_sensor'].data['filament_detected']=True
    p.run('CX_CONFIRM_TOOL TOOL=0\nG90\nG1 X150 Y150 Z20 F6000')
    p.trace.clear();p.moves.clear();p.heater_events.clear();p.hardware_events.clear()
    def physical_switch(gcmd):
        if gcmd.get_command()=='_CX_AFTER_RELEASE':
            p.objects['filament_switch_sensor cx_tool_sensor'].data['filament_detected']=False
        elif gcmd.get_command()=='_CX_VERIFY_PICKUP':
            p.objects['filament_switch_sensor cx_tool_sensor'].data['filament_detected']=True
    p.before_command=physical_switch
    return p


def test_deployment_includes_resolve_and_saved_bed_probe_values_survive(merged_tree):
    config,files=merged_tree
    names=[Path(p).name for p in files]
    assert {'printer.cfg','cxchanger.cfg','mainsail.cfg','KNOMI.cfg','klipper_backup.cfg',
            'nevermore.cfg','stealthburner_leds.cfg','hardware.cfg','hotends.cfg',
            'toolchange.cfg','tap.cfg','print.cfg','pins-m8p-v1.1.cfg'}<=set(names)
    assert 'macros.cfg' not in names
    assert config.getfloat('probe','z_offset')==pytest.approx(-.896)
    assert config.getfloat('heater_bed','pid_kp')==pytest.approx(47.218)
    assert config.get('save_variables','filename')=='~/printer_data/config/variables.cfg'
    assert config.get('heater_bed','heater_pin')=='PB7'
    assert not config.has_section('output_pin caselight')


def test_resolved_physical_pins_have_one_owner_and_unresolved_switch_is_explicit(merged_tree):
    config,_=merged_tree;audit=audit_pins(config)
    assert not audit['collisions']
    assert audit['unresolved']==[('filament_switch_sensor cx_tool_sensor.switch_pin','REPLACE_WITH_VERIFIED_GPIO21_POLARITY')]
    assert audit['owners']['mcu:PB5']==['extruder1.heater_pin']
    assert audit['owners']['mcu:PB6']==['extruder2.heater_pin']
    assert audit['owners']['EBBCan:gpio14']==['heater_fan hotend_fan.pin']


def test_six_heaters_share_exactly_one_motor_and_all_cooling_associations(merged_tree):
    config,_=merged_tree
    heaters={'extruder' if n==0 else f'extruder{n}' for n in range(6)}
    assert {s for s in config.sections() if s=='extruder' or s.startswith('extruder') and s[8:].isdigit()}==heaters
    assert config.get('extruder','step_pin').replace(' ','')=='EBBCan:gpio18'
    for n in range(1,6):
        for field in ('step_pin','dir_pin','enable_pin','microsteps','rotation_distance','gear_ratio'):
            assert not config.has_option(f'extruder{n}',field)
        assert not config.has_section(f'tmc2209 extruder{n}')
    assert not config.has_option('extruder','pid_kp')
    for section in ('heater_fan hotend_fan','heater_fan cx_dock_cooling_a','heater_fan cx_dock_cooling_b'):
        assert {v.strip() for v in config.get(section,'heater').split(',')}==heaters
    for section in ('controller_fan Electronics_Fan','controller_fan Electronics_Fan1'):
        assert {v.strip() for v in config.get(section,'heater').split(',')}==heaters|{'heater_bed'}


def test_final_macro_aliases_resolve_without_legacy_mainsail_base_calls(merged_printer):
    p=merged_printer
    aliases=[values['rename_existing'] for section,values in p.sections.items()
             if section.startswith('gcode_macro ') and 'rename_existing' in values]
    assert all(alias.upper() in p.gcode.ready_gcode_handlers for alias in aliases)
    legacy={'PAUSE_BASE','RESUME_BASE','CANCEL_PRINT_BASE'}
    for section,values in p.sections.items():
        if section.startswith('gcode_macro '):
            for line in values.get('gcode','').splitlines():
                if line.strip():assert line.strip().split()[0] not in legacy

@pytest.mark.parametrize('tool',range(6))
def test_nevermore_named_heater_routes_exact_tool_while_t5_active(merged_printer,tool):
    p=merged_printer;p.run('T5')
    baseline={name:p.objects[name].heater.target for name in ['extruder']+[f'extruder{n}' for n in range(1,6)]}
    name='extruder' if tool==0 else f'extruder{tool}'
    p.run(f'SET_HEATER_TEMPERATURE HEATER={name} TARGET=233.5')
    for heater,target in baseline.items():
        assert p.objects[heater].heater.target==(233.5 if heater==name else target)
    assert p.toolhead.active=='extruder5'
    assert p.objects['fan_generic BedFans'].data['speed']==0


def test_nevermore_bed_target_preserves_fan_threshold_and_monitoring(merged_printer):
    p=merged_printer
    p.run('SET_HEATER_TEMPERATURE HEATER=heater_bed TARGET=65.5')
    assert p.objects['heater_bed'].data['target']==65.5
    assert p.objects['fan_generic BedFans'].data['speed']==p.macro('_BEDFANVARS')['slow']
    assert p.delayed['bedfanloop']==1
    p.run('M140 S45')
    assert p.objects['heater_bed'].data['target']==45
    assert p.objects['fan_generic BedFans'].data['speed']==0
    assert p.delayed['bedfanloop']==0


def test_nevermore_m190_keeps_native_wait_and_knomi_status(merged_printer):
    p=merged_printer
    seen=[];previous=p.before_command
    def observe(gcmd):
        previous(gcmd)
        if gcmd.get_command()=='M99190':seen.append(dict(p.macro('_KNOMI_STATUS')))
    p.before_command=observe
    p.run('M190 S65')
    assert seen and seen[0]['heating_bed']
    assert not p.macro('_KNOMI_STATUS')['heating_bed']
    assert p.objects['heater_bed'].data['temperature']==65
    assert p.objects['fan_generic BedFans'].data['speed']==p.macro('_BEDFANVARS')['fast']


def test_knomi_m109_wrapper_preserves_explicit_tool_argument(merged_printer):
    p=merged_printer
    p.run('M109 T5 S235')
    event=p.heater_events[-1]
    assert event[:3]==('extruder5',235,True)
    assert event[3]['heating_nozzle']
    assert not p.macro('_KNOMI_STATUS')['heating_nozzle']
    assert p.objects['extruder'].heater.target==220


def test_merged_tap_wrappers_preserve_knomi_status_and_native_calls(merged_printer):
    p=merged_printer
    seen=[];previous=p.before_command
    flag_by_command={'G9928':'homing','CX_BASE_QUAD_GANTRY_LEVEL':'qgling','CX_BASE_BED_MESH_CALIBRATE':'probing'}
    def observe(gcmd):
        previous(gcmd)
        if gcmd.get_command() in flag_by_command:
            seen.append((flag_by_command[gcmd.get_command()],dict(p.macro('_KNOMI_STATUS'))))
    p.before_command=observe
    p.run('G28 Z\nQUAD_GANTRY_LEVEL\nBED_MESH_CALIBRATE')
    assert len(seen)==3
    assert all(values[flag] for flag,values in seen)
    assert all(not value for value in p.macro('_KNOMI_STATUS').values())
    assert len(p.hardware_events)==3


def test_cancel_clears_all_six_heaters_bed_fans_and_mainsail_layer_requests(merged_printer):
    p=merged_printer
    p.run('T5\nM140 S65\nSET_PAUSE_NEXT_LAYER ENABLE=1\nSET_PAUSE_AT_LAYER ENABLE=1 LAYER=12')
    p.macro('_KNOMI_STATUS').update(homing=True,probing=True,qgling=True,heating_nozzle=True,heating_bed=True)
    p.moves.clear();p.extrusions.clear()
    p.run('CANCEL_PRINT')
    assert all(p.objects['extruder' if n==0 else f'extruder{n}'].heater.target==0 for n in range(6))
    assert p.objects['heater_bed'].data['target']==0
    assert p.objects['fan_generic BedFans'].data['speed']==0
    assert p.delayed['bedfanloop']==0
    assert not p.macro('SET_PRINT_STATS_INFO')['pause_next_layer']['enable']
    assert not p.macro('SET_PRINT_STATS_INFO')['pause_at_layer']['enable']
    assert all(not value for value in p.macro('_KNOMI_STATUS').values())
    assert p.motor_queue==''
    assert not p.moves and not p.extrusions
    p.run('SET_PRINT_STATS_INFO CURRENT_LAYER=12')
    assert not p.objects['pause_resume'].is_paused


def test_mainsail_layer_pause_uses_safe_cx_pause(merged_printer):
    p=merged_printer
    p.run('SET_PAUSE_AT_LAYER LAYER=12')
    p.moves.clear();p.extrusions.clear()
    before=list(p.toolhead.position)
    p.run('SET_PRINT_STATS_INFO CURRENT_LAYER=12')
    assert p.objects['pause_resume'].is_paused
    assert not p.extrusions
    assert p.toolhead.position[:2]==before[:2]
    assert p.toolhead.position[2]==before[2]+5
    assert not p.macro('SET_PRINT_STATS_INFO')['pause_at_layer']['enable']


def test_merged_six_tool_start_and_end_use_final_wrappers(merged_printer):
    p=merged_printer
    params=' '.join(f'T{n}_USED=1 T{n}_TEMP={220+n}' for n in range(6))
    p.run(f'PRINT_START INITIAL_TOOL=5 BED=65 {params}')
    assert p.macro('_CX_STATE')['current_tool']==5
    assert p.motor_queue==p.toolhead.active=='extruder5'
    assert len(p.extrusions)==12 and all(e['physical'] for e in p.extrusions)
    assert p.objects['fan_generic BedFans'].data['speed']==p.macro('_BEDFANVARS')['fast']
    assert all(not value for value in p.macro('_KNOMI_STATUS').values())
    p.moves.clear()
    p.run('PRINT_END')
    assert p.macro('_CX_STATE')['current_tool']==-1
    assert p.motor_queue==''
    assert all(move['end'][2]>=move['start'][2] for move in p.moves)
    assert all(p.objects['extruder' if n==0 else f'extruder{n}'].heater.target==0 for n in range(6))
    assert p.objects['heater_bed'].data['target']==0
    assert p.objects['fan_generic BedFans'].data['speed']==0
    assert p.delayed['bedfanloop']==0
