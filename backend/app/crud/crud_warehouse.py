from typing import List, Optional
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.warehouse import Warehouse, StorageLocation
from app.schemas.warehouse import WarehouseCreate, WarehouseUpdate, StorageLocationCreate, StorageLocationUpdate

class CRUDWarehouse(CRUDBase[Warehouse, WarehouseCreate, WarehouseUpdate]):
    def get_by_code(self, db: Session, *, code: str) -> Optional[Warehouse]:
        return db.query(Warehouse).filter(Warehouse.code == code).first()

    def get_multi_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Warehouse]:
        return (
            db.query(Warehouse)
            .filter(Warehouse.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

class CRUDStorageLocation(CRUDBase[StorageLocation, StorageLocationCreate, StorageLocationUpdate]):
    def get_by_code(self, db: Session, *, code: str, warehouse_id: int) -> Optional[StorageLocation]:
        return (
            db.query(StorageLocation)
            .filter(StorageLocation.code == code, StorageLocation.warehouse_id == warehouse_id)
            .first()
        )

    def get_multi_by_warehouse(
        self, db: Session, *, warehouse_id: int, skip: int = 0, limit: int = 100
    ) -> List[StorageLocation]:
        return (
            db.query(StorageLocation)
            .filter(StorageLocation.warehouse_id == warehouse_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

warehouse = CRUDWarehouse(Warehouse)
storage_location = CRUDStorageLocation(StorageLocation) 