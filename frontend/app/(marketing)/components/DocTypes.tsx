'use client'

import { motion } from 'framer-motion'

export default function DocTypes() {
  const docTypes = [
    'Research Paper',
    'Project Report', 
    'Implementation Report',
    'User Manual',
    'Documentation',
    'School Project Report',
    'Assignment',
    'School Assignment',
    'General Report'
  ]

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.05,
      },
    },
  }

  const itemVariants = {
    hidden: { opacity: 0, scale: 0.8 },
    visible: {
      opacity: 1,
      scale: 1,
      transition: {
        duration: 0.3,
      },
    },
  }

  return (
    <div className="text-center">
      <motion.p
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        transition={{ duration: 0.6 }}
        className="text-lg text-neutral-300 mb-8 max-w-3xl mx-auto"
      >
        SlideForge isn't just for research papers — it formats reports, manuals, and assignments with the same precision.
      </motion.p>

      <motion.div
        variants={containerVariants}
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, margin: "-50px" }}
        className="flex flex-wrap justify-center gap-3"
      >
        {docTypes.map((docType, index) => (
          <motion.span
            key={index}
            variants={itemVariants}
            className="inline-flex items-center px-4 py-2 rounded-full text-sm font-medium bg-indigo-600/20 text-indigo-300 border border-indigo-600/30 hover:bg-indigo-600/30 hover:border-indigo-600/50 transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 focus:ring-offset-neutral-950"
          >
            {docType}
          </motion.span>
        ))}
      </motion.div>
    </div>
  )
}
