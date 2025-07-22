"use client"

import { useState } from 'react'
import { X } from 'lucide-react'

interface SaveCompanionBannerProps {
  onSignIn: () => void
  petName?: string
  interactionCount: number
}

export function SaveCompanionBanner({ onSignIn, petName, interactionCount }: SaveCompanionBannerProps) {
  const [isDismissed, setIsDismissed] = useState(false)

  // Only show after 3 interactions and if not dismissed
  if (interactionCount < 3 || isDismissed) {
    return null
  }

  return (
    <div className="fixed bottom-4 left-4 right-4 max-w-md mx-auto animate-slide-up">
      <div className="bg-gradient-to-r from-purple-600 to-pink-600 rounded-2xl shadow-xl p-4 text-white">
        <button
          onClick={() => setIsDismissed(true)}
          className="absolute top-2 right-2 text-white/70 hover:text-white"
          aria-label="Dismiss"
        >
          <X className="w-4 h-4" />
        </button>
        
        <div className="pr-6">
          <h3 className="font-bold text-lg mb-1">
            {petName ? `Save ${petName}!` : 'Save Your Companion!'}
          </h3>
          <p className="text-sm text-white/90 mb-3">
            Your companion is learning about you! Sign up to continue your journey together across devices.
          </p>
          
          <div className="flex items-center gap-3">
            <button
              onClick={onSignIn}
              className="bg-white text-purple-600 px-4 py-2 rounded-lg font-semibold text-sm hover:bg-white/90 transition-colors"
            >
              Sign Up Free
            </button>
            <span className="text-xs text-white/70">
              No credit card required
            </span>
          </div>
        </div>
      </div>
    </div>
  )
}