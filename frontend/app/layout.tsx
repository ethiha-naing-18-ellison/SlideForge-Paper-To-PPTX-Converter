import type { Metadata, Viewport } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'SlideForge — Paper-to-PPTX & Docs-to-Slides',
  description: 'Forge beautiful, overflow-safe slide decks from papers, reports, manuals, and assignments — instantly.',
  keywords: ['research', 'papers', 'powerpoint', 'presentation', 'academic', 'slides', 'converter', 'pdf', 'pptx'],
  authors: [{ name: 'SlideForge Team' }],
  metadataBase: new URL('https://slideforge.com'),
  openGraph: {
    title: 'SlideForge — Paper-to-PPTX & Docs-to-Slides',
    description: 'Forge beautiful, overflow-safe slide decks from papers, reports, manuals, and assignments — instantly.',
    type: 'website',
    images: ['/images/logo/logo.png'],
  },
  twitter: {
    card: 'summary_large_image',
    title: 'SlideForge — Paper-to-PPTX & Docs-to-Slides',
    description: 'Forge beautiful, overflow-safe slide decks from papers, reports, manuals, and assignments — instantly.',
    images: ['/images/logo/logo.png'],
  },
}

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="dark">
      <body className="min-h-screen bg-neutral-950 text-neutral-100">
        <div className="min-h-screen">
          {children}
        </div>
      </body>
    </html>
  )
}
