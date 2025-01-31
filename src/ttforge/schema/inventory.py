
from typing import *
from pydantic import BaseModel

class InventoryEntryModel(BaseModel):
    id: str
    qty: int = 1
    data: dict = {}

class InventorySchema(BaseModel):
    content: List[InventoryEntryModel] = []
