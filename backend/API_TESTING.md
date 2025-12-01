# API Testing Guide - Curl Examples

This document provides curl command examples to test all Lumina API endpoints.

**Base URL**: `http://localhost:8000`

---

## 1. Health Check

Simple endpoint to verify the API is running.

```bash
curl -X GET http://localhost:8000/api/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "service": "Lumina API"
}
```

---

## 2. Get Telemetry

Get system telemetry and status information.

```bash
curl -X GET http://localhost:8000/api/telemetry
```

**Expected Response:**
```json
{
  "status": "operational",
  "database": {
    "connected": true,
    "total_vectors": 75,
    "dimension": 1024,
    "namespaces": {
      "images": 75
    }
  },
  "embedding_service": {
    "available": true,
    "model": "embed-v4.0"
  },
  "uptime_seconds": 3600
}
```

---

## 3. Get Database Statistics

Get statistics about the vector database.

```bash
curl -X GET http://localhost:8000/api/stats
```

**Expected Response:**
```json
{
  "total_vectors": 75,
  "dimension": 1024,
  "namespaces": {
    "images": 75
  }
}
```

---

## 4. Upload Single Image

Upload and index a single image.

```bash
curl -X POST http://localhost:8000/api/upload \
  -F "file=@/path/to/your/image.jpg"
```

**Example with actual file (relative path - if you're in the backend directory):**
```bash
curl -X POST http://localhost:8000/api/upload \
  -F "file=@photos/DSCF2724.JPG"
```

**Example with absolute path:**
```bash
curl -X POST http://localhost:8000/api/upload \
  -F "file=@/home/roneettopi/Desktop/Lumina/backend/photos/DSCF2724.JPG"
```

**Expected Response:**
```json
{
  "message": "Image uploaded successfully",
  "image_id": "Image_a1b2c3d4",
  "filename": "DSCF2724.JPG"
}
```

**Note:** Replace `/path/to/your/image.jpg` with the actual path to an image file on your system.

---

## 5. Upload Multiple Images (Batch)

Upload and index multiple images at once.

```bash
curl -X POST http://localhost:8000/api/upload/batch \
  -F "files=@/path/to/image1.jpg" \
  -F "files=@/path/to/image2.jpg" \
  -F "files=@/path/to/image3.jpg"
```

**Example with actual files (relative path - if you're in the backend directory):**
```bash
curl -X POST http://localhost:8000/api/upload/batch \
  -F "files=@photos/DSCF2724.JPG" \
  -F "files=@photos/DSCF2725.JPG" \
  -F "files=@photos/DSCF2729.JPG"
```

**Example with absolute paths:**
```bash
curl -X POST http://localhost:8000/api/upload/batch \
  -F "files=@/home/roneettopi/Desktop/Lumina/backend/photos/DSCF2724.JPG" \
  -F "files=@/home/roneettopi/Desktop/Lumina/backend/photos/DSCF2725.JPG" \
  -F "files=@/home/roneettopi/Desktop/Lumina/backend/photos/DSCF2729.JPG"
```

**Expected Response:**
```json
{
  "message": "Uploaded 3 images",
  "uploaded_ids": [
    "Image_a1b2c3d4",
    "Image_e5f6g7h8",
    "Image_i9j0k1l2"
  ],
  "failed": [],
  "total_uploaded": 3,
  "total_failed": 0
}
```

**Note:** You can add as many `-F "files=@..."` parameters as needed.

---

## 6. Search Images by Text Query

Search for images using a text description.

### Basic Search (using query parameter in URL)

```bash
curl -X POST "http://localhost:8000/api/search?top_k=10&namespace=images" \
  -H "Content-Type: application/json" \
  -d '{"query": "a bearded man scratching his beard"}'
```

### Search with JSON body only

```bash
curl -X POST http://localhost:8000/api/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "a person with a beard",
    "top_k": 5,
    "namespace": "images"
  }'
```

### Simple search (defaults: top_k=10, namespace=images)

```bash
curl -X POST http://localhost:8000/api/search \
  -H "Content-Type: application/json" \
  -d '{"query": "portrait photo"}'
```

**Expected Response:**
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
    {
      "id": "Image_15",
      "filename": "DSCF2775.JPG",
      "score": 0.82,
      "similarity_percent": 91.0
    }
  ],
  "total_found": 2
}
```

**More Search Examples:**

```bash
# Search for portraits
curl -X POST http://localhost:8000/api/search \
  -H "Content-Type: application/json" \
  -d '{"query": "portrait of a person"}'

