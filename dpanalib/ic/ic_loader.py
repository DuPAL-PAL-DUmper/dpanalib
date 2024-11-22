"""This class contains code to extract an IC definition from a properly formatted TOML file read from a BufferedReader"""

from io import BufferedReader
from typing import Any, final
from dpanalib.ic.ic_definition import ICDefinition

from functools import reduce

import tomllib
import tomli_w

type TomlData = int | str | list[str] | list[int] | None

@final
class ICLoader:
    _KEY_NAME: str = 'name'
    _KEY_PINOUT: str = 'pinout'
    _KEY_PINOUT_PINS_PER_SIDE = 'pins_per_side'
    _KEY_PINOUT_ZIFMAP: str = 'ZIF_map'
    _KEY_PINOUT_NAMES_OVERRIDE = 'names_override'
    _KEY_PINOUT_CLKP: str = 'clk_pins'
    _KEY_PINOUT_INP: str = 'in_pins'
    _KEY_PINOUT_IOP: str = 'io_pins'
    _KEY_PINOUT_OP: str = 'o_pins'
    _KEY_PINOUT_FP: str = 'f_pins'
    _KEY_PINOUT_HIZ_O: str = 'hiz_o_pins'
    _KEY_PINOUT_QP: str = 'q_pins'
    _KEY_PINOUT_OEH: str = 'oe_h_pins'
    _KEY_PINOUT_OEL: str = 'oe_l_pins'
    _KEY_PINOUT_ROT_SHIFT: str = 'rot_shift'
    _KEY_ADAPTER: str = 'adapter'
    _KEY_ADAPTER_HI_PINS: str = 'hi_pins'
    _KEY_ADAPTER_NOTES: str = 'notes'
    _KEY_REQUIREMENTS: str = 'requirements'
    _KEY_REQUIREMENTS_HARDWARE: str = 'hardware'

    _TOML_KEY_MAP: dict[str, list[str]] = {
        'name': [_KEY_NAME],
        'pins_per_side': [_KEY_PINOUT, _KEY_PINOUT_PINS_PER_SIDE],
        'zif_map': [_KEY_PINOUT, _KEY_PINOUT_ZIFMAP],
        'clk_pins': [_KEY_PINOUT, _KEY_PINOUT_CLKP],
        'in_pins': [_KEY_PINOUT, _KEY_PINOUT_INP],
        'io_pins': [_KEY_PINOUT, _KEY_PINOUT_IOP],
        'o_pins': [_KEY_PINOUT, _KEY_PINOUT_OP],
        'f_pins': [_KEY_PINOUT, _KEY_PINOUT_FP],
        'hiz_o_pins': [_KEY_PINOUT, _KEY_PINOUT_HIZ_O],
        'q_pins': [_KEY_PINOUT, _KEY_PINOUT_QP],
        'oe_l_pins': [_KEY_PINOUT, _KEY_PINOUT_OEL],
        'oe_h_pins': [_KEY_PINOUT, _KEY_PINOUT_OEH],
        'hw_model': [_KEY_REQUIREMENTS, _KEY_REQUIREMENTS_HARDWARE],
        'adapter_hi_pins': [_KEY_ADAPTER, _KEY_ADAPTER_HI_PINS],
        'pin_rot_shift': [_KEY_PINOUT, _KEY_PINOUT_ROT_SHIFT],
        'adapter_notes': [_KEY_ADAPTER, _KEY_ADAPTER_NOTES],
        'pin_names_override': [_KEY_PINOUT, _KEY_PINOUT_NAMES_OVERRIDE]
    }

    @classmethod
    def _toml_rebuild(cls, definition: ICDefinition) -> dict[str, Any]: 
        data: dict[str, Any] = {}

        for name, path in cls._TOML_KEY_MAP.items():
            temp_data = data
            path_length = len(path)
            for i, elem in enumerate(path):
                if (i == path_length - 1):
                    temp_data[elem] = definition[name]
                else:
                    if not elem in temp_data:
                        temp_data[elem] = {}
                    temp_data = temp_data[elem]

        return data
    
    @classmethod
    def _deref_multi(cls, data: dict[str, Any], keys: list[str]) -> TomlData:
        # Walk the path through data using a list of keys
        return reduce((lambda d, key: d.get(key, None)), keys, data)

    @classmethod
    def rebuild_toml_from_definition(cls, definition: ICDefinition) -> str:
        """Rebuilds a TOML structure using a loaded ICDefinition

        Args:
            definition (ICDefinition): IC definition that will be turned into a TOML string

        Returns:
            str: string representing a TOML structure of the loaded IC definition
        """        
        return tomli_w.dumps(cls._toml_rebuild(definition))

    
    @classmethod
    def extract_definition_from_buffered_reader(cls, filebuf: BufferedReader) -> ICDefinition:
        """Reads TOML data linked to the BufferedReader and genrates an ICDefinition from it

        Args:
            filebuf (BufferedReader): reader pointing to TOML data containing an IC definition

        Returns:
            ICDefinition: Loaded IC definition
        """        
        toml_data: dict[str, Any] = tomllib.load(filebuf)

        # Build a dictionary containing all the parameters to instantiate an ICDefinition
        ic_def_parameters: dict[str, TomlData] = { k:dv for k, v in cls._TOML_KEY_MAP.items() if (dv:=cls._deref_multi(toml_data, v)) is not None }

        return ICDefinition(**ic_def_parameters)