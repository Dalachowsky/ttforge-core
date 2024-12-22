import logging
import random
from typing import *
from abc import ABC, abstractmethod

from .characteristic_base import CharacteristicBase, characteristic_base, ICharacteristicObserver, CharacteristicUpdateEvent
from .exceptions import CharacteristicInvalid

from ttforge.core.dice import IDie
from ttforge.core.exception import DoesNotDepend

LOG = logging.getLogger(f"{__name__}")

class CharacteristicDerivedBase(CharacteristicBase, ICharacteristicObserver):

    DEPENDENCIES: List[str] = None

    ABBREV: str = None

    def __init__(self):
        super().__init__(0)
        self._observedValues: Dict[str, int | float] = {}

    def connectObservables(self, getObservableCallback: Callable[[str], CharacteristicBase]):
        for dep in self.DEPENDENCIES:
            observable = getObservableCallback(dep)
            observable.registerObserver(self)
            self._observedValues[observable.REGISTRY_ID] = observable.getValue()
        self.recalculate()

    def onCharacteristicUpdate(self, event: CharacteristicUpdateEvent):
        self._observedValues[event.regID] = event.value
        self.recalculate()

    def getValue(self):
        return self._value

    def getDep(self, regID: str):
        """Get value of dependency"""
        try:
            return self._observedValues[regID]
        except KeyError as e:
            raise DoesNotDepend(self, regID) 

    def _setValue(self, value):
        self._value = value
        self._notifyObservers()

    def recalculate(self):
        self._setValue(self._recalculate())

    @abstractmethod
    def _recalculate(self) -> float | int:
        """
        Called every time a dependency is updated. 
        Values of dependent characteristics can be accessed by self.getDep()
        Should return new value
        """
        pass

def characteristicDerived(namespace: str):
    '''Decorator for derived characteristic'''
    def decorator(cls: type[CharacteristicDerivedBase]):
        characteristic_base(namespace)(cls)
        if cls.DEPENDENCIES is None:
            raise CharacteristicInvalid(f"{cls.REGISTRY_ID} DEPENDENCIES not defined")
        if len(cls.DEPENDENCIES) == 0:
            raise CharacteristicInvalid(f"{cls.REGISTRY_ID}: DEPENDENCIES list is empty")
        return cls
    return decorator

def sortDerivedCharacteristics(list: List[CharacteristicDerivedBase]):
    ITERATIONS_REMAINING = len(list)*2

    listReordered = True
    while listReordered and ITERATIONS_REMAINING > 0: 
        listReordered = False
        for i, ch in enumerate(list):
            for dep in ch.DEPENDENCIES:
                # Check if depnedent characteristic is located after this one
                for j, _ch in enumerate(list[i:]):
                    if dep == _ch.REGISTRY_ID:
                        # Move after the dependent
                        list = list[:i] + list[i+1:j+1] + [_ch] + list[j+1:]
                        listReordered = True
                        continue

        ITERATIONS_REMAINING -= 1
    return list