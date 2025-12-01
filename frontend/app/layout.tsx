import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Lumina - Image Search',
  description: 'Semantic image search powered by AI',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}


