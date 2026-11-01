"""Run real Klipper macro/dispatch/motion code with fake, nonconnected hardware.

Requires KLIPPER_SOURCE (checkout root or klippy directory), Jinja2, and pytest.
No MCU, serial, network, printer config, or persistent printer file is touched.
"""
import ast
import configparser
import contextlib
import importlib
import math
import os
from pathlib import Path
import sys
from types import SimpleNamespace

SOURCE = Path(os.environ.get('KLIPPER_SOURCE', str(Path.home() / 'klipper')))
if (SOURCE / 'klippy').is_dir():
    SOURCE = SOURCE / 'klippy'
if not (SOURCE / 'gcode.py').is_file():
    raise RuntimeError('Set KLIPPER_SOURCE to an existing Klipper checkout or its klippy directory')
sys.path.insert(0, str(SOURCE))
from gcode import GCodeDispatch, CommandError, Coord
from extras.gcode_macro import PrinterGCodeMacro, GCodeMacro
from extras.gcode_move import GCodeMove
from extras.pause_resume import PauseResume
from kinematics.extruder import PrinterExtruder


class Status:
    def __init__(self, **data): self.data = data
    def get_status(self, eventtime): return self.data
    def is_active(self): return self.data.get("is_active", False)


class Config:
    error = CommandError
    missing = object()
    def __init__(self, printer, name, values=None):
        self.printer, self.name, self.values = printer, name, values or {}
    def get_printer(self): return self.printer
    def get_name(self): return self.name
    def get(self, name, default=missing):
        if name in self.values: return self.values[name]
        if default is not self.missing: return default
        raise self.error(f'Missing {self.name}:{name}')
    def getfloat(self, name, default=missing, **kwargs):
        value = self.get(name, default)
        return None if value is None else float(value)
    def getint(self, name, default=missing, **kwargs): return int(self.get(name, default))
    def getboolean(self, name, default=missing):
        return str(self.get(name, default)).lower() in ('true', '1', 'yes')
    def get_prefix_options(self, prefix): return [key for key in self.values if key.startswith(prefix)]


class Heater:
    def __init__(self, name, temperature=220, target=220):
        self.name, self.temperature, self.target = name, temperature, target
        self.min_extrude_temp = 170
    @property
    def can_extrude(self): return self.temperature >= self.min_extrude_temp
    def get_status(self, eventtime):
        return dict(temperature=self.temperature, target=self.target, power=0)


class Toolhead:
    def __init__(self, printer):
        self.printer = printer
        self.position = [150., 150., 20., 0.]
        self.active = 'extruder'
        self.homed_axes = 'xyz'
        self.max_accel = 3000.
        self.axis_minimum = Coord((-50., -50., 0., 0.))
        self.axis_maximum = Coord((350., 350., 350., 0.))
    def get_status(self, eventtime):
        return dict(position=Coord(self.position), extruder=self.active,
                    homed_axes=self.homed_axes, max_accel=self.max_accel,
                    max_velocity=300., axis_minimum=self.axis_minimum,
                    axis_maximum=self.axis_maximum)
    def get_position(self): return list(self.position)
    def get_extruder(self): return self.printer.objects[self.active]
    def set_extruder(self, extruder, position):
        self.active = extruder.name
        self.position[3] = position
    def flush_step_generation(self): pass
    def move(self, end, speed):
        end = list(end)
        delta = [a-b for a,b in zip(end, self.position)]
        for i in range(3):
            if end[i] < self.axis_minimum[i] - 1e-6 or end[i] > self.axis_maximum[i] + 1e-6:
                raise CommandError(f'Move out of range {end}')
        if any(delta[:3]) and self.homed_axes != 'xyz':
            raise CommandError('Must home axis first')
        if delta[3]:
            distance = math.sqrt(sum(v*v for v in delta[:3])) or abs(delta[3])
            move = SimpleNamespace(axes_d=delta, axes_r=[v/distance for v in delta],
                                   move_d=distance, limit_speed=lambda *args: None)
            self.get_extruder().check_move(move, 3)
            self.printer.extrusions.append(dict(active=self.active, queue=self.printer.motor_queue,
                                                amount=delta[3], physical=self.printer.motor_queue == self.active,
                                                trace_index=len(self.printer.trace)))
        self.printer.moves.append(dict(start=list(self.position), end=end, speed=speed,
                                       trace_index=len(self.printer.trace)))
        self.position = end
        self.get_extruder().last_position = end[3]


