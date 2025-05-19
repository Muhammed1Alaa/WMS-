from pydantic import BaseModel
from typing import Optional, List

class StorageLocationBase(BaseModel):
    name: str
    code: str
    type: Optional[str] = None
    capacity: Optional[int] = None

class StorageLocationCreate(StorageLocationBase):
    warehouse_id: int

class StorageLocationUpdate(StorageLocationBase):
    pass

class StorageLocation(StorageLocationBase):
    id: int
    warehouse_id: int

    class Config:
        from_attributes = True

class WarehouseBase(BaseModel):
    name: str
    code: str
    address: Optional[str] = None
    description: Optional[str] = None

class WarehouseCreate(WarehouseBase):
    pass

class WarehouseUpdate(WarehouseBase):
    pass

class Warehouse(WarehouseBase):
    id: int
    storage_locations: List[StorageLocation] = []

    class Config:
        from_attributes = True 