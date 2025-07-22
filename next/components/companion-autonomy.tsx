"use client"

import { useState, useEffect } from 'react'
import { Brain, Heart, Zap, Target } from 'lucide-react'

interface CompanionAutonomyProps {
  petData?: any
  interactionCount: number
}

export function CompanionAutonomy({ petData, interactionCount }: CompanionAutonomyProps) {
  const [isClient, setIsClient] = useState(false)
  const [autonomyLevel, setAutonomyLevel] = useState(0.5)
  const [currentGoal, setCurrentGoal] = useState('Exploring connections')
  const [personality, setPersonality] = useState('Curious')

  // Initialize client state
  useEffect(() => {
    setIsClient(true)
  }, [])

  useEffect(() => {
    if (!isClient || !petData) return
    
    if (petData) {
      // Calculate autonomy based on traits and interactions
      const traits = petData.traits || {}
      const openness = traits.openness || 0.5
      const consciousness = traits.conscientiousness || 0.5
      const curiosity = traits.curiosity || 0.5
      
      const baseAutonomy = (openness + consciousness + curiosity) / 3
      const interactionBonus = Math.min(interactionCount * 0.05, 0.3)
      setAutonomyLevel(Math.min(baseAutonomy + interactionBonus, 1.0))

      // Set personality description
      if (traits.playfulness > 0.7) {
        setPersonality('Playful Explorer')
        setCurrentGoal('Seeking fun interactions')
      } else if (traits.affection > 0.7) {
        setPersonality('Warm Companion')
        setCurrentGoal('Building deeper bonds')
      } else if (traits.curiosity > 0.7) {
        setPersonality('Curious Observer')
        setCurrentGoal('Learning about you')
      } else {
        setPersonality('Thoughtful Friend')
        setCurrentGoal('Finding balance')
      }
    }
  }, [petData, interactionCount, isClient])

  const getAutonomyColor = () => {
    if (autonomyLevel > 0.7) return 'text-emerald-600 bg-emerald-50'
    if (autonomyLevel > 0.4) return 'text-blue-600 bg-blue-50'
    return 'text-purple-600 bg-purple-50'
  }

  const getAutonomyLabel = () => {
    if (autonomyLevel > 0.7) return 'Highly Autonomous'
    if (autonomyLevel > 0.4) return 'Developing Agency'
    return 'Early Formation'
  }

  return (
    <div className="bg-white/90 backdrop-blur-sm rounded-xl p-4 border border-emerald-200 shadow-lg">
      <div className="flex items-center gap-2 mb-3">
        <div className={`p-1 rounded-full ${getAutonomyColor()}`}>
          <Brain className="w-4 h-4" />
        </div>
        <h3 className="text-lg font-semibold text-emerald-700 font-sans">
          Companion Agency
        </h3>
      </div>
      
      <div className="space-y-3">
        {/* Autonomy Level */}
        <div className="space-y-1">
          <div className="flex justify-between items-center">
            <span className="text-xs text-emerald-600 font-medium">Independence</span>
            <span className="text-xs text-emerald-500">{getAutonomyLabel()}</span>
          </div>
          <div className="w-full bg-emerald-100 rounded-full h-2">
            <div 
              className="bg-emerald-500 h-2 rounded-full transition-all duration-1000"
              style={{ width: `${autonomyLevel * 100}%` }}
            />
          </div>
        </div>

        {/* Current Status */}
        <div className="space-y-2">
          <div className="flex items-center gap-1">
            <Heart className="w-3 h-3 text-emerald-500" />
            <span className="text-xs text-emerald-600 font-medium">{personality}</span>
          </div>
          <div className="flex items-center gap-1">
            <Target className="w-3 h-3 text-emerald-500" />
            <span className="text-xs text-emerald-600">{currentGoal}</span>
          </div>
        </div>

        {/* Agency Indicators */}
        <div className="grid grid-cols-3 gap-2 pt-2 border-t border-emerald-100">
          <div className="text-center">
            <div className="text-xs text-emerald-500">Initiative</div>
            <div className="text-sm font-semibold text-emerald-600">
              {Math.round((petData?.traits?.conscientiousness || 0.5) * 100)}%
            </div>
          </div>
          <div className="text-center">
            <div className="text-xs text-emerald-500">Creativity</div>
            <div className="text-sm font-semibold text-emerald-600">
              {Math.round((petData?.traits?.openness || 0.5) * 100)}%
            </div>
          </div>
          <div className="text-center">
            <div className="text-xs text-emerald-500">Adaptability</div>
            <div className="text-sm font-semibold text-emerald-600">
              {Math.round(autonomyLevel * 100)}%
            </div>
          </div>
        </div>

        {/* Autonomous Behavior Hint */}
        {autonomyLevel > 0.6 && (
          <div className="mt-2 p-2 bg-emerald-50 rounded-lg">
            <p className="text-xs text-emerald-700">
              🌱 Your companion is developing their own preferences and may surprise you!
            </p>
          </div>
        )}
      </div>
    </div>
  )
}