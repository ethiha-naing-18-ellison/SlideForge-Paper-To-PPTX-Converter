'use client'

import Link from 'next/link'
import Image from 'next/image'
import { ArrowLeft, Shield } from 'lucide-react'

export default function TermsPage() {
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
                <p className="text-sm text-neutral-400">Terms of Service</p>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center mb-12">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-indigo-600/20 rounded-full mb-6">
            <Shield className="w-8 h-8 text-indigo-400" />
          </div>
          <h1 className="text-4xl font-bold text-neutral-100 mb-4">
            Terms of Service
          </h1>
          <p className="text-xl text-neutral-300 max-w-2xl mx-auto">
            Last updated: {new Date().toLocaleDateString()}
          </p>
        </div>

        <div className="bg-neutral-900/50 border border-neutral-800 rounded-xl p-8">
          <div className="prose prose-invert max-w-none">
            <h2 className="text-2xl font-bold text-neutral-100 mb-4">1. Acceptance of Terms</h2>
            <p className="text-neutral-300 mb-6">
              By accessing and using SlideForge, you accept and agree to be bound by the terms and provision of this agreement.
            </p>

            <h2 className="text-2xl font-bold text-neutral-100 mb-4">2. Use License</h2>
            <p className="text-neutral-300 mb-6">
              Permission is granted to temporarily use SlideForge for personal, non-commercial transitory viewing only. This is the grant of a license, not a transfer of title.
            </p>

            <h2 className="text-2xl font-bold text-neutral-100 mb-4">3. Disclaimer</h2>
            <p className="text-neutral-300 mb-6">
              The materials on SlideForge are provided on an 'as is' basis. SlideForge makes no warranties, expressed or implied, and hereby disclaims and negates all other warranties including without limitation, implied warranties or conditions of merchantability, fitness for a particular purpose, or non-infringement of intellectual property or other violation of rights.
            </p>

            <h2 className="text-2xl font-bold text-neutral-100 mb-4">4. Limitations</h2>
            <p className="text-neutral-300 mb-6">
              In no event shall SlideForge or its suppliers be liable for any damages (including, without limitation, damages for loss of data or profit, or due to business interruption) arising out of the use or inability to use the materials on SlideForge.
            </p>

            <h2 className="text-2xl font-bold text-neutral-100 mb-4">5. Revisions and Errata</h2>
            <p className="text-neutral-300 mb-6">
              The materials appearing on SlideForge could include technical, typographical, or photographic errors. SlideForge does not warrant that any of the materials on its website are accurate, complete or current.
            </p>

            <h2 className="text-2xl font-bold text-neutral-100 mb-4">6. Links</h2>
            <p className="text-neutral-300 mb-6">
              SlideForge has not reviewed all of the sites linked to its website and is not responsible for the contents of any such linked site. The inclusion of any link does not imply endorsement by SlideForge of the site.
            </p>

            <h2 className="text-2xl font-bold text-neutral-100 mb-4">7. Modifications</h2>
            <p className="text-neutral-300 mb-6">
              SlideForge may revise these terms of service for its website at any time without notice. By using this website you are agreeing to be bound by the then current version of these Terms and Conditions of Use.
            </p>

            <h2 className="text-2xl font-bold text-neutral-100 mb-4">8. Governing Law</h2>
            <p className="text-neutral-300 mb-6">
              Any claim relating to SlideForge shall be governed by the laws of the jurisdiction in which the service is operated without regard to its conflict of law provisions.
            </p>
          </div>
        </div>

        <div className="mt-8 text-center">
          <Link
            href="/"
            className="inline-flex items-center px-6 py-3 bg-indigo-600 text-white rounded-lg font-medium hover:bg-indigo-700 transition-colors duration-200"
          >
            Back to SlideForge
          </Link>
        </div>
      </main>
    </div>
  )
}
