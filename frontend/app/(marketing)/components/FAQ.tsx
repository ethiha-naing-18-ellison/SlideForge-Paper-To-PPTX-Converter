'use client'

import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { ChevronDown } from 'lucide-react'

export default function FAQ() {
  const [openIndex, setOpenIndex] = useState<number | null>(null)

  const faqs = [
    {
      question: "Does SlideForge only work with research papers?",
      answer: "No, SlideForge supports a wide variety of document types including research papers, project reports, implementation reports, user manuals, documentation, school project reports, assignments, and general reports. The system adapts its formatting and summarization approach based on the document type."
    },
    {
      question: "Will content overflow the slides?",
      answer: "No, SlideForge uses intelligent pagination and layout algorithms to ensure content never overflows slide boundaries. The system automatically breaks content into appropriate slide lengths and adjusts formatting to maintain readability and professional appearance."
    },
    {
      question: "Can I choose between bullets or numbering?",
      answer: "Yes, SlideForge allows you to choose between bullet points and numbered lists per section. The system also supports mixed formatting where you can have bullets for some sections and numbering for others, depending on the content structure."
    },
    {
      question: "Can I set a target slide count (e.g., 20 slides)?",
      answer: "Yes, SlideForge offers a 20-slide expansion option for comprehensive presentations. The system intelligently distributes content across the target number of slides while maintaining logical flow and ensuring each slide has meaningful content."
    },
    {
      question: "What export formats are supported?",
      answer: "SlideForge exports presentations in PPTX format, which is compatible with Microsoft PowerPoint, Google Slides, Apple Keynote, and other presentation software. The exported files maintain all formatting, styling, and layout elements."
    }
  ]

  const toggleFAQ = (index: number) => {
    setOpenIndex(openIndex === index ? null : index)
  }

  return (
    <div className="max-w-4xl mx-auto space-y-4">
      {faqs.map((faq, index) => (
        <motion.div
          key={index}
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5, delay: index * 0.1 }}
          className="bg-neutral-900/50 border border-neutral-800 rounded-lg overflow-hidden hover:border-neutral-700 transition-colors duration-200"
        >
          <button
            onClick={() => toggleFAQ(index)}
            className="w-full px-6 py-4 text-left flex items-center justify-between hover:bg-neutral-900/30 transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 focus:ring-offset-neutral-950"
            aria-expanded={openIndex === index}
            aria-label={`Toggle FAQ: ${faq.question}`}
          >
            <h3 className="text-lg font-semibold text-neutral-100 pr-4">
              {faq.question}
            </h3>
            <ChevronDown 
              className={`w-5 h-5 text-neutral-400 transition-transform duration-200 ${
                openIndex === index ? 'rotate-180' : ''
              }`} 
            />
          </button>
          
          <AnimatePresence>
            {openIndex === index && (
              <motion.div
                initial={{ height: 0, opacity: 0 }}
                animate={{ height: 'auto', opacity: 1 }}
                exit={{ height: 0, opacity: 0 }}
                transition={{ duration: 0.3, ease: 'easeInOut' }}
                className="overflow-hidden"
              >
                <div className="px-6 pb-4">
                  <p className="text-neutral-300 leading-relaxed">
                    {faq.answer}
                  </p>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </motion.div>
      ))}
    </div>
  )
}
