'use client'

import Link from 'next/link'
import { motion } from 'framer-motion'
import { CheckCircle, ArrowRight } from 'lucide-react'

export default function Hero() {
  const trustFeatures = [
    { icon: CheckCircle, text: 'No overflow guarantee' },
    { icon: CheckCircle, text: 'Auto pagination' },
    { icon: CheckCircle, text: 'Exports PPTX/PDF' },
  ]

  return (
    <section className="relative overflow-hidden py-20 md:py-32">
      {/* Background Glow */}
      <div className="absolute inset-0 bg-gradient-to-b from-indigo-600/10 via-transparent to-transparent" />
      
      <div className="relative mx-auto max-w-7xl px-4 md:px-6">
        <div className="text-center">
          {/* Main Headline */}
          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="text-4xl md:text-6xl lg:text-7xl font-bold text-neutral-100 mb-6 leading-tight"
          >
            Forge beautiful slide decks from{' '}
            <span className="bg-gradient-to-r from-indigo-400 via-purple-400 to-cyan-400 bg-clip-text text-transparent">
              any document
            </span>{' '}
            — instantly.
          </motion.h1>

          {/* Subtext */}
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.1 }}
            className="text-xl md:text-2xl text-neutral-300 mb-8 max-w-4xl mx-auto leading-relaxed"
          >
            Upload a PDF or paste a link. SlideForge summarizes content, applies smart layouts, 
            paginates without overflow, and exports a polished .pptx ready for class, meetings, or conferences.
          </motion.p>

          {/* CTA Buttons */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-12"
          >
            <Link
              href="/app"
              className="group px-8 py-4 bg-indigo-600 text-white rounded-lg font-semibold text-lg hover:bg-indigo-700 transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 focus:ring-offset-neutral-950 flex items-center space-x-2"
              aria-label="Get started with SlideForge"
            >
              <span>Get Started</span>
              <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform duration-200" />
            </Link>
            
            <Link
              href="#features"
              className="px-8 py-4 border border-neutral-600 text-neutral-300 rounded-lg font-semibold text-lg hover:bg-neutral-800 hover:text-neutral-100 transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-neutral-500 focus:ring-offset-2 focus:ring-offset-neutral-950"
              aria-label="Learn more about SlideForge features"
            >
              Learn More
            </Link>
          </motion.div>

          {/* Trust Indicators */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.3 }}
            className="flex flex-wrap justify-center items-center gap-6 md:gap-8 text-neutral-400"
          >
            {trustFeatures.map((feature, index) => (
              <div
                key={index}
                className="flex items-center space-x-2 text-sm md:text-base"
              >
                <feature.icon className="w-5 h-5 text-green-400" />
                <span>{feature.text}</span>
              </div>
            ))}
          </motion.div>
        </div>
      </div>
    </section>
  )
}
