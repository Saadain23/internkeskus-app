# app/db/mongodb.py

from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
from bson import ObjectId

class DataBase:
    client: AsyncIOMotorClient = None
    database = None

db = DataBase()

async def connect_to_mongo():
    db.client = AsyncIOMotorClient(settings.MONGODB_URL)
    db.database = db.client[settings.PROJECT_NAME]
    print("Connected to MongoDB.")

async def close_mongo_connection():
    db.client.close()
    print("Closed connection with MongoDB.")

# CRUD operations
def create_document(collection: str, document: dict):
    result = db.database[collection].insert_one(document)
    return str(result.inserted_id)

def read_document(collection: str, document_id: str):
    return db.database[collection].find_one({"_id": ObjectId(document_id)})

def update_document(collection: str, document_id: str, update_data: dict):
    result = db.database[collection].update_one(
        {"_id": ObjectId(document_id)},
        {"$set": update_data}
    )
    return result.modified_count

def delete_document(collection: str, document_id: str):
    result = db.database[collection].delete_one({"_id": ObjectId(document_id)})
    return result.deleted_count
