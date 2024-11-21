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

    # Check that there is no difference between a TOML generated from the string built upon our definition
    # and the TOML read directly from the file
    assert(not DeepDiff(toml_rebuilt_struct, toml_structure_PAL16L8))