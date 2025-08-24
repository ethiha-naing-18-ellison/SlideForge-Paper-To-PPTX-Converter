'use client'

import { useState } from 'react'
import { slideforgeApi, GenerateResponse } from '@/app/lib/api'
import UploadPanel from '@/app/components/UploadPanel'
import ResultCard from '@/app/components/ResultCard'

export default function Home() {
  const [isLoading, setIsLoading] = useState(false)
  const [result, setResult] = useState<GenerateResponse | null>(null)
  const [error, setError] = useState<string | null>(null)

  const handleUpload = async (file: File, options: { theme: string; maxBullets: number }) => {
    setIsLoading(true)
    setError(null)
    
    try {
      const response = await slideforgeApi.generateFromPDF(file, options)
      setResult(response)
    } catch (err: any) {
      console.error('Generation failed:', err)
      setError(err.response?.data?.detail || err.message || 'Failed to generate presentation')
    } finally {
      setIsLoading(false)
    }
  }

  const handleDOI = async (doi: string, options: { theme: string; maxBullets: number }) => {
    setIsLoading(true)
    setError(null)
    
    try {
      const response = await slideforgeApi.generateFromDOI(doi, options)
      setResult(response)
    } catch (err: any) {
      console.error('Generation failed:', err)
      setError(err.response?.data?.detail || err.message || 'Failed to generate presentation')
    } finally {
      setIsLoading(false)
    }
  }

  const handleURL = async (url: string, options: { theme: string; maxBullets: number }) => {
    setIsLoading(true)
    setError(null)
    
    try {
      const response = await slideforgeApi.generateFromURL(url, options)
      setResult(response)
    } catch (err: any) {
      console.error('Generation failed:', err)
      setError(err.response?.data?.detail || err.message || 'Failed to generate presentation')
    } finally {
      setIsLoading(false)
    }
  }

  const handleReset = () => {
    setResult(null)
    setError(null)
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">SlideForge</h1>
              <p className="text-gray-600">Paper-to-PPTX Converter</p>
            </div>
            <div className="text-right">
              <p className="text-sm text-gray-500">Version 0.1.0</p>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {error && (
          <div className="mb-6 bg-red-50 border border-red-200 rounded-lg p-4">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <h3 className="text-sm font-medium text-red-800">Error</h3>
                <div className="mt-2 text-sm text-red-700">
                  <p>{error}</p>
                </div>
                <div className="mt-4">
                  <button
                    type="button"
                    onClick={handleReset}
                    className="bg-red-50 px-2 py-1.5 rounded-md text-sm font-medium text-red-800 hover:bg-red-100 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-red-50 focus:ring-red-600"
                  >
                    Try Again
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {result ? (
          <ResultCard result={result} onReset={handleReset} />
        ) : (
          <UploadPanel
            onUpload={handleUpload}
            onDOI={handleDOI}
            onURL={handleURL}
            isLoading={isLoading}
          />
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center">
            <p className="text-gray-500 text-sm">
              © 2024 SlideForge. Convert research papers into professional PowerPoint presentations.
            </p>
            <div className="mt-4 flex justify-center space-x-6 text-sm text-gray-500">
              <a href="#" className="hover:text-gray-900">Privacy Policy</a>
              <a href="#" className="hover:text-gray-900">Terms of Service</a>
              <a href="#" className="hover:text-gray-900">Documentation</a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}
