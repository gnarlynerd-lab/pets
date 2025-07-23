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
    <div className="bg-gray-800 border border-gray-700 p-4 font-mono">
      <h3 className="text-sm font-bold text-green-400 mb-3">[INPUT] Emoji Communication Module</h3>
      
      {/* Input and Send Area */}
      <div className="flex flex-col sm:flex-row items-stretch gap-2 mb-3">
        {/* Input display */}
        <div className="flex-1 bg-black border border-gray-600 p-3 min-h-[50px] flex items-center font-mono">
          <div className="text-xl flex-1">
            {selectedEmojis || (
              <span className="text-gray-500 text-xs">$ awaiting_input...</span>
            )}
          </div>
          <div className="flex gap-1 ml-2">
            <Button
              variant="ghost"
              size="sm"
              onClick={handleBackspace}
              disabled={!selectedEmojis}
              className="h-7 w-7 p-0 text-green-400 hover:bg-gray-700 border border-gray-600"
            >
              ⌫
            </Button>
            <Button
              variant="ghost"
              size="sm"
              onClick={handleClear}
              disabled={!selectedEmojis}
              className="h-7 px-3 text-green-400 hover:bg-gray-700 text-xs font-mono border border-gray-600"
            >
              Clear
            </Button>
          </div>
        </div>

        {/* Send button */}
        <Button
          onClick={handleSend}
          disabled={!selectedEmojis.trim() || isLoading}
          className="bg-green-600 hover:bg-green-500 text-black px-8 h-[50px] font-bold border border-green-400 transition-colors duration-200"
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
          className="border-gray-600 bg-gray-700 text-gray-300 hover:bg-gray-600 hover:text-green-400 font-mono"
        >
          {showEmojiPicker ? 'Hide' : 'Show'} Emoji Picker
        </Button>
        
        {/* Quick access emoji row */}
        <div className="flex gap-1 overflow-x-auto flex-1">
          {['👋', '😊', '❤️', '🍎', '🎮', '✨', '👍', '🎉'].map((emoji) => (
            <Button
              key={emoji}
              variant="ghost"
              className="aspect-square text-lg p-1 text-gray-300 hover:bg-gray-700 hover:text-green-400 transition-colors duration-200 flex-shrink-0 border border-gray-600 bg-gray-800"
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
        <div className="space-y-4 border-t border-gray-600 pt-4">
          {/* Category tabs */}
          <div className="flex gap-1 overflow-x-auto">
            {Object.entries(EMOJI_CATEGORIES).map(([key, category]) => (
              <Button
                key={key}
                variant={activeCategory === key ? "default" : "outline"}
                size="sm"
                onClick={() => setActiveCategory(key as keyof typeof EMOJI_CATEGORIES)}
                className={`whitespace-nowrap text-sm flex-shrink-0 font-mono ${
                  activeCategory === key 
                    ? 'bg-green-600 text-black border-green-400' 
                    : 'border-gray-600 bg-gray-700 text-gray-300 hover:bg-gray-600 hover:text-green-400'
                }`}
              >
                {category.name}
              </Button>
            ))}
          </div>

          {/* Emoji grid */}
          <div className="grid grid-cols-6 gap-2 max-h-32 overflow-y-auto scrollbar-thin scrollbar-thumb-gray-600 scrollbar-track-gray-800">
            {EMOJI_CATEGORIES[activeCategory].emojis.map((emoji) => (
              <Button
                key={emoji}
                variant="ghost"
                className="aspect-square text-lg p-0 text-gray-300 hover:bg-gray-700 hover:text-green-400 transition-colors duration-200 border border-gray-600 bg-gray-800"
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
      <div className="mt-4 pt-4 border-t border-gray-600">
        <p className="text-xs text-green-400 mb-3 font-mono">[SUGGESTIONS]</p>
        <div className="flex flex-wrap gap-2">
          {['👋😊', '🍎😋', '🎮🎯', '❤️✨', '😴💤'].map((suggestion) => (
            <Button
              key={suggestion}
              variant="ghost"
              size="sm"
              onClick={() => setSelectedEmojis(suggestion)}
              disabled={isLoading}
              className="text-lg h-10 px-3 text-gray-300 hover:bg-gray-700 hover:text-green-400 border border-gray-600 bg-gray-800 transition-colors duration-200"
            >
              {suggestion}
            </Button>
          ))}
        </div>
      </div>
    </div>
  )
}
