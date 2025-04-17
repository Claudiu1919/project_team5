from fastapi import Depends, FastAPI, HTTPException
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from create_db import Base, OrderProduct, Plant, PlantMaterial, PlantProduct, Product, Material, ProductMaterial, StorageProduct, StorageMaterial, Order
from typing import List
from pydantic import BaseModel


### FastAPI example quick setup, need to import base classes for Tables structures
app = FastAPI()


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_FILE = os.path.join(BASE_DIR, "project.db")
DATABASE_URL = "sqlite:///" + DATABASE_FILE
engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()
SessionLocal=sessionmaker(bind=engine, autocommit=False, autoflash=False)

# Test connection
try:
    with engine.connect() as connection:
        print("Database connected successfully!")
except Exception as e:
    print(f"Error connecting to database: {e}")


Session = sessionmaker(bind=engine)
session = Session()


@app.get('/')
async def root():
    return {'message': 'Welcome!'}


# Dependency to get the database session
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class PlantCreate(BaseModel):
    name:str
    location: str
    capacity: int
   


class PlantResponse(BaseModel):
    id: int
    name: str
    location: str
    capacity: int


    class Config:
        from_attributes = True  # Enables compatibility with SQLAlchemy models


class PlantUpdate(BaseModel):
    id: int
    name: str
    location: str
    capacity: int


# get all plants
@app.get("/plants/", response_model=List[PlantCreate])
def read_all_plants(db: Session = Depends(get_db)):
    plants = db.query(Plant).all()
    return plants


#post
@app.post("/plants/", response_model=PlantResponse)
def create_plant(product: PlantCreate, db: Session = Depends(get_db)):
    db_plant = Plant(**product.model_dump())
    db.add(db_plant)
    db.commit()
    db.refresh(db_plant)
    return db_plant

#get id
@app.get("/plants/{plant_id}", response_model=PlantResponse)
def read_plant(plant_id: int, db: Session = Depends(get_db)):
    plant = db.query(Plant).filter(Plant.id == plant_id).first()
    if plant is None:
        raise HTTPException(status_code=404, detail="Plant not found")
    return plant

# PUT /plants/{id}: Update a specific plant.
@app.put("/plants/{plant_id}", response_model=PlantResponse)
def update_plant(plant_id: int, plant: PlantCreate, db: Session = Depends(get_db)):
    db_plant = db.query(Plant).filter(Plant.id == plant_id).first()
    if db_plant is None:
        raise HTTPException(status_code=404, detail="Plant not found")
    
    for key, value in plant.model_dump().items():
        setattr(db_plant, key, value)
    
    db.commit()
    db.refresh(db_plant)
    return db_plant

#delete
app.delete("/plants/{plant_id}")
def delete_plant(plant_id: int, db: Session = Depends(get_db)):
    db_plant = db.query(Plant).filter(Plant.id == plant_id).first()
    if db_plant is None:
        raise HTTPException(status_code=404, detail="Plant not found")
   
    db.delete(db_plant)
    db.commit()
    return {"detail": "Plant deleted"}

# @app.patch("/plants/{plant_id}", response_model=PlantResponse)
# def patch_plant(plant_id: int, plant_update: PlantUpdate, db: Session = Depends(get_db)):
#     db_plant = db.query(Plant).filter(Plant.id == plant_id).first()
#     if db_plant is None:
#         raise HTTPException(status_code=404, detail="Plant not found")
    

