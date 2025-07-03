"use client"

import { useEffect, useState } from "react"

interface EmojiMessage {
  emojis: string[]
  isPersonalized: boolean
  timestamp: number
}

interface EmojiCommunicationProps {
  message: EmojiMessage | null
  petStage: number
  relationshipStrength: number
}

export default function EmojiCommunication({ message, petStage, relationshipStrength }: EmojiCommunicationProps) {
  const [isVisible, setIsVisible] = useState(false)
  const [currentMessage, setCurrentMessage] = useState<EmojiMessage | null>(null)

  useEffect(() => {
    if (message && message !== currentMessage) {
      setCurrentMessage(message)
      setIsVisible(true)

      // Hide message after 4 seconds
      const timer = setTimeout(() => {
        setIsVisible(false)
      }, 4000)

      return () => clearTimeout(timer)
    }
  }, [message, currentMessage])

  if (!currentMessage || !isVisible) {
    return null
  }

  // Determine bubble size based on pet stage (complexity)
  const maxEmojis = Math.min(petStage + 1, 5)
  const displayEmojis = currentMessage.emojis.slice(0, maxEmojis)

  return (
    <div className="absolute top-6 left-1/2 transform -translate-x-1/2 z-20">
      <div
        className={`
          relative bg-gradient-to-br from-[#2F4F4F] to-[#1a2f2f] rounded-xl shadow-2xl p-4 min-w-[100px] max-w-[220px]
          border-2 border-[#8A6C3C] font-mono
          transition-all duration-300 ease-out
          ${isVisible ? "opacity-100 translate-y-0 scale-100" : "opacity-0 -translate-y-2 scale-95"}
          ${currentMessage.isPersonalized ? "ring-2 ring-[#FF6347] ring-opacity-70" : ""}
        `}
      >
        {/* Scientific Data Header */}
        <div className="text-xs text-[#4682B4] mb-2 flex justify-between">
          <span>DATA:</span>
          <span>{new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}</span>
        </div>

        {/* Speech bubble pointer */}
        <div className="absolute top-full left-1/2 transform -translate-x-1/2">
          <div className="w-0 h-0 border-l-[10px] border-r-[10px] border-t-[10px] border-l-transparent border-r-transparent border-t-[#8A6C3C]"></div>
          <div className="absolute -top-1 left-1/2 transform -translate-x-1/2 w-0 h-0 border-l-[8px] border-r-[8px] border-t-[8px] border-l-transparent border-r-transparent border-t-[#2F4F4F]"></div>
        </div>

        {/* Emoji content with scientific styling */}
        <div className="flex flex-wrap justify-center gap-2 bg-[#1a2f2f] rounded-lg p-2 border border-[#4682B4]/30">
          {displayEmojis.map((emoji, index) => (
            <span
              key={index}
              className={`
                text-2xl transition-all duration-200 ease-out
                ${currentMessage.isPersonalized ? "animate-pulse" : ""}
              `}
              style={{
                animationDelay: `${index * 100}ms`,
                filter: "drop-shadow(0 0 4px rgba(255, 99, 71, 0.5))",
              }}
            >
              {emoji}
            </span>
          ))}
        </div>

        {/* Personalized indicator */}
        {currentMessage.isPersonalized && (
          <div className="absolute -top-2 -right-2 w-4 h-4 bg-gradient-to-r from-[#FF6347] to-[#8A6C3C] rounded-full animate-pulse border-2 border-[#2F4F4F]"></div>
        )}

        {/* Scientific measurement lines */}
        <div className="absolute -left-1 top-1/2 w-2 h-px bg-[#8A6C3C]"></div>
        <div className="absolute -right-1 top-1/2 w-2 h-px bg-[#8A6C3C]"></div>
      </div>
    </div>
  )
}
