
from .registry_base import RegistryBase
from .registry_dict import RegistryDict
from .registry_main import RegistryMain

class RegistryID(str):

    def __new__(cls, namespace: str, id: str):
        return str.__new__(cls, f"{namespace}:{id}")
