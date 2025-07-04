"use client"

import type React from "react"

import { useState, useRef, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Send, Smile, History, Terminal, Zap } from "lucide-react"

interface EmojiExchange {
  userEmojis: string[]
  petResponse: string[]
  timestamp: number
  understood: boolean
}

interface UserEmojiInputProps {
  onSendEmoji: (emojis: string[]) => void
  emojiHistory: EmojiExchange[]
  petResponse: string[] | null
}

// Common emoji categories for the picker
const EMOJI_CATEGORIES = {
  emotions: [
    "😀",
    "😃",
    "😄",
    "😁",
    "😊",
    "😍",
    "🥰",
    "😘",
    "😗",
    "😙",
    "😚",
    "😋",
    "😛",
    "😝",
    "😜",
    "🤪",
    "🤨",
    "🧐",
    "🤓",
    "😎",
    "🤩",
    "🥳",
    "😏",
    "😒",
    "😞",
    "😔",
    "😟",
    "😕",
    "🙁",
    "☹️",
    "😣",
    "😖",
    "😫",
    "😩",
    "🥺",
    "😢",
    "😭",
    "😤",
    "😠",
    "😡",
    "🤬",
    "🤯",
    "😳",
    "🥵",
    "🥶",
    "😱",
    "😨",
    "😰",
    "😥",
    "😓",
  ],
  animals: [
    "🐶",
    "🐱",
    "🐭",
    "🐹",
    "🐰",
    "🦊",
    "🐻",
    "🐼",
    "🐨",
    "🐯",
    "🦁",
    "🐮",
    "🐷",
    "🐸",
    "🐵",
    "🐔",
    "🐧",
    "🐦",
    "🐤",
    "🐣",
    "🐥",
    "🦆",
    "🦅",
    "🦉",
    "🦇",
    "🐺",
    "🐗",
    "🐴",
    "🦄",
    "🐝",
    "🐛",
    "🦋",
    "🐌",
    "🐞",
    "🐜",
    "🦟",
    "🦗",
    "🕷️",
    "🦂",
    "🐢",
    "🐍",
    "🦎",
    "🦖",
    "🦕",
    "🐙",
    "🦑",
    "🦐",
    "🦞",
    "🦀",
    "🐡",
    "🐠",
    "🐟",
    "🐬",
    "🐳",
    "🐋",
    "🦈",
    "🐊",
  ],
  food: [
    "🍎",
    "🍊",
    "🍋",
    "🍌",
    "🍉",
    "🍇",
    "🍓",
    "🫐",
    "🍈",
    "🍒",
    "🍑",
    "🥭",
    "🍍",
    "🥥",
    "🥝",
    "🍅",
    "🍆",
    "🥑",
    "🥦",
    "🥬",
    "🥒",
    "🌶️",
    "🫑",
    "🌽",
    "🥕",
    "🫒",
    "🧄",
    "🧅",
    "🥔",
    "🍠",
    "🥐",
    "🥯",
    "🍞",
    "🥖",
    "🥨",
    "🧀",
    "🥚",
    "🍳",
    "🧈",
    "🥞",
    "🧇",
    "🥓",
    "🥩",
    "🍗",
    "🍖",
    "🦴",
    "🌭",
    "🍔",
    "🍟",
    "🍕",
  ],
  activities: [
    "⚽",
    "🏀",
    "🏈",
    "⚾",
    "🥎",
    "🎾",
    "🏐",
    "🏉",
    "🥏",
    "🎱",
    "🪀",
    "🏓",
    "🏸",
    "🏒",
    "🏑",
    "🥍",
    "🏏",
    "🪃",
    "🥅",
    "⛳",
    "🪁",
    "🏹",
    "🎣",
    "🤿",
    "🥊",
    "🥋",
    "🎽",
    "🛹",
    "🛷",
    "⛸️",
    "🥌",
    "🎿",
    "⛷️",
    "🏂",
    "🪂",
    "🏋️",
    "🤼",
    "🤸",
    "⛹️",
    "🤺",
    "🏇",
    "🧘",
    "🏄",
    "🏊",
    "🤽",
    "🚣",
    "🧗",
    "🚵",
    "🚴",
    "🏆",
    "🥇",
    "🥈",
    "🥉",
    "🏅",
    "🎖️",
    "🏵️",
    "🎗️",
  ],
  objects: [
    "❤️",
    "🧡",
    "💛",
    "💚",
    "💙",
    "💜",
    "🖤",
    "🤍",
    "🤎",
    "💔",
    "❣️",
    "💕",
    "💞",
    "💓",
    "💗",
    "💖",
    "💘",
    "💝",
    "💟",
    "☮️",
    "✝️",
    "☪️",
    "🕉️",
    "☸️",
    "✡️",
    "🔯",
    "🕎",
    "☯️",
    "☦️",
    "🛐",
    "⛎",
    "♈",
    "♉",
    "♊",
    "♋",
    "♌",
    "♍",
    "♎",
    "♏",
    "♐",
    "♑",
    "♒",
    "♓",
    "🆔",
    "⚛️",
    "🉑",
    "☢️",
    "☣️",
    "📴",
    "📳",
    "🈶",
    "🈚",
    "🈸",
    "🈺",
    "🈷️",
    "✴️",
    "🆚",
    "💮",
    "🉐",
    "㊙️",
    "㊗️",
    "🈴",
    "🈵",
    "🈹",
    "🈲",
    "🅰️",
    "🅱️",
    "🆎",
    "🆑",
    "🅾️",
    "🆘",
    "❌",
    "⭕",
    "🛑",
    "⛔",
    "📛",
    "🚫",
    "💯",
    "💢",
    "♨️",
    "🚷",
    "🚯",
    "🚳",
    "🚱",
    "🔞",
    "📵",
    "🚭",
  ],
}

