from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas import StockMovementCreate, StockMovementOut
from app.models import StockMovement, Item, StorageLocation, User
from app.auth import get_current_user

router = APIRouter(
    prefix="/movements",
    tags=["movements"]
)

@router.post("/", response_model=StockMovementOut)
def create_movement(
    movement: StockMovementCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Verify item exists
    item = db.query(Item).filter(Item.id == movement.item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Verify locations exist if provided
    if movement.from_location_id:
        from_location = db.query(StorageLocation).filter(StorageLocation.id == movement.from_location_id).first()
        if not from_location:
            raise HTTPException(status_code=404, detail="From location not found")
    
    if movement.to_location_id:
        to_location = db.query(StorageLocation).filter(StorageLocation.id == movement.to_location_id).first()
        if not to_location:
            raise HTTPException(status_code=404, detail="To location not found")
    
    # Create movement
    db_movement = StockMovement(
        item_id=movement.item_id,
        user_id=current_user.id,
        from_location_id=movement.from_location_id,
        to_location_id=movement.to_location_id,
        quantity=movement.quantity,
        movement_type=movement.movement_type
    )
    
    # Update item quantity based on movement type
    if movement.movement_type == "inbound":
        item.quantity += movement.quantity
    elif movement.movement_type == "outbound":
        if item.quantity < movement.quantity:
            raise HTTPException(status_code=400, detail="Insufficient stock")
        item.quantity -= movement.quantity
    elif movement.movement_type == "move":
        if item.quantity < movement.quantity:
            raise HTTPException(status_code=400, detail="Insufficient stock")
        item.location_id = movement.to_location_id
    
    db.add(db_movement)
    db.commit()
    db.refresh(db_movement)
    return db_movement

@router.get("/", response_model=List[StockMovementOut])
def get_movements(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    movements = db.query(StockMovement).offset(skip).limit(limit).all()
    return movements

@router.get("/{movement_id}", response_model=StockMovementOut)
def get_movement(
    movement_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    movement = db.query(StockMovement).filter(StockMovement.id == movement_id).first()
    if not movement:
        raise HTTPException(status_code=404, detail="Movement not found")
    return movement

@router.get("/item/{item_id}", response_model=List[StockMovementOut])
def get_item_movements(
    item_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    movements = db.query(StockMovement)\
        .filter(StockMovement.item_id == item_id)\
        .offset(skip)\
        .limit(limit)\
        .all()
    return movements 