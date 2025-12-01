"""
API Routes - FastAPI endpoint handlers
Handles HTTP requests and calls service layer
"""

from fastapi import APIRouter, UploadFile, File, Request, HTTPException
from fastapi.responses import JSONResponse
from typing import List, Optional
from services.image_service import ImageService

# Initialize router and service
router = APIRouter()
image_service = ImageService()


@router.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    """
    Upload and index a single image
    
    Request: Multipart form data with image file
    Response: Success message with image ID
    """
    try:
        # Validate file type (basic check)
        if not file.content_type or not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        result = await image_service.upload_image(file)
        
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return JSONResponse(content=result, status_code=200)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@router.post("/upload/batch")
async def upload_images_batch(files: List[UploadFile] = File(...)):
    """
    Upload and index multiple images at once
    
    Request: Multiple image files
    Response: List of uploaded image IDs
    """
    try:
        # Validate all files are images
        for file in files:
            if not file.content_type or not file.content_type.startswith('image/'):
                raise HTTPException(
                    status_code=400, 
                    detail=f"File {file.filename} must be an image"
                )
        
        result = await image_service.upload_images_batch(files)
        return JSONResponse(content=result, status_code=200)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch upload failed: {str(e)}")


@router.post("/search")
async def search(request: Request):
    """
    Search images by text query
    
    Request: JSON body with query text
    Optional query parameters: top_k, namespace
    
    Example:
        POST /api/search?top_k=10&namespace=images
        Body: {"query": "a bearded man"}
    """
    try:
        # Get JSON body
        body = await request.json()
        query = body.get("query", "")
        
        if not query:
            raise HTTPException(status_code=400, detail="Query parameter is required")
        
        # Get optional parameters from query string or body
        top_k = int(request.query_params.get("top_k", body.get("top_k", 10)))
        namespace = request.query_params.get("namespace", body.get("namespace", "images"))
        
        # Validate top_k
        if top_k < 1 or top_k > 100:
            raise HTTPException(status_code=400, detail="top_k must be between 1 and 100")
        
        result = image_service.search_images(query, top_k, namespace)
        
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return JSONResponse(content=result, status_code=200)
        
    except HTTPException:
        raise
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid top_k value")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@router.get("/stats")
async def get_stats():
    """
    Get database statistics
    
    Response: Vector count, dimensions, namespaces
    """
    try:
        stats = image_service.get_database_stats()
        
        if "error" in stats:
            raise HTTPException(status_code=500, detail=stats["error"])
        
        return JSONResponse(content=stats, status_code=200)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get stats: {str(e)}")


@router.delete("/images/{image_id}")
async def delete_image(image_id: str, namespace: Optional[str] = None):
    """
    Delete a specific image from the index
    
    Path parameter: image_id
    Optional query parameter: namespace (defaults to "images")
    
    Response: Success message
    """
    try:
        if not namespace:
            namespace = "images"
        
        result = image_service.delete_image(image_id, namespace)
        
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return JSONResponse(content=result, status_code=200)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Delete failed: {str(e)}")


@router.get("/health")
async def health_check():
    """
    Health check endpoint
    
    Response: Simple status message
    """
    return JSONResponse(
        content={
            "status": "healthy",
            "service": "Lumina API"
        },
        status_code=200
    )


@router.get("/telemetry")
async def get_telemetry():
    """
    Get system telemetry and status information
    
    Response: Detailed system information including database status,
    embedding service status, and uptime
    """
    try:
        telemetry = image_service.get_telemetry()
        return JSONResponse(content=telemetry, status_code=200)
        
    except Exception as e:
        return JSONResponse(
            content={
                "status": "error",
                "error": str(e)
            },
            status_code=500
        )

