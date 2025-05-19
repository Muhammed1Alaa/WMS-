from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.inventory import MovementType

class InventoryItemBase(BaseModel):
    name: str
    barcode: str
    description: Optional[str] = None
    min_quantity: Optional[int] = 0

class InventoryItemCreate(InventoryItemBase):
    storage_location_id: int
    quantity: int = 0

class InventoryItemUpdate(InventoryItemBase):
    storage_location_id: Optional[int] = None
    quantity: Optional[int] = None

class InventoryItem(InventoryItemBase):
    id: int
    quantity: int
    storage_location_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class StockMovementBase(BaseModel):
    item_id: int
    quantity: int
    movement_type: MovementType
    from_location_id: Optional[int] = None
    to_location_id: Optional[int] = None
    notes: Optional[str] = None

class StockMovementCreate(StockMovementBase):
    pass

class StockMovement(StockMovementBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True 