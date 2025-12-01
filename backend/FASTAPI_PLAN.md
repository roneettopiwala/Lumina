# FastAPI Backend Implementation Plan

## Overview
This document outlines the plan to create a simple, readable FastAPI backend for the Lumina image search application.

## Project Structure
```
backend/
├── main.py                 # FastAPI app entry point
├── api/
│   ├── __init__.py
│   └── routes.py           # API route handlers
├── services/
│   ├── __init__.py
│   └── image_service.py    # Business logic for image operations
├── clipEmbeddings.py       # (existing) Embedding service
├── vectorStore.py          # (existing) Pinecone vector store
└── photos/                 # (existing) Image storage directory
```

## API Endpoints

### 1. **POST /api/upload**
   - **Purpose**: Upload and index a single image
   - **Request**: Multipart form data with image file
   - **Response**: Success message with image ID
   - **Example**:
     ```json
     {
       "message": "Image uploaded successfully",
       "image_id": "Image_123",
       "filename": "photo.jpg"
     }
     ```

### 2. **POST /api/upload/batch**
   - **Purpose**: Upload and index multiple images at once
   - **Request**: Multiple image files
   - **Response**: List of uploaded image IDs
   - **Example**:
     ```json
     {
       "message": "Uploaded 5 images",
       "uploaded_ids": ["Image_1", "Image_2", ...],
       "failed": []
     }
     ```

### 3. **POST /api/search**
   - **Purpose**: Search images by text query
   - **Request**: JSON body with query text (top_k and namespace are optional query parameters)
   - **Response**: List of matching images with similarity scores
   - **Example Request**:
     ```
     POST /api/search?top_k=10&namespace=images
     Body: {"query": "a bearded man scratching his beard"}
     ```
   - **Example Response**:
     ```json
     {
       "query": "a bearded man scratching his beard",
       "results": [
         {
           "id": "Image_42",
           "filename": "DSCF3419.JPG",
           "score": 0.85,
           "similarity_percent": 92.5
         },
         ...
       ],
       "total_found": 10
     }
     ```

### 4. **GET /api/stats**
   - **Purpose**: Get database statistics
   - **Response**: Vector count, dimensions, namespaces
   - **Example**:
     ```json
     {
       "total_vectors": 75,
       "dimension": 1024,
       "namespaces": {
         "images": 75
       }
     }
     ```

### 5. **DELETE /api/images/{image_id}**
   - **Purpose**: Delete a specific image from the index
   - **Response**: Success message
   - **Example**:
     ```json
     {
       "message": "Image deleted successfully",
       "image_id": "Image_42"
     }
     ```

### 6. **GET /api/health**
   - **Purpose**: Health check endpoint
   - **Response**: Simple status message
   - **Example**:
     ```json
     {
       "status": "healthy",
       "service": "Lumina API"
     }
     ```

### 7. **GET /api/telemetry**
   - **Purpose**: Get system telemetry and status information
   - **Response**: Detailed system information
   - **Example**:
     ```json
     {
       "status": "operational",
       "database": {
         "connected": true,
         "total_vectors": 75,
         "namespaces": ["images"]
       },
       "embedding_service": {
         "available": true,
         "model": "embed-v4.0"
       },
       "uptime_seconds": 3600
     }
     ```

## Code Organization

### main.py (Entry Point)
- Initialize FastAPI app
- Include CORS middleware (for frontend integration)
- Register API routes
- Include `if __name__ == "__main__"` block with uvicorn.run() so you can run it with: `python main.py`

### api/routes.py
- Define all endpoint functions
- Handle HTTP requests/responses
- Parse JSON request bodies manually (simple dict access)
- Call service layer for business logic
- Return JSON responses (dictionaries)

### services/image_service.py
- `upload_image(image_file, image_id)`: Process single image upload
- `upload_images_batch(image_files)`: Process batch upload
- `search_images(query, top_k, namespace)`: Perform semantic search
- `delete_image(image_id, namespace)`: Delete image from index
- `get_database_stats()`: Get statistics
- `get_telemetry()`: Get system telemetry information (database status, embedding service status, uptime)

## Key Features

### 1. **Simple & Readable**
   - Clear function names
   - Comments explaining what each section does
   - Logical flow: Route → Service → Existing Classes

### 2. **Error Handling**
   - Try-catch blocks with meaningful error messages
   - HTTP status codes (400, 404, 500, etc.)
   - User-friendly error responses

### 3. **File Upload Handling**
   - Accept common image formats (JPG, PNG, etc.)
   - Validate file size
   - Generate unique IDs for images

### 4. **Rate Limiting Consideration**
   - Note in code about Cohere API rate limits
   - Batch processing where possible
   - Clear error messages if rate limited

## Dependencies
- FastAPI (already in venv)
- uvicorn (already in venv)
- python-multipart (for file uploads - may need to install: `pip install python-multipart`)

## Example Code Structure Preview

### main.py (simplified preview)
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router
import uvicorn

app = FastAPI(title="Lumina API", version="1.0")

# Allow frontend to call API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routes
app.include_router(router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Lumina API is running"}

# Run the server when you execute: python main.py
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
```

### api/routes.py (simplified preview)
```python
from fastapi import APIRouter, UploadFile, File
from fastapi.requests import Request
from services.image_service import ImageService

router = APIRouter()
image_service = ImageService()

@router.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    """Upload and index a single image"""
    # Call service to handle the upload
    result = await image_service.upload_image(file)
    return result

@router.post("/search")
async def search(request: Request):
    """Search images by text query"""
    # Get JSON body as dictionary
    body = await request.json()
    query = body.get("query", "")
    top_k = body.get("top_k", 10)
    namespace = body.get("namespace", "images")
    
    # Call service
    results = image_service.search_images(query, top_k, namespace)
    return results
```

## Testing
- Run the server: `python main.py` (or `python3 main.py`)
- Server will start on `http://localhost:8000`
- Use FastAPI's automatic `/docs` endpoint at `http://localhost:8000/docs` for interactive testing
- Example curl commands will be provided in comments

## Next Steps After Approval
1. Create file structure (api/, services/ directories)
2. Implement services/image_service.py
3. Implement api/routes.py
4. Implement main.py
5. Test all endpoints
6. Add error handling

---

**Ready to implement?** This plan keeps the code simple, readable, and easy to modify. Each file has a clear purpose, and the flow is straightforward.

