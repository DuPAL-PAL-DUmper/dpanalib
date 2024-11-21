"""Tests for TOML generation from IC definitions"""

# pylint: disable=wrong-import-position,wrong-import-order

import sys

import tomllib

sys.path.insert(0, './src') # Make VSCode happy...

from dpanalib.ic.ic_definition import ICDefinition
from dpanalib.ic.ic_loader import ICLoader

from deepdiff import DeepDiff

def test_PAL16L8_toml_generation(ic_definition_PAL16L8, toml_structure_PAL16L8):
    toml_rebuilt_struct = tomllib.loads(ICLoader.rebuild_toml_from_definition(ic_definition_PAL16L8))

    # Exclude these entries, as they are optional, the definition sets a default value for them
    # causing a false positive for a mismatch to trigger
    exclude_paths: list[str] = [
        'root[\'pinout\'][\'rot_shift\']',
        'root[\'pinout\'][\'names_override\']',
        'root[\'adapter\'][\'adapter_notes\']',
    ]

    # Check that there is no difference between a TOML generated from the string built upon our definition
    # and the TOML read directly from the file
    assert(not DeepDiff(toml_rebuilt_struct, toml_structure_PAL16L8, exclude_paths=exclude_paths))