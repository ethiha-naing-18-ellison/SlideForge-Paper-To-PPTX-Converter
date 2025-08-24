import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'SlideForge - Paper-to-PPTX Converter',
  description: 'Convert research papers into professional PowerPoint presentations',
  keywords: ['research', 'papers', 'powerpoint', 'presentation', 'academic'],
  authors: [{ name: 'SlideForge Team' }],
  viewport: 'width=device-width, initial-scale=1',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-gray-50">
        <div className="min-h-screen">
          {children}
        </div>
      </body>
    </html>
  )
}
