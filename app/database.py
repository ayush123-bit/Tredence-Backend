from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "pair_programming")

# Async client for FastAPI
motor_client = AsyncIOMotorClient(MONGODB_URL)
async_database = motor_client[DATABASE_NAME]

# Sync client for initial setup
sync_client = MongoClient(MONGODB_URL)
sync_database = sync_client[DATABASE_NAME]

def get_database():
    """Get async database instance"""
    return async_database

async def init_db():
    """Initialize database indexes"""
    rooms_collection = async_database.rooms
    
    # Create unique index on room_id
    await rooms_collection.create_index("room_id", unique=True)
    await rooms_collection.create_index("created_at")
    
    print("Database indexes created successfully")

async def close_db():
    """Close database connection"""
    motor_client.close()