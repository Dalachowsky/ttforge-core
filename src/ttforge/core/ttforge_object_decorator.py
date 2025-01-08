
import logging
from typing import *

from ttforge.core.exception import TTForgeException
from ttforge.system.system import TTForgeSystem

from .ttforge_object import TTForgeObject, TTForgeObjectInvalid, generateRegistryID, objectNameToID, TTForgeValidateRegistryIDError, validateRegistryID

LOG = logging.getLogger(f"{__name__}")

class TTForgeDecoratorInvalid(TTForgeException):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)

TTForgeObjectDecoratorType = Callable[
    [str], Callable[
        [type[TTForgeObject]], type[TTForgeObject]
    ]]
decoratorStep = Callable[[type[TTForgeObject]], type[TTForgeObject]]

def TTForgeObjectDecorator(namespace: str, steps: List[decoratorStep] = [], base=None):
    def decorator(cls: type[TTForgeObject]):
        if cls.NAME is None:
            raise TTForgeObjectInvalid(f"Object {cls} does not have name set")

        # Set TAGS
        #for k, v in tags.items():
        #    tag(k, v)(cls)

        # Set registry ID
        if cls.ID is None:
            regID = objectNameToID(cls.NAME)
            try:
                validateRegistryID(regID)
            except TTForgeValidateRegistryIDError as e:
                raise TTForgeObjectInvalid(f"Characteristic \"{cls.NAME}\" does not have registry ID set and trying to derive it from name returned {regID} -> {e}")
            cls.ID = regID
        cls.REGISTRY_ID = generateRegistryID(namespace, cls.ID)

        if base is not None:
            base(namespace)(cls)

        for step in steps:
            cls = step(cls)
        return cls
    return decorator

def checkForAttribute(cls: type[TTForgeObject], name: str):
    if not hasattr(cls, name) or getattr(cls, name) == None:
        raise TTForgeObjectInvalid(f"Object {cls} does not have {name} set")
    return cls

def setAttributeDefault(cls: type[TTForgeObject], name: str, default: Any):
    if not hasattr(cls, name):
        setattr(cls, name, default)
    return cls

class TTForgeDecoratorBuilder:
    def __init__(self) -> None:
        self.reset()

    def reset(self):
        self._decorator_steps: List[decoratorStep] = []
        self._baseDecorator: TTForgeObjectDecoratorType | None = None
        self._targetRegistry: str | None = None

    def setBaseDecorator(self, base: TTForgeObjectDecoratorType):
        self._baseDecorator = base

    def addStep(self, step: decoratorStep):
        self._decorator_steps.append(step)

    def addAttribute(self, 
                    name: str, 
                    default: Any = None,
                    required = True):
        if required:
            self.addStep(lambda cls: checkForAttribute(cls, name))
            if default is not None:
                raise Exception(f"Cannot have default and required specified for attribute")
        else:
            self.addStep(lambda cls: setAttributeDefault(cls, name, default))

    def setRegistry(self, registryName: str):
        self._targetRegistry = registryName

    def build(self) -> Callable[[str], Callable[[type[TTForgeObject]], type[TTForgeObject]]]:
        if self._targetRegistry is not None:
            def registerStep(cls: type[TTForgeObject], reg: str):
                TTForgeSystem().registry.register(reg, cls)
                return cls
            self.addStep(lambda cls, reg=self._targetRegistry: registerStep(cls, reg))
        return lambda NS, steps=self._decorator_steps, base=self._baseDecorator: TTForgeObjectDecorator(NS, steps, base=base)

def tag(tagID: str, tagValue: Any = None):
    def decorator(cls: type[TTForgeObject]):
        if not hasattr(cls, "TAGS"):
            raise TTForgeException(f"Class {cls} is not taggable")
        if tagID in cls.TAGS:
            LOG.warning(f"TAG \"{tagID}\" already present in {cls.NAME} overriding value {cls.TAGS[tagID]} with {tagValue}")
        cls.TAGS[tagID] = tagValue
        return cls
    return decorator

def tagIcon(iconPath: str):
    """
    Add core:icon tag to class.
    This tag is recommended for setting the displayed icon in UI
    """
    def decorator(cls: type[TTForgeObject]):
        tag("core:icon", iconPath)(cls)
        return cls
    return decorator

def ttforgeObjectClassFromJSON(cls, namespace: str, d: dict):
        cls.NAME = d["name"]
        cls.ID = d.get("id", None)
        cls.REGISTRY_ID = d.get("registryID", None)
        TTForgeObjectDecorator(namespace)(cls)
        return cls