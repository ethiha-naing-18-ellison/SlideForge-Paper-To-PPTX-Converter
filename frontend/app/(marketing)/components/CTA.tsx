'use client'

import Link from 'next/link'
import { motion } from 'framer-motion'
import { ArrowRight, BookOpen } from 'lucide-react'

export default function CTA() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 30 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ duration: 0.8 }}
      className="relative bg-neutral-900/50 border border-gradient-to-r from-indigo-600/50 via-purple-600/50 to-cyan-600/50 rounded-2xl p-8 md:p-12 overflow-hidden"
    >
      {/* Gradient Border Effect */}
      <div className="absolute inset-0 bg-gradient-to-r from-indigo-600/20 via-purple-600/20 to-cyan-600/20 rounded-2xl opacity-0 hover:opacity-100 transition-opacity duration-500" />
      
      {/* Background Glow */}
      <div className="absolute inset-0 bg-gradient-to-br from-indigo-600/10 via-purple-600/5 to-cyan-600/10 rounded-2xl" />
      
      <div className="relative text-center">
        {/* Headline */}
        <h2 className="text-3xl md:text-4xl font-bold text-neutral-100 mb-4">
          Ready to forge your next deck?
        </h2>
        
        {/* Subtext */}
        <p className="text-xl text-neutral-300 mb-8 max-w-2xl mx-auto">
          Turn dense documents into presentation-ready slides in minutes.
        </p>
        
        {/* CTA Buttons */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
          <Link
            href="/app"
            className="group px-8 py-4 bg-indigo-600 text-white rounded-lg font-semibold text-lg hover:bg-indigo-700 transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 focus:ring-offset-neutral-950 flex items-center space-x-2"
            aria-label="Launch SlideForge App"
          >
            <span>Launch App</span>
            <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform duration-200" />
          </Link>
          
          <Link
            href="/docs"
            className="group px-8 py-4 border border-neutral-600 text-neutral-300 rounded-lg font-semibold text-lg hover:bg-neutral-800 hover:text-neutral-100 transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-neutral-500 focus:ring-offset-2 focus:ring-offset-neutral-950 flex items-center space-x-2"
            aria-label="View SlideForge Documentation"
          >
            <BookOpen className="w-5 h-5" />
            <span>View Docs</span>
          </Link>
        </div>
      </div>
    </motion.div>
  )
}
