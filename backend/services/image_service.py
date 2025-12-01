"""
Image Service - Business logic for image operations
Handles image upload, embedding, storage, and search operations
"""

import time
import uuid
from typing import List, Dict, Optional
from PIL import Image
from io import BytesIO

from clipEmbeddings import Embedder
from vectorStore import VectorStore


class ImageService:
    """Service class for handling image-related operations"""
    
    def __init__(self):
        """Initialize the image service with embedder and vector store"""
        self.embedder = Embedder()
        self.storage = VectorStore("lumina")
        self.start_time = time.time()  # For uptime calculation
    
    async def upload_image(self, image_file, image_id: Optional[str] = None) -> Dict:
        """
        Upload and index a single image
        
        Args:
            image_file: Uploaded file object
            image_id: Optional custom ID, otherwise generates one
            
        Returns:
            Dictionary with upload result
        """
        try:
            # Generate ID if not provided
            if not image_id:
                image_id = f"Image_{uuid.uuid4().hex[:8]}"
            
            # Read image file (async)
            image_bytes = await image_file.read()
            # Reset file pointer in case it's needed again
            await image_file.seek(0)
            image = Image.open(BytesIO(image_bytes))
            
            # Generate embedding
            embedding = self.embedder.embedImage(image)
            
            # Store in vector database
            self.storage.storeImage(
                imageId=image_id,
                embeddings=embedding,
                fileName=image_file.filename,
                nameSpace="images"
            )
            
            return {
                "message": "Image uploaded successfully",
                "image_id": image_id,
                "filename": image_file.filename
            }
            
        except Exception as e:
            return {
                "error": f"Failed to upload image: {str(e)}",
                "image_id": image_id if image_id else None
            }
    
    async def upload_images_batch(self, image_files: List) -> Dict:
        """
        Upload and index multiple images at once
        
        Args:
            image_files: List of uploaded file objects
            
        Returns:
            Dictionary with batch upload results
        """
        uploaded_ids = []
        failed = []
        
        for image_file in image_files:
            try:
                # Generate unique ID for each image
                image_id = f"Image_{uuid.uuid4().hex[:8]}"
                
                # Read image file (async)
                image_bytes = await image_file.read()
                # Reset file pointer in case it's needed again
                await image_file.seek(0)
                image = Image.open(BytesIO(image_bytes))
                
                # Generate embedding
                embedding = self.embedder.embedImage(image)
                
                # Store in vector database
                self.storage.storeImage(
                    imageId=image_id,
                    embeddings=embedding,
                    fileName=image_file.filename,
                    nameSpace="images"
                )
                
                uploaded_ids.append(image_id)
                
            except Exception as e:
                failed.append({
                    "filename": image_file.filename if hasattr(image_file, 'filename') else "unknown",
                    "error": str(e)
                })
        
        return {
            "message": f"Uploaded {len(uploaded_ids)} images",
            "uploaded_ids": uploaded_ids,
            "failed": failed,
            "total_uploaded": len(uploaded_ids),
            "total_failed": len(failed)
        }
    
    def search_images(self, query: str, top_k: int = 10, namespace: str = "images") -> Dict:
        """
        Search images by text query
        
        Args:
            query: Text query to search for
            top_k: Number of results to return
            namespace: Namespace to search in
            
        Returns:
            Dictionary with search results
        """
        try:
            # Generate query embedding
            query_embedding = self.embedder.embedText(query)
            
            # Perform semantic search
            results = self.storage.semanticSearch(
                queryEmbedding=query_embedding,
                namespace=namespace,
                top_k=top_k
            )
            
            # Format results
            formatted_results = []
            for match in results:
                metadata = match.get('metadata', {})
                formatted_results.append({
                    "id": match.get('id', 'Unknown'),
                    "filename": metadata.get('filename', 'Unknown'),
                    "score": match.get('score', 0),
                    "similarity_percent": ((match.get('score', 0) + 1) / 2) * 100
                })
            
            return {
                "query": query,
                "results": formatted_results,
                "total_found": len(formatted_results)
            }
            
        except Exception as e:
            return {
                "error": f"Search failed: {str(e)}",
                "query": query,
                "results": [],
                "total_found": 0
            }
    
    def delete_image(self, image_id: str, namespace: str = "images") -> Dict:
        """
        Delete a specific image from the index
        
        Args:
            image_id: ID of the image to delete
            namespace: Namespace where the image is stored
            
        Returns:
            Dictionary with deletion result
        """
        try:
            self.storage.deleteId(ids=[image_id], namespace=namespace)
            return {
                "message": "Image deleted successfully",
                "image_id": image_id
            }
        except Exception as e:
            return {
                "error": f"Failed to delete image: {str(e)}",
                "image_id": image_id
            }
    
    def get_database_stats(self) -> Dict:
        """
        Get database statistics
        
        Returns:
            Dictionary with database stats (already JSON-serializable from vectorStore)
        """
        try:
            stats = self.storage.getStats()
            # Stats are already converted to JSON-serializable format in vectorStore.getStats()
            return stats
        except Exception as e:
            return {
                "error": f"Failed to get stats: {str(e)}"
            }
    
    def get_telemetry(self) -> Dict:
        """
        Get system telemetry and status information
        
        Returns:
            Dictionary with system telemetry
        """
        try:
            # Get database stats (this will handle JSON serialization)
            stats = self.get_database_stats()
            
            # Calculate uptime
            uptime_seconds = int(time.time() - self.start_time)
            
            # Check embedding service availability
            # Just check if embedder is initialized (don't make API call)
            embedding_available = (
                hasattr(self.embedder, 'client') and 
                self.embedder.client is not None
            )
            
            return {
                "status": "operational",
                "database": {
                    "connected": True,
                    "total_vectors": stats.get("total_vectors", 0),
                    "dimension": stats.get("dimension", 0),
                    "namespaces": stats.get("namespaces", {})
                },
                "embedding_service": {
                    "available": embedding_available,
                    "model": self.embedder.model
                },
                "uptime_seconds": uptime_seconds
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "database": {
                    "connected": False
                },
                "embedding_service": {
                    "available": False
                }
            }

