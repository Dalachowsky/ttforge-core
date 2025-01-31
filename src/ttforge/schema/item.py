
from typing import *
from pydantic import BaseModel

from ttforge.schema.inventory import InventorySchema

class ContainerItemSchema(BaseModel):
    inventory: InventorySchema = InventorySchema()
