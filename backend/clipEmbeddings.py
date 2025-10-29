import os, base64
from io import BytesIO
from typing import List, Union
import cohere
from PIL import Image
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()


class Embedder:

    def __init__(self):

        cohereKey= os.getenv("COHERE_API_KEY")

        self.client = cohere.ClientV2(api_key=cohereKey)
        self.model = "embed-v4.0"
    

    def _image_to_base64(self, image: Image.Image) -> str:

            # Resize large images to reduce API payload size and costwhy 
            max_size = 512
            if max(image.size) > max_size:
                ratio = max_size / max(image.size)
                new_size = tuple(int(dim * ratio) for dim in image.size)
                image = image.resize(new_size, Image.Resampling.LANCZOS)
            
            # Convert image to RGB (some images are RGBA, grayscale, etc.)
            if image.mode != "RGB":
                image = image.convert("RGB")
            
            # Save to bytes buffer and encode as base64
            buffered = BytesIO()
            image.save(buffered, format="JPEG")
            img_bytes = buffered.getvalue()
            base64_string = base64.b64encode(img_bytes).decode("utf-8")
            return f"data:image/jpeg;base64,{base64_string}"


    def embedText(self, text: str) -> List[float]:

        response = self.client.embed(
            texts=[text],
            model= self.model,
            input_type="search_query",
            embedding_types=["float"],
        )

        #return vector of floats
        return response.embeddings.float[0]
    

    def embedImage(self, image: Image.Image) -> List[float]:

        properImage = self._image_to_base64(image)

        response = self.client.embed(
            images = [properImage],
            model = self.model,
            input_type = "image",
            embedding_types = ["float"],
        )

        return response.embeddings.float[0]

    def embedmultipleImages(self, images: List[Image.Image]) -> List[List[float]]:
        properImages = [self._image_to_base64(img) for img in images]

        response = self.client.embed(
            images = properImages,
            model = self.model,
            input_type = "image",
            embedding_types = ["float"],
        )

        return response.embeddings.float




# embedder = Embedder()
    
# Test text
# query_text = embedder.embedText("a bearded man scratching his beard")
# print(f"Text: {len(query_text)} dims, sample: {query_text[:3]}")

# Get first photo from photos directory
# photos_dir = Path("photos")
# first_photo = list(photos_dir.glob("*.JPG"))[7]  # Gets first .JPG file
# print(f"\nTesting with: {first_photo.name}")

# photo = Image.open(first_photo)
# image_vector = embedder.embedImage(photo)
# print(f"Image: {len(image_vector)} dims, sample: {image_vector[:3]}")

# if __name__ == "__main__":
#     embedder = Embedder()
#     query_text = embedder.embedText("test query")
#     print(f"Text: {len(query_text)} dims")
