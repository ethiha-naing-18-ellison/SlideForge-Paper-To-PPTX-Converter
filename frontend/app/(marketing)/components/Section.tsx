import { ReactNode } from 'react'

interface SectionProps {
  id?: string
  title?: string
  children: ReactNode
  className?: string
}

export default function Section({ id, title, children, className = '' }: SectionProps) {
  return (
    <section id={id} className={`mx-auto max-w-7xl px-4 md:px-6 py-16 ${className}`}>
      {title && (
        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-bold text-neutral-100 mb-4">
            {title}
          </h2>
        </div>
      )}
      {children}
    </section>
  )
}
