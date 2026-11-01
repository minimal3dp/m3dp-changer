"""Macro contract tests with synthetic contact-probe results, no physical probe."""
import math
import pytest
from klipper_harness import CommandError, Status
from test_toolchange import make_printer, STAGE


def calibration_printer(enabled=True,pickup=True):
    p=make_printer(-1,pickup=pickup,extra_paths=[STAGE/'calibration.cfg'])
    p.macro('_CX_CALIB_CONFIG').update(enabled=enabled,approach=[20.,20.,5.],clearance_z=30.)
    p.objects['tools_calibrate']=Status(last_result=[99.,99.,99.])
    p.probe_calls=[]
    def probe(gcmd):
        p.trace.append(gcmd.get_commandline())
        tool=p.macro('_CX_STATE')['current_tool']
        p.probe_calls.append((gcmd.get_command(),tool))
        p.objects['tools_calibrate'].data['last_result']=[tool*.2,-tool*.1,tool*.03]
    p.gcode.register_command('TOOL_LOCATE_SENSOR',probe)
    p.gcode.register_command('TOOL_CALIBRATE_TOOL_OFFSET',probe)
    return p


def test_disabled_calibration_cannot_move():
    p=calibration_printer(enabled=False)
    with pytest.raises(CommandError,match='before enabling calibration'):p.run('CALIBRATE_TOOL TOOL=0')
    assert not p.moves
    assert not p.probe_calls


def test_nonreference_tool_requires_reference_in_current_session():
    p=calibration_printer()
    with pytest.raises(CommandError,match='Calibrate T0'):p.run('CALIBRATE_TOOL TOOL=5')
    assert not p.moves
    assert not p.probe_calls


def test_all_six_calibration_results_saved_after_probe_and_tools_returned():
    p=calibration_printer()
    p.run('CALIBRATE_ALL_TOOLS')
    assert p.probe_calls==[('TOOL_LOCATE_SENSOR',0)]+[('TOOL_CALIBRATE_TOOL_OFFSET',n) for n in range(1,6)]
    svv=p.objects['save_variables'].data['variables']
    for n in range(6):
        assert [svv[f't{n}_offset_{axis}'] for axis in 'xyz']==pytest.approx([n*.2,-n*.1,n*.03])
    assert p.macro('_CX_STATE')['current_tool']==-1
    assert p.motor_queue==''
    assert not p.extrusions


def test_failed_pickup_prevents_probe_or_saved_offsets():
    p=calibration_printer(pickup=False)
    previous=dict(p.objects['save_variables'].data['variables'])
    with pytest.raises(CommandError,match='Pickup failed'):p.run('CALIBRATE_TOOL TOOL=0')
    assert not p.probe_calls
    assert p.objects['save_variables'].data['variables']==previous
    assert not p.macro('_CX_CALIB_STATE')['reference_valid']

@pytest.mark.parametrize('result',[[math.nan,0.,0.],[math.inf,0.,0.],[401.,0.,0.]])
def test_invalid_probe_result_does_not_partially_save(result):
    p=calibration_printer()
    p.objects['tools_calibrate'].data['last_result']=result
    previous=dict(p.objects['save_variables'].data['variables'])
    with pytest.raises(CommandError,match='Invalid nozzle calibration result'):p.run('_CX_SAVE_CALIBRATION TOOL=5')
    assert p.objects['save_variables'].data['variables']==previous
