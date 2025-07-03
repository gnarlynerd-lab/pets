"use client"

import { useState } from 'react'
import { Button } from '@/components/ui/button'

interface EmojiInteractionProps {
  onSendEmoji: (emojiSequence: string) => void
  isLoading: boolean
}

// Emoji categories for easy selection
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
  },
  modifiers: {
    name: 'Modifiers',
    emojis: ['❓', '✨', '🔥', '💫', '⭐', '💨', '⚡', '🌟', '💝', '🎊']
  }
}

export default function EmojiInteraction({ onSendEmoji, isLoading }: EmojiInteractionProps) {
  const [selectedEmojis, setSelectedEmojis] = useState<string>('')
  const [activeCategory, setActiveCategory] = useState<keyof typeof EMOJI_CATEGORIES>('expressions')

  const handleEmojiClick = (emoji: string) => {
    setSelectedEmojis(prev => prev + emoji)
  }

  const handleSend = () => {
    if (selectedEmojis.trim()) {
      onSendEmoji(selectedEmojis)
      setSelectedEmojis('')
    }
  }

  const handleClear = () => {
    setSelectedEmojis('')
  }

  const handleBackspace = () => {
    setSelectedEmojis(prev => prev.slice(0, -1))
  }

  return (
    <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700">
      <h3 className="text-lg font-semibold text-white mb-4">Communicate with Emojis</h3>
      
      {/* Input display */}
      <div className="bg-slate-900/50 rounded-lg p-4 mb-4 min-h-[60px] flex items-center">
        <div className="text-2xl flex-1">
          {selectedEmojis || (
            <span className="text-slate-500 text-base">Select emojis to communicate...</span>
          )}
        </div>
        <div className="flex gap-2 ml-4">
          <Button
            variant="outline"
            size="sm"
            onClick={handleBackspace}
            disabled={!selectedEmojis}
            className="h-8 w-8 p-0"
          >
            ⌫
          </Button>
          <Button
            variant="outline"
            size="sm"
            onClick={handleClear}
            disabled={!selectedEmojis}
            className="h-8 px-3"
          >
            Clear
          </Button>
        </div>
      </div>

      {/* Category tabs */}
      <div className="flex gap-2 mb-4 overflow-x-auto">
        {Object.entries(EMOJI_CATEGORIES).map(([key, category]) => (
          <Button
            key={key}
            variant={activeCategory === key ? "default" : "outline"}
            size="sm"
            onClick={() => setActiveCategory(key as keyof typeof EMOJI_CATEGORIES)}
            className="whitespace-nowrap"
          >
            {category.name}
          </Button>
        ))}
      </div>

      {/* Emoji grid */}
      <div className="grid grid-cols-5 sm:grid-cols-10 gap-2 mb-6">
        {EMOJI_CATEGORIES[activeCategory].emojis.map((emoji) => (
          <Button
            key={emoji}
            variant="outline"
            className="aspect-square text-2xl p-0 hover:scale-110 transition-transform"
            onClick={() => handleEmojiClick(emoji)}
            disabled={isLoading}
          >
            {emoji}
          </Button>
        ))}
      </div>

      {/* Send button */}
      <div className="flex gap-3">
        <Button
          onClick={handleSend}
          disabled={!selectedEmojis.trim() || isLoading}
          className="flex-1 bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700"
        >
          {isLoading ? (
            <>
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
              Sending...
            </>
          ) : (
            'Send to Pet'
          )}
        </Button>
      </div>

      {/* Quick suggestions */}
      <div className="mt-4 pt-4 border-t border-slate-700">
        <p className="text-sm text-slate-400 mb-2">Quick suggestions:</p>
        <div className="flex flex-wrap gap-2">
          {['👋😊', '🍎😋', '🎮🎯', '❤️✨', '😴💤'].map((suggestion) => (
            <Button
              key={suggestion}
              variant="ghost"
              size="sm"
              onClick={() => setSelectedEmojis(suggestion)}
              disabled={isLoading}
              className="text-lg h-8"
            >
              {suggestion}
            </Button>
          ))}
        </div>
      </div>
    </div>
  )
}
