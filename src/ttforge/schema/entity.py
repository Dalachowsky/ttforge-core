
from typing import *
from pydantic import BaseModel, Field

# Inventory
# ---------

class InventoryEntryModel(BaseModel):
    id: str
    qty: int = 1
    data: dict = {}

class InventorySchema(BaseModel):
    content: List[InventoryEntryModel] = []


# Base model
# ----------

class TTForgeEntityBaseModel(BaseModel):
    """
    Model used for serialization with all fields.
    Entity SERIAL_MODELs should be based on this class
    and not INHERIT from it.
    """
    inventory: Optional[InventorySchema] = None 
    resourcePools: Optional[List[ResourcePoolSchema]] = None
