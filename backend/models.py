from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    movements = relationship("StockMovement", back_populates="user")

class Warehouse(Base):
    __tablename__ = "warehouses"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    locations = relationship("StorageLocation", back_populates="warehouse")

class StorageLocation(Base):
    __tablename__ = "storage_locations"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"))
    warehouse = relationship("Warehouse", back_populates="locations")
    items = relationship("Item", back_populates="location")

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    barcode = Column(String, unique=True, index=True, nullable=False)
    quantity = Column(Float, default=0)
    location_id = Column(Integer, ForeignKey("storage_locations.id"))
    location = relationship("StorageLocation", back_populates="items")
    movements = relationship("StockMovement", back_populates="item")

class StockMovement(Base):
    __tablename__ = "stock_movements"
    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("items.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    from_location_id = Column(Integer, ForeignKey("storage_locations.id"), nullable=True)
    to_location_id = Column(Integer, ForeignKey("storage_locations.id"), nullable=True)
    quantity = Column(Float, nullable=False)
    movement_type = Column(String, nullable=False)  # inbound, outbound, move
    timestamp = Column(DateTime, default=datetime.utcnow)
    item = relationship("Item", back_populates="movements")
    user = relationship("User", back_populates="movements")
