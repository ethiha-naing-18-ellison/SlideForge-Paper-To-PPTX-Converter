'use client'

import Navbar from './(marketing)/components/Navbar'
import Hero from './(marketing)/components/Hero'
import FeatureGrid from './(marketing)/components/FeatureGrid'
import HowItWorks from './(marketing)/components/HowItWorks'
import DocTypes from './(marketing)/components/DocTypes'
import Description from './(marketing)/components/Description'
import CTA from './(marketing)/components/CTA'
import FAQ from './(marketing)/components/FAQ'
import Footer from './(marketing)/components/Footer'
import Section from './(marketing)/components/Section'
import Glow from './(marketing)/components/Glow'

export default function Home() {
  return (
    <div className="min-h-screen bg-neutral-950 text-neutral-100">
      {/* Skip Link for Accessibility */}
      <a
        href="#main"
        className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 bg-indigo-600 text-white px-4 py-2 rounded-lg z-50"
      >
        Skip to main content
      </a>

      {/* Background Glow Effects */}
      <Glow />

      {/* Navigation */}
      <Navbar />

      {/* Main Content */}
      <main id="main">
        {/* Hero Section */}
        <Hero />

        {/* Features Section */}
        <Section id="features" title="Powerful Features">
          <FeatureGrid />
        </Section>

        {/* How It Works Section */}
        <Section id="how-it-works" title="How It Works">
          <HowItWorks />
        </Section>

        {/* Document Types Section */}
        <Section id="doc-types" title="Supported Document Types">
          <DocTypes />
        </Section>

        {/* Description Section */}
        <Section title="About SlideForge">
          <Description />
        </Section>

        {/* CTA Section */}
        <Section>
          <CTA />
        </Section>

        {/* FAQ Section */}
        <Section id="faq" title="Frequently Asked Questions">
          <FAQ />
        </Section>
      </main>

      {/* Footer */}
      <Footer />
    </div>
  )
}
