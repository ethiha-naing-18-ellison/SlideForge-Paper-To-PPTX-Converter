'use client'

import { motion } from 'framer-motion'

export default function Description() {
  return (
    <div className="max-w-4xl mx-auto">
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        transition={{ duration: 0.8 }}
        className="space-y-6 text-lg text-neutral-300 leading-relaxed"
      >
        <p>
          <strong className="text-neutral-100">SlideForge</strong> is an intelligent document-to-presentation converter 
          that transforms dense academic papers, technical reports, and educational materials into clear, 
          professional slide decks. Using advanced AI summarization and smart layout algorithms, 
          it extracts key insights while maintaining academic rigor and ensuring content never overflows slide boundaries.
        </p>

        <p>
          Whether you're a researcher preparing for conferences, a student working on assignments, 
          or a professional creating training materials, SlideForge saves hours of manual work. 
          The system features a dark theme interface, intelligent key-phrase color highlighting, 
          automatic pagination, and a 20-slide expansion option for comprehensive presentations. 
          Every output is export-ready for PowerPoint, Google Slides, or Keynote, ensuring 
          your presentations look polished and professional from the first slide to the last.
        </p>
      </motion.div>
    </div>
  )
}
