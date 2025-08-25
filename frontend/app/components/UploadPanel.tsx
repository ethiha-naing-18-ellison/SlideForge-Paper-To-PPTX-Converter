'use client'

import { useState, useRef } from 'react'
import { useForm } from 'react-hook-form'
import { Upload, FileText, Link, AlertCircle, CheckCircle } from 'lucide-react'
import { cn } from '@/app/lib/utils'

interface UploadPanelProps {
  onUpload: (file: File, options: { theme: string; maxBullets: number }) => void
  onDOI: (doi: string, options: { theme: string; maxBullets: number }) => void
  onURL: (url: string, options: { theme: string; maxBullets: number }) => void
  isLoading?: boolean
}

interface FormData {
  theme: string
  maxBullets: number
  doi?: string
  url?: string
}

export default function UploadPanel({
  onUpload,
  onDOI,
  onURL,
  isLoading = false,
}: UploadPanelProps) {
  const [uploadMethod, setUploadMethod] = useState<'file' | 'doi' | 'url'>('file')
  const [dragActive, setDragActive] = useState(false)
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const {
    register,
    handleSubmit,
    formState: { errors },
    watch,
  } = useForm<FormData>({
    defaultValues: {
      theme: 'academic',
      maxBullets: 6,
    },
  })

  const watchedValues = watch()

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true)
    } else if (e.type === 'dragleave') {
      setDragActive(false)
    }
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0]
      if (file.type === 'application/pdf') {
        setSelectedFile(file)
      }
    }
  }

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setSelectedFile(e.target.files[0])
    }
  }

  const onSubmit = (data: FormData) => {
    const options = {
      theme: data.theme,
      maxBullets: data.maxBullets,
    }

    if (uploadMethod === 'file' && selectedFile) {
      onUpload(selectedFile, options)
    } else if (uploadMethod === 'doi' && data.doi) {
      onDOI(data.doi, options)
    } else if (uploadMethod === 'url' && data.url) {
      onURL(data.url, options)
    }
  }

  return (
    <div className="bg-neutral-900/50 border border-neutral-800 rounded-xl p-6 max-w-2xl mx-auto">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-neutral-100 mb-2">
          Convert Research Paper to PowerPoint
        </h2>
        <p className="text-neutral-300">
          Upload a PDF or provide a DOI/URL to generate a professional presentation
        </p>
      </div>

      {/* Upload Method Tabs */}
      <div className="flex space-x-1 mb-6 bg-neutral-800 p-1 rounded-lg">
        <button
          type="button"
          onClick={() => setUploadMethod('file')}
          className={cn(
            'flex items-center space-x-2 px-4 py-2 rounded-md text-sm font-medium transition-colors',
            uploadMethod === 'file'
              ? 'bg-neutral-700 text-indigo-400 shadow-sm'
              : 'text-neutral-400 hover:text-neutral-200'
          )}
        >
          <Upload className="w-4 h-4" />
          <span>Upload PDF</span>
        </button>
        <button
          type="button"
          onClick={() => setUploadMethod('doi')}
          className={cn(
            'flex items-center space-x-2 px-4 py-2 rounded-md text-sm font-medium transition-colors',
            uploadMethod === 'doi'
              ? 'bg-neutral-700 text-indigo-400 shadow-sm'
              : 'text-neutral-400 hover:text-neutral-200'
          )}
        >
          <FileText className="w-4 h-4" />
          <span>DOI</span>
        </button>
        <button
          type="button"
          onClick={() => setUploadMethod('url')}
          className={cn(
            'flex items-center space-x-2 px-4 py-2 rounded-md text-sm font-medium transition-colors',
            uploadMethod === 'url'
              ? 'bg-neutral-700 text-indigo-400 shadow-sm'
              : 'text-neutral-400 hover:text-neutral-200'
          )}
        >
          <Link className="w-4 h-4" />
          <span>URL</span>
        </button>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
        {/* File Upload */}
        {uploadMethod === 'file' && (
          <div>
            <label className="block text-sm font-medium text-neutral-200 mb-2">
              Upload PDF File
            </label>
            <div
              className={cn(
                'border-2 border-dashed rounded-lg p-6 text-center transition-colors',
                dragActive
                  ? 'border-indigo-400 bg-indigo-900/20'
                  : 'border-neutral-600 hover:border-neutral-500',
                selectedFile && 'border-green-400 bg-green-900/20'
              )}
              onDragEnter={handleDrag}
              onDragLeave={handleDrag}
              onDragOver={handleDrag}
              onDrop={handleDrop}
            >
              <input
                ref={fileInputRef}
                type="file"
                accept=".pdf"
                onChange={handleFileSelect}
                className="hidden"
              />
              
              {selectedFile ? (
                <div className="flex items-center justify-center space-x-2">
                  <CheckCircle className="w-5 h-5 text-green-400" />
                  <span className="text-sm text-neutral-300">
                    {selectedFile.name} ({(selectedFile.size / 1024 / 1024).toFixed(2)} MB)
                  </span>
                </div>
              ) : (
                <div>
                  <Upload className="mx-auto h-12 w-12 text-neutral-400" />
                  <p className="mt-2 text-sm text-neutral-300">
                    Drag and drop a PDF file here, or{' '}
                    <button
                      type="button"
                      onClick={() => fileInputRef.current?.click()}
                      className="text-indigo-400 hover:text-indigo-300 font-medium"
                    >
                      browse
                    </button>
                  </p>
                  <p className="text-xs text-neutral-400 mt-1">
                    Maximum file size: 50MB
                  </p>
                </div>
              )}
            </div>
          </div>
        )}

        {/* DOI Input */}
        {uploadMethod === 'doi' && (
          <div>
            <label htmlFor="doi" className="block text-sm font-medium text-neutral-200 mb-2">
              DOI Identifier
            </label>
            <input
              {...register('doi', { required: 'DOI is required' })}
              type="text"
              id="doi"
              placeholder="e.g., 10.1038/nature12373"
              className="w-full px-3 py-2 border border-neutral-600 rounded-lg bg-neutral-800 text-neutral-100 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent placeholder-neutral-400"
            />
            {errors.doi && (
              <p className="mt-1 text-sm text-red-400 flex items-center">
                <AlertCircle className="w-4 h-4 mr-1" />
                {errors.doi.message}
              </p>
            )}
          </div>
        )}

        {/* URL Input */}
        {uploadMethod === 'url' && (
          <div>
            <label htmlFor="url" className="block text-sm font-medium text-neutral-200 mb-2">
              Paper URL
            </label>
            <input
              {...register('url', { 
                required: 'URL is required',
                pattern: {
                  value: /^https?:\/\/.+/,
                  message: 'Please enter a valid URL'
                }
              })}
              type="url"
              id="url"
              placeholder="https://example.com/paper"
              className="w-full px-3 py-2 border border-neutral-600 rounded-lg bg-neutral-800 text-neutral-100 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent placeholder-neutral-400"
            />
            {errors.url && (
              <p className="mt-1 text-sm text-red-400 flex items-center">
                <AlertCircle className="w-4 h-4 mr-1" />
                {errors.url.message}
              </p>
            )}
          </div>
        )}

        {/* Theme Selection */}
        <div>
          <label htmlFor="theme" className="block text-sm font-medium text-neutral-200 mb-2">
            Presentation Theme
          </label>
          <select
            {...register('theme')}
            id="theme"
            className="w-full px-3 py-2 border border-neutral-600 rounded-lg bg-neutral-800 text-neutral-100 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
          >
            <option value="academic">Academic</option>
            <option value="minimal">Minimal</option>
            <option value="corporate">Corporate</option>
          </select>
        </div>

        {/* Max Bullets */}
        <div>
          <label htmlFor="maxBullets" className="block text-sm font-medium text-neutral-200 mb-2">
            Maximum Bullets per Section
          </label>
          <input
            {...register('maxBullets', {
              min: { value: 1, message: 'Minimum 1 bullet' },
              max: { value: 10, message: 'Maximum 10 bullets' },
            })}
            type="number"
            id="maxBullets"
            min="1"
            max="10"
            className="w-full px-3 py-2 border border-neutral-600 rounded-lg bg-neutral-800 text-neutral-100 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
          />
          {errors.maxBullets && (
            <p className="mt-1 text-sm text-red-400 flex items-center">
              <AlertCircle className="w-4 h-4 mr-1" />
              {errors.maxBullets.message}
            </p>
          )}
        </div>

        {/* Submit Button */}
        <button
          type="submit"
          disabled={isLoading || (uploadMethod === 'file' && !selectedFile)}
          className="w-full px-4 py-3 bg-indigo-600 text-white rounded-lg font-medium hover:bg-indigo-700 transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 focus:ring-offset-neutral-950 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isLoading ? (
            <div className="flex items-center justify-center space-x-2">
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
              <span>Generating Presentation...</span>
            </div>
          ) : (
            'Generate Presentation'
          )}
        </button>
      </form>
    </div>
  )
}
