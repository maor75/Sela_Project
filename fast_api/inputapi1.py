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

client = MongoClient(f"mongodb://{MONGO_DB_USERNAME}:{MONGO_DB_PASSWORD}@localhost:{MONGO_DB_PORT}")
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

@app.post("/delete")
def delete_customer(customer: Customer):
    try:
        db.customers.delete_one(customer.dict())
        return {"message": "Customer delete successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error delete customer")
    
@app.post("/update")
def update_customer(customer: Customer):
    try:
        current_customer = db.customers.find_one({"mail": customer.mail})
        if not current_customer:
            raise HTTPException(status_code=404, detail="Customer not found")

        # Build the update query based on provided data
        update_data = {}
        if customer.name != current_customer.get("name"):
            update_data["name"] = customer.name
        if customer.phone != current_customer.get("phone"):
            update_data["phone"] = customer.phone
        # If no changes, raise an exception or handle it accordingly
        if not update_data:
            return {"message": "No changes detected."}

        result = db.customers.find_one_and_update(
            {"mail": customer.mail},
            {"$set": update_data},
            return_document=True
        )

        return {"message": "Customer updated successfully.", "updated_customer": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating customer: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)