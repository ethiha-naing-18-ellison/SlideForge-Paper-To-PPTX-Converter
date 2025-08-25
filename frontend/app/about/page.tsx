'use client'

import Link from 'next/link'
import Image from 'next/image'
import { ArrowLeft, Users, Target, Zap } from 'lucide-react'

export default function AboutPage() {
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
                <p className="text-sm text-neutral-400">About Us</p>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center mb-12">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-indigo-600/20 rounded-full mb-6">
            <Users className="w-8 h-8 text-indigo-400" />
          </div>
          <h1 className="text-4xl font-bold text-neutral-100 mb-4">
            About SlideForge
          </h1>
          <p className="text-xl text-neutral-300 max-w-2xl mx-auto">
            Transforming the way researchers, students, and professionals create presentations from academic content.
          </p>
        </div>

        {/* Mission */}
        <div className="bg-neutral-900/50 border border-neutral-800 rounded-xl p-8 mb-8">
          <div className="flex items-start space-x-4">
            <div className="w-12 h-12 bg-indigo-600/20 rounded-lg flex items-center justify-center flex-shrink-0">
              <Target className="w-6 h-6 text-indigo-400" />
            </div>
            <div>
              <h2 className="text-2xl font-bold text-neutral-100 mb-4">Our Mission</h2>
              <p className="text-neutral-300 leading-relaxed">
                SlideForge was created to bridge the gap between dense academic content and engaging presentations. 
                We believe that valuable research and knowledge should be accessible and presentable to any audience. 
                Our AI-powered platform transforms complex documents into clear, professional presentations while 
                maintaining the integrity and depth of the original content.
              </p>
            </div>
          </div>
        </div>

        {/* What We Do */}
        <div className="bg-neutral-900/50 border border-neutral-800 rounded-xl p-8 mb-8">
          <h2 className="text-2xl font-bold text-neutral-100 mb-6">What We Do</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h3 className="text-lg font-semibold text-neutral-100 mb-3">Smart Content Analysis</h3>
              <p className="text-neutral-300">
                Our advanced AI algorithms analyze document structure, extract key insights, and identify the most 
                important information to include in presentations.
              </p>
            </div>
            <div>
              <h3 className="text-lg font-semibold text-neutral-100 mb-3">Professional Layouts</h3>
              <p className="text-neutral-300">
                We create clean, professional slide layouts with proper spacing, typography, and visual hierarchy 
                that work across all presentation platforms.
              </p>
            </div>
            <div>
              <h3 className="text-lg font-semibold text-neutral-100 mb-3">Overflow Protection</h3>
              <p className="text-neutral-300">
                Our intelligent pagination system ensures content never overflows slides, automatically breaking 
                content into appropriate slide lengths.
              </p>
            </div>
            <div>
              <h3 className="text-lg font-semibold text-neutral-100 mb-3">Multi-Format Support</h3>
              <p className="text-neutral-300">
                Support for research papers, reports, manuals, assignments, and more. Export to PPTX format 
                compatible with PowerPoint, Keynote, and Google Slides.
              </p>
            </div>
          </div>
        </div>

        {/* Technology */}
        <div className="bg-neutral-900/50 border border-neutral-800 rounded-xl p-8 mb-8">
          <div className="flex items-start space-x-4">
            <div className="w-12 h-12 bg-indigo-600/20 rounded-lg flex items-center justify-center flex-shrink-0">
              <Zap className="w-6 h-6 text-indigo-400" />
            </div>
            <div>
              <h2 className="text-2xl font-bold text-neutral-100 mb-4">Our Technology</h2>
              <p className="text-neutral-300 leading-relaxed mb-4">
                SlideForge combines cutting-edge natural language processing, document analysis, and presentation 
                design principles to deliver exceptional results. Our system understands academic content structure, 
                identifies key concepts, and creates presentations that maintain scholarly rigor while being 
                accessible to diverse audiences.
              </p>
              <p className="text-neutral-300 leading-relaxed">
                Built with modern web technologies and designed for scalability, SlideForge provides both web-based 
                and command-line interfaces to meet the needs of individual users and organizations.
              </p>
            </div>
          </div>
        </div>

        {/* CTA */}
        <div className="text-center">
          <h2 className="text-2xl font-bold text-neutral-100 mb-4">
            Ready to Transform Your Documents?
          </h2>
          <p className="text-neutral-300 mb-6">
            Join researchers, students, and professionals who are already using SlideForge to create better presentations.
          </p>
          <Link
            href="/app"
            className="inline-flex items-center px-8 py-4 bg-indigo-600 text-white rounded-lg font-semibold text-lg hover:bg-indigo-700 transition-colors duration-200"
          >
            Get Started with SlideForge
          </Link>
        </div>
      </main>
    </div>
  )
}
