from sqlalchemy import Column, ForeignKey, Integer, Numeric, String,DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os


# Connect to DB
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_FILE = os.path.join(BASE_DIR, "project.db")
DATABASE_URL = "sqlite:///" + DATABASE_FILE
engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()

### Test DB Connections
# Test connection
try:
    with engine.connect() as connection:
        print("Database connected successfully!")
except Exception as e:
    print(f"Error connecting to database: {e}")

Session = sessionmaker(bind=engine)
session = Session()

class Plant(Base):
    __tablename__ = 'plants'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    location = Column(String)
    capacity = Column(Integer)

    # Relationship with Products
    plant_products = relationship("PlantProduct", back_populates="plant")
    plant_materials = relationship('PlantMaterial', back_populates='plant')


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    category = Column(String)
    price = Column(Numeric(10, 2), nullable=False)

    plant_products = relationship('PlantProduct', back_populates='product')
    product_materials = relationship('ProductMaterial', back_populates='product')
    order_products = relationship('OrderProduct', back_populates='product')
    storage_products = relationship('StorageProduct', back_populates='product')


class Material(Base):
    __tablename__ = 'materials'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    unit = Column(String)
    cost = Column(Numeric(10, 2), nullable=False)

    product_materials = relationship('ProductMaterial', back_populates='material')
    plant_materials = relationship('PlantMaterial', back_populates='material')
    storage_materials = relationship('StorageMaterial', back_populates='material')


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    order_date = Column(DateTime, nullable=False)  # type: ignore
    customer_name = Column(String, nullable=False)
    status = Column(String, nullable=False)

    order_products = relationship('OrderProduct', back_populates='order')


class PlantProduct(Base):
    __tablename__ = 'plant_products'

    id = Column(Integer, primary_key=True)
    plant_id = Column(Integer, ForeignKey('plants.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Numeric(10, 2), nullable=False)

    plant = relationship('Plant', back_populates='plant_products')
    product = relationship('Product', back_populates='plant_products')


class ProductMaterial(Base):
    __tablename__ = 'product_materials'

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    material_id = Column(Integer, ForeignKey('materials.id'), nullable=False)
    quantity = Column(Numeric(10, 2), nullable=False)

    product = relationship('Product', back_populates='product_materials')
    material = relationship('Material', back_populates='product_materials')


class PlantMaterial(Base):
    __tablename__ = 'plant_materials'

    id = Column(Integer, primary_key=True)
    plant_id = Column(Integer, ForeignKey('plants.id'), nullable=False)
    material_id = Column(Integer, ForeignKey('materials.id'), nullable=False)
    quantity = Column(Numeric(10, 2), nullable=False)

    plant = relationship('Plant', back_populates='plant_materials')
    material = relationship('Material', back_populates='plant_materials')


class OrderProduct(Base):
    __tablename__ = 'order_products'

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)

    order = relationship('Order', back_populates='order_products')
    product = relationship('Product', back_populates='order_products')


class StorageProduct(Base):
    __tablename__ = 'storage_products'

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)

    product = relationship('Product', back_populates='storage_products')


class StorageMaterial(Base):
    __tablename__ = 'storage_materials'

    id = Column(Integer, primary_key=True)
    material_id = Column(Integer, ForeignKey('materials.id'), nullable=False)
    quantity = Column(Integer, nullable=False)

    material = relationship('Material', back_populates='storage_materials')


Base.metadata.create_all(engine)