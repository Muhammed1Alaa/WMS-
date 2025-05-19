from typing import List, Optional
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.inventory import InventoryItem, StockMovement
from app.schemas.inventory import InventoryItemCreate, InventoryItemUpdate, StockMovementCreate

class CRUDInventoryItem(CRUDBase[InventoryItem, InventoryItemCreate, InventoryItemUpdate]):
    def get_by_barcode(self, db: Session, *, barcode: str) -> Optional[InventoryItem]:
        return db.query(InventoryItem).filter(InventoryItem.barcode == barcode).first()

    def get_multi_by_location(
        self, db: Session, *, location_id: int, skip: int = 0, limit: int = 100
    ) -> List[InventoryItem]:
        return (
            db.query(InventoryItem)
            .filter(InventoryItem.storage_location_id == location_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def search_by_name(
        self, db: Session, *, name: str, skip: int = 0, limit: int = 100
    ) -> List[InventoryItem]:
        return (
            db.query(InventoryItem)
            .filter(InventoryItem.name.ilike(f"%{name}%"))
            .offset(skip)
            .limit(limit)
            .all()
        )

class CRUDStockMovement(CRUDBase[StockMovement, StockMovementCreate, StockMovementCreate]):
    def get_multi_by_item(
        self, db: Session, *, item_id: int, skip: int = 0, limit: int = 100
    ) -> List[StockMovement]:
        return (
            db.query(StockMovement)
            .filter(StockMovement.item_id == item_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create_with_item_update(
        self, db: Session, *, obj_in: StockMovementCreate, user_id: int
    ) -> StockMovement:
        # Create the movement record
        db_obj = StockMovement(
            **obj_in.dict(),
            user_id=user_id
        )
        db.add(db_obj)
        
        # Update the item quantity
        item = db.query(InventoryItem).filter(InventoryItem.id == obj_in.item_id).first()
        if not item:
            raise ValueError("Item not found")
            
        if obj_in.movement_type == "inbound":
            item.quantity += obj_in.quantity
        elif obj_in.movement_type == "outbound":
            if item.quantity < obj_in.quantity:
                raise ValueError("Insufficient stock")
            item.quantity -= obj_in.quantity
        elif obj_in.movement_type == "transfer":
            if item.quantity < obj_in.quantity:
                raise ValueError("Insufficient stock")
            item.quantity -= obj_in.quantity
            item.storage_location_id = obj_in.to_location_id
            
        db.add(item)
        db.commit()
        db.refresh(db_obj)
        return db_obj

inventory_item = CRUDInventoryItem(InventoryItem)
stock_movement = CRUDStockMovement(StockMovement) 