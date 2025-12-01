"""
Lumina API - FastAPI Backend
Main entry point for the image search API
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router
import uvicorn

# Initialize FastAPI app
app = FastAPI(
    title="Lumina API",
    version="1.0",
    description="Image search API using semantic embeddings"
)

# Allow frontend to call API
# In production, replace "*" with specific frontend URL
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all API routes
app.include_router(router, prefix="/api")


@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "Lumina API is running",
        "docs": "/docs",
        "health": "/api/health"
    }


# Run the server when you execute: python main.py
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

