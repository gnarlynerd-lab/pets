"use client"

import { useEffect, useState } from 'react'

interface PetData {
  id: string
  traits: Record<string, number>
  mood: number
  energy: number
  health: number
  attention: number
  needs: {
    hunger: number
    thirst: number
    social: number
    play: number
    rest: number
  }
  age: number
  stage: string
  current_emoji_message?: string
  personality_summary?: string
}

interface PetDisplayProps {
  petData: PetData | null
  petResponse: string
  isLoading: boolean
}

export default function PetDisplay({ petData, petResponse, isLoading }: PetDisplayProps) {
  const [displayMessage, setDisplayMessage] = useState('')
  const [isAnimating, setIsAnimating] = useState(false)

  useEffect(() => {
    if (petResponse && petResponse !== displayMessage) {
      setIsAnimating(true)
      setDisplayMessage(petResponse)
      
      // Reset animation after a delay
      const timer = setTimeout(() => {
        setIsAnimating(false)
      }, 2000)
      
      return () => clearTimeout(timer)
    }
  }, [petResponse, displayMessage])

  // Get pet character emoji based on mood
  const getPetCharacter = () => {
    if (!petData) return '🐾'
    
    const mood = petData.mood / 100.0  // Convert to 0-1 scale
    const energy = petData.energy / 100.0  // Convert to 0-1 scale
    
    if (mood > 0.8) return '😊'
    if (mood > 0.6) return '🙂'
    if (mood > 0.4) return '😐'
    if (mood > 0.2) return '😔'
    if (energy < 0.3) return '😴'
    return '🤔'
  }

  // Get background gradient based on pet's emotional state
  const getBackgroundGradient = () => {
    if (!petData) return 'from-slate-700 to-slate-800'
    
    const mood = petData.mood / 100.0  // Convert to 0-1 scale
    const energy = petData.energy / 100.0  // Convert to 0-1 scale
    
    if (mood > 0.7 && energy > 0.7) return 'from-green-600 to-emerald-700'
    if (mood > 0.5) return 'from-blue-600 to-indigo-700'
    if (energy < 0.3) return 'from-purple-600 to-purple-800'
    if (mood < 0.3) return 'from-gray-600 to-gray-800'
    return 'from-slate-600 to-slate-700'
  }

  return (
    <div className={`relative bg-gradient-to-br ${getBackgroundGradient()} rounded-2xl shadow-2xl border border-slate-600 overflow-hidden`}>
      {/* Loading overlay */}
      {isLoading && (
        <div className="absolute inset-0 bg-black/20 backdrop-blur-sm z-20 flex items-center justify-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-white"></div>
        </div>
      )}

      <div className="p-8 h-80 flex flex-col items-center justify-center text-center">
        {/* Pet Character */}
        <div className={`text-8xl mb-6 pet-glow rounded-full bg-white/10 p-4 ${isAnimating ? 'emoji-bounce' : ''}`}>
          {getPetCharacter()}
        </div>

        {/* Pet name and status */}
        <div className="mb-4">
          <h2 className="text-2xl font-bold text-white mb-1">
            {petData?.id || 'Digital Pet'}
          </h2>
          <p className="text-slate-200 text-sm">
            {petData?.personality_summary || 'Getting to know you...'}
          </p>
        </div>

        {/* Pet's emoji message */}
        <div className="bg-white/10 backdrop-blur-sm rounded-lg px-6 py-4 border border-white/20">
          <div className={`text-3xl ${isAnimating ? 'emoji-pulse' : ''}`}>
            {displayMessage || '👋'}
          </div>
          {displayMessage && (
            <p className="text-xs text-slate-300 mt-2">
              Pet says...
            </p>
          )}
        </div>

        {/* Interaction hints */}
        {!displayMessage && (
          <div className="mt-6 text-slate-300 text-sm text-center">
            <p>Say hello with emojis! 👋😊</p>
            <p className="text-xs text-slate-400 mt-1">
              Your pet will learn and develop its own personality based on your interactions
            </p>
          </div>
        )}
      </div>

      {/* Decorative elements */}
      <div className="absolute top-4 right-4">
        <div className="flex space-x-1">
          <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
          <div className="w-2 h-2 bg-blue-400 rounded-full animate-pulse" style={{ animationDelay: '0.5s' }}></div>
          <div className="w-2 h-2 bg-purple-400 rounded-full animate-pulse" style={{ animationDelay: '1s' }}></div>
        </div>
      </div>
    </div>
  )
}
