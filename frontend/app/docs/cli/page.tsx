'use client'

import Link from 'next/link'
import Image from 'next/image'
import { ArrowLeft, Terminal, Download, Code } from 'lucide-react'

export default function CLIPage() {
  return (
    <div className="min-h-screen bg-neutral-950 text-neutral-100">
      {/* Header */}
      <header className="bg-neutral-900/80 backdrop-blur-md border-b border-neutral-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center space-x-4">
              <Link
                href="/docs"
                className="flex items-center space-x-2 text-neutral-300 hover:text-neutral-100 transition-colors duration-200"
                aria-label="Back to Documentation"
              >
                <ArrowLeft className="w-5 h-5" />
                <span>Back to Docs</span>
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
                <p className="text-sm text-neutral-400">CLI Guide</p>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center mb-12">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-indigo-600/20 rounded-full mb-6">
            <Terminal className="w-8 h-8 text-indigo-400" />
          </div>
          <h1 className="text-4xl font-bold text-neutral-100 mb-4">
            SlideForge CLI
          </h1>
          <p className="text-xl text-neutral-300 max-w-2xl mx-auto">
            Use SlideForge from the command line for batch processing and automation.
          </p>
        </div>

        {/* Installation */}
        <div className="bg-neutral-900/50 border border-neutral-800 rounded-xl p-6 mb-8">
          <h2 className="text-2xl font-bold text-neutral-100 mb-4">Installation</h2>
          <div className="bg-neutral-800 rounded-lg p-4 mb-4">
            <code className="text-green-400">pip install slideforge-cli</code>
          </div>
          <p className="text-neutral-300">
            Or install from source using Poetry for development.
          </p>
        </div>

        {/* Basic Usage */}
        <div className="bg-neutral-900/50 border border-neutral-800 rounded-xl p-6 mb-8">
          <h2 className="text-2xl font-bold text-neutral-100 mb-4">Basic Usage</h2>
          <div className="space-y-4">
            <div>
              <h3 className="text-lg font-semibold text-neutral-100 mb-2">Convert a PDF file</h3>
              <div className="bg-neutral-800 rounded-lg p-4">
                <code className="text-green-400">slideforge convert paper.pdf --theme academic</code>
              </div>
            </div>
            <div>
              <h3 className="text-lg font-semibold text-neutral-100 mb-2">Convert from DOI</h3>
              <div className="bg-neutral-800 rounded-lg p-4">
                <code className="text-green-400">slideforge convert --doi 10.1038/nature12373</code>
              </div>
            </div>
            <div>
              <h3 className="text-lg font-semibold text-neutral-100 mb-2">Batch processing</h3>
              <div className="bg-neutral-800 rounded-lg p-4">
                <code className="text-green-400">slideforge batch papers/ --output presentations/</code>
              </div>
            </div>
          </div>
        </div>

        {/* Options */}
        <div className="bg-neutral-900/50 border border-neutral-800 rounded-xl p-6 mb-8">
          <h2 className="text-2xl font-bold text-neutral-100 mb-4">Command Options</h2>
          <div className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <h3 className="font-semibold text-neutral-100 mb-2">--theme</h3>
                <p className="text-neutral-300 text-sm">Presentation theme (academic, minimal, corporate)</p>
              </div>
              <div>
                <h3 className="font-semibold text-neutral-100 mb-2">--max-bullets</h3>
                <p className="text-neutral-300 text-sm">Maximum bullets per section (1-10)</p>
              </div>
              <div>
                <h3 className="font-semibold text-neutral-100 mb-2">--output</h3>
                <p className="text-neutral-300 text-sm">Output directory for generated presentations</p>
              </div>
              <div>
                <h3 className="font-semibold text-neutral-100 mb-2">--format</h3>
                <p className="text-neutral-300 text-sm">Output format (pptx, pdf)</p>
              </div>
            </div>
          </div>
        </div>

        {/* Coming Soon */}
        <div className="bg-neutral-900/50 border border-neutral-800 rounded-xl p-8 text-center">
          <h2 className="text-2xl font-bold text-neutral-100 mb-4">
            CLI Documentation Coming Soon
          </h2>
          <p className="text-neutral-300 mb-6">
            We're working on comprehensive CLI documentation including advanced usage, configuration, and examples.
          </p>
          <Link
            href="/app"
            className="inline-flex items-center px-6 py-3 bg-indigo-600 text-white rounded-lg font-medium hover:bg-indigo-700 transition-colors duration-200"
          >
            Try Web Interface
          </Link>
        </div>
      </main>
    </div>
  )
}