export default function UserEmojiInput({ onSendEmoji, emojiHistory, petResponse }: UserEmojiInputProps) {
  const [inputValue, setInputValue] = useState("")
  const [showEmojiPicker, setShowEmojiPicker] = useState(false)
  const [showHistory, setShowHistory] = useState(false)
  const [selectedCategory, setSelectedCategory] = useState<keyof typeof EMOJI_CATEGORIES>("emotions")
  const inputRef = useRef<HTMLInputElement>(null)
  const pickerRef = useRef<HTMLDivElement>(null)
  const [inputFocused, setInputFocused] = useState(false)

  // Close emoji picker when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (pickerRef.current && !pickerRef.current.contains(event.target as Node)) {
        setShowEmojiPicker(false)
      }
    }

    document.addEventListener("mousedown", handleClickOutside)
    return () => document.removeEventListener("mousedown", handleClickOutside)
  }, [])

  // Extract emojis from input string
  const extractEmojis = (text: string): string[] => {
    const emojiRegex =
      /[\u{1F600}-\u{1F64F}]|[\u{1F300}-\u{1F5FF}]|[\u{1F680}-\u{1F6FF}]|[\u{1F1E0}-\u{1F1FF}]|[\u{2600}-\u{26FF}]|[\u{2700}-\u{27BF}]/gu
    return text.match(emojiRegex) || []
  }

  const handleSend = () => {
    const emojis = extractEmojis(inputValue)
    if (emojis.length > 0) {
      onSendEmoji(emojis)
      setInputValue("")
    }
  }

  const handleEmojiClick = (emoji: string) => {
    setInputValue((prev) => prev + emoji)
    if (inputRef.current) {
      inputRef.current.focus()
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter") {
      handleSend()
    }
  }

  return (
    <div className="mt-2 space-y-2 w-full max-w-xl mx-auto">
      {/* Communication Terminal */}
      <div className="bg-white/80 dark:bg-[#23272f] p-4 rounded-xl border border-[#e0c68a] shadow font-mono transition-all">
        <div className="flex flex-col sm:flex-row items-center gap-2 mb-2">
          <div className="relative flex-1 w-full">
            <Input
              ref={inputRef}
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              onFocus={() => setInputFocused(true)}
              onBlur={() => setTimeout(() => setInputFocused(false), 200)}
              placeholder="Send emoji... 😊🎮❤️"
              className="pr-10 text-base h-12 bg-white dark:bg-[#23272f] border border-[#e0c68a] focus:border-[#FF6347] focus:ring-[#FF6347] text-[#222] dark:text-[#e0c68a] placeholder:text-[#bfa76a] font-mono rounded-lg shadow-sm"
            />
            <Button
              variant="ghost"
              size="icon"
              type="button"
              onClick={() => setShowEmojiPicker((v) => !v)}
              className="absolute right-1 top-1 h-10 w-10 text-[#FF6347] hover:bg-[#e0c68a]/20 border border-[#e0c68a] bg-white dark:bg-[#23272f]"
              tabIndex={-1}
            >
              <Smile className="h-5 w-5" />
            </Button>
          </div>
          <Button
            onClick={handleSend}
            disabled={extractEmojis(inputValue).length === 0}
            className="h-12 px-6 bg-gradient-to-r from-[#FF6347] to-[#e0c68a] hover:from-[#e0c68a] hover:to-[#FF6347] text-white font-bold border border-[#e0c68a] rounded-lg shadow-sm w-full sm:w-auto"
          >
            <Send className="h-5 w-5 mr-1" />
            Send
          </Button>
          <Button
            variant="outline"
            onClick={() => setShowHistory(!showHistory)}
            className="h-12 px-4 border border-[#e0c68a] text-[#FF6347] hover:bg-[#e0c68a]/20 font-mono rounded-lg w-full sm:w-auto"
          >
            <History className="h-5 w-5" />
          </Button>
        </div>

        {/* Emoji Picker Overlay */}
        {(showEmojiPicker || inputFocused) && (
          <div ref={pickerRef} className="fixed inset-0 z-40 flex items-end sm:items-center justify-center bg-black/20" onClick={() => setShowEmojiPicker(false)}>
            <div className="bg-white dark:bg-[#23272f] rounded-xl shadow-2xl border border-[#e0c68a] p-4 mb-8 sm:mb-0 max-w-lg w-full mx-2 relative z-50" onClick={e => e.stopPropagation()}>
              {/* Category Tabs */}
              <div className="flex space-x-2 mb-2 overflow-x-auto">
                {Object.keys(EMOJI_CATEGORIES).map((category) => (
                  <Button
                    key={category}
                    variant={selectedCategory === category ? "default" : "outline"}
                    size="sm"
                    onClick={() => setSelectedCategory(category as keyof typeof EMOJI_CATEGORIES)}
                    className={`capitalize whitespace-nowrap font-mono rounded-full px-3 py-1 text-xs ${
                      selectedCategory === category
                        ? "bg-gradient-to-r from-[#FF6347] to-[#e0c68a] border-[#FF6347] text-white"
                        : "border-[#e0c68a] text-[#FF6347] hover:bg-[#e0c68a]/20"
                    }`}
                  >
                    {category.toUpperCase()}
                  </Button>
                ))}
              </div>
              {/* Emoji Grid */}
              <div className="grid grid-cols-8 gap-2 max-h-40 overflow-y-auto bg-transparent rounded-lg p-2">
                {EMOJI_CATEGORIES[selectedCategory].map((emoji, index) => (
                  <button
                    key={index}
                    onClick={() => handleEmojiClick(emoji)}
                    className="text-2xl p-1 hover:bg-[#e0c68a]/30 rounded-lg transition-all duration-200 border border-transparent focus:border-[#FF6347] bg-transparent"
                    style={{ background: "none" }}
                  >
                    {emoji}
                  </button>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Pet Response Feedback */}
        {petResponse && (
          <div className="bg-[#f9f6f0] dark:bg-[#1a2f2f] rounded-xl p-3 border border-[#FF6347] mt-2">
            <div className="flex items-center space-x-2">
              <Zap className="h-5 w-5 text-[#FF6347] animate-pulse" />
              <span className="text-xs font-bold text-[#FF6347]">Pet Response:</span>
              <div className="flex space-x-1">
                {petResponse.map((emoji, index) => (
                  <span key={index} className="text-xl animate-bounce" style={{ animationDelay: `${index * 100}ms` }}>{emoji}</span>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>

      {/* History Panel */}
      {showHistory && (
        <div className="bg-white/80 dark:bg-[#23272f] rounded-xl shadow border border-[#e0c68a] p-4 font-mono mt-2">
          <h3 className="text-xs font-bold text-[#FF6347] mb-2 flex items-center">
            <History className="h-4 w-4 mr-1" />
            Communication Log
          </h3>
          {emojiHistory.length === 0 ? (
            <p className="text-[#bfa76a] text-xs text-center py-4 bg-white/60 dark:bg-[#23272f] rounded border border-[#e0c68a]">
              No transmissions yet.
            </p>
          ) : (
            <div className="space-y-2 max-h-40 overflow-y-auto">
              {emojiHistory.slice(-5).reverse().map((exchange, index) => (
                <div key={exchange.timestamp} className="flex items-center justify-between p-2 bg-white/60 dark:bg-[#23272f] rounded border border-[#e0c68a]">
                  <div className="flex items-center space-x-2">
                    <span className="text-xs text-[#FF6347] font-bold">You:</span>
                    {exchange.userEmojis.map((emoji, i) => (
                      <span key={i} className="text-lg">{emoji}</span>
                    ))}
                    <span className="text-[#e0c68a]">→</span>
                    <span className="text-xs text-[#FF6347] font-bold">Pet:</span>
                    {exchange.petResponse.map((emoji, i) => (
                      <span key={i} className="text-lg">{emoji}</span>
                    ))}
                  </div>
                  <div className="flex items-center space-x-2">
                    {exchange.understood ? (
                      <span className="text-xs bg-[#FF6347]/10 text-[#FF6347] px-2 py-0.5 rounded-full border border-[#FF6347] font-bold">Decoded</span>
                    ) : (
                      <span className="text-xs bg-[#e0c68a]/10 text-[#e0c68a] px-2 py-0.5 rounded-full border border-[#e0c68a] font-bold">Error</span>
                    )}
                    <span className="text-xs text-[#bfa76a] font-mono">{new Date(exchange.timestamp).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}</span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  )
}
