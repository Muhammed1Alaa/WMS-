from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserLogin(UserBase):
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class WarehouseBase(BaseModel):
    name: str

class WarehouseCreate(WarehouseBase):
    pass

class WarehouseOut(WarehouseBase):
    id: int
    class Config:
        orm_mode = True

class StorageLocationBase(BaseModel):
    name: str
    warehouse_id: int

class StorageLocationCreate(StorageLocationBase):
    pass

class StorageLocationOut(StorageLocationBase):
    id: int
    class Config:
        orm_mode = True

class ItemBase(BaseModel):
    name: str
    barcode: str
    quantity: float
    location_id: int

class ItemCreate(ItemBase):
    pass

class ItemUpdate(BaseModel):
    name: Optional[str]
    barcode: Optional[str]
    quantity: Optional[float]
    location_id: Optional[int]

class ItemOut(ItemBase):
    id: int
    class Config:
        orm_mode = True

class StockMovementBase(BaseModel):
    item_id: int
    user_id: int
    from_location_id: Optional[int]
    to_location_id: Optional[int]
    quantity: float
    movement_type: str
    timestamp: Optional[datetime]

class StockMovementCreate(StockMovementBase):
    pass

class StockMovementOut(StockMovementBase):
    id: int
    class Config:
        orm_mode = True
