from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class Warehouse(BaseModel):
    __tablename__ = "warehouses"

    name = Column(String, nullable=False)
    code = Column(String, unique=True, nullable=False)
    address = Column(String)
    description = Column(String)
    
    # Relationships
    storage_locations = relationship("StorageLocation", back_populates="warehouse", cascade="all, delete-orphan")

class StorageLocation(BaseModel):
    __tablename__ = "storage_locations"

    name = Column(String, nullable=False)
    code = Column(String, nullable=False)
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=False)
    type = Column(String)  # e.g., "rack", "bin", "shelf"
    capacity = Column(Integer)
    
    # Relationships
    warehouse = relationship("Warehouse", back_populates="storage_locations")
    items = relationship("InventoryItem", back_populates="storage_location") 