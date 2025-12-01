# Lumina Frontend

Next.js frontend for the Lumina semantic image search application.

## Getting Started

### Prerequisites

- Node.js 18+ installed
- Backend API running on `http://localhost:8000`

### Installation

1. Install dependencies:
```bash
npm install
```

2. Create `.env.local` file (already created, but verify):
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

3. Run the development server:
```bash
npm run dev
```

4. Open [http://localhost:3000](http://localhost:3000) in your browser

## Project Structure

```
frontend/
├── app/                    # Next.js App Router
│   ├── layout.tsx          # Root layout
│   ├── page.tsx            # Main page
│   └── globals.css          # Global styles
├── components/             # React components
│   ├── FileUpload.tsx      # File upload component
│   ├── SearchBar.tsx       # Search input component
│   ├── ImageGrid.tsx       # Results display
│   └── LoadingSpinner.tsx  # Loading indicator
├── lib/                    # Utilities
│   └── api.ts              # API functions
└── public/                 # Static assets
```

## Features

- **File Upload**: Drag & drop or click to upload multiple images
- **Search**: Text-based semantic search for images
- **Results Display**: Grid layout showing search results with similarity scores
- **Responsive Design**: Works on mobile, tablet, and desktop

## Development

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint

## Notes

- Make sure the backend API is running before using the frontend
- The API URL can be configured in `.env.local`
- Images are displayed as placeholders in the grid (you can enhance this later to show actual images)


