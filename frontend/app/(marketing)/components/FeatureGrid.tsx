'use client'

import { motion } from 'framer-motion'
import { 
  Brain, 
  Layout, 
  Palette, 
  FileText, 
  Download, 
  Terminal 
} from 'lucide-react'

export default function FeatureGrid() {
  const features = [
    {
      icon: Brain,
      title: 'Smart Summaries',
      description: 'Distills sections into concise bullets while preserving key insights and academic rigor.',
    },
    {
      icon: Layout,
      title: 'Overflow-Safe Layouts',
      description: 'Never out of bounds. Auto-paginates content to ensure every slide fits perfectly.',
    },
    {
      icon: Palette,
      title: 'Rich Styling',
      description: 'Bullets, numbering, bold/italic/underline, and key-color highlights for emphasis.',
    },
    {
      icon: FileText,
      title: 'Multi-Doc Types',
      description: 'Research papers, project reports, user manuals, assignments, and general documentation.',
    },
    {
      icon: Download,
      title: 'Export Ready',
      description: 'PPTX/PDF ready for Google Slides, Keynote, PowerPoint, or any presentation software.',
    },
    {
      icon: Terminal,
      title: 'CLI & API',
      description: 'Automation-friendly with command-line interface and REST API for batch processing.',
    },
  ]

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
      },
    },
  }

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        duration: 0.5,
      },
    },
  }

  return (
    <motion.div
      variants={containerVariants}
      initial="hidden"
      whileInView="visible"
      viewport={{ once: true, margin: "-100px" }}
      className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
    >
      {features.map((feature, index) => (
        <motion.div
          key={index}
          variants={itemVariants}
          className="group relative bg-neutral-900/50 border border-neutral-800 rounded-xl p-6 hover:border-neutral-700 hover:bg-neutral-900/70 transition-all duration-300 focus-within:ring-2 focus-within:ring-indigo-500 focus-within:ring-offset-2 focus-within:ring-offset-neutral-950"
        >
          {/* Subtle glow on hover */}
          <div className="absolute inset-0 bg-gradient-to-r from-indigo-600/5 to-purple-600/5 rounded-xl opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
          
          <div className="relative">
            {/* Icon */}
            <div className="w-12 h-12 bg-indigo-600/20 rounded-lg flex items-center justify-center mb-4 group-hover:bg-indigo-600/30 transition-colors duration-300">
              <feature.icon className="w-6 h-6 text-indigo-400" />
            </div>

            {/* Title */}
            <h3 className="text-xl font-semibold text-neutral-100 mb-3 group-hover:text-indigo-300 transition-colors duration-300">
              {feature.title}
            </h3>

            {/* Description */}
            <p className="text-neutral-400 leading-relaxed">
              {feature.description}
            </p>
          </div>
        </motion.div>
      ))}
    </motion.div>
  )
}
