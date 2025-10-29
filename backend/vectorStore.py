import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from typing import List
import time 

load_dotenv()




class VectorStore:
    
    def __init__(self, idxName):
        api_key = os.getenv("PINECONE_API_KEY")
        self.pcone = Pinecone(api_key=api_key)
        self.indexName = idxName

        existingIndex = self.pcone.list_indexes().names()


        #create index
        if idxName not in existingIndex:

            self.pcone.create_index(
                name=idxName,
                dimension=1536,
                metric="cosine",
                spec=ServerlessSpec(
                    cloud="aws",
                    region="us-east-1"
                )
            )


            while not self.pcone.describe_index(idxName).status['ready']:
                print("Waiting")

                time.sleep(1)
            print("Index created")

    
        self.idx = self.pcone.Index(idxName)


    def storeText(self, textId: str, embeddings: list[float], ogText: str, nameSpace: str):

        self.idx.upsert(
            vectors = [(textId, embeddings, {"type": "text", "text": ogText, "timestamp": time.time()})],
            nameSpace=nameSpace
        )

        print(f"Stored at {textId}")

    
    def storeImage(self, imageId, embeddings, fileName, nameSpace):

        self.idx.upsert(
            vectors = [(imageId, embeddings, {"type": "image", "fileName": fileName, "timestamp": time.time()})],
            nameSpace=nameSpace
        )

        print(f"Stored at {imageId}") 

    

    def storeMultipleImages(self, imageData: List[dict], nameSpace: str):

        vectors = [
            (
                item["id"],
                item["embedding"],
                {
                    "type": "image",
                    "filename": item["filename"],
                    "timestamp": time.time()
                }
            )
            for item in imageData
        ]

        maxSize = 100

        for i in range(0, len(vectors), maxSize):
            batch = vectors[i:i + maxSize]
            self.idx.upsert(vectors=batch, namespace=nameSpace)
            print(f"Stored batch {i//maxSize + 1}")
        
        print(f"Total stored {len(vectors)} images")



    
    def semanticSearch(self, queryEmbedding, namespace, filterDict=None, top_k=5):

        results = self.idx.query(
            vector=queryEmbedding,
            top_k=top_k,
            namespace=namespace,
            filter=filterDict,
            include_metadata=True #get the metadata 
        )

        return results.matches#returns the matches as a list of dictionaries

    
    def getStats(self):
        
        stats = self.idx.describe_index_stats()
        
        # Fixed: Access as attributes
        print(f"Total vectors: {stats.total_vector_count}")
        print(f"Namespaces: {stats.namespaces}")
        
        return {
            "total_vectors": stats.total_vector_count,
            "dimension": stats.dimension,
            "namespaces": stats.namespaces
        }

    def deleteId (self, ids, namespace):

        self.idx.delete(ids=ids, namespace=namespace)
        print(f"Deleted {len(ids)} vectors")
    


    # Test
if __name__ == "__main__":
    store = VectorStore("lumina")
    stats = store.getStats()
    print(f"\nIndex ready with {stats['total_vectors']} vectors")


    





