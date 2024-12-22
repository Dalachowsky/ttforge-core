
from .registry_base import RegistryBase
from .registry_base import RegistryDict

from .utils import validateRegistryID
from .utils import TTForgeValidateRegistryIDError

class RegistryID(str):

    def __new__(cls, namespace: str, id: str):
        return str.__new__(cls, f"{namespace}:{id}")
