import uuid
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.middleware.error_handler import ErrorHandler
from src.config import Config
from src.api.routes import auth, todos
from src.database.database import create_db_and_tables

# Create the FastAPI app
app = FastAPI(
    title="Todo Web Application API",
    description="REST API for the Todo Web Application with authentication and todo management",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:3002",
        "http://localhost:3003",
        "http://localhost:3004",
        "http://localhost:3005",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "http://127.0.0.1:3002",
        "http://127.0.0.1:3003",
        "http://127.0.0.1:3004",
        "http://127.0.0.1:3005",
        "http://localhost:8000",  # For direct API testing
        "http://127.0.0.1:8000"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "X-Requested-With"],
)

# Add global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return await ErrorHandler.handle_error(request, exc)

# Include API routes
app.include_router(auth.router, prefix="/api", tags=["authentication"])
app.include_router(todos.router, prefix="/api", tags=["todos"])

@app.on_event("startup")
async def startup_event():
    """Initialize database tables on startup"""
    print("Creating database tables...")
    create_db_and_tables()
    print("Database tables created successfully!")

@app.get("/")
def read_root():
    """Root endpoint to verify API is running"""
    return {
        "message": "Welcome to the Todo Web Application API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": __import__('datetime').datetime.utcnow().isoformat()}