# Search for outdoor scenes
curl -X POST http://localhost:8000/api/search \
  -H "Content-Type: application/json" \
  -d '{"query": "outdoor landscape"}'

# Search with more results
curl -X POST http://localhost:8000/api/search \
  -H "Content-Type: application/json" \
  -d '{"query": "person", "top_k": 20}'
```

---

## 7. Delete Image

Delete a specific image from the index.

```bash
curl -X DELETE "http://localhost:8000/api/images/Image_a1b2c3d4?namespace=images"
```

**Or with default namespace (images):**

```bash
curl -X DELETE http://localhost:8000/api/images/Image_a1b2c3d4
```

**Expected Response:**
```json
{
  "message": "Image deleted successfully",
  "image_id": "Image_a1b2c3d4"
}
```

**Note:** Replace `Image_a1b2c3d4` with an actual image ID from your database (you can get IDs from search results or upload responses).

---

## Testing Tips

### 1. Pretty Print JSON Responses

Add `| python -m json.tool` or `| jq` to format JSON output:

```bash
curl -X GET http://localhost:8000/api/stats | python -m json.tool
```

### 2. Verbose Output

Add `-v` flag to see request/response headers:

```bash
curl -v -X GET http://localhost:8000/api/health
```

### 3. Save Response to File

```bash
curl -X GET http://localhost:8000/api/stats -o response.json
```

### 4. Test from Different Directory

If you're not in the `backend` directory, use absolute paths:

```bash
# Make sure to use the FULL absolute path starting with /home/
curl -X POST http://localhost:8000/api/upload \
  -F "file=@/home/roneettopi/Desktop/Lumina/backend/photos/DSCF2724.JPG"
```

**Important:** The `@` symbol in curl means "read from file", and the path must be:
- **Absolute path**: `/home/username/full/path/to/file.jpg` (starts with `/`)
- **Relative path**: `photos/file.jpg` (relative to your current directory)

**Common mistake:** `/Desktop/...` is NOT an absolute path. It should be `/home/yourusername/Desktop/...`

---

## Complete Testing Workflow

Here's a suggested order to test all endpoints:

1. **Health Check** - Verify API is running
   ```bash
   curl -X GET http://localhost:8000/api/health
   ```

2. **Get Stats** - Check current database state
   ```bash
   curl -X GET http://localhost:8000/api/stats
   ```

3. **Upload Image** - Add a test image
   ```bash
   curl -X POST http://localhost:8000/api/upload \
     -F "file=@photos/DSCF2724.JPG"
   ```
   **Save the `image_id` from the response!**

4. **Search** - Test search functionality
   ```bash
   curl -X POST http://localhost:8000/api/search \
     -H "Content-Type: application/json" \
     -d '{"query": "test query", "top_k": 5}'
   ```

5. **Get Telemetry** - Check system status
   ```bash
   curl -X GET http://localhost:8000/api/telemetry
   ```

6. **Delete Image** - Clean up test image (use image_id from step 3)
   ```bash
   curl -X DELETE http://localhost:8000/api/images/Image_XXXXX
   ```

---

## Error Examples

### Missing Query Parameter
```bash
curl -X POST http://localhost:8000/api/search \
  -H "Content-Type: application/json" \
  -d '{}'
```
**Expected Error:** `400 Bad Request - Query parameter is required`

### Invalid File Type
```bash
curl -X POST http://localhost:8000/api/upload \
  -F "file=@somefile.txt"
```
**Expected Error:** `400 Bad Request - File must be an image`

### Invalid Image ID
```bash
curl -X DELETE http://localhost:8000/api/images/nonexistent_id
```
**Expected Error:** May return 500 or succeed silently if ID doesn't exist

---

## Using FastAPI Interactive Docs

For easier testing, you can also use the interactive API documentation:

1. Start the server: `python main.py`
2. Open browser: `http://localhost:8000/docs`
3. Click on any endpoint to test it directly in the browser

This is often easier than curl for file uploads and complex requests!

