from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.crud import crud_warehouse
from app.schemas.warehouse import (
    Warehouse,
    WarehouseCreate,
    WarehouseUpdate,
    StorageLocation,
    StorageLocationCreate,
    StorageLocationUpdate,
)

router = APIRouter()

@router.get("/", response_model=List[Warehouse])
def read_warehouses(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: Any = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve warehouses.
    """
    warehouses = crud_warehouse.warehouse.get_multi(db, skip=skip, limit=limit)
    return warehouses

@router.post("/", response_model=Warehouse)
def create_warehouse(
    *,
    db: Session = Depends(deps.get_db),
    warehouse_in: WarehouseCreate,
    current_user: Any = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new warehouse.
    """
    warehouse = crud_warehouse.warehouse.get_by_code(db, code=warehouse_in.code)
    if warehouse:
        raise HTTPException(
            status_code=400,
            detail="A warehouse with this code already exists.",
        )
    warehouse = crud_warehouse.warehouse.create(db, obj_in=warehouse_in)
    return warehouse

@router.put("/{warehouse_id}", response_model=Warehouse)
def update_warehouse(
    *,
    db: Session = Depends(deps.get_db),
    warehouse_id: int,
    warehouse_in: WarehouseUpdate,
    current_user: Any = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a warehouse.
    """
    warehouse = crud_warehouse.warehouse.get(db, id=warehouse_id)
    if not warehouse:
        raise HTTPException(status_code=404, detail="Warehouse not found")
    warehouse = crud_warehouse.warehouse.update(db, db_obj=warehouse, obj_in=warehouse_in)
    return warehouse

@router.get("/{warehouse_id}/locations", response_model=List[StorageLocation])
def read_storage_locations(
    *,
    db: Session = Depends(deps.get_db),
    warehouse_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: Any = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve storage locations for a warehouse.
    """
    locations = crud_warehouse.storage_location.get_multi_by_warehouse(
        db, warehouse_id=warehouse_id, skip=skip, limit=limit
    )
    return locations

@router.post("/{warehouse_id}/locations", response_model=StorageLocation)
def create_storage_location(
    *,
    db: Session = Depends(deps.get_db),
    warehouse_id: int,
    location_in: StorageLocationCreate,
    current_user: Any = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new storage location in a warehouse.
    """
    location = crud_warehouse.storage_location.get_by_code(
        db, code=location_in.code, warehouse_id=warehouse_id
    )
    if location:
        raise HTTPException(
            status_code=400,
            detail="A location with this code already exists in this warehouse.",
        )
    location_in.warehouse_id = warehouse_id
    location = crud_warehouse.storage_location.create(db, obj_in=location_in)
    return location

@router.put("/locations/{location_id}", response_model=StorageLocation)
def update_storage_location(
    *,
    db: Session = Depends(deps.get_db),
    location_id: int,
    location_in: StorageLocationUpdate,
    current_user: Any = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a storage location.
    """
    location = crud_warehouse.storage_location.get(db, id=location_id)
    if not location:
        raise HTTPException(status_code=404, detail="Storage location not found")
    location = crud_warehouse.storage_location.update(
        db, db_obj=location, obj_in=location_in
    )
    return location 