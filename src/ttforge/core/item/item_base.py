
import re

from ttforge.core.object import TTForgeObject
from ttforge.core.object.decorator import TTForgeObjectDecorator
from ttforge.core.exception import TTForgeException

from ttforge.core.entity import TTForgeEntity
from ttforge.system import TTForgeSystem

class TTForgeOuncesParsingError(TTForgeException):
    def __init__(self, weightString: str) -> None:
        super().__init__(f"Cannot parse ounces from \"{weightString}\"")

def parseOunces(weightOz: str):
    try:
        return round(float(re.match(r"(\d+\.?\d*)\s*oz", weightOz).group(1)) / 35.27, 2)
    except Exception as e:
        raise TTForgeOuncesParsingError(weightOz) 

class ItemBase(TTForgeObject, TTForgeEntity):

    # Weight in kg
    WEIGHT = 0.0

    def __init__(self):
        super().__init__()

    @classmethod
    def isUnique(cls):
        """Whether the item is unique or can it be stacked"""
        return cls.SERIAL_MODEL is not None

    def getWeight(self):
        """Weight in kg"""
        return self.WEIGHT

    def getWeightOunces(self):
        return self.getWeight() * 35.27

#class ItemContainer(ItemBase):
#
#    def __init__(self):
#        # TODO inventory class
#        self._inventory = Inventory()
#
#    def getWeight(self):
#        """Weight in kg"""
#        return self._inventory.getWeight()

#def tagItemSlot(slotID: str):
#    """
#    Add tag core:itemSlot to class.
#    This is a recommended way to indicate that item is equippable.
#    """
#    def decorator(cls: type[ItemBase]):
#        # TODO check slot ID?
#        tag("core:itemSlot", slotID)(cls)
#        return cls
#    return decorator

def item(namespace: str):
    def decorator(cls: type[ItemBase]):
        TTForgeObjectDecorator(namespace)(cls)

        if isinstance(cls.WEIGHT, str):
            cls.WEIGHT = parseOunces(cls.WEIGHT)
        TTForgeSystem().registry.registerItem(cls)
        return cls
    return decorator