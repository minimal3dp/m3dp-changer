"""Safety assertions expected to fail against the untouched upstream examples."""
from pathlib import Path
import os
import pytest
from klipper_harness import Printer, CommandError

ORIGINAL = Path(os.environ.get('CXCHANGER_SOURCE', str(Path(__file__).resolve().parents[3]))) / 'reference' / 'cxchanger' / 'klipper'
pytestmark = pytest.mark.xfail(strict=True, reason='Original reference macro defect reproduced')


def test_failed_pickup_aborts_enclosing_print_script():
    p = Printer([ORIGINAL/'toolchange.cfg'])
    p.macro('_toolchanger_cfg')['enable_sensor_check'] = 1
    p.objects['filament_switch_sensor tool_sensor'].data['filament_detected'] = False
    with pytest.raises(CommandError):
        p.run('T1\nCX_TEST_MARKER')
    assert 'CX_TEST_MARKER' not in p.trace


def test_hot_t1_uses_t1_cold_extrusion_interlock():
    p = Printer([ORIGINAL/'toolchange.cfg'])
    p.objects['extruder'].heater.temperature = 25
    p.objects['extruder1'].heater.temperature = 220
    p.run('T1')
    assert p.toolhead.active == p.motor_queue == 'extruder1'


def test_cold_t1_cannot_extrude_using_hot_t0_interlock():
    p = Printer([ORIGINAL/'toolchange.cfg'])
    p.objects['extruder1'].heater.temperature = 25
    p.objects['extruder1'].heater.target = 0
    p.run('T1')
    with pytest.raises(CommandError, match='minimum temp'):
        p.run('M83\nG1 E1 F60')


def test_toolchange_removes_hop_and_preserves_logical_z():
    p = Printer([ORIGINAL/'toolchange.cfg'])
    p.macro('_toolchanger_cfg')['z_hop'] = 5
    p.objects['save_variables'].data['variables']['t1_offset_z'] = .3
    before = p.motion.get_status()['gcode_position'].z
    p.run('T1')
    assert p.motion.get_status()['gcode_position'].z == pytest.approx(before)


def test_print_end_does_not_descend_into_tall_model(tmp_path):
    # Only load PRINT_END to avoid unrelated base-printer setup dependencies.
    src = (ORIGINAL/'printer.cfg').read_text()
    body = src.split('[gcode_macro PRINT_END]',1)[1].split('#*#',1)[0]
    end = tmp_path/'print-end.cfg'
    end.write_text('[gcode_macro PRINT_END]'+body)
    p = Printer([ORIGINAL/'toolchange.cfg',end])
    p.run('G90\nG0 Z340 F600')
    p.moves.clear()
    p.run('PRINT_END')
    assert all(move['end'][2] >= move['start'][2] for move in p.moves)


def test_six_tool_selectors_exist():
    p = Printer([ORIGINAL/'toolchange.cfg'])
    assert all('T'+str(n) in p.gcode.ready_gcode_handlers for n in range(6))
