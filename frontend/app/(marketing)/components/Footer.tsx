'use client'

import Link from 'next/link'
import Image from 'next/image'
import { ArrowUp, Mail, Phone, Github, Linkedin } from 'lucide-react'

export default function Footer() {
  const currentYear = new Date().getFullYear()

  const footerLinks = {
    product: [
      { href: '#features', label: 'Features' },
      { href: '#how-it-works', label: 'How it Works' },
      { href: '#doc-types', label: 'Doc Types' },
    ],
    resources: [
      { href: '#faq', label: 'FAQ' },
      { href: '/docs', label: 'Documentation' },
      { href: '/docs/cli', label: 'CLI Guide' },
    ],
    company: [
      { href: '/about', label: 'About' },
      { href: '#contact', label: 'Contact' },
    ],
  }

  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  return (
    <footer className="bg-neutral-950 border-t border-neutral-800">
      <div className="mx-auto max-w-7xl px-4 md:px-6 py-12">
        {/* Main Footer Content */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-8 mb-8">
          {/* Brand Section */}
          <div className="lg:col-span-1">
            <Link href="/" className="flex items-center space-x-3 mb-4" aria-label="SlideForge Home">
              <Image
                src="/images/logo/logo.png"
                alt="SlideForge Logo"
                width={32}
                height={32}
                className="w-8 h-8"
              />
              <span className="text-lg font-bold text-neutral-100">SlideForge</span>
            </Link>
            <p className="text-neutral-400 text-sm leading-relaxed">
              SlideForge turns dense documents into clear, presentation-ready decks.
            </p>
          </div>

          {/* Product Links */}
          <div>
            <h3 className="text-neutral-100 font-semibold mb-4">Product</h3>
            <ul className="space-y-2">
              {footerLinks.product.map((link) => (
                <li key={link.href}>
                  <Link
                    href={link.href}
                    className="text-neutral-400 hover:text-neutral-100 transition-colors duration-200 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 focus:ring-offset-neutral-950 rounded"
                    aria-label={`Navigate to ${link.label}`}
                  >
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Resources Links */}
          <div>
            <h3 className="text-neutral-100 font-semibold mb-4">Resources</h3>
            <ul className="space-y-2">
              {footerLinks.resources.map((link) => (
                <li key={link.href}>
                  <Link
                    href={link.href}
                    className="text-neutral-400 hover:text-neutral-100 transition-colors duration-200 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 focus:ring-offset-neutral-950 rounded"
                    aria-label={`Navigate to ${link.label}`}
                  >
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Company Links */}
          <div>
            <h3 className="text-neutral-100 font-semibold mb-4">Company</h3>
            <ul className="space-y-2">
              {footerLinks.company.map((link) => (
                <li key={link.href}>
                  <Link
                    href={link.href}
                    className="text-neutral-400 hover:text-neutral-100 transition-colors duration-200 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 focus:ring-offset-neutral-950 rounded"
                    aria-label={`Navigate to ${link.label}`}
                  >
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Developer Contact */}
          <div>
            <h3 className="text-neutral-100 font-semibold mb-4">Developer</h3>
            <div className="space-y-3">
              <div>
                <p className="text-neutral-100 font-medium text-sm">Thiha Naing</p>
                <p className="text-neutral-400 text-xs">Software Engineer, Data Analyst</p>
              </div>
              
              <div className="space-y-2">
                <a
                  href="mailto:thiha.naing.codev@gmail.com"
                  className="flex items-center space-x-2 text-neutral-400 hover:text-neutral-100 transition-colors duration-200 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 focus:ring-offset-neutral-950 rounded"
                  aria-label="Email Thiha Naing"
                >
                  <Mail className="w-4 h-4" />
                  <span>thiha.naing.codev@gmail.com</span>
                </a>
                
                <a
                  href="tel:+60187799581"
                  className="flex items-center space-x-2 text-neutral-400 hover:text-neutral-100 transition-colors duration-200 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 focus:ring-offset-neutral-950 rounded"
                  aria-label="Call Thiha Naing"
                >
                  <Phone className="w-4 h-4" />
                  <span>+60187799581</span>
                </a>
                
                <a
                  href="https://github.com/ethiha-naing-18-ellison"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center space-x-2 text-neutral-400 hover:text-neutral-100 transition-colors duration-200 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 focus:ring-offset-neutral-950 rounded"
                  aria-label="Visit Thiha Naing's GitHub profile"
                >
                  <Github className="w-4 h-4" />
                  <span>GitHub</span>
                </a>
                
                <a
                  href="https://www.linkedin.com/in/thiha-naing-18t43"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center space-x-2 text-neutral-400 hover:text-neutral-100 transition-colors duration-200 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 focus:ring-offset-neutral-950 rounded"
                  aria-label="Visit Thiha Naing's LinkedIn profile"
                >
                  <Linkedin className="w-4 h-4" />
                  <span>LinkedIn</span>
                </a>
              </div>
            </div>
          </div>
        </div>

        {/* Contact Section */}
        <div id="contact" className="border-t border-neutral-800 pt-8 mb-8">
          <div className="text-center">
            <h3 className="text-neutral-100 font-semibold mb-4">Get in Touch</h3>
            <p className="text-neutral-400 text-sm mb-4">
              Have questions or need support? We're here to help.
            </p>
            <a
              href="https://wa.me/60187799581"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center px-4 py-2 bg-indigo-600 text-white rounded-lg font-medium hover:bg-indigo-700 transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 focus:ring-offset-neutral-950"
              aria-label="Contact SlideForge via WhatsApp"
            >
              Contact Us
            </a>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="border-t border-neutral-800 pt-8 flex flex-col md:flex-row justify-between items-center">
          <p className="text-neutral-400 text-sm mb-4 md:mb-0">
            © {currentYear} SlideForge. All rights reserved.
          </p>
          
          <div className="flex items-center space-x-6">
            <Link
              href="/legal/terms"
              className="text-neutral-400 hover:text-neutral-100 transition-colors duration-200 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 focus:ring-offset-neutral-950 rounded"
              aria-label="View Terms of Service"
            >
              Terms of Service
            </Link>
            <Link
              href="/legal/privacy"
              className="text-neutral-400 hover:text-neutral-100 transition-colors duration-200 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 focus:ring-offset-neutral-950 rounded"
              aria-label="View Privacy Policy"
            >
              Privacy Policy
            </Link>
            
            {/* Back to Top Button */}
            <button
              onClick={scrollToTop}
              className="p-2 text-neutral-400 hover:text-neutral-100 hover:bg-neutral-800 rounded-lg transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 focus:ring-offset-neutral-950"
              aria-label="Back to top"
            >
              <ArrowUp className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
    </footer>
  )
}
