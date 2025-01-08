
from typing import *
from abc import ABC, abstractmethod
from dataclasses import dataclass

from ttforge.core import TTForgeObject, TTForgeObjectDecorator

from ttforge.system import TTForgeSystem

ResourcePoolType = int | float

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

    def __init__(self, value: ResourcePoolType, maxval: ResourcePoolType, minval: ResourcePoolType = 0) -> None:
        self._min = minval
        self._max = maxval
        self._observers: List[IResourcePoolObserver] = []
        self._value = minval
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
        if value > self._max:
            self._value = self._max

        evt.new = self._value
        self._notifyObservers(evt)

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
