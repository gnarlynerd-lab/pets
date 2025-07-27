"use client"

import { useState, useEffect, useRef } from 'react'
import { useAuthenticatedPetState } from '@/hooks/use-authenticated-pet-state'
import { VersionNav } from '@/components/version-nav'

export default function MinimalHome() {
  const {
    petData,
    isLoading,
    sendEmojiInteraction,
    petResponse,
    interactionHistory,
    petName,
  } = useAuthenticatedPetState()

  const [currentEmoji, setCurrentEmoji] = useState('')
  const chatContainerRef = useRef<HTMLDivElement>(null)

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    setTimeout(() => {
      if (chatContainerRef.current) {
        chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight
      }
    }, 100)
  }, [interactionHistory])

  const handleEmojiSend = () => {
    if (currentEmoji.trim()) {
      sendEmojiInteraction(currentEmoji.trim())
      setCurrentEmoji('')
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleEmojiSend()
    }
  }

  const quickEmojis = ['👋', '❤️', '😊', '🤔', '👍', '😴', '🍎', '🎮']
  const companionName = petName || 'Companion'

  return (
    <div className="min-h-screen bg-white text-black font-mono">
      <VersionNav />
      <div className="max-w-4xl mx-auto p-8">
        
        {/* Header */}
        <div className="border-b border-black pb-4 mb-8">
          <h1 className="text-2xl font-bold tracking-tight">
            {petName || 'Digital Companion'}
          </h1>
          <p className="text-sm text-gray-600 mt-1">
            Interactive communication system
          </p>
        </div>

        {/* Main Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-12">
          
          {/* Left: Companion Display */}
          <div className="space-y-6">
            {/* Companion Visual */}
            <div className="border border-black p-8 h-64 flex items-center justify-center">
              <div className="text-center">
                <div className="text-6xl mb-4">
                  {petResponse?.split('').slice(-1)[0] || '●'}
                </div>
                <div className="text-sm">
                  {isLoading ? 'Thinking...' : 'Ready'}
                </div>
              </div>
            </div>

            {/* Status */}
            <div className="border border-black p-4 space-y-2 text-sm">
              <div className="grid grid-cols-2 gap-4">
                <div>Energy: {Math.round(petData?.energy || 0)}%</div>
                <div>Mood: {Math.round(petData?.mood || 0)}%</div>
                <div>Health: {Math.round(petData?.health || 0)}%</div>
                <div>Attention: {Math.round(petData?.attention || 0)}%</div>
              </div>
            </div>
          </div>

          {/* Right: Communication */}
          <div className="space-y-6">
            
            {/* Conversation */}
            <div className="border border-black h-64 overflow-hidden">
              <div className="border-b border-black p-2 text-sm font-bold">
                Conversation
              </div>
              <div 
                ref={chatContainerRef}
                className="p-4 h-48 overflow-y-auto space-y-3 text-sm"
              >
                {interactionHistory.length === 0 ? (
                  <div className="text-gray-600 italic">
                    Start a conversation...
                  </div>
                ) : (
                  interactionHistory.slice(-10).map((interaction, index) => (
                    <div key={index} className="space-y-1">
                      <div className="flex">
                        <span className="w-8 text-right mr-2">You:</span>
                        <span>{interaction.userEmojis}</span>
                      </div>
                      <div className="flex">
                        <span className="w-8 text-right mr-2">{companionName}:</span>
                        <span>{interaction.petResponse}</span>
                      </div>
                    </div>
                  ))
                )}
              </div>
            </div>

            {/* Input */}
            <div className="space-y-4">
              <div className="border border-black">
                <input
                  type="text"
                  value={currentEmoji}
                  onChange={(e) => setCurrentEmoji(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="Type emojis here..."
                  className="w-full p-4 text-lg font-mono bg-white border-none outline-none"
                  disabled={isLoading}
                />
              </div>
              
              <div className="flex gap-2 justify-between">
                <div className="flex gap-1 flex-wrap">
                  {quickEmojis.map((emoji) => (
                    <button
                      key={emoji}
                      onClick={() => setCurrentEmoji(prev => prev + emoji)}
                      className="w-10 h-10 border border-black hover:bg-black hover:text-white transition-colors text-lg"
                      disabled={isLoading}
                    >
                      {emoji}
                    </button>
                  ))}
                </div>
                
                <button
                  onClick={handleEmojiSend}
                  disabled={!currentEmoji.trim() || isLoading}
                  className="px-6 py-2 border border-black hover:bg-black hover:text-white transition-colors disabled:opacity-50 disabled:cursor-not-allowed font-bold"
                >
                  Send
                </button>
              </div>
            </div>

            {/* Stats */}
            <div className="border border-black p-4 text-xs space-y-2">
              <div>Total interactions: {interactionHistory.length}</div>
              <div>Session: Anonymous</div>
              <div>Connection: Active</div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="border-t border-black pt-4 mt-12 text-center">
          <div 
            className="text-xl font-bold tracking-wider mb-2"
            style={{ 
              fontFamily: 'Inter, "Helvetica Neue", Arial, sans-serif',
              fontWeight: 700,
              letterSpacing: '2px',
              color: '#006666'
            }}
          >
            AFFINITY
          </div>
          <div className="text-xs text-gray-600">
            Minimal Interface
          </div>
        </div>
      </div>
    </div>
  )
}