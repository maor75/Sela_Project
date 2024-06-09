from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

MONGO_DB_USERNAME = 'root'
MONGO_DB_PASSWORD = 'maor'
MONGO_DB_HOST = 'mongodb'
MONGO_DB_PORT = 27017
MONGO_DB_NAME = 'mydb'

client = MongoClient(f"mongodb://{MONGO_DB_USERNAME}:{MONGO_DB_PASSWORD}@mongodb")
db = client[MONGO_DB_NAME]

class Customer(BaseModel):
    name: str
    mail: str
    phone: str

class Product(BaseModel):
    id: str
    name: str
    provider: str

@app.get("/customers")
def get_customers():
    try:
        customers = list(db.customers.find({}, {"_id": 0}))  # Fetch all customers and exclude the MongoDB _id field
        return {"table": customers}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to fetch customers")

@app.get("/product")
def get_products():
    try:
        products = list(db.products.find({}, {"_id": 0}))  # Fetch all products and exclude the MongoDB _id field
        return {"table": products}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to fetch products")

@app.post("/input")
def create_customer(customer: Customer):
    try:
        db.customers.insert_one(customer.dict())
        return {"message": "Customer created successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error creating customer")

@app.post("/input_product")
def create_product(products: list[Product]):
    try:
        db.products.insert_many([product.dict() for product in products])
        return {"message": "Products created successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error creating products")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)