from sqlalchemy import Column, String, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum
from app.models.base import BaseModel

class MovementType(enum.Enum):
    INBOUND = "inbound"
    OUTBOUND = "outbound"
    TRANSFER = "transfer"

class InventoryItem(BaseModel):
    __tablename__ = "inventory_items"

    name = Column(String, nullable=False)
    barcode = Column(String, unique=True, nullable=False)
    quantity = Column(Integer, default=0)
    storage_location_id = Column(Integer, ForeignKey("storage_locations.id"), nullable=False)
    description = Column(String)
    min_quantity = Column(Integer, default=0)
    
    # Relationships
    storage_location = relationship("StorageLocation", back_populates="items")
    movements = relationship("StockMovement", back_populates="item")

class StockMovement(BaseModel):
    __tablename__ = "stock_movements"

    item_id = Column(Integer, ForeignKey("inventory_items.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    movement_type = Column(Enum(MovementType), nullable=False)
    from_location_id = Column(Integer, ForeignKey("storage_locations.id"))
    to_location_id = Column(Integer, ForeignKey("storage_locations.id"))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    notes = Column(String)
    
    # Relationships
    item = relationship("InventoryItem", back_populates="movements")
    from_location = relationship("StorageLocation", foreign_keys=[from_location_id])
    to_location = relationship("StorageLocation", foreign_keys=[to_location_id])
    user = relationship("User") 