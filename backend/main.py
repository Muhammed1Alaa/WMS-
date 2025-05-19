from fastapi import FastAPI
from routers import auth, warehouse, item

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(warehouse.router, prefix="/warehouses", tags=["warehouses"])
app.include_router(item.router, prefix="/items", tags=["items"])
