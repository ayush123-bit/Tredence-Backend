from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.routers import rooms, autocomplete, websocket
from app.database import init_db, close_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize database
    await init_db()
    print("✅ Database initialized successfully")
    yield
    # Shutdown: Close database connection
    await close_db()
    print("👋 Database connection closed")

app = FastAPI(
    title="Pair Programming API",
    description="Real-time collaborative coding platform with MongoDB",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(rooms.router)
app.include_router(autocomplete.router)
app.include_router(websocket.router)

@app.get("/")
def read_root():
    return {
        "message": "Pair Programming API with MongoDB",
        "version": "1.0.0",
        "database": "MongoDB",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "database": "MongoDB"
    }