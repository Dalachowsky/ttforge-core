
import re
from ttforge.core.exception import TTForgeException

class TTForgeValidateRegistryIDError(TTForgeException):
    def __init__(self, registryID: str, message: str):
        super().__init__(f"registry ID \"{registryID}\" is invalid. {message}")

def validateRegistryID(registryID: str):
    if registryID == "":
        raise TTForgeValidateRegistryIDError(registryID, "Is empty")
    if not re.match(r"^[a-z0-9:_]+$", registryID):
        raise TTForgeValidateRegistryIDError(registryID, "Contains forbidden characters. Allowed characters: a-z0-9")
    if registryID.startswith(':') or registryID.endswith(':'):
        raise TTForgeValidateRegistryIDError(registryID, "Registry ID cannot start nor end with ':'")