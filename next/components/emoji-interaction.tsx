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
  const [showEmojiPicker, setShowEmojiPicker] = useState(false)

  const handleEmojiClick = (emoji: string) => {
    setSelectedEmojis(prev => prev + emoji)
  }

  const handleSend = () => {
    if (selectedEmojis.trim()) {
      onSendEmoji(selectedEmojis)
      setSelectedEmojis('')
      setShowEmojiPicker(false)
    }
  }

  const handleClear = () => {
    setSelectedEmojis('')
  }

  const handleBackspace = () => {
    setSelectedEmojis(prev => prev.slice(0, -1))
  }

  return (
    <div className="bg-white/90 backdrop-blur-sm rounded-xl p-4 border border-pink-200 shadow-lg">
      <h3 className="text-lg font-semibold text-pink-700 mb-3 font-sans">Communicate with Emojis</h3>
      
      {/* Input and Send Area */}
      <div className="flex flex-col sm:flex-row items-stretch gap-2 mb-3">
        {/* Input display */}
        <div className="flex-1 bg-pink-50/70 rounded-lg p-3 min-h-[50px] flex items-center border border-pink-200">
          <div className="text-xl flex-1">
            {selectedEmojis || (
              <span className="text-pink-400 text-sm">Select emojis to communicate...</span>
            )}
          </div>
          <div className="flex gap-1 ml-2">
            <Button
              variant="ghost"
              size="sm"
              onClick={handleBackspace}
              disabled={!selectedEmojis}
              className="h-7 w-7 p-0 text-pink-600 hover:bg-pink-100"
            >
              ⌫
            </Button>
            <Button
              variant="ghost"
              size="sm"
              onClick={handleClear}
              disabled={!selectedEmojis}
              className="h-7 px-2 text-pink-600 hover:bg-pink-100 text-xs"
            >
              Clear
            </Button>
          </div>
        </div>

        {/* Send button */}
        <Button
          onClick={handleSend}
          disabled={!selectedEmojis.trim() || isLoading}
          className="bg-gradient-to-r from-pink-500 to-purple-600 hover:from-pink-600 hover:to-purple-700 text-white px-6 h-[50px]"
        >
          {isLoading ? (
            <>
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
              Sending...
            </>
          ) : (
            'Send'
          )}
        </Button>
      </div>

      {/* Emoji Picker Toggle */}
      <div className="flex gap-2 mb-3">
        <Button
          variant="outline"
          size="sm"
          onClick={() => setShowEmojiPicker(!showEmojiPicker)}
          className="border-pink-200 text-pink-600 hover:bg-pink-50"
        >
          {showEmojiPicker ? 'Hide' : 'Show'} Emoji Picker
        </Button>
        
        {/* Quick access emoji row */}
        <div className="flex gap-1 overflow-x-auto flex-1">
          {['👋', '😊', '❤️', '🍎', '🎮', '✨', '👍', '🎉'].map((emoji) => (
            <Button
              key={emoji}
              variant="ghost"
              className="aspect-square text-lg p-1 text-pink-600 hover:bg-pink-50 hover:scale-110 transition-transform flex-shrink-0 border border-pink-100"
              onClick={() => handleEmojiClick(emoji)}
              disabled={isLoading}
            >
              {emoji}
            </Button>
          ))}
        </div>
      </div>

      {/* Collapsible Emoji Picker */}
      {showEmojiPicker && (
        <div className="space-y-3 border-t border-pink-200 pt-3">
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
                    ? 'bg-pink-500 hover:bg-pink-600' 
                    : 'border-pink-200 text-pink-600 hover:bg-pink-50'
                }`}
              >
                {category.name}
              </Button>
            ))}
          </div>

          {/* Emoji grid */}
          <div className="grid grid-cols-6 gap-1 max-h-32 overflow-y-auto scrollbar-thin scrollbar-thumb-pink-300 scrollbar-track-pink-100">
            {EMOJI_CATEGORIES[activeCategory].emojis.map((emoji) => (
              <Button
                key={emoji}
                variant="ghost"
                className="aspect-square text-lg p-0 text-pink-600 hover:bg-pink-50 hover:scale-110 transition-transform border border-pink-100"
                onClick={() => handleEmojiClick(emoji)}
                disabled={isLoading}
              >
                {emoji}
              </Button>
            ))}
          </div>
        </div>
      )}

      {/* Quick suggestions */}
      <div className="mt-3 pt-3 border-t border-pink-200">
        <p className="text-sm text-pink-600 mb-2 font-sans">Quick suggestions:</p>
        <div className="flex flex-wrap gap-2">
          {['👋😊', '🍎😋', '🎮🎯', '❤️✨', '😴💤'].map((suggestion) => (
            <Button
              key={suggestion}
              variant="ghost"
              size="sm"
              onClick={() => setSelectedEmojis(suggestion)}
              disabled={isLoading}
              className="text-lg h-8 text-pink-600 hover:bg-pink-50 border border-pink-200"
            >
              {suggestion}
            </Button>
          ))}
        </div>
      </div>
    </div>
  )
}
