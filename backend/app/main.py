from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, warehouse, item, movement

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(warehouse.router, prefix="/warehouses", tags=["warehouses"])
app.include_router(item.router, prefix="/items", tags=["items"])
app.include_router(movement.router, prefix="/movements", tags=["movements"])

@app.get("/")
async def root():
    return {"message": "WMS API is running"}
