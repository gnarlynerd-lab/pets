"use client"

import { useState, useEffect, useCallback } from "react"

interface PetStats {
  energy: number
  mood: number
  attention: number
  evolutionProgress: number
}

interface EmojiMessage {
  emojis: string[]
  isPersonalized: boolean
  timestamp: number
}

interface EmojiExchange {
  userEmojis: string[]
  petResponse: string[]
  timestamp: number
  understood: boolean
}

// Sample emoji sets for different moods and situations
const EMOJI_SETS = {
  happy: ["😊", "😄", "🥰", "😍", "🤗"],
  sad: ["😢", "😞", "😔", "😿", "💔"],
  excited: ["🤩", "🎉", "✨", "🌟", "🎊"],
  hungry: ["😋", "🍎", "🥕", "🍖", "🤤"],
  playful: ["😆", "🎮", "⚽", "🎯", "🏃"],
  sleepy: ["😴", "💤", "🌙", "😪", "🛏️"],
  love: ["💕", "💖", "💝", "🥰", "😘"],
  neutral: ["😐", "🙂", "😌", "👋", "👀"],
}

export function usePetState() {
  const [petStats, setPetStats] = useState<PetStats>({
    energy: 70,
    mood: 60,
    attention: 50,
    evolutionProgress: 25,
  })

  const [petStage, setPetStage] = useState(1)
  const [relationshipStrength, setRelationshipStrength] = useState(30)
  const [currentMessage, setCurrentMessage] = useState<EmojiMessage | null>(null)
  const [communicationHistory, setCommunicationHistory] = useState<EmojiMessage[]>([])
  const [emojiHistory, setEmojiHistory] = useState<EmojiExchange[]>([])
  const [petResponse, setPetResponse] = useState<string[] | null>(null)

  // Load pet state from localStorage
  useEffect(() => {
    const savedStats = localStorage.getItem("petStats")
    const savedStage = localStorage.getItem("petStage")
    const savedRelationship = localStorage.getItem("relationshipStrength")
    const savedHistory = localStorage.getItem("communicationHistory")
    const savedEmojiHistory = localStorage.getItem("emojiHistory")

    if (savedStats) setPetStats(JSON.parse(savedStats))
    if (savedStage) setPetStage(Number.parseInt(savedStage, 10))
    if (savedRelationship) setRelationshipStrength(Number.parseInt(savedRelationship, 10))
    if (savedHistory) setCommunicationHistory(JSON.parse(savedHistory))
    if (savedEmojiHistory) setEmojiHistory(JSON.parse(savedEmojiHistory))
  }, [])

  // Save pet state to localStorage
  useEffect(() => {
    localStorage.setItem("petStats", JSON.stringify(petStats))
    localStorage.setItem("petStage", petStage.toString())
    localStorage.setItem("relationshipStrength", relationshipStrength.toString())
    localStorage.setItem("communicationHistory", JSON.stringify(communicationHistory))
    localStorage.setItem("emojiHistory", JSON.stringify(emojiHistory))
  }, [petStats, petStage, relationshipStrength, communicationHistory, emojiHistory])

  // Generate emoji message based on pet state
  const generateEmojiMessage = useCallback(
    (trigger: string) => {
      let emojiSet: string[] = []
      let isPersonalized = false

      // Determine emoji set based on stats and trigger
      if (trigger === "feed") {
        emojiSet = petStats.energy > 80 ? EMOJI_SETS.happy : EMOJI_SETS.hungry
      } else if (trigger === "play") {
        emojiSet = EMOJI_SETS.playful
      } else if (trigger === "pet") {
        emojiSet = relationshipStrength > 60 ? EMOJI_SETS.love : EMOJI_SETS.happy
        isPersonalized = relationshipStrength > 60
      } else {
        // Idle message based on current mood
        if (petStats.mood > 80) emojiSet = EMOJI_SETS.happy
        else if (petStats.mood < 30) emojiSet = EMOJI_SETS.sad
        else if (petStats.energy < 20) emojiSet = EMOJI_SETS.sleepy
        else emojiSet = EMOJI_SETS.neutral
      }

      // Select random emojis from the set
      const numEmojis = Math.min(petStage + 1, Math.floor(Math.random() * 3) + 1)
      const selectedEmojis: string[] = []

      for (let i = 0; i < numEmojis; i++) {
        const randomEmoji = emojiSet[Math.floor(Math.random() * emojiSet.length)]
        if (!selectedEmojis.includes(randomEmoji)) {
          selectedEmojis.push(randomEmoji)
        }
      }

      const message: EmojiMessage = {
        emojis: selectedEmojis,
        isPersonalized,
        timestamp: Date.now(),
      }

      setCurrentMessage(message)
      setCommunicationHistory((prev) => [...prev.slice(-9), message]) // Keep last 10 messages

      return message
    },
    [petStats, petStage, relationshipStrength],
  )

  // Interaction handlers
  const handleFeed = useCallback(() => {
    setPetStats((prev) => ({
      ...prev,
      energy: Math.min(100, prev.energy + 15),
      mood: Math.min(100, prev.mood + 5),
      evolutionProgress: Math.min(100, prev.evolutionProgress + 2),
    }))

    setRelationshipStrength((prev) => Math.min(100, prev + 2))
    generateEmojiMessage("feed")
    checkEvolution()
  }, [generateEmojiMessage])

  const handlePlay = useCallback(() => {
    setPetStats((prev) => ({
      ...prev,
      energy: Math.max(0, prev.energy - 10),
      mood: Math.min(100, prev.mood + 20),
      attention: Math.min(100, prev.attention + 15),
      evolutionProgress: Math.min(100, prev.evolutionProgress + 5),
    }))

    setRelationshipStrength((prev) => Math.min(100, prev + 3))
    generateEmojiMessage("play")
    checkEvolution()
  }, [generateEmojiMessage])

  const handlePet = useCallback(() => {
    setPetStats((prev) => ({
      ...prev,
      mood: Math.min(100, prev.mood + 10),
      attention: Math.min(100, prev.attention + 20),
      evolutionProgress: Math.min(100, prev.evolutionProgress + 3),
    }))

    setRelationshipStrength((prev) => Math.min(100, prev + 4))
    generateEmojiMessage("pet")
    checkEvolution()
  }, [generateEmojiMessage])

  // Check for evolution
  const checkEvolution = useCallback(() => {
    if (petStats.evolutionProgress >= 100 && petStage < 4) {
      setPetStage((prev) => prev + 1)
      setPetStats((prev) => ({
        ...prev,
        evolutionProgress: 0,
      }))

      // Special evolution message
      setTimeout(() => {
        generateEmojiMessage("evolve")
      }, 1000)
    }
  }, [petStats.evolutionProgress, petStage, generateEmojiMessage])

  // Occasional idle messages
  useEffect(() => {
    const interval = setInterval(() => {
      if (Math.random() < 0.3) {
        // 30% chance every interval
        generateEmojiMessage("idle")
      }
    }, 15000) // Every 15 seconds

    return () => clearInterval(interval)
  }, [generateEmojiMessage])

  const handleUserEmoji = useCallback(
    (userEmojis: string[]) => {
      // Generate pet response based on user input
      let responseEmojis: string[] = []
      let understood = true

      // Simple logic to determine pet response (this would integrate with CommunicationSystem)
      if (userEmojis.some((emoji) => EMOJI_SETS.love.includes(emoji))) {
        responseEmojis = [EMOJI_SETS.love[Math.floor(Math.random() * EMOJI_SETS.love.length)]]
      } else if (userEmojis.some((emoji) => EMOJI_SETS.happy.includes(emoji))) {
        responseEmojis = [EMOJI_SETS.happy[Math.floor(Math.random() * EMOJI_SETS.happy.length)]]
      } else if (userEmojis.some((emoji) => EMOJI_SETS.playful.includes(emoji))) {
        responseEmojis = [EMOJI_SETS.playful[Math.floor(Math.random() * EMOJI_SETS.playful.length)]]
      } else if (userEmojis.some((emoji) => EMOJI_SETS.hungry.includes(emoji))) {
        responseEmojis = [EMOJI_SETS.hungry[Math.floor(Math.random() * EMOJI_SETS.hungry.length)]]
      } else {
        // Pet doesn't understand - random confused response
        responseEmojis = ["🤔", "❓", "😕"]
        understood = false
      }

      // Create exchange record
      const exchange: EmojiExchange = {
        userEmojis,
        petResponse: responseEmojis,
        timestamp: Date.now(),
        understood,
      }

      // Update history
      setEmojiHistory((prev) => [...prev.slice(-9), exchange]) // Keep last 10 exchanges

      // Show pet response
      setPetResponse(responseEmojis)

      // Clear pet response after 3 seconds
      setTimeout(() => setPetResponse(null), 3000)

      // Update relationship based on understanding
      if (understood) {
        setRelationshipStrength((prev) => Math.min(100, prev + 1))
        setPetStats((prev) => ({
          ...prev,
          mood: Math.min(100, prev.mood + 5),
          attention: Math.min(100, prev.attention + 3),
        }))
      }

      // Generate pet's own emoji message
      setTimeout(() => {
        generateEmojiMessage("user_interaction")
      }, 1500)
    },
    [generateEmojiMessage],
  )

  return {
    petStats,
    petStage,
    relationshipStrength,
    currentMessage,
    communicationHistory,
    handleFeed,
    handlePlay,
    handlePet,
    emojiHistory,
    petResponse,
    handleUserEmoji,
  }
}
