"""
Simple test script to verify MongoDB connection
Run: python test_mongodb.py
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "pair_programming")

async def test_connection():
    try:
        client = AsyncIOMotorClient(MONGODB_URL)
        db = client[DATABASE_NAME]
        
        # Test connection
        await db.command("ping")
        print("✅ MongoDB connection successful!")
        
        # List collections
        collections = await db.list_collection_names()
        print(f"📚 Collections: {collections}")
        
        # Count rooms
        rooms_count = await db.rooms.count_documents({})
        print(f"🏠 Total rooms: {rooms_count}")
        
        client.close()
        
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_connection())