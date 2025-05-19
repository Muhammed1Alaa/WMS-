from fastapi import FastAPI
from routers import auth, warehouse, item, movement

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(warehouse.router, prefix="/warehouses", tags=["warehouses"])
app.include_router(item.router, prefix="/items", tags=["items"])
app.include_router(movement.router, prefix="/movements", tags=["movements"])
