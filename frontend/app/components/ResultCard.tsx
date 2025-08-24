'use client'

import { useState } from 'react'
import { Download, FileText, Users, Calendar, ExternalLink, CheckCircle } from 'lucide-react'
import { slideforgeApi, GenerateResponse } from '@/app/lib/api'
import { downloadBlob } from '@/app/lib/utils'

interface ResultCardProps {
  result: GenerateResponse
  onReset: () => void
}

export default function ResultCard({ result, onReset }: ResultCardProps) {
  const [isDownloading, setIsDownloading] = useState(false)

  const handleDownload = async () => {
    setIsDownloading(true)
    try {
      const blob = await slideforgeApi.downloadPresentation(result.file_id)
      const filename = `${result.metadata.title.replace(/[^a-z0-9]/gi, '_').toLowerCase()}_presentation.pptx`
      downloadBlob(blob, filename)
    } catch (error) {
      console.error('Download failed:', error)
      alert('Download failed. Please try again.')
    } finally {
      setIsDownloading(false)
    }
  }

  return (
    <div className="card max-w-2xl mx-auto animate-fade-in">
      <div className="text-center mb-6">
        <div className="inline-flex items-center justify-center w-16 h-16 bg-green-100 rounded-full mb-4">
          <CheckCircle className="w-8 h-8 text-green-600" />
        </div>
        <h2 className="text-2xl font-bold text-gray-900 mb-2">
          Presentation Generated Successfully!
        </h2>
        <p className="text-gray-600">
          Your PowerPoint presentation is ready for download
        </p>
      </div>

      {/* Paper Information */}
      <div className="bg-gray-50 rounded-lg p-4 mb-6">
        <h3 className="font-semibold text-gray-900 mb-3 flex items-center">
          <FileText className="w-4 h-4 mr-2" />
          Paper Information
        </h3>
        
        <div className="space-y-2">
          <div>
            <span className="text-sm font-medium text-gray-700">Title:</span>
            <p className="text-sm text-gray-900">{result.metadata.title}</p>
          </div>
          
          {result.metadata.authors && result.metadata.authors.length > 0 && (
            <div>
              <span className="text-sm font-medium text-gray-700 flex items-center">
                <Users className="w-3 h-3 mr-1" />
                Authors:
              </span>
              <p className="text-sm text-gray-900">
                {result.metadata.authors.slice(0, 3).join(', ')}
                {result.metadata.authors.length > 3 && ` et al. (${result.metadata.authors.length} authors)`}
              </p>
            </div>
          )}
          
          {(result.metadata.venue || result.metadata.year) && (
            <div>
              <span className="text-sm font-medium text-gray-700 flex items-center">
                <Calendar className="w-3 h-3 mr-1" />
                Publication:
              </span>
              <p className="text-sm text-gray-900">
                {result.metadata.venue}
                {result.metadata.venue && result.metadata.year && ' • '}
                {result.metadata.year}
              </p>
            </div>
          )}
          
          {result.metadata.doi && (
            <div>
              <span className="text-sm font-medium text-gray-700">DOI:</span>
              <a
                href={`https://doi.org/${result.metadata.doi}`}
                target="_blank"
                rel="noopener noreferrer"
                className="text-sm text-primary-600 hover:text-primary-500 flex items-center"
              >
                {result.metadata.doi}
                <ExternalLink className="w-3 h-3 ml-1" />
              </a>
            </div>
          )}
        </div>
      </div>

      {/* Presentation Details */}
      <div className="bg-blue-50 rounded-lg p-4 mb-6">
        <h3 className="font-semibold text-gray-900 mb-3">Presentation Details</h3>
        
        <div className="grid grid-cols-2 gap-4">
          <div className="text-center">
            <div className="text-2xl font-bold text-blue-600">{result.slide_count}</div>
            <div className="text-sm text-gray-600">Slides Generated</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-blue-600">
              {result.metadata.title.length > 20 ? '...' : result.metadata.title.length}
            </div>
            <div className="text-sm text-gray-600">Characters in Title</div>
          </div>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="flex flex-col sm:flex-row gap-3">
        <button
          onClick={handleDownload}
          disabled={isDownloading}
          className="flex-1 btn-primary flex items-center justify-center space-x-2"
        >
          {isDownloading ? (
            <>
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
              <span>Downloading...</span>
            </>
          ) : (
            <>
              <Download className="w-4 h-4" />
              <span>Download PowerPoint</span>
            </>
          )}
        </button>
        
        <button
          onClick={onReset}
          className="flex-1 btn-outline"
        >
          Generate Another
        </button>
      </div>

      {/* Tips */}
      <div className="mt-6 p-4 bg-yellow-50 rounded-lg border border-yellow-200">
        <h4 className="font-medium text-yellow-800 mb-2">💡 Tips</h4>
        <ul className="text-sm text-yellow-700 space-y-1">
          <li>• The presentation includes a title slide, agenda, and section slides</li>
          <li>• Each section contains up to 6 bullet points (max 20 words each)</li>
          <li>• You can customize the theme and bullet count in future generations</li>
          <li>• The file is compatible with PowerPoint, Keynote, and Google Slides</li>
        </ul>
      </div>
    </div>
  )
}
