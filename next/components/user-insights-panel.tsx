"use client"

import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'

interface UserInsights {
  profile?: {
    personality?: {
      dominant_style?: string
      confidence_level?: number
    }
    relationship?: {
      phase?: string
      trust?: number
      familiarity?: number
      affection?: number
    }
    memory?: {
      recent_interactions?: number
      favorite_activities?: Array<[string, number]>
    }
    insights?: {
      user_style?: string
      relationship_phase?: string
      trust_level?: number
      familiarity_level?: number
    }
  }
  prediction?: {
    likely_need?: string
    confidence?: number
    suggested_response?: string
  }
  adaptation_suggestions?: string[]
}

interface UserInsightsPanelProps {
  petId: string
  userId: string
  userInsights?: UserInsights
  onRefresh?: () => void
}

export default function UserInsightsPanel({ 
  petId, 
  userId, 
  userInsights, 
  onRefresh 
}: UserInsightsPanelProps) {
  const [isExpanded, setIsExpanded] = useState(false)
  const [isLoading, setIsLoading] = useState(false)

  const formatPercentage = (value: number) => `${Math.round(value * 100)}%`
  const formatPhase = (phase: string) => phase.charAt(0).toUpperCase() + phase.slice(1)

  const getRelationshipColor = (value: number) => {
    if (value > 0.7) return 'text-green-600'
    if (value > 0.4) return 'text-yellow-600'
    return 'text-red-600'
  }

  const getPhaseColor = (phase: string) => {
    switch (phase) {
      case 'maturity': return 'text-green-600'
      case 'development': return 'text-blue-600'
      case 'formation': return 'text-purple-600'
      case 'adaptation': return 'text-orange-600'
      default: return 'text-gray-600'
    }
  }

  const getStyleColor = (style: string) => {
    switch (style) {
      case 'playful': return 'text-blue-600'
      case 'nurturing': return 'text-green-600'
      case 'serious': return 'text-purple-600'
      case 'gentle': return 'text-pink-600'
      case 'distant': return 'text-gray-600'
      default: return 'text-gray-600'
    }
  }

  return (
    <div className="bg-white/90 backdrop-blur-sm rounded-xl p-4 border border-pink-200 shadow-lg">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-lg font-semibold text-pink-700 font-sans">
          Relationship Insights
        </h3>
        <div className="flex gap-2">
          <Button
            variant="outline"
            size="sm"
            onClick={() => setIsExpanded(!isExpanded)}
            className="border-pink-200 text-pink-600 hover:bg-pink-50"
          >
            {isExpanded ? 'Hide' : 'Show'} Details
          </Button>
          {onRefresh && (
            <Button
              variant="outline"
              size="sm"
              onClick={onRefresh}
              disabled={isLoading}
              className="border-pink-200 text-pink-600 hover:bg-pink-50"
            >
              {isLoading ? '...' : '↻'}
            </Button>
          )}
        </div>
      </div>

      {userInsights ? (
        <div className="space-y-3">
          {/* Quick Summary */}
          <div className="grid grid-cols-2 gap-3 text-sm">
            {userInsights.profile?.personality?.dominant_style && (
              <div className="bg-pink-50 rounded-lg p-2">
                <div className="text-pink-600 font-medium">Style</div>
                <div className={getStyleColor(userInsights.profile.personality.dominant_style)}>
                  {userInsights.profile.personality.dominant_style}
                </div>
              </div>
            )}
            
            {userInsights.profile?.relationship?.phase && (
              <div className="bg-pink-50 rounded-lg p-2">
                <div className="text-pink-600 font-medium">Phase</div>
                <div className={getPhaseColor(userInsights.profile.relationship.phase)}>
                  {formatPhase(userInsights.profile.relationship.phase)}
                </div>
              </div>
            )}
            
            {userInsights.profile?.relationship?.trust !== undefined && (
              <div className="bg-pink-50 rounded-lg p-2">
                <div className="text-pink-600 font-medium">Trust</div>
                <div className={getRelationshipColor(userInsights.profile.relationship.trust)}>
                  {formatPercentage(userInsights.profile.relationship.trust)}
                </div>
              </div>
            )}
            
            {userInsights.profile?.relationship?.familiarity !== undefined && (
              <div className="bg-pink-50 rounded-lg p-2">
                <div className="text-pink-600 font-medium">Familiarity</div>
                <div className={getRelationshipColor(userInsights.profile.relationship.familiarity)}>
                  {formatPercentage(userInsights.profile.relationship.familiarity)}
                </div>
              </div>
            )}
          </div>

          {/* Expanded Details */}
          {isExpanded && (
            <div className="space-y-4 pt-3 border-t border-pink-200">
              {/* Personality Insights */}
              {userInsights.profile?.personality && (
                <div>
                  <h4 className="text-sm font-semibold text-pink-700 mb-2">Personality</h4>
                  <div className="bg-pink-50 rounded-lg p-3 space-y-2">
                    <div className="flex justify-between">
                      <span className="text-sm text-pink-600">Dominant Style:</span>
                      <span className={getStyleColor(userInsights.profile.personality.dominant_style || '')}>
                        {userInsights.profile.personality.dominant_style}
                      </span>
                    </div>
                    {userInsights.profile.personality.confidence_level !== undefined && (
                      <div className="flex justify-between">
                        <span className="text-sm text-pink-600">Confidence:</span>
                        <span className="text-sm text-gray-700">
                          {formatPercentage(userInsights.profile.personality.confidence_level)}
                        </span>
                      </div>
                    )}
                  </div>
                </div>
              )}

              {/* Relationship Details */}
              {userInsights.profile?.relationship && (
                <div>
                  <h4 className="text-sm font-semibold text-pink-700 mb-2">Relationship</h4>
                  <div className="bg-pink-50 rounded-lg p-3 space-y-2">
                    <div className="flex justify-between">
                      <span className="text-sm text-pink-600">Phase:</span>
                      <span className={getPhaseColor(userInsights.profile.relationship.phase || '')}>
                        {formatPhase(userInsights.profile.relationship.phase || '')}
                      </span>
                    </div>
                    {userInsights.profile.relationship.trust !== undefined && (
                      <div className="flex justify-between">
                        <span className="text-sm text-pink-600">Trust:</span>
                        <span className={getRelationshipColor(userInsights.profile.relationship.trust)}>
                          {formatPercentage(userInsights.profile.relationship.trust)}
                        </span>
                      </div>
                    )}
                    {userInsights.profile.relationship.affection !== undefined && (
                      <div className="flex justify-between">
                        <span className="text-sm text-pink-600">Affection:</span>
                        <span className={getRelationshipColor(userInsights.profile.relationship.affection)}>
                          {formatPercentage(userInsights.profile.relationship.affection)}
                        </span>
                      </div>
                    )}
                  </div>
                </div>
              )}

              {/* Memory Insights */}
              {userInsights.profile?.memory && (
                <div>
                  <h4 className="text-sm font-semibold text-pink-700 mb-2">Memory</h4>
                  <div className="bg-pink-50 rounded-lg p-3 space-y-2">
                    {userInsights.profile.memory.recent_interactions !== undefined && (
                      <div className="flex justify-between">
                        <span className="text-sm text-pink-600">Recent Interactions:</span>
                        <span className="text-sm text-gray-700">
                          {userInsights.profile.memory.recent_interactions}
                        </span>
                      </div>
                    )}
                    {userInsights.profile.memory.favorite_activities && userInsights.profile.memory.favorite_activities.length > 0 && (
                      <div>
                        <span className="text-sm text-pink-600">Favorite Activity:</span>
                        <div className="text-sm text-gray-700 mt-1">
                          {userInsights.profile.memory.favorite_activities[0][0]} ({userInsights.profile.memory.favorite_activities[0][1]} times)
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              )}

              {/* Predictions */}
              {userInsights.prediction && (
                <div>
                  <h4 className="text-sm font-semibold text-pink-700 mb-2">Predictions</h4>
                  <div className="bg-pink-50 rounded-lg p-3 space-y-2">
                    <div className="flex justify-between">
                      <span className="text-sm text-pink-600">Likely Need:</span>
                      <span className="text-sm text-gray-700 capitalize">
                        {userInsights.prediction.likely_need}
                      </span>
                    </div>
                    {userInsights.prediction.confidence !== undefined && (
                      <div className="flex justify-between">
                        <span className="text-sm text-pink-600">Confidence:</span>
                        <span className="text-sm text-gray-700">
                          {formatPercentage(userInsights.prediction.confidence)}
                        </span>
                      </div>
                    )}
                    {userInsights.prediction.suggested_response && (
                      <div className="flex justify-between">
                        <span className="text-sm text-pink-600">Suggested Response:</span>
                        <span className="text-sm text-gray-700 capitalize">
                          {userInsights.prediction.suggested_response}
                        </span>
                      </div>
                    )}
                  </div>
                </div>
              )}

              {/* Adaptation Suggestions */}
              {userInsights.adaptation_suggestions && userInsights.adaptation_suggestions.length > 0 && (
                <div>
                  <h4 className="text-sm font-semibold text-pink-700 mb-2">Adaptation Suggestions</h4>
                  <div className="bg-pink-50 rounded-lg p-3">
                    <ul className="space-y-1">
                      {userInsights.adaptation_suggestions.map((suggestion, index) => (
                        <li key={index} className="text-sm text-gray-700 flex items-start">
                          <span className="text-pink-500 mr-2">•</span>
                          {suggestion}
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      ) : (
        <div className="text-center text-pink-600 text-sm py-4">
          No relationship data available yet. Start chatting to build a relationship! 💕
        </div>
      )}
    </div>
  )
} 