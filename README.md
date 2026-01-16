# Lumina

Lumina is a powerful semantic image search application that allows you to find images from your personal collection using natural language descriptions. Instead of relying on filenames or tags, Lumina understands the *content* of your photos. This project combines a modern web interface with a robust AI-powered backend.

## Features

-   **Semantic Search**: Use descriptive text like "a person with a beard" or "outdoor landscape" to find your photos.
-   **Batch Image Upload**: Easily upload and index multiple images at once through a simple drag-and-drop interface.
-   **High-Performance Vector Search**: Powered by Pinecone for fast and scalable similarity searches across thousands of images.
-   **AI-Powered Embeddings**: Utilizes Cohere's state-of-the-art embedding models to convert images and text into meaningful vector representations.
-   **Clean Web Interface**: A minimalist frontend built with Next.js and Tailwind CSS for a smooth user experience.
-   **RESTful API**: A well-structured FastAPI backend that exposes clear endpoints for image management and search.

## How It Works

1.  **Upload**: Users upload their images through the web UI.
2.  **Indexing**: The FastAPI backend receives the images, and for each one, calls the Cohere API to generate a vector embedding (a numerical representation).
3.  **Storage**: Each embedding, along with its filename, is stored in a Pinecone serverless vector index named `lumina`.
4.  **Search**: When a user enters a text query, the backend generates an embedding for the text using the Cohere API.
5.  **Querying**: The text embedding is used to query the Pinecone index, which returns the most similar image embeddings based on cosine similarity.
6.  **Results**: The frontend displays the matching images, ranked by similarity score.

## Tech Stack

-   **Frontend**: Next.js, React, TypeScript, Tailwind CSS
-   **Backend**: Python, FastAPI
-   **AI & Database**: Cohere (Embeddings), Pinecone (Vector Database)

## Getting Started

### Prerequisites

-   Python 3.8+
-   Node.js 18+
-   Git
-   API keys from:
    -   [Cohere](https://cohere.com/)
    -   [Pinecone](https://www.pinecone.io/)

### Backend Setup

1.  Clone the repository:
    ```bash
    git clone https://github.com/roneettopiwala/Lumina.git
    cd Lumina
    ```

2.  Navigate to the backend directory, create a virtual environment, and activate it:
    ```bash
    cd backend
    python -m venv venv
    source venv/bin/activate
    # On Windows, use: venv\Scripts\activate
    ```

3.  Install the required Python packages:
    ```bash
    pip install fastapi uvicorn python-dotenv cohere Pillow pinecone-client python-multipart
    ```

4.  Create a `.env` file in the `backend` directory and add your API keys:
    ```env
    COHERE_API_KEY="YOUR_COHERE_KEY"
    PINECONE_API_KEY="YOUR_PINECONE_KEY"
    ```

5.  Run the backend server:
    ```bash
    python main.py
    ```
    The backend will be running at `http://localhost:8000`.

### Frontend Setup

1.  In a **new terminal**, navigate to the frontend directory:
    ```bash
    cd frontend 
    ```
    *(Assuming you are in the project's root `Lumina` directory)*

2.  Install the Node.js dependencies:
    ```bash
    npm install
    ```

3.  Run the development server:
    ```bash
    npm run dev
    ```
    The frontend will be running at `http://localhost:3000`.

### Usage

1.  Open your browser and navigate to `http://localhost:3000`.
2.  Use the file uploader to select and upload your desired images.
3.  Once the upload and indexing are complete, use the search bar to find images using a text description.

## API Documentation

The FastAPI backend provides a RESTful API for all operations. When the backend is running, you can access interactive documentation at `http://localhost:8000/docs`.

