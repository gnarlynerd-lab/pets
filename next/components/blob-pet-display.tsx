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

interface BlobPetDisplayProps {
  petData: PetData | null
  petResponse: string
  isLoading: boolean
  petName?: string
}

export default function BlobPetDisplay({ petData, petResponse, isLoading, petName }: BlobPetDisplayProps) {
  const [displayMessage, setDisplayMessage] = useState('')
  const [isAnimating, setIsAnimating] = useState(false)
  const [breathingPhase, setBreathingPhase] = useState(0)

  useEffect(() => {
    if (petResponse && petResponse !== displayMessage) {
      setIsAnimating(true)
      setDisplayMessage(petResponse)
      
      const timer = setTimeout(() => {
        setIsAnimating(false)
      }, 2000)
      
      return () => clearTimeout(timer)
    }
  }, [petResponse, displayMessage])

  // Breathing animation
  useEffect(() => {
    const interval = setInterval(() => {
      setBreathingPhase(prev => (prev + 1) % 100)
    }, 50)
    return () => clearInterval(interval)
  }, [])

  // Calculate evolution stage (0-100%)
  const getEvolutionStage = () => {
    if (!petData) return 0
    const ageFactor = Math.min(petData.age / 100, 1)
    const attentionFactor = Math.min(petData.attention / 100, 1)
    return Math.min((ageFactor + attentionFactor) * 50, 100)
  }

  const evolutionStage = getEvolutionStage()

  // Get blob features based on evolution stage
  const getBlobFeatures = () => {
    const features = {
      hasEyes: evolutionStage >= 25,
      hasExpression: evolutionStage >= 50,
      hasAppendages: evolutionStage >= 75,
      isHumanoid: evolutionStage >= 100
    }
    return features
  }

  const features = getBlobFeatures()

  // Generate blob path with breathing animation
  const generateBlobPath = () => {
    const baseSize = 80
    const breathingScale = 1 + Math.sin(breathingPhase * 0.1) * 0.05
    const size = baseSize * breathingScale
    
    const centerX = 100
    const centerY = 100
    
    const points = []
    const numPoints = 8
    
    for (let i = 0; i < numPoints; i++) {
      const angle = (i / numPoints) * 2 * Math.PI
      const radius = size + Math.sin(angle * 3 + breathingPhase * 0.05) * 10
      const x = centerX + Math.cos(angle) * radius
      const y = centerY + Math.sin(angle) * radius
      points.push({ x, y })
    }
    
    let path = `M ${points[0].x} ${points[0].y}`
    for (let i = 0; i < points.length; i++) {
      const current = points[i]
      const next = points[(i + 1) % points.length]
      const midX = (current.x + next.x) / 2
      const midY = (current.y + next.y) / 2
      path += ` Q ${current.x} ${current.y} ${midX} ${midY}`
    }
    path += ' Z'
    
    return path
  }

  return (
    <div className="bg-gradient-to-br from-indigo-100 to-slate-100 rounded-3xl shadow-lg border-2 border-indigo-200 p-6 min-h-[350px] flex flex-col items-center justify-center w-full">
      {/* Loading overlay */}
      {isLoading && (
        <div className="absolute inset-0 bg-white/20 backdrop-blur-sm z-20 flex items-center justify-center rounded-3xl">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-500"></div>
        </div>
      )}

      {/* SVG Blob Pet */}
      <div className="w-48 h-48 mb-4">
        <svg
          viewBox="0 0 200 200"
          className="w-full h-full"
          style={{
            filter: 'drop-shadow(0 4px 8px rgba(79, 70, 229, 0.3))'
          }}
        >
          {/* Blob body */}
          <path
            d={generateBlobPath()}
            fill="url(#blobGradient)"
            className="transition-all duration-300"
          />
          
          {/* Gradient definition */}
          <defs>
            <linearGradient id="blobGradient" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#A5B4FC" />
              <stop offset="50%" stopColor="#C7D2FE" />
              <stop offset="100%" stopColor="#E0E7FF" />
            </linearGradient>
          </defs>

          {/* Eyes (if evolved enough) */}
          {features.hasEyes && (
            <>
              <circle
                cx="85"
                cy="90"
                r="6"
                fill="#2D3748"
                className="animate-pulse"
              />
              <circle
                cx="115"
                cy="90"
                r="6"
                fill="#2D3748"
                className="animate-pulse"
                style={{ animationDelay: '0.5s' }}
              />
              <circle cx="87" cy="88" r="2" fill="white" />
              <circle cx="117" cy="88" r="2" fill="white" />
            </>
          )}

          {/* Expression (if evolved enough) */}
          {features.hasExpression && (
            <path
              d="M 90 110 Q 100 120 110 110"
              stroke="#2D3748"
              strokeWidth="3"
              fill="none"
              className="transition-all duration-300"
            />
          )}

          {/* Appendages (if evolved enough) */}
          {features.hasAppendages && (
            <>
              <ellipse
                cx="60"
                cy="120"
                rx="8"
                ry="15"
                fill="url(#blobGradient)"
                className="animate-bounce"
                style={{ animationDelay: '0.2s' }}
              />
              <ellipse
                cx="140"
                cy="120"
                rx="8"
                ry="15"
                fill="url(#blobGradient)"
                className="animate-bounce"
                style={{ animationDelay: '0.8s' }}
              />
            </>
          )}
        </svg>
      </div>

      {/* Pet's emoji message */}
      {displayMessage && (
        <div className="bg-indigo-100 rounded-2xl px-4 py-2 border border-indigo-200 shadow-md mb-4">
          <div className={`text-2xl ${isAnimating ? 'animate-bounce' : ''}`}>
            {displayMessage}
          </div>
        </div>
      )}

      {/* Pet name and status */}
      <div className="text-center">
        <h2 className="text-xl font-bold text-indigo-700 mb-1 font-sans">
          {petName || petData?.id || 'Blobby'}
        </h2>
        <p className="text-indigo-600 text-sm font-sans">
          {petData?.personality_summary || 'Getting to know you...'}
        </p>
      </div>

      {/* Interaction hints */}
      {!displayMessage && (
        <div className="text-center mt-4">
          <p className="text-slate-600 text-sm font-sans opacity-70">
            Say hello with emojis! 👋😊
          </p>
        </div>
      )}
    </div>
  )
} 