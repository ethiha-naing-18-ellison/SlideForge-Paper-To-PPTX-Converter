'use client'

import Link from 'next/link'
import Image from 'next/image'
import { ArrowLeft, BookOpen, Terminal, FileText } from 'lucide-react'

export default function DocsPage() {
  return (
    <div className="min-h-screen bg-neutral-950 text-neutral-100">
      {/* Header */}
      <header className="bg-neutral-900/80 backdrop-blur-md border-b border-neutral-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center space-x-4">
              <Link
                href="/"
                className="flex items-center space-x-2 text-neutral-300 hover:text-neutral-100 transition-colors duration-200"
                aria-label="Back to SlideForge Home"
              >
                <ArrowLeft className="w-5 h-5" />
                <span>Back to Home</span>
              </Link>
            </div>
            <div className="flex items-center space-x-3">
              <Image
                src="/images/logo/logo.png"
                alt="SlideForge Logo"
                width={32}
                height={32}
                className="w-8 h-8"
              />
              <div>
                <h1 className="text-xl font-bold text-neutral-100">SlideForge</h1>
                <p className="text-sm text-neutral-400">Documentation</p>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center mb-12">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-indigo-600/20 rounded-full mb-6">
            <BookOpen className="w-8 h-8 text-indigo-400" />
          </div>
          <h1 className="text-4xl font-bold text-neutral-100 mb-4">
            SlideForge Documentation
          </h1>
          <p className="text-xl text-neutral-300 max-w-2xl mx-auto">
            Learn how to use SlideForge to convert your documents into professional presentations.
          </p>
        </div>

        {/* Documentation Sections */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-12">
          <div className="bg-neutral-900/50 border border-neutral-800 rounded-xl p-6 hover:border-neutral-700 transition-colors duration-200">
            <div className="flex items-center space-x-3 mb-4">
              <div className="w-10 h-10 bg-indigo-600/20 rounded-lg flex items-center justify-center">
                <FileText className="w-5 h-5 text-indigo-400" />
              </div>
              <h3 className="text-lg font-semibold text-neutral-100">Getting Started</h3>
            </div>
            <p className="text-neutral-300 mb-4">
              Learn the basics of using SlideForge to convert your first document into a presentation.
            </p>
            <Link
              href="/app"
              className="inline-flex items-center text-indigo-400 hover:text-indigo-300 font-medium"
            >
              Try it now →
            </Link>
          </div>

          <div className="bg-neutral-900/50 border border-neutral-800 rounded-xl p-6 hover:border-neutral-700 transition-colors duration-200">
            <div className="flex items-center space-x-3 mb-4">
              <div className="w-10 h-10 bg-indigo-600/20 rounded-lg flex items-center justify-center">
                <Terminal className="w-5 h-5 text-indigo-400" />
              </div>
              <h3 className="text-lg font-semibold text-neutral-100">CLI Guide</h3>
            </div>
            <p className="text-neutral-300 mb-4">
              Use SlideForge from the command line for batch processing and automation.
            </p>
            <Link
              href="/docs/cli"
              className="inline-flex items-center text-indigo-400 hover:text-indigo-300 font-medium"
            >
              View CLI docs →
            </Link>
          </div>
        </div>

        {/* Coming Soon */}
        <div className="bg-neutral-900/50 border border-neutral-800 rounded-xl p-8 text-center">
          <h2 className="text-2xl font-bold text-neutral-100 mb-4">
            More Documentation Coming Soon
          </h2>
          <p className="text-neutral-300 mb-6">
            We're working on comprehensive documentation including API references, tutorials, and best practices.
          </p>
          <Link
            href="/app"
            className="inline-flex items-center px-6 py-3 bg-indigo-600 text-white rounded-lg font-medium hover:bg-indigo-700 transition-colors duration-200"
          >
            Start Using SlideForge
          </Link>
        </div>
      </main>
    </div>
  )
}
