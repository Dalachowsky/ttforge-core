
from typing import *
from pydantic import BaseModel, Field

ResourcePoolType = float | int

# Characteristics
# ---------------

class CharacteristicSchema(BaseModel):
    id: str
    value: str

# Inventory
# ---------

class InventoryEntryModel(BaseModel):
    id: str
    qty: int = 1
    data: dict = {}

class InventorySchema(BaseModel):
    content: List[InventoryEntryModel] = []

# Resource pools
# --------------

class ResourcePoolSchema(BaseModel):
    id: str 
    value: ResourcePoolType
    minVal: Optional[ResourcePoolType] = None
    maxVal: Optional[ResourcePoolType] = None

# Base model
# ----------

class TTForgeEntityBaseModel(BaseModel):
    """
    Model used for serialization with all fields.
    Entity SERIAL_MODELs should be based on this class
    and not INHERIT from it.
    """
    characteristics: Optional[List[CharacteristicSchema]] = None
    inventory: Optional[InventorySchema] = None 
    resourcePools: Optional[List[ResourcePoolSchema]] = None
