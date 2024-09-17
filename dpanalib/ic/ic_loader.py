"""This class contains code to extract an IC definition from a properly formatted TOML file read from a BufferedReader"""

from io import BufferedReader
from typing import Any, final
from dpanalib.ic.ic_definition import ICDefinition

import tomllib

@final
class ICLoader:
    _KEY_NAME: str = 'name'
    _KEY_PINOUT: str = 'pinout'
    _KEY_PINOUT_PINS_PER_SIDE = 'pins_per_side'
    _KEY_PINOUT_ZIFMAP:str = 'ZIF_map'
    _KEY_PINOUT_NAMES_OVERRIDE = 'names_override'
    _KEY_PINOUT_CLKP:str = 'clk_pins'
    _KEY_PINOUT_INP:str = 'in_pins'
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

    @classmethod
    def extract_definition_from_buffered_reader(cls, filebuf: BufferedReader) -> ICDefinition:
        toml_data: dict[str, Any] = tomllib.load(filebuf)

        return ICDefinition(name=toml_data[cls._KEY_NAME],
                                pins_per_side=toml_data[cls._KEY_PINOUT][cls._KEY_PINOUT_PINS_PER_SIDE],
                                zif_map=toml_data[cls._KEY_PINOUT][cls._KEY_PINOUT_ZIFMAP],
                                clk_pins=toml_data[cls._KEY_PINOUT][cls._KEY_PINOUT_CLKP],
                                in_pins=toml_data[cls._KEY_PINOUT][cls._KEY_PINOUT_INP],
                                io_pins=toml_data[cls._KEY_PINOUT][cls._KEY_PINOUT_IOP],
                                o_pins=toml_data[cls._KEY_PINOUT][cls._KEY_PINOUT_OP],
                                f_pins=toml_data[cls._KEY_PINOUT][cls._KEY_PINOUT_FP],
                                hiz_o_pins=toml_data[cls._KEY_PINOUT][cls._KEY_PINOUT_HIZ_O],
                                q_pins=toml_data[cls._KEY_PINOUT][cls._KEY_PINOUT_QP],
                                oe_l_pins=toml_data[cls._KEY_PINOUT][cls._KEY_PINOUT_OEL],
                                oe_h_pins=toml_data[cls._KEY_PINOUT][cls._KEY_PINOUT_OEH],
                                hw_model=toml_data[cls._KEY_REQUIREMENTS][cls._KEY_REQUIREMENTS_HARDWARE],
                                adapter_hi_pins=toml_data[cls._KEY_ADAPTER][cls._KEY_ADAPTER_HI_PINS],
                                pin_rot_shift=toml_data[cls._KEY_PINOUT].get(cls._KEY_PINOUT_ROT_SHIFT, 0),
                                adapter_notes=toml_data[cls._KEY_ADAPTER].get(cls._KEY_ADAPTER_NOTES, None),
                                pin_names_override=toml_data[cls._KEY_PINOUT].get(cls._KEY_PINOUT_NAMES_OVERRIDE, []))
