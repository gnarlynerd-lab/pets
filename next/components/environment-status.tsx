"use client"

import { useState, useEffect } from 'react'
import { CloudSun, Waves, Zap, Users } from 'lucide-react'

interface EnvironmentStatusProps {
  companionCount?: number
  activeConnections?: number
}

export function EnvironmentStatus({ 
  companionCount = 0, 
  activeConnections = 0 
}: EnvironmentStatusProps) {
  const [isClient, setIsClient] = useState(false)
  const [environmentMood, setEnvironmentMood] = useState<'thriving' | 'balanced' | 'quiet'>('balanced')
  const [environmentMessage, setEnvironmentMessage] = useState('A peaceful moment for deep connection')

  // Initialize client state
  useEffect(() => {
    setIsClient(true)
  }, [])

  // Simulate environment intelligence based on activity
  useEffect(() => {
    if (!isClient) return
    
    if (activeConnections > 3) {
      setEnvironmentMood('thriving')
      setEnvironmentMessage('The ecosystem feels vibrant with active connections')
    } else if (activeConnections > 1) {
      setEnvironmentMood('balanced')
      setEnvironmentMessage('The environment encourages new relationships')
    } else {
      setEnvironmentMood('quiet')
      setEnvironmentMessage('A peaceful moment for deep connection')
    }
  }, [activeConnections, isClient])

  const getMoodColor = () => {
    switch (environmentMood) {
      case 'thriving': return 'text-green-600 bg-green-50'
      case 'balanced': return 'text-blue-600 bg-blue-50'
      case 'quiet': return 'text-purple-600 bg-purple-50'
      default: return 'text-gray-600 bg-gray-50'
    }
  }

  const getMoodIcon = () => {
    switch (environmentMood) {
      case 'thriving': return <Zap className="w-4 h-4" />
      case 'balanced': return <CloudSun className="w-4 h-4" />
      case 'quiet': return <Waves className="w-4 h-4" />
      default: return <CloudSun className="w-4 h-4" />
    }
  }

  return (
    <div className="bg-white/90 backdrop-blur-sm rounded-xl p-4 border border-indigo-200 shadow-lg">
      <div className="flex items-center gap-2 mb-3">
        <div className={`p-1 rounded-full ${getMoodColor()}`}>
          {getMoodIcon()}
        </div>
        <h3 className="text-lg font-semibold text-indigo-700 font-sans">
          Environment
        </h3>
      </div>
      
      <div className="space-y-2">
        <p className="text-xs text-indigo-600 font-medium">
          {environmentMessage}
        </p>
        
        <div className="grid grid-cols-2 gap-3 text-xs">
          <div className="flex items-center gap-1">
            <Users className="w-3 h-3 text-indigo-500" />
            <span className="text-indigo-600">{companionCount} Companions</span>
          </div>
          <div className="flex items-center gap-1">
            <Waves className="w-3 h-3 text-indigo-500" />
            <span className="text-indigo-600">{activeConnections} Active</span>
          </div>
        </div>

        {/* Environment suggestions */}
        {environmentMood === 'quiet' && (
          <div className="mt-2 p-2 bg-purple-50 rounded-lg">
            <p className="text-xs text-purple-700">
              🌸 The environment suggests gentle, thoughtful interaction
            </p>
          </div>
        )}
        
        {environmentMood === 'thriving' && (
          <div className="mt-2 p-2 bg-green-50 rounded-lg">
            <p className="text-xs text-green-700">
              ✨ High energy! Great time for playful connections
            </p>
          </div>
        )}
      </div>
    </div>
  )
}