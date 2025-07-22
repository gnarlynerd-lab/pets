"use client"

import { Sparkles, Shield, Clock } from 'lucide-react'

interface SessionInfoProps {
  isAuthenticated: boolean
  sessionId?: string | null
  petName?: string
  interactionCount: number
  onSignIn: () => void
}

export function SessionInfo({ 
  isAuthenticated, 
  sessionId, 
  petName, 
  interactionCount,
  onSignIn 
}: SessionInfoProps) {
  if (isAuthenticated) {
    return (
      <div className="bg-gradient-to-r from-green-50 to-emerald-50 rounded-xl p-3 border border-green-200">
        <div className="flex items-center gap-2">
          <Shield className="w-4 h-4 text-green-600" />
          <div className="flex-1">
            <p className="text-sm font-semibold text-green-700">Saved Progress</p>
            <p className="text-xs text-green-600">Your companion is safe across all devices</p>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="bg-gradient-to-r from-amber-50 to-orange-50 rounded-xl p-3 border border-orange-200">
      <div className="flex items-center gap-2">
        <Sparkles className="w-4 h-4 text-orange-600" />
        <div className="flex-1">
          <p className="text-sm font-semibold text-orange-700">Guest Session</p>
          <p className="text-xs text-orange-600">
            {interactionCount > 0 
              ? `${interactionCount} interaction${interactionCount !== 1 ? 's' : ''} with ${petName || 'your companion'}`
              : 'Start chatting to build a relationship!'
            }
          </p>
        </div>
        {interactionCount > 0 && (
          <button
            onClick={onSignIn}
            className="text-xs bg-orange-500 hover:bg-orange-600 text-white px-3 py-1.5 rounded-md font-medium transition-colors"
          >
            Save Progress
          </button>
        )}
      </div>
      
      {sessionId && (
        <div className="mt-2 flex items-center gap-1 text-xs text-orange-600/70">
          <Clock className="w-3 h-3" />
          <span>Session active in this browser</span>
        </div>
      )}
    </div>
  )
}