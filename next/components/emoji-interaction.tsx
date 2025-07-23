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
    <div className="bg-white/95 backdrop-blur-sm rounded-2xl p-6 border border-slate-200/50 shadow-xl hover:shadow-2xl transition-all duration-300">
      <h3 className="text-xl font-semibold text-indigo-700 mb-4 font-sans">Communicate with Emojis</h3>
      
      {/* Input and Send Area */}
      <div className="flex flex-col sm:flex-row items-stretch gap-2 mb-3">
        {/* Input display */}
        <div className="flex-1 bg-slate-50/70 rounded-lg p-4 min-h-[50px] flex items-center border border-slate-200/30 shadow-inner">
          <div className="text-xl flex-1">
            {selectedEmojis || (
              <span className="text-slate-400 text-sm">Select emojis to communicate...</span>
            )}
          </div>
          <div className="flex gap-1 ml-2">
            <Button
              variant="ghost"
              size="sm"
              onClick={handleBackspace}
              disabled={!selectedEmojis}
              className="h-7 w-7 p-0 text-slate-600 hover:bg-slate-100"
            >
              ⌫
            </Button>
            <Button
              variant="ghost"
              size="sm"
              onClick={handleClear}
              disabled={!selectedEmojis}
              className="h-7 px-3 text-slate-600 hover:bg-slate-100 text-xs font-medium"
            >
              Clear
            </Button>
          </div>
        </div>

        {/* Send button */}
        <Button
          onClick={handleSend}
          disabled={!selectedEmojis.trim() || isLoading}
          className="bg-gradient-to-r from-indigo-500 to-indigo-600 hover:from-indigo-600 hover:to-indigo-700 text-white px-8 h-[50px] font-medium shadow-lg hover:shadow-xl transition-all duration-200 transform hover:-translate-y-0.5 active:translate-y-0"
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
          className="border-slate-200 text-slate-600 hover:bg-slate-50"
        >
          {showEmojiPicker ? 'Hide' : 'Show'} Emoji Picker
        </Button>
        
        {/* Quick access emoji row */}
        <div className="flex gap-1 overflow-x-auto flex-1">
          {['👋', '😊', '❤️', '🍎', '🎮', '✨', '👍', '🎉'].map((emoji) => (
            <Button
              key={emoji}
              variant="ghost"
              className="aspect-square text-lg p-1 text-slate-600 hover:bg-slate-100 hover:scale-110 transition-all duration-200 flex-shrink-0 border border-slate-200/50 shadow-sm hover:shadow-md transform hover:-translate-y-0.5"
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
        <div className="space-y-4 border-t border-slate-200 pt-4">
          {/* Category tabs */}
          <div className="flex gap-1 overflow-x-auto">
            {Object.entries(EMOJI_CATEGORIES).map(([key, category]) => (
              <Button
                key={key}
                variant={activeCategory === key ? "default" : "outline"}
                size="sm"
                onClick={() => setActiveCategory(key as keyof typeof EMOJI_CATEGORIES)}
                className={`whitespace-nowrap text-sm flex-shrink-0 font-medium ${
                  activeCategory === key 
                    ? 'bg-indigo-500 hover:bg-indigo-600 text-white' 
                    : 'border-slate-200 text-slate-600 hover:bg-slate-50'
                }`}
              >
                {category.name}
              </Button>
            ))}
          </div>

          {/* Emoji grid */}
          <div className="grid grid-cols-6 gap-2 max-h-32 overflow-y-auto scrollbar-thin scrollbar-thumb-slate-300 scrollbar-track-slate-100">
            {EMOJI_CATEGORIES[activeCategory].emojis.map((emoji) => (
              <Button
                key={emoji}
                variant="ghost"
                className="aspect-square text-lg p-0 text-slate-600 hover:bg-slate-100 hover:scale-110 transition-all duration-200 border border-slate-200/50 shadow-sm hover:shadow-md transform hover:-translate-y-0.5"
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
      <div className="mt-4 pt-4 border-t border-slate-200">
        <p className="text-sm text-slate-600 mb-3 font-sans font-medium">Quick suggestions:</p>
        <div className="flex flex-wrap gap-2">
          {['👋😊', '🍎😋', '🎮🎯', '❤️✨', '😴💤'].map((suggestion) => (
            <Button
              key={suggestion}
              variant="ghost"
              size="sm"
              onClick={() => setSelectedEmojis(suggestion)}
              disabled={isLoading}
              className="text-lg h-10 px-3 text-slate-600 hover:bg-slate-100 border border-slate-200/50 rounded-lg shadow-sm hover:shadow-md transition-all duration-200 transform hover:-translate-y-0.5 active:translate-y-0"
            >
              {suggestion}
            </Button>
          ))}
        </div>
      </div>
    </div>
  )
}
