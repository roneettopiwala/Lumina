/**
 * FileUpload Component
 * Handles file selection (drag & drop + click) and upload
 */

'use client';

import { useState, useRef, DragEvent } from 'react';
import { uploadImages } from '@/lib/api';
import LoadingSpinner from './LoadingSpinner';

interface FileUploadProps {
  onUploadComplete: () => void;
  onUploadError: (error: string) => void;
}

export default function FileUpload({ onUploadComplete, onUploadError }: FileUploadProps) {
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
  const [isDragging, setIsDragging] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState('');
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Handle file selection
  const handleFileSelect = (files: FileList | null) => {
    if (!files) return;

    const fileArray = Array.from(files);
    // Filter to only image files
    const imageFiles = fileArray.filter((file) => file.type.startsWith('image/'));
    
    if (imageFiles.length !== fileArray.length) {
      onUploadError('Some files were not images and were skipped');
    }

    setSelectedFiles((prev) => [...prev, ...imageFiles]);
  };

  // Handle drag and drop
  const handleDragOver = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);
    handleFileSelect(e.dataTransfer.files);
  };

  // Handle click to select files
  const handleClick = () => {
    fileInputRef.current?.click();
  };

  // Remove file from selection
  const removeFile = (index: number) => {
    setSelectedFiles((prev) => prev.filter((_, i) => i !== index));
  };

  // Upload files
  const handleUpload = async () => {
    if (selectedFiles.length === 0) {
      onUploadError('Please select at least one image');
      return;
    }

    setIsUploading(true);
    setUploadProgress(`Uploading ${selectedFiles.length} image(s)...`);

    try {
      const result = await uploadImages(selectedFiles);
      
      if (result.error) {
        throw new Error(result.error);
      }

      setUploadProgress(`Successfully uploaded ${result.total_uploaded} image(s)!`);
      
      // Clear selected files after successful upload
      setTimeout(() => {
        setSelectedFiles([]);
        setIsUploading(false);
        setUploadProgress('');
        onUploadComplete();
      }, 1500);
    } catch (error: any) {
      setIsUploading(false);
      setUploadProgress('');
      onUploadError(error.message || 'Upload failed. Please try again.');
    }
  };

  return (
    <div className="w-full max-w-4xl mx-auto">
      {/* Drag and Drop Area */}
      <div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={handleClick}
        className={`
          border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors
          ${isDragging 
            ? 'border-blue-500 bg-blue-50' 
            : 'border-gray-300 hover:border-gray-400 bg-gray-50'
          }
        `}
      >
        <input
          ref={fileInputRef}
          type="file"
          multiple
          accept="image/*"
          onChange={(e) => handleFileSelect(e.target.files)}
          className="hidden"
        />
        
        {isUploading ? (
          <div className="py-8">
            <LoadingSpinner message={uploadProgress} />
          </div>
        ) : (
          <>
            <svg
              className="mx-auto h-12 w-12 text-gray-400"
              stroke="currentColor"
              fill="none"
              viewBox="0 0 48 48"
            >
              <path
                d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02"
                strokeWidth={2}
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
            <p className="mt-2 text-sm text-gray-600">
              <span className="font-semibold">Click to upload</span> or drag and drop
            </p>
            <p className="text-xs text-gray-500 mt-1">
              PNG, JPG, GIF up to 10MB each
            </p>
          </>
        )}
      </div>

      {/* Selected Files List */}
      {selectedFiles.length > 0 && !isUploading && (
        <div className="mt-4">
          <h3 className="text-sm font-medium text-gray-700 mb-2">
            Selected Files ({selectedFiles.length})
          </h3>
          <div className="space-y-2 max-h-48 overflow-y-auto">
            {selectedFiles.map((file, index) => (
              <div
                key={index}
                className="flex items-center justify-between p-2 bg-white border border-gray-200 rounded"
              >
                <span className="text-sm text-gray-700 truncate flex-1">
                  {file.name}
                </span>
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    removeFile(index);
                  }}
                  className="ml-2 text-red-500 hover:text-red-700 text-sm"
                >
                  Remove
                </button>
              </div>
            ))}
          </div>
          <button
            onClick={handleUpload}
            disabled={isUploading}
            className="mt-4 w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
          >
            Upload {selectedFiles.length} Image(s)
          </button>
        </div>
      )}
    </div>
  );
}


