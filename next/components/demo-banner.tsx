"use client"

import { useEffect, useState } from 'react'

interface DemoBannerProps {
  interactionCount: number
  maxInteractions?: number
}

export function DemoBanner({ 
  interactionCount, 
  maxInteractions = 50 
}: DemoBannerProps) {
  const [timeRemaining, setTimeRemaining] = useState<string>('')
  
  useEffect(() => {
    // Calculate session time remaining (30 minutes)
    const sessionStart = sessionStorage.getItem('session_start')
    if (!sessionStart) {
      sessionStorage.setItem('session_start', Date.now().toString())
    }
    
    const interval = setInterval(() => {
      const start = parseInt(sessionStorage.getItem('session_start') || '0')
      const elapsed = Date.now() - start
      const remaining = Math.max(0, 30 * 60 * 1000 - elapsed) // 30 minutes
      
      const minutes = Math.floor(remaining / 60000)
      const seconds = Math.floor((remaining % 60000) / 1000)
      
      setTimeRemaining(`${minutes}:${seconds.toString().padStart(2, '0')}`)
      
      if (remaining === 0) {
        // Session expired
        sessionStorage.clear()
        window.location.reload()
      }
    }, 1000)
    
    return () => clearInterval(interval)
  }, [])
  
  const remainingInteractions = maxInteractions - interactionCount
  const percentUsed = (interactionCount / maxInteractions) * 100
  
  // Only show in demo mode
  if (process.env.NEXT_PUBLIC_DEMO_MODE !== 'true') {
    return null
  }
  
  return (
    <div className="fixed top-0 left-0 right-0 bg-gray-900 text-white text-xs py-2 px-4 z-50">
      <div className="max-w-4xl mx-auto flex items-center justify-between">
        <div className="flex items-center gap-4">
          <span className="font-mono">DEMO MODE</span>
          <span className="text-gray-400">•</span>
          <span>
            {remainingInteractions} interactions remaining
          </span>
          <span className="text-gray-400">•</span>
          <span>
            Session: {timeRemaining}
          </span>
        </div>
        
        <div className="flex items-center gap-2">
          <div className="w-24 h-1 bg-gray-700 rounded-full overflow-hidden">
            <div 
              className="h-full bg-green-500 transition-all duration-300"
              style={{ 
                width: `${100 - percentUsed}%`,
                backgroundColor: percentUsed > 80 ? '#ef4444' : percentUsed > 60 ? '#eab308' : '#22c55e'
              }}
            />
          </div>
          <span className="text-gray-400 text-xs">
            Data resets daily
          </span>
        </div>
      </div>
    </div>
  )
}