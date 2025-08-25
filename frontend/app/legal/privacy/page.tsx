'use client'

import Link from 'next/link'
import Image from 'next/image'
import { ArrowLeft, Lock } from 'lucide-react'

export default function PrivacyPage() {
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
                <p className="text-sm text-neutral-400">Privacy Policy</p>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center mb-12">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-indigo-600/20 rounded-full mb-6">
            <Lock className="w-8 h-8 text-indigo-400" />
          </div>
          <h1 className="text-4xl font-bold text-neutral-100 mb-4">
            Privacy Policy
          </h1>
          <p className="text-xl text-neutral-300 max-w-2xl mx-auto">
            Last updated: {new Date().toLocaleDateString()}
          </p>
        </div>

        <div className="bg-neutral-900/50 border border-neutral-800 rounded-xl p-8">
          <div className="prose prose-invert max-w-none">
            <h2 className="text-2xl font-bold text-neutral-100 mb-4">1. Information We Collect</h2>
            <p className="text-neutral-300 mb-6">
              We collect information you provide directly to us, such as when you upload documents, create an account, or contact us for support. This may include documents you upload, metadata about those documents, and any personal information you choose to provide.
            </p>

            <h2 className="text-2xl font-bold text-neutral-100 mb-4">2. How We Use Your Information</h2>
            <p className="text-neutral-300 mb-6">
              We use the information we collect to provide, maintain, and improve our services, to process your requests, and to communicate with you about our services.
            </p>

            <h2 className="text-2xl font-bold text-neutral-100 mb-4">3. Information Sharing</h2>
            <p className="text-neutral-300 mb-6">
              We do not sell, trade, or otherwise transfer your personal information to third parties without your consent, except as described in this privacy policy or as required by law.
            </p>

            <h2 className="text-2xl font-bold text-neutral-100 mb-4">4. Data Security</h2>
            <p className="text-neutral-300 mb-6">
              We implement appropriate security measures to protect your personal information against unauthorized access, alteration, disclosure, or destruction.
            </p>

            <h2 className="text-2xl font-bold text-neutral-100 mb-4">5. Data Retention</h2>
            <p className="text-neutral-300 mb-6">
              We retain your information for as long as necessary to provide our services and fulfill the purposes outlined in this privacy policy, unless a longer retention period is required or permitted by law.
            </p>

            <h2 className="text-2xl font-bold text-neutral-100 mb-4">6. Your Rights</h2>
            <p className="text-neutral-300 mb-6">
              You have the right to access, correct, or delete your personal information. You may also have the right to restrict or object to certain processing of your information.
            </p>

            <h2 className="text-2xl font-bold text-neutral-100 mb-4">7. Cookies and Tracking</h2>
            <p className="text-neutral-300 mb-6">
              We may use cookies and similar tracking technologies to collect information about your browsing activities and to remember your preferences.
            </p>

            <h2 className="text-2xl font-bold text-neutral-100 mb-4">8. Changes to This Policy</h2>
            <p className="text-neutral-300 mb-6">
              We may update this privacy policy from time to time. We will notify you of any changes by posting the new privacy policy on this page and updating the "Last updated" date.
            </p>

            <h2 className="text-2xl font-bold text-neutral-100 mb-4">9. Contact Us</h2>
            <p className="text-neutral-300 mb-6">
              If you have any questions about this privacy policy, please contact us at privacy@slideforge.com.
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
