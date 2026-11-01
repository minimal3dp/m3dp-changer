"""Read Klipper's active include tree and audit resolved pin ownership offline."""
from collections import defaultdict
from pathlib import Path
import re
from klipper_harness import SOURCE
from configfile import ConfigFileReader, ConfigAutoSave
from pins import PrinterPins, error as PinError


class TrackingReader(ConfigFileReader):
    def __init__(self): self.files=[]
    def read_config_file(self, filename):
        self.files.append(str(Path(filename).resolve()))
        return super().read_config_file(filename)


def read_active_config(entry):
    """Klipper include semantics plus the entrypoint's SAVE_CONFIG values only."""
    reader=TrackingReader()
    data=reader.read_config_file(str(entry))
    # This method only separates text; it does not construct/save printer state.
    autosave=ConfigAutoSave.__new__(ConfigAutoSave)
    regular,saved=autosave._find_autosave_data(data)
    config=reader.build_fileconfig_with_includes(regular,str(entry))
    if saved:
        saved=autosave._strip_duplicates(saved,config)
        reader.append_fileconfig(config,saved,str(entry)+':SAVE_CONFIG')
    return config,reader.files


def audit_pins(config):
    ppins=PrinterPins()
    mcu_names=['mcu']+[section.split(' ',1)[1] for section in config.sections() if section.startswith('mcu ')]
    for name in set(mcu_names):ppins.register_chip(name,object())
    unresolved=[];owners=defaultdict(list);collisions=[]
    for section in config.sections():
        if not section.startswith('board_pins'):continue
        for mcu in config.get(section,'mcu',fallback='mcu').split(','):
            resolver=ppins.get_pin_resolver(mcu.strip())
            for option,value in config[section].items():
                if option.startswith('aliases'):
                    for item in value.replace('\n','').split(','):
                        if not item.strip():continue
                        alias,pin=[x.strip() for x in item.split('=',1)]
                        resolver.alias_pin(alias,pin)
    for section in config.sections():
        for option,value in config[section].items():
            if option!='pin' and not option.endswith('_pin'):continue
            locator=f'{section}.{option}'
            if 'REPLACE' in value or value.strip().lower()=='none':
                unresolved.append((locator,value));continue
            if 'virtual_endstop' in value:continue
            try:parsed=ppins.parse_pin(value,can_invert=True,can_pullup=True)
            except PinError as e:
                unresolved.append((locator,str(e)));continue
            name=parsed['chip_name'];resolver=ppins.get_pin_resolver(name)
            pin=resolver.aliases.get(parsed['pin'],parsed['pin'])
            if not re.fullmatch(r'(P[A-Z]\d+|gpio\d+)',pin):
                unresolved.append((locator,f'unresolved/nonphysical pin {name}:{pin}'));continue
            key=f'{name}:{pin}'
            owners[key].append(locator)
            prefix=('^' if parsed['pullup']==1 else '~' if parsed['pullup']==-1 else '')+('!' if parsed['invert'] else '')
            try:ppins.lookup_pin(prefix+key,can_invert=True,can_pullup=True)
            except PinError as e:collisions.append((key,list(owners[key]),str(e)))
    return dict(owners=owners,unresolved=unresolved,collisions=collisions)
