/**
 * API utility functions for communicating with the backend
 */

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

/**
 * Upload multiple images to the backend
 * @param files - Array of File objects to upload
 * @returns Promise with upload response
 */
export async function uploadImages(files: File[]): Promise<any> {
  const formData = new FormData();
  
  // Append all files to FormData
  files.forEach((file) => {
    formData.append('files', file);
  });

  try {
    const response = await fetch(`${API_URL}/api/upload/batch`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Upload failed');
    }

    return await response.json();
  } catch (error) {
    console.error('Upload error:', error);
    throw error;
  }
}

/**
 * Search for images using a text query
 * @param query - Text query to search for
 * @param topK - Number of results to return (default: 10)
 * @returns Promise with search results
 */
export async function searchImages(query: string, topK: number = 10): Promise<any> {
  try {
    const response = await fetch(`${API_URL}/api/search`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query, top_k: topK }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Search failed');
    }

    return await response.json();
  } catch (error) {
    console.error('Search error:', error);
    throw error;
  }
}

/**
 * Get database statistics
 * @returns Promise with stats
 */
export async function getStats(): Promise<any> {
  try {
    const response = await fetch(`${API_URL}/api/stats`);

    if (!response.ok) {
      throw new Error('Failed to get stats');
    }

    return await response.json();
  } catch (error) {
    console.error('Stats error:', error);
    throw error;
  }
}


