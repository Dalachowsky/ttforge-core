
from typing import *
from abc import ABC, abstractmethod
from dataclasses import dataclass

from ttforge.core.object import TTForgeObject 
from ttforge.core.object.decorator import TTForgeObjectDecorator

from ttforge.schema.entity import ResourcePoolSchema, ResourcePoolType

from ttforge.system import TTForgeSystem

@dataclass
class ResourcePoolUpdateEvent:
    regID: str
    old: ResourcePoolType
    new: ResourcePoolType

class IResourcePoolObserver(ABC):

    @abstractmethod
    def onResourcePoolUpdate(self, event: ResourcePoolUpdateEvent):
        pass

class ResourcePoolBase(TTForgeObject):

    def __init__(self, value: ResourcePoolType, maxval: Optional[ResourcePoolType] = None, minval: Optional[ResourcePoolType] = None) -> None:
        if minval is not None:
            self._min = minval
        else:
            self._min = 0
        self._max = maxval
        self._observers: List[IResourcePoolObserver] = []
        self._value = self._min
        self.set(value)

    def get(self):
        return self._value

    def add(self, value: ResourcePoolType):
        self.set(self._value + value)

    def set(self, value: ResourcePoolType):
        evt = ResourcePoolUpdateEvent(
            regID=self.REGISTRY_ID,
            old=self._value,
            new = value
            )

        self._value = value
        if value < self._min:
            self._value = self._min
        if self._max is not None and value > self._max:
            self._value = self._max

        evt.new = self._value
        self._notifyObservers(evt)

    @classmethod
    def deserialize(cls, data: dict):
        d = ResourcePoolSchema.model_validate(data)
        kwargs = {}
        if d.value is not None:
            kwargs["value"] = d.value
        if d.minVal is not None:
            kwargs["minval"] = d.minVal
        kwargs["maxval"] = d.maxVal
        obj = cls(**kwargs)
        return obj

    def registerObserver(self, observer: IResourcePoolObserver):
        self._observers.append(observer)

    def removeObserver(self, observer: IResourcePoolObserver):
        self._observers.remove(observer)

    def _notifyObservers(self, event: ResourcePoolUpdateEvent):
        for o in self._observers:
            o.onResourcePoolUpdate(event)

def resourcePool(namespace: str):
    def decorator(cls: type[ResourcePoolBase]):
        TTForgeObjectDecorator(namespace)(cls)
        TTForgeSystem().registry.registerResourcePool(cls)
        return cls
    return decorator
