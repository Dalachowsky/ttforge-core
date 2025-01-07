
from tests.unit.fixture import clear_TTForge_singleton

from ttforge.system import TTForgeSystem

def test_import_packages():
    TTForgeSystem().importPackages("tests/unit/test_system/example_modules/modules")
    TTForgeSystem().registry.CHARACTERISTICS.get("test:primary")
    TTForgeSystem().registry.CHARACTERISTICS_DERIVED.get("test:derived")
