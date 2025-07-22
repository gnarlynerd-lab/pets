"use client"

import { useState, useEffect } from 'react'

interface ClientOnlyProps {
  children: React.ReactNode
  fallback?: React.ReactNode
}

export function ClientOnly({ children, fallback }: ClientOnlyProps) {
  const [hasMounted, setHasMounted] = useState(false)

  useEffect(() => {
    // Double-check for Safari compatibility
    const timer = setTimeout(() => {
      setHasMounted(true)
    }, 0)
    
    return () => clearTimeout(timer)
  }, [])

  // Additional check for Safari
  if (typeof window === 'undefined' || !hasMounted) {
    return fallback || null
  }

  return <>{children}</>
}