
import re
import logging
from typing import *
from abc import ABC

from ttforge.core.exception import TTForgeException

LOG = logging.getLogger(f"{__name__}")

class TTForgeValidateRegistryIDError(TTForgeException):
    def __init__(self, registryID: str, message: str):
        super().__init__(f"registry ID \"{registryID}\" is invalid. {message}")

def objectNameToID(objectName: str):
    objectName = objectName.lower().replace(' ','_')
    objectName = re.sub('[^0-9a-zA-Z_]+', '', objectName) # Remove all non alphanumeric characters
    return objectName

def generateRegistryID(namespace: str, ID: str):
    return f"{namespace}:{ID}"

def validateRegistryID(registryID: str):
    if registryID == "":
        raise TTForgeValidateRegistryIDError(registryID, "Is empty")
    if not re.match(r"^[a-z0-9:_]+$", registryID):
        raise TTForgeValidateRegistryIDError(registryID, "Contains forbidden characters. Allowed characters: a-z0-9")
    if registryID.startswith(':') or registryID.endswith(':'):
        raise TTForgeValidateRegistryIDError(registryID, "Registry ID cannot start nor end with ':'")

class TTForgeObjectInvalid(TTForgeException):
    pass

class TTForgeObject(ABC):

    NAME: str = None
    ID: str = None
    REGISTRY_ID: str = None
    TAGS: Dict[str, Any] = {}
