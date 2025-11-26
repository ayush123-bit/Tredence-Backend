"""
Script to initialize MongoDB with sample data
Run: python init_mongo.py
"""
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "pair_programming")

def init_database():
    client = MongoClient(MONGODB_URL)
    db = client[DATABASE_NAME]
    
    # Create rooms collection with indexes
    rooms = db.rooms
    rooms.create_index("room_id", unique=True)
    rooms.create_index("created_at")
    
    print(f"✅ Database '{DATABASE_NAME}' initialized successfully")
    print(f"✅ Indexes created on 'rooms' collection")
    
    # Check existing rooms
    count = rooms.count_documents({})
    print(f"📊 Current room count: {count}")
    
    client.close()

if __name__ == "__main__":
    init_database()