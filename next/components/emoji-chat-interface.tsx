"use client"

import { useState, useRef, useEffect } from 'react'
import { Button } from '@/components/ui/button'

interface InteractionHistory {
  userEmojis: string
  petResponse: string
  timestamp?: string | number
}

interface EmojiChatInterfaceProps {
  onSendEmoji: (emojiSequence: string) => void
  isLoading: boolean
  interactionHistory: InteractionHistory[]
  petName?: string
  onPetNameChange?: (name: string) => void
}

// Simplified emoji categories
const EMOJI_CATEGORIES = {
  expressions: {
    name: 'Expressions',
    emojis: ['😊', '😔', '😴', '🤔', '😋', '😆', '😍', '🥰', '😌', '😎']
  },
  needs: {
    name: 'Needs',
    emojis: ['🍎', '🍕', '🎮', '💤', '🤗', '🚿', '🎯', '⚽', '📚', '🎵']
  },
  responses: {
    name: 'Responses',
    emojis: ['❤️', '👍', '👎', '❓', '✨', '🎉', '💔', '😤', '🙏', '👋']
  }
}

export default function EmojiChatInterface({ 
  onSendEmoji, 
  isLoading, 
  interactionHistory,
  petName,
  onPetNameChange
}: EmojiChatInterfaceProps) {
  const [activeCategory, setActiveCategory] = useState<keyof typeof EMOJI_CATEGORIES>('expressions')
  const [isEditingName, setIsEditingName] = useState(false)
  const [tempPetName, setTempPetName] = useState(petName || '')
  const chatEndRef = useRef<HTMLDivElement>(null)
  const chatContainerRef = useRef<HTMLDivElement>(null)

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    if (chatEndRef.current) {
      chatEndRef.current.scrollIntoView({ behavior: 'smooth' })
    }
  }, [interactionHistory])

  // Keep scroll position when component re-renders
  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight
    }
  }, [interactionHistory])

  const handleEmojiClick = (emoji: string) => {
    // Send emoji immediately when clicked
    if (!isLoading) {
      onSendEmoji(emoji)
    }
  }

  const handleNameSave = () => {
    if (onPetNameChange && tempPetName.trim()) {
      onPetNameChange(tempPetName.trim())
    }
    setIsEditingName(false)
  }

  const handleNameCancel = () => {
    setTempPetName(petName || '')
    setIsEditingName(false)
  }

  return (
    <div className="bg-white/90 backdrop-blur-sm rounded-3xl shadow-lg border-2 border-indigo-200 p-6">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        {/* Chat History Panel */}
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-semibold text-slate-600 font-sans">Chat History</h3>
            
            {/* Pet Name Editor */}
            <div className="flex items-center gap-2">
              {isEditingName ? (
                <>
                  <input
                    type="text"
                    value={tempPetName}
                    onChange={(e) => setTempPetName(e.target.value)}
                    className="text-sm px-2 py-1 border border-indigo-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                    placeholder="Pet name..."
                    maxLength={20}
                  />
                  <Button
                    size="sm"
                    onClick={handleNameSave}
                    className="bg-gradient-to-r from-indigo-500 to-indigo-600 hover:from-indigo-600 hover:to-indigo-700 text-white text-xs px-2 py-1"
                  >
                    Save
                  </Button>
                  <Button
                    size="sm"
                    variant="outline"
                    onClick={handleNameCancel}
                    className="border-indigo-300 text-slate-600 text-xs px-2 py-1"
                  >
                    Cancel
                  </Button>
                </>
              ) : (
                <Button
                  size="sm"
                  variant="ghost"
                  onClick={() => setIsEditingName(true)}
                  className="text-slate-600 hover:bg-indigo-50 text-xs"
                >
                  {petName ? `Name: ${petName}` : 'Name Pet'}
                </Button>
              )}
            </div>
          </div>
          
          <div 
            ref={chatContainerRef}
            className="bg-indigo-50/70 rounded-2xl p-4 h-64 overflow-y-auto space-y-3 scrollbar-thin scrollbar-thumb-indigo-300 scrollbar-track-indigo-100"
          >
            {interactionHistory.length === 0 ? (
              <div className="text-center text-slate-600 text-sm font-sans py-8">
                No conversations yet. Start chatting! 👋
              </div>
            ) : (
              <>
                {interactionHistory.slice(-20).reverse().map((interaction, index) => (
                  <div key={`${interaction.timestamp || index}-${index}`} className="space-y-2">
                    {/* User message */}
                    <div className="flex justify-end">
                      <div className="bg-indigo-100 rounded-2xl px-3 py-2 max-w-xs shadow-sm">
                        <div className="text-lg">{interaction.userEmojis}</div>
                        <div className="text-xs text-indigo-600 mt-1">You</div>
                      </div>
                    </div>
                    
                    {/* Pet response */}
                    <div className="flex justify-start">
                      <div className="bg-slate-500 rounded-2xl px-3 py-2 max-w-xs shadow-sm">
                        <div className="text-lg">{interaction.petResponse}</div>
                        <div className="text-xs text-slate-600 mt-1">{petName || 'Pet'}</div>
                      </div>
                    </div>
                  </div>
                ))}
                <div ref={chatEndRef} />
              </>
            )}
          </div>
        </div>

        {/* Emoji Selection Interface */}
        <div className="space-y-4">
          <h3 className="text-lg font-semibold text-slate-600 font-sans">Click to Send Emoji</h3>
          
          {/* Quick access emoji row */}
          <div className="flex gap-1 overflow-x-auto pb-2">
            {['👋', '😊', '❤️', '🍎', '🎮', '✨', '👍', '🎉'].map((emoji) => (
              <Button
                key={emoji}
                variant="outline"
                className="aspect-square text-lg p-1 border-indigo-200 text-slate-600 hover:bg-indigo-50 hover:scale-110 transition-transform flex-shrink-0"
                onClick={() => handleEmojiClick(emoji)}
                disabled={isLoading}
              >
                {emoji}
              </Button>
            ))}
          </div>

          {/* Category tabs */}
          <div className="flex gap-1 overflow-x-auto">
            {Object.entries(EMOJI_CATEGORIES).map(([key, category]) => (
              <Button
                key={key}
                variant={activeCategory === key ? "default" : "outline"}
                size="sm"
                onClick={() => setActiveCategory(key as keyof typeof EMOJI_CATEGORIES)}
                className={`whitespace-nowrap text-xs flex-shrink-0 ${
                  activeCategory === key 
                    ? 'bg-gradient-to-r from-indigo-500 to-indigo-600 hover:from-indigo-600 hover:to-indigo-700' 
                    : 'border-indigo-200 text-slate-600 hover:bg-indigo-50'
                }`}
              >
                {category.name}
              </Button>
            ))}
          </div>

          {/* Emoji grid */}
          <div className="grid grid-cols-6 gap-1 max-h-32 overflow-y-auto scrollbar-thin scrollbar-thumb-indigo-300 scrollbar-track-indigo-100">
            {EMOJI_CATEGORIES[activeCategory].emojis.map((emoji) => (
              <Button
                key={emoji}
                variant="outline"
                className="aspect-square text-lg p-0 border-indigo-200 text-slate-600 hover:bg-indigo-50 hover:scale-110 transition-transform"
                onClick={() => handleEmojiClick(emoji)}
                disabled={isLoading}
              >
                {emoji}
              </Button>
            ))}
          </div>

          {/* Status indicator */}
          <div className="text-center">
            {isLoading ? (
              <div className="flex items-center justify-center text-slate-600 text-sm">
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-indigo-600 mr-2"></div>
                Pet is thinking...
              </div>
            ) : (
              <div className="text-slate-600 text-sm font-sans">
                Click any emoji to send it to your pet
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
} 