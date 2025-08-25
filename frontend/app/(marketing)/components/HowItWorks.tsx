'use client'

import { motion } from 'framer-motion'
import { Upload, Search, Layout, Download } from 'lucide-react'

export default function HowItWorks() {
  const steps = [
    {
      number: '01',
      icon: Upload,
      title: 'Upload a PDF or paste a link',
      description: 'Simply drag and drop your PDF file or paste a DOI/URL to get started.',
    },
    {
      number: '02',
      icon: Search,
      title: 'Analyze sections & extract key points',
      description: 'Our AI analyzes the document structure and extracts the most important information.',
    },
    {
      number: '03',
      icon: Layout,
      title: 'Lay out slides with pagination & themes',
      description: 'Smart layout engine creates professional slides with automatic pagination and styling.',
    },
    {
      number: '04',
      icon: Download,
      title: 'Export PPTX/PDF and present',
      description: 'Download your presentation ready for any platform - PowerPoint, Google Slides, or Keynote.',
    },
  ]

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.2,
      },
    },
  }

  const itemVariants = {
    hidden: { opacity: 0, y: 30 },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        duration: 0.6,
      },
    },
  }

  return (
    <motion.div
      variants={containerVariants}
      initial="hidden"
      whileInView="visible"
      viewport={{ once: true, margin: "-100px" }}
      className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8"
    >
      {steps.map((step, index) => (
        <motion.div
          key={index}
          variants={itemVariants}
          className="relative group"
        >
          {/* Step Number */}
          <div className="absolute -top-4 -left-4 w-12 h-12 bg-indigo-600 rounded-full flex items-center justify-center text-white font-bold text-lg group-hover:bg-indigo-700 transition-colors duration-300">
            {step.number}
          </div>

          {/* Card */}
          <div className="bg-neutral-900/50 border border-neutral-800 rounded-xl p-6 pt-8 hover:border-neutral-700 hover:bg-neutral-900/70 transition-all duration-300">
            {/* Icon */}
            <div className="w-12 h-12 bg-indigo-600/20 rounded-lg flex items-center justify-center mb-4 group-hover:bg-indigo-600/30 transition-colors duration-300">
              <step.icon className="w-6 h-6 text-indigo-400" />
            </div>

            {/* Title */}
            <h3 className="text-lg font-semibold text-neutral-100 mb-3 group-hover:text-indigo-300 transition-colors duration-300">
              {step.title}
            </h3>

            {/* Description */}
            <p className="text-neutral-400 text-sm leading-relaxed">
              {step.description}
            </p>
          </div>

          {/* Connecting Line (except for last item) */}
          {index < steps.length - 1 && (
            <div className="hidden lg:block absolute top-1/2 -right-4 w-8 h-0.5 bg-gradient-to-r from-indigo-600/50 to-transparent transform -translate-y-1/2" />
          )}
        </motion.div>
      ))}
    </motion.div>
  )
}
