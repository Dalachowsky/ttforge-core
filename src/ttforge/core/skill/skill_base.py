
from abc import abstractmethod
from typing import *

from ttforge.system import TTForgeSystem

from ttforge.core import TTForgeObject, ttforge_object
from ttforge.core.characteristic import CharacteristicBase, ICharacteristicObserver
from ttforge.core.characteristic import CharacteristicUpdateEvent
from ttforge.core.exception import DoesNotDepend

class SkillBase(TTForgeObject, ICharacteristicObserver):

    DEPENDENCIES: List[str] = []

    def __init__(self, value: float | int) -> None:
        self._observedValues: Dict[str, float | int] = {}
        self._valueBase = value
        self._value = value

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
            raise DoesNotDepend(self.REGISTRY_ID, regID) 

    def _setValue(self, value):
        self._value = value

    def recalculate(self):
        self._setValue(self._recalculate())

    @abstractmethod
    def _recalculate(self) -> float | int:
        pass

def skill(namespace: str):
    """Decorator for @skill"""
    def decorator(cls: type[SkillBase]):
        ttforge_object(namespace)(cls)
        TTForgeSystem().registry.registerSkill(cls)
        return cls
    return decorator