
import pytest
from ttforge.system import TTForgeSystem

@pytest.fixture(autouse=True)
def clear_TTForge_singleton():
    yield
    TTForgeSystem().clear()