
import re
import logging
from typing import *
from abc import ABC

from ttforge.core.exception import TTForgeException

LOG = logging.getLogger(f"{__name__}")

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

class TTForgeObjectInvalid(TTForgeException):
    pass

class TTForgeObject(ABC):

    NAME: str = None
    ID: str = None
    REGISTRY_ID: str = None
    TAGS: Dict[str, Any] = {}

def tag(tagID: str, tagValue: Any = None):
    def decorator(cls: type[TTForgeObject]):
        if not hasattr(cls, "TAGS"):
            raise TTForgeException(f"Class {cls} is not taggable")
        if tagID in cls.TAGS:
            LOG.warning(f"TAG \"{tagID}\" already present in {cls.NAME} overriding value {cls.TAGS[tagID]} with {tagValue}")
        cls.TAGS[tagID] = tagValue
        return cls
    return decorator

def ttforge_object(namespace: str, tags: Dict[str, Any] = {}):
    def decorator(cls: type[TTForgeObject]):
        if cls.NAME is None:
            raise TTForgeObjectInvalid("Characteristic does not have name set")

        # Set TAGS
        for k, v in tags.items():
            tag(k, v)(cls)

        # Set registry ID
        if cls.ID is None:
            regID = cls.NAME.lower().replace(' ','_')
            try:
                validateRegistryID(regID)
            except TTForgeValidateRegistryIDError as e:
                raise TTForgeObjectInvalid(f"Characteristic \"{cls.NAME}\" does not have registry ID set and trying to derive it from name returned {regID} -> {e}")
            cls.ID = regID
        cls.REGISTRY_ID = f"{namespace}:{cls.ID}"

        return cls
    return decorator
