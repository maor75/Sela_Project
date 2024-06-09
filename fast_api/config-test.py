from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

# Configuration details
MONGO_DB_USERNAME = 'root'
MONGO_DB_PASSWORD = 'edmon'
MONGO_DB_HOST = 'mongodb'
MONGO_DB_PORT = 27017
MONGO_DB_NAME = 'mydb'

def test_mongodb_connection():
    # Initialize MongoDB client
    client = MongoClient(f"mongodb://{MONGO_DB_USERNAME}:{MONGO_DB_PASSWORD}@mongodb")


    db = client[MONGO_DB_NAME]

    # Test inserting a document
    test_customer = {"name": "Test User", "mail": "test@example.com", "phone": "1234567890"}
    result = db.customers.insert_one(test_customer)
    if result.inserted_id is not None:
        print("Document inserted successfully.")
    else:
        print("Failed to insert document.")

    # Test finding the inserted document
    found_customer = db.customers.find_one({"name": "Test User"})
    if found_customer is not None:
        print("Document found successfully.")
    else:
        print("Failed to find inserted document.")

    # Test deleting the document
    delete_result = db.customers.delete_one({"name": "Test User"})
    if delete_result.deleted_count == 1:
        print("Document deleted successfully.")
    else:
        print("Failed to delete document.")

    # Cleanup
    client.close()

if __name__ == "__main__":
    test_mongodb_connection()
