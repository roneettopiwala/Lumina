/**
 * ImageGrid Component
 * Displays search results in a responsive grid layout
 */

'use client';

interface ImageResult {
  id: string;
  filename: string;
  score: number;
  similarity_percent: number;
}

interface ImageGridProps {
  results: ImageResult[];
  query: string;
}

export default function ImageGrid({ results, query }: ImageGridProps) {
  if (results.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-600">No results found for &quot;{query}&quot;</p>
        <p className="text-sm text-gray-500 mt-2">Try a different search query</p>
      </div>
    );
  }

  return (
    <div className="w-full">
      <div className="mb-4">
        <h2 className="text-lg font-semibold text-gray-800">
          Found {results.length} result{results.length !== 1 ? 's' : ''} for &quot;{query}&quot;
        </h2>
      </div>
      
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        {results.map((result) => (
          <div
            key={result.id}
            className="bg-white border border-gray-200 rounded-lg overflow-hidden shadow-sm hover:shadow-md transition-shadow"
          >
            {/* Image placeholder - in real app, you'd load the actual image */}
            <div className="w-full h-48 bg-gray-200 flex items-center justify-center">
              <svg
                className="w-16 h-16 text-gray-400"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
                />
              </svg>
            </div>
            
            {/* Image info */}
            <div className="p-3">
              <p className="text-sm font-medium text-gray-800 truncate" title={result.filename}>
                {result.filename}
              </p>
              <div className="mt-2 flex items-center justify-between">
                <span className="text-xs text-gray-500">Similarity</span>
                <span className="text-sm font-semibold text-blue-600">
                  {result.similarity_percent.toFixed(1)}%
                </span>
              </div>
              <div className="mt-1">
                <div className="w-full bg-gray-200 rounded-full h-1.5">
                  <div
                    className="bg-blue-600 h-1.5 rounded-full"
                    style={{ width: `${result.similarity_percent}%` }}
                  ></div>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}


