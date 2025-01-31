
from typing import *
from pydantic import BaseModel, Field

from ttforge.schema.inventory import InventorySchema

class TTForgeEntityModel(BaseModel):
    """Model used for serialization"""
    inventory: Optional[InventorySchema] = None 