class Printer:
    command_error = config_error = CommandError
    def __init__(self, paths=(), fileconfig=None):
        self.objects, self.events = {}, {}
        self.trace, self.moves, self.extrusions, self.output = [], [], [], []
        self.motor_queue = 'extruder'
        self.waits = []
        self.hardware_events = []
        self.delayed = {}
        self.heater_events = []
        self.wait_events = []
        self.before_command = None
        self.reactor = SimpleNamespace(monotonic=lambda: 1., assert_no_pause=contextlib.nullcontext,
                                       mutex=contextlib.nullcontext)
        self.objects['gcode'] = self.gcode = GCodeDispatch(self)
        self.gcode.register_output_handler(self.output.append)
        self.objects['toolhead'] = self.toolhead = Toolhead(self)
        self.objects['webhooks'] = SimpleNamespace(register_endpoint=lambda *args: None)
        self.objects['save_variables'] = Status(variables={})
        self.objects['virtual_sdcard'] = Status(is_active=False, file_position=0)
        self.objects['idle_timeout'] = Status(state='Printing')
        self.objects['print_stats'] = Status(state='printing')
        self.objects['filament_switch_sensor cx_tool_sensor'] = Status(filament_detected=True, enabled=False)
        self.objects['filament_switch_sensor tool_sensor'] = Status(filament_detected=True, enabled=False)
        self.objects['heaters'] = SimpleNamespace(set_temperature=self.set_temperature)
        settings = {}
        for i in range(6):
            name = 'extruder' if not i else f'extruder{i}'
            obj = PrinterExtruder.__new__(PrinterExtruder)
            obj.printer, obj.name, obj.heater = self, name, Heater(name)
            obj.last_position, obj.extruder_stepper = 0., None
            obj.max_e_dist, obj.max_e_velocity, obj.max_e_accel = 100., 50., 1000.
            obj.max_extrude_ratio, obj.nozzle_diameter, obj.filament_area = 2., .4, 2.405
            self.objects[name] = obj
            settings[name] = dict(min_extrude_temp=170., min_temp=0., max_temp=300.)
        self.objects['heater_bed'] = Status(temperature=60., target=60.)
        settings['heater_bed'] = dict(min_temp=0., max_temp=130.)
        self.objects['configfile'] = Status(settings=settings, config={f'stepper_{a}': {'position_max': '350'} for a in 'xyz'})
        self.objects['gcode_macro'] = PrinterGCodeMacro(Config(self, 'gcode_macro'))
        self.objects['gcode_move'] = self.motion = GCodeMove(Config(self, 'gcode_move'))
        self.objects['pause_resume'] = PauseResume(Config(self, 'pause_resume'))
        self._register_hardware()
        self.sections = {}
        if fileconfig is not None:
            self.sections.update({name: dict(fileconfig[name]) for name in fileconfig.sections()})
        for path in paths:
            parser = configparser.RawConfigParser(strict=False, inline_comment_prefixes=('#', ';'))
            parser.read(path, encoding='utf-8-sig')
            self.sections.update({name: dict(parser[name]) for name in parser.sections()})
        for name in self.sections:
            if name.startswith('fan_generic '):
                self.objects[name] = Status(speed=0.)
        for name, values in self.sections.items():
            if name.startswith('gcode_macro '):
                self.objects[name] = GCodeMacro(Config(self, name, values))
        self.send_event('klippy:connect')
        self.send_event('klippy:ready')
        # Wrap registered handlers only after rename_existing has completed.
        for name, handler in list(self.gcode.ready_gcode_handlers.items()):
            def traced(gcmd, handler=handler):
                self.trace.append(gcmd.get_commandline())
                if self.before_command is not None:
                    self.before_command(gcmd)
                return handler(gcmd)
            self.gcode.ready_gcode_handlers[name] = traced
        self.trace.clear()
    def get_reactor(self): return self.reactor
    def get_start_args(self): return {}
    def register_event_handler(self, event, callback): self.events.setdefault(event, []).append(callback)
    def send_event(self, event, *args):
        for cb in self.events.get(event, []): cb(*args)
    def lookup_object(self, name, default=Config.missing):
        if name in self.objects: return self.objects[name]
        if default is not Config.missing: return default
        raise CommandError(f'Unknown printer object: {name}')
    def lookup_objects(self): return self.objects.items()
    def load_object(self, config, name): return self.lookup_object(name)
    def invoke_shutdown(self, message): raise CommandError(f'Shutdown: {message}')
    def request_exit(self, message): raise CommandError(message)
    def run(self, script): self.gcode.run_script_from_command(script)
    def macro(self, name): return self.objects['gcode_macro ' + name].variables
    def set_temperature(self, heater, temperature, wait=False):
        if temperature < 0 or temperature > 300: raise CommandError('Temperature out of range')
        heater.target = temperature
        ui = dict(self.objects['gcode_macro _KNOMI_STATUS'].variables) if 'gcode_macro _KNOMI_STATUS' in self.objects else {}
        self.heater_events.append((heater.name, temperature, wait, ui))
        if wait and temperature > 0: heater.temperature = temperature
    def _register_hardware(self):
        g = self.gcode
        g.register_command('M104', self.objects['extruder'].cmd_M104)
        g.register_command('M109', self.objects['extruder'].cmd_M109)
        for name in ('M118','M117','RESPOND','G4','M400','M106','M107','M84','M18',
                     'BED_MESH_CLEAR','Z_TILT_ADJUST',
                     'SET_PRESSURE_ADVANCE','SET_IDLE_TIMEOUT','CX_TEST_MARKER'):
            g.register_command(name, lambda gcmd: None)
        for name in ('BED_MESH_CALIBRATE', 'QUAD_GANTRY_LEVEL', 'PROBE', 'PROBE_ACCURACY', 'PROBE_CALIBRATE'):
            g.register_command(name, lambda gcmd, operation=name: self.hardware_events.append(('probe', operation)))
        g.register_command('UPDATE_DELAYED_GCODE', self._delayed)
        g.register_command('SET_FAN_SPEED', self._fan)
        g.register_command('SET_PRINT_STATS_INFO', self._stats)
        g.register_command('G28', self._home)
        g.register_command('SET_VELOCITY_LIMIT', self._velocity)
        g.register_command('SET_FILAMENT_SENSOR', self._sensor)
        g.register_command('SAVE_VARIABLE', self._save)
        g.register_command('SYNC_EXTRUDER_MOTION', self._sync)
        g.register_command('ACTIVATE_EXTRUDER', self._activate)
        g.register_command('SET_HEATER_TEMPERATURE', self._set_heater)
        g.register_command('TEMPERATURE_WAIT', self._wait)
        g.register_command('TURN_OFF_HEATERS', self._off)
        g.register_command('M140', lambda gcmd: self._bed(gcmd, wait=False))
        g.register_command('M190', lambda gcmd: self._bed(gcmd, wait=True))
    def _delayed(self, gcmd): self.delayed[gcmd.get('ID')] = gcmd.get_float('DURATION')
    def _fan(self, gcmd): self.objects['fan_generic '+gcmd.get('FAN')].data['speed'] = gcmd.get_float('SPEED')
    def _stats(self, gcmd):
        self.objects['print_stats'].data.setdefault('info', {}).update({k.lower(): int(v) for k,v in gcmd.get_command_parameters().items()})
    def _home(self, gcmd):
        self.hardware_events.append(('home', dict(gcmd.get_command_parameters())))
        self.toolhead.homed_axes = 'xyz'
        self.toolhead.position[:3] = [0., 0., 0.]
        self.send_event('toolhead:set_position')
    def _velocity(self, gcmd): self.toolhead.max_accel = gcmd.get_float('ACCEL', self.toolhead.max_accel)
    def _sensor(self, gcmd): self.objects['filament_switch_sensor '+gcmd.get('SENSOR')].data['enabled'] = bool(gcmd.get_int('ENABLE',1))
    def _save(self, gcmd): self.objects['save_variables'].data['variables'][gcmd.get('VARIABLE')] = ast.literal_eval(gcmd.get('VALUE'))
    def _sync(self, gcmd):
        if gcmd.get('EXTRUDER') != 'extruder': raise CommandError('Only shared extruder motor exists')
        queue = gcmd.get('MOTION_QUEUE')
        if queue and queue not in self.objects: raise CommandError('Unknown extruder queue')
        self.motor_queue = queue
    def _activate(self, gcmd):
        self.objects[gcmd.get('EXTRUDER')].cmd_ACTIVATE_EXTRUDER(gcmd)
    def _set_heater(self, gcmd):
        name, target = gcmd.get('HEATER'), gcmd.get_float('TARGET')
        if name == 'heater_bed': self.objects[name].data['target'] = target
        else: self.set_temperature(self.objects[name].heater,target)
    def _wait(self, gcmd):
        name = gcmd.get('SENSOR')
        low, high = gcmd.get_float('MINIMUM', -math.inf), gcmd.get_float('MAXIMUM', math.inf)
        self.waits.append((name,low,high))
        ui = dict(self.objects['gcode_macro _KNOMI_STATUS'].variables) if 'gcode_macro _KNOMI_STATUS' in self.objects else {}
        self.wait_events.append((name,low,high,ui))
        obj = self.objects[name]
        if hasattr(obj, 'heater'): obj.heater.temperature = max(low,min(high,obj.heater.temperature))
        else: obj.data['temperature'] = max(low,min(high,obj.data['temperature']))
    def _off(self, gcmd):
        for name, obj in self.objects.items():
            if isinstance(obj,PrinterExtruder): obj.heater.target = 0
        self.objects['heater_bed'].data['target'] = 0
    def _bed(self, gcmd, wait=False):
        self.objects['heater_bed'].data['target'] = gcmd.get_float('S',0)
        if wait: self.objects['heater_bed'].data['temperature'] = gcmd.get_float('S',0)
