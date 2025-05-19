from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.crud import crud_inventory
from app.schemas.inventory import (
    InventoryItem,
    InventoryItemCreate,
    InventoryItemUpdate,
    StockMovement,
    StockMovementCreate,
)

router = APIRouter()

@router.get("/items", response_model=List[InventoryItem])
def read_items(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: Any = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve inventory items.
    """
    items = crud_inventory.inventory_item.get_multi(db, skip=skip, limit=limit)
    return items

@router.post("/items", response_model=InventoryItem)
def create_item(
    *,
    db: Session = Depends(deps.get_db),
    item_in: InventoryItemCreate,
    current_user: Any = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new inventory item.
    """
    item = crud_inventory.inventory_item.get_by_barcode(db, barcode=item_in.barcode)
    if item:
        raise HTTPException(
            status_code=400,
            detail="An item with this barcode already exists.",
        )
    item = crud_inventory.inventory_item.create(db, obj_in=item_in)
    return item

@router.get("/items/{item_id}", response_model=InventoryItem)
def read_item(
    *,
    db: Session = Depends(deps.get_db),
    item_id: int,
    current_user: Any = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get inventory item by ID.
    """
    item = crud_inventory.inventory_item.get(db, id=item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.put("/items/{item_id}", response_model=InventoryItem)
def update_item(
    *,
    db: Session = Depends(deps.get_db),
    item_id: int,
    item_in: InventoryItemUpdate,
    current_user: Any = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an inventory item.
    """
    item = crud_inventory.inventory_item.get(db, id=item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    item = crud_inventory.inventory_item.update(db, db_obj=item, obj_in=item_in)
    return item

@router.get("/items/search/{name}", response_model=List[InventoryItem])
def search_items(
    *,
    db: Session = Depends(deps.get_db),
    name: str,
    skip: int = 0,
    limit: int = 100,
    current_user: Any = Depends(deps.get_current_active_user),
) -> Any:
    """
    Search inventory items by name.
    """
    items = crud_inventory.inventory_item.search_by_name(
        db, name=name, skip=skip, limit=limit
    )
    return items

@router.get("/items/barcode/{barcode}", response_model=InventoryItem)
def get_item_by_barcode(
    *,
    db: Session = Depends(deps.get_db),
    barcode: str,
    current_user: Any = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get inventory item by barcode.
    """
    item = crud_inventory.inventory_item.get_by_barcode(db, barcode=barcode)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.post("/movements", response_model=StockMovement)
def create_stock_movement(
    *,
    db: Session = Depends(deps.get_db),
    movement_in: StockMovementCreate,
    current_user: Any = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new stock movement.
    """
    try:
        movement = crud_inventory.stock_movement.create_with_item_update(
            db, obj_in=movement_in, user_id=current_user.id
        )
        return movement
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/movements/item/{item_id}", response_model=List[StockMovement])
def read_item_movements(
    *,
    db: Session = Depends(deps.get_db),
    item_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: Any = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve stock movements for an item.
    """
    movements = crud_inventory.stock_movement.get_multi_by_item(
        db, item_id=item_id, skip=skip, limit=limit
    )
    return movements 