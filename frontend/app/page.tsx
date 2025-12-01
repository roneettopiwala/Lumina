/**
 * Main Page Component
 * Orchestrates the entire application flow
 */

'use client';

import { useState } from 'react';
import FileUpload from '@/components/FileUpload';
import SearchBar from '@/components/SearchBar';
import ImageGrid from '@/components/ImageGrid';
import LoadingSpinner from '@/components/LoadingSpinner';
import { searchImages } from '@/lib/api';

type UploadStatus = 'idle' | 'uploading' | 'complete' | 'error';

export default function Home() {
  // State management
  const [uploadStatus, setUploadStatus] = useState<UploadStatus>('idle');
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<any[]>([]);
  const [isSearching, setIsSearching] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Handle upload completion
  const handleUploadComplete = () => {
    setUploadStatus('complete');
    setError(null);
  };

  // Handle upload error
  const handleUploadError = (errorMessage: string) => {
    setError(errorMessage);
    setUploadStatus('error');
  };

  // Handle search
  const handleSearch = async (query: string) => {
    setSearchQuery(query);
    setIsSearching(true);
    setError(null);
    setSearchResults([]);

    try {
      const results = await searchImages(query, 20);
      
      if (results.error) {
        throw new Error(results.error);
      }

      setSearchResults(results.results || []);
    } catch (err: any) {
      setError(err.message || 'Search failed. Please try again.');
      setSearchResults([]);
    } finally {
      setIsSearching(false);
    }
  };

  return (
    <main className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <h1 className="text-3xl font-bold text-gray-900">Lumina</h1>
          <p className="text-gray-600 mt-1">Semantic Image Search</p>
        </div>
      </header>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Error Display */}
        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
            <p className="text-red-800 text-sm">{error}</p>
            <button
              onClick={() => setError(null)}
              className="mt-2 text-red-600 hover:text-red-800 text-sm underline"
            >
              Dismiss
            </button>
          </div>
        )}

        {/* Upload Section - Show when not uploaded or on error */}
        {(uploadStatus === 'idle' || uploadStatus === 'error') && (
          <div className="mb-8">
            <div className="mb-4">
              <h2 className="text-xl font-semibold text-gray-800 mb-2">
                Step 1: Upload Images
              </h2>
              <p className="text-gray-600 text-sm">
                Upload your images to get started. They will be processed and indexed for search.
              </p>
            </div>
            <FileUpload
              onUploadComplete={handleUploadComplete}
              onUploadError={handleUploadError}
            />
          </div>
        )}

        {/* Loading State - Show while uploading */}
        {uploadStatus === 'uploading' && (
          <div className="mb-8 text-center py-12">
            <LoadingSpinner message="Processing your images..." size="lg" />
          </div>
        )}

        {/* Search Section - Show after successful upload */}
        {uploadStatus === 'complete' && (
          <>
            <div className="mb-8">
              <div className="mb-4">
                <h2 className="text-xl font-semibold text-gray-800 mb-2">
                  Step 2: Search Images
                </h2>
                <p className="text-gray-600 text-sm">
                  Enter a text description to find similar images.
                </p>
              </div>
              <SearchBar onSearch={handleSearch} isSearching={isSearching} />
            </div>

            {/* Search Results */}
            {isSearching && (
              <div className="py-12 text-center">
                <LoadingSpinner message="Searching..." size="lg" />
              </div>
            )}

            {!isSearching && searchQuery && (
              <div className="mt-8">
                <ImageGrid results={searchResults} query={searchQuery} />
              </div>
            )}

            {/* Initial state after upload */}
            {!isSearching && !searchQuery && (
              <div className="text-center py-12">
                <p className="text-gray-600">
                  Upload complete! Start searching for your images above.
                </p>
              </div>
            )}

            {/* Reset button */}
            <div className="mt-8 text-center">
              <button
                onClick={() => {
                  setUploadStatus('idle');
                  setSearchQuery('');
                  setSearchResults([]);
                  setError(null);
                }}
                className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors"
              >
                Upload New Images
              </button>
            </div>
          </>
        )}
      </div>
    </main>
  );
}


