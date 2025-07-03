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
    <div className="mt-6 space-y-4">
      {/* Laboratory Communication Terminal */}
      <div className="bg-gradient-to-br from-[#2F4F4F] to-[#1a2f2f] p-6 rounded-2xl border-2 border-[#8A6C3C] shadow-2xl font-mono">
        <div className="flex items-center mb-4">
          <Terminal className="h-5 w-5 mr-2 text-[#FF6347]" />
          <span className="text-sm font-bold text-[#4682B4]">COMMUNICATION INTERFACE</span>
          <div className="ml-auto flex space-x-1">
            <div className="w-2 h-2 bg-[#FF6347] rounded-full animate-pulse"></div>
            <div className="w-2 h-2 bg-[#8A6C3C] rounded-full"></div>
            <div className="w-2 h-2 bg-[#4682B4] rounded-full"></div>
          </div>
        </div>

        <div className="flex items-center space-x-3 mb-4">
          <div className="relative flex-1">
            <Input
              ref={inputRef}
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="TRANSMIT EMOTIONAL DATA... 😊🎮❤️"
              className="pr-12 text-lg h-14 bg-[#1a2f2f] border-2 border-[#8A6C3C] focus:border-[#FF6347] focus:ring-[#FF6347] text-[#4682B4] placeholder:text-[#8A6C3C] font-mono"
            />
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setShowEmojiPicker(!showEmojiPicker)}
              className="absolute right-2 top-2 h-10 w-10 text-[#FF6347] hover:bg-[#8A6C3C]/20 border border-[#8A6C3C]"
            >
              <Smile className="h-5 w-5" />
            </Button>
          </div>

          <Button
            onClick={handleSend}
            disabled={extractEmojis(inputValue).length === 0}
            className="h-14 px-8 bg-gradient-to-r from-[#FF6347] to-[#8A6C3C] hover:from-[#8A6C3C] hover:to-[#FF6347] transition-all duration-300 font-mono font-bold border-2 border-[#8A6C3C] relative overflow-hidden group"
          >
            <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent transform -skew-x-12 group-hover:translate-x-full transition-transform duration-700"></div>
            <Send className="h-6 w-6 mr-2" />
            TRANSMIT
          </Button>

          <Button
            variant="outline"
            onClick={() => setShowHistory(!showHistory)}
            className="h-14 px-6 border-2 border-[#8A6C3C] text-[#4682B4] hover:bg-[#8A6C3C]/20 font-mono"
          >
            <History className="h-5 w-5" />
          </Button>
        </div>

        {/* Laboratory Emoji Picker */}
        {showEmojiPicker && (
          <div ref={pickerRef} className="bg-[#1a2f2f] rounded-xl shadow-2xl border-2 border-[#8A6C3C] p-6 mb-4">
            {/* Category Tabs */}
            <div className="flex space-x-2 mb-4 overflow-x-auto">
              {Object.keys(EMOJI_CATEGORIES).map((category) => (
                <Button
                  key={category}
                  variant={selectedCategory === category ? "default" : "outline"}
                  size="sm"
                  onClick={() => setSelectedCategory(category as keyof typeof EMOJI_CATEGORIES)}
                  className={`capitalize whitespace-nowrap font-mono ${
                    selectedCategory === category
                      ? "bg-gradient-to-r from-[#FF6347] to-[#8A6C3C] border-[#FF6347]"
                      : "border-[#8A6C3C] text-[#4682B4] hover:bg-[#8A6C3C]/20"
                  }`}
                >
                  {category.toUpperCase()}
                </Button>
              ))}
            </div>

            {/* Emoji Grid */}
            <div className="grid grid-cols-8 gap-3 max-h-48 overflow-y-auto bg-[#2F4F4F] rounded-lg p-4 border border-[#8A6C3C]">
              {EMOJI_CATEGORIES[selectedCategory].map((emoji, index) => (
                <button
                  key={index}
                  onClick={() => handleEmojiClick(emoji)}
                  className="text-2xl p-3 hover:bg-[#8A6C3C]/30 rounded-lg transition-all duration-200 border border-transparent hover:border-[#FF6347]"
                >
                  {emoji}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Pet Response Feedback */}
        {petResponse && (
          <div className="bg-[#1a2f2f] rounded-xl p-4 border-2 border-[#FF6347] bg-gradient-to-r from-[#FF6347]/10 to-[#8A6C3C]/10">
            <div className="flex items-center space-x-3">
              <Zap className="h-5 w-5 text-[#FF6347] animate-pulse" />
              <span className="text-sm font-bold text-[#4682B4]">SPECIMEN RESPONSE DETECTED:</span>
              <div className="flex space-x-2">
                {petResponse.map((emoji, index) => (
                  <span key={index} className="text-xl animate-bounce" style={{ animationDelay: `${index * 100}ms` }}>
                    {emoji}
                  </span>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Laboratory History Panel */}
      {showHistory && (
        <div className="bg-gradient-to-br from-[#2F4F4F] to-[#1a2f2f] rounded-2xl shadow-2xl border-2 border-[#8A6C3C] p-6 font-mono">
          <h3 className="text-sm font-bold text-[#FF6347] mb-4 flex items-center">
            <History className="h-4 w-4 mr-2" />
            COMMUNICATION LOG
          </h3>

          {emojiHistory.length === 0 ? (
            <p className="text-[#8A6C3C] text-sm text-center py-6 bg-[#1a2f2f] rounded border border-[#8A6C3C]">
              NO TRANSMISSIONS RECORDED. INITIATE COMMUNICATION PROTOCOL.
            </p>
          ) : (
            <div className="space-y-3 max-h-64 overflow-y-auto">
              {emojiHistory
                .slice(-5)
                .reverse()
                .map((exchange, index) => (
                  <div
                    key={exchange.timestamp}
                    className="flex items-center justify-between p-4 bg-[#1a2f2f] rounded-lg border border-[#8A6C3C]"
                  >
                    <div className="flex items-center space-x-4">
                      <div className="flex items-center space-x-2">
                        <span className="text-xs text-[#4682B4] font-bold">USER:</span>
                        {exchange.userEmojis.map((emoji, i) => (
                          <span key={i} className="text-lg">
                            {emoji}
                          </span>
                        ))}
                      </div>
                      <span className="text-[#8A6C3C]">→</span>
                      <div className="flex items-center space-x-2">
                        <span className="text-xs text-[#4682B4] font-bold">SPECIMEN:</span>
                        {exchange.petResponse.map((emoji, i) => (
                          <span key={i} className="text-lg">
                            {emoji}
                          </span>
                        ))}
                      </div>
                    </div>

                    <div className="flex items-center space-x-3">
                      {exchange.understood ? (
                        <span className="text-xs bg-[#FF6347]/20 text-[#FF6347] px-3 py-1 rounded-full border border-[#FF6347] font-bold">
                          DECODED
                        </span>
                      ) : (
                        <span className="text-xs bg-[#8A6C3C]/20 text-[#8A6C3C] px-3 py-1 rounded-full border border-[#8A6C3C] font-bold">
                          ERROR
                        </span>
                      )}
                      <span className="text-xs text-[#4682B4] font-mono">
                        {new Date(exchange.timestamp).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
                      </span>
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
