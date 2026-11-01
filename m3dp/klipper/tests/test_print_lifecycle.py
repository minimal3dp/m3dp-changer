from pathlib import Path
import pytest
from klipper_harness import Printer, CommandError

STAGE = Path(__file__).resolve().parent.parent

@pytest.fixture
def print_only(tmp_path):
    # State fixture only; tests here do not simulate a successful tool change.
    state = tmp_path/'state.cfg'
    state.write_text('''[gcode_macro _CX_STATE]
variable_current_tool: 0
variable_faulted: False
variable_busy: False
gcode:
[gcode_macro CX_ASSERT_READY]
gcode:
    CX_TEST_MARKER
''')
    p = Printer([state, STAGE/'print.cfg'])
    for tool in range(6):
        for axis in 'xyz':
            p.objects['save_variables'].data['variables'][f't{tool}_offset_{axis}'] = 0.
    return p

@pytest.mark.parametrize('height,homed,expected',[(20,'xyz',25),(349,'xyz',350),(350,'xyz',350),(20,'',20)])
def test_pause_lift_bounded_and_idempotent(print_only,height,homed,expected):
    p=print_only
    p.toolhead.position[2] = height
    p.motion.reset_last_position()
    p.toolhead.homed_axes = homed
    p.run('PAUSE')
    assert p.toolhead.position[2] == expected
    assert p.objects['pause_resume'].is_paused
    count = len(p.moves)
    p.run('PAUSE')
    assert len(p.moves)==count


def test_cancel_shuts_every_heater_and_disconnects_without_movement(print_only):
    p=print_only
    p.macro('_CX_STATE')['current_tool']=5
    p.motor_queue='extruder5'
    p.run('CANCEL_PRINT')
    assert all(p.objects['extruder' if n==0 else f'extruder{n}'].heater.target==0 for n in range(6))
    assert p.objects['heater_bed'].data['target']==0
    assert p.motor_queue==''
    assert not p.moves
    assert p.macro('_CX_STATE')['current_tool']==-2

@pytest.mark.parametrize('params',[
    'INITIAL_TOOL=6 T0_USED=1 T0_TEMP=220',
    'INITIAL_TOOL=abc T0_USED=1 T0_TEMP=220',
    'INITIAL_TOOL=1.5 T1_USED=1 T1_TEMP=220',
    'INITIAL_TOOL=0 T0_USED=1 T0_TEMP=nan',
    'INITIAL_TOOL=0 T0_USED=1 T0_TEMP=220 BED=nan',
    'INITIAL_TOOL=0 T0_USED=1',
    'INITIAL_TOOL=0 T0_USED=maybe T0_TEMP=220',
    'INITIAL_TOOL=0 T0_USED=0 T1_USED=1 T1_TEMP=220',
    'INITIAL_TOOL=0 T0_USED=1 T0_TEMP=100',
    'INITIAL_TOOL=0 T0_USED=1 T0_TEMP=300',
    'INITIAL_TOOL=0 T0_USED=1 T0_TEMP=220 BED=140',
])
def test_start_rejects_invalid_inputs_before_any_command(print_only,params):
    p=print_only
    with pytest.raises(CommandError): p.run('PRINT_START '+params)
    assert p.trace==['PRINT_START '+params]
    assert not p.moves

@pytest.mark.parametrize('tool',[1,5])
def test_start_requires_calibrated_offsets_before_any_command(print_only,tool):
    p=print_only
    del p.objects['save_variables'].data['variables'][f't{tool}_offset_z']
    command=f'PRINT_START INITIAL_TOOL={tool} T{tool}_USED=1 T{tool}_TEMP=220'
    with pytest.raises(CommandError,match='Calibrate'): p.run(command)
    assert p.trace==[command]

@pytest.mark.parametrize('state',[dict(current_tool=-1),dict(current_tool=1),dict(faulted=True),dict(busy=True)])
def test_start_rejects_missing_t0_or_uncertain_head_before_motion(print_only,state):
    p=print_only;p.macro('_CX_STATE').update(state)
    command='PRINT_START INITIAL_TOOL=0 T0_USED=1 T0_TEMP=220'
    with pytest.raises(CommandError): p.run(command)
    assert p.trace==[command]


def test_start_rejects_priming_z_above_travel_before_heating(print_only):
    p=print_only;p.macro('_CX_PRINT_CONFIG')['prime_z']=351
    command='PRINT_START INITIAL_TOOL=0 T0_USED=1 T0_TEMP=220'
    with pytest.raises(CommandError,match='Priming strip'):p.run(command)
    assert p.trace==[command]
