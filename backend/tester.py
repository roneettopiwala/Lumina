from clipEmbeddings import Embedder
from vectorStore import VectorStore
from PIL import Image
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

embedder = Embedder()
storage = VectorStore("lumina")

# === STEP 1: Store all your photos ===
allPhotos = Path("photos")
photo_paths = list(allPhotos.glob("*.JPG"))
print(f"Found {len(photo_paths)} photos")

# Production batch settings (much faster than trial!)
EMBED_BATCH_SIZE = 50  # Production allows up to 96, using 50 to be safe

allImages = []
total_batches = (len(photo_paths) + EMBED_BATCH_SIZE - 1) // EMBED_BATCH_SIZE

print(f"Processing {len(photo_paths)} images in {total_batches} batches of {EMBED_BATCH_SIZE}...")

for batch_num in range(total_batches):
    start_idx = batch_num * EMBED_BATCH_SIZE
    end_idx = min(start_idx + EMBED_BATCH_SIZE, len(photo_paths))
    batch_paths = photo_paths[start_idx:end_idx]
    
    # Load images
    batch_images = []
    batch_metadata = []
    
    for i, photoPath in enumerate(batch_paths):
        try:
            photo = Image.open(photoPath)
            batch_images.append(photo)
            batch_metadata.append({
                "id": f"Image_{start_idx + i}",
                "filename": photoPath.name
            })
        except Exception as e:
            print(f"  Error loading {photoPath.name}: {e}")
            continue
    
    # Embed the batch
    if batch_images:
        print(f"Batch {batch_num + 1}/{total_batches}: Embedding {len(batch_images)} images...", end=" ")
        
        try:
            batch_embeddings = embedder.embedmultipleImages(batch_images)
            
            # Combine with metadata
            for i, embedding in enumerate(batch_embeddings):
                allImages.append({
                    "id": batch_metadata[i]["id"],
                    "embedding": embedding,
                    "filename": batch_metadata[i]["filename"]
                })
            
            print(f"✓ ({len(allImages)}/{len(photo_paths)} complete)")
            
        except Exception as e:
            print(f"✗ Error: {e}")

# Store in Pinecone
if allImages:
    print(f"\nStoring {len(allImages)} images in Pinecone...")
    storage.storeMultipleImages(allImages, nameSpace="images")
    print(f"✓ Stored successfully!")

# === STEP 2: Test search ===
queryText =  input("what are you looking for?")


while queryText != "exit":
    queryText =  input("what are you looking for?")

    # Check database stats
    stats = storage.getStats()
    total_vectors = stats.get('total_vectors', 0)
    print(f"Database contains {total_vectors} vectors")

    if total_vectors > 0:
        queryEmbedding = embedder.embedText(queryText)
        results = storage.semanticSearch(queryEmbedding, namespace="images", top_k=5)

    print(f"\n✓ Found {len(results)} results:\n")

    if results:
        for i, match in enumerate(results, 1):
            metadata = match.get('metadata', {})
            filename = metadata.get('filename', 'Unknown')
            score = match.get('score', 0)
            similarity_pct = (score + 1) / 2 * 100  # Convert to percentage
            print(f"  {i}. {filename}")
            print(f"     Similarity: {similarity_pct:.1f}% | Score: {score:.4f}\n")
    else:
        print("  No results found. Try a broader query like 'person' or 'portrait'.")

    print(f"\n{'='*60}")
    print(f"✓ All done! Processed {len(allImages)} photos")
