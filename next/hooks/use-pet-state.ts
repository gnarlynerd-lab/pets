"use client"

import { useState, useEffect, useCallback } from 'react'

interface PetData {
  id: string
  traits: Record<string, number>
  mood: number
  energy: number
  health: number
  attention: number
  needs: {
    hunger: number
    thirst: number
    social: number
    play: number
    rest: number
  }
  age: number
  stage: string
  current_emoji_message?: string
  personality_summary?: string
}

interface InteractionResult {
  userEmojis: string
  petResponse: string
  surpriseLevel: number
  responseConfidence: number
  timestamp: number
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export function usePetState() {
  const [petData, setPetData] = useState<PetData | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [petResponse, setPetResponse] = useState<string>('')
  const [interactionHistory, setInteractionHistory] = useState<InteractionResult[]>([])
  const [availablePetId, setAvailablePetId] = useState<string | null>(null)
  const [petName, setPetName] = useState<string>('')

  // Load pet name from localStorage
  useEffect(() => {
    const savedName = localStorage.getItem('emoji-pet-name')
    if (savedName) {
      setPetName(savedName)
    }
  }, [])

  // Save pet name to localStorage
  const updatePetName = useCallback((name: string) => {
    setPetName(name)
    localStorage.setItem('emoji-pet-name', name)
  }, [])

  // Get the first available pet ID
  const getAvailablePetId = useCallback(async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/pets`)
      if (response.ok) {
        const data = await response.json()
        if (data.pets && data.pets.length > 0) {
          const petId = data.pets[0].id
          setAvailablePetId(petId)
          return petId
        }
      }
    } catch (error) {
      console.error('Failed to get available pets:', error)
    }
    return null
  }, [])

  // Load pet data from backend
  const refreshPetState = useCallback(async () => {
    try {
      setIsLoading(true)
      
      // Get available pet ID if we don't have one
      let petId = availablePetId
      if (!petId) {
        petId = await getAvailablePetId()
        if (!petId) {
          console.error('No pets available')
          return
        }
      }
      
      const response = await fetch(`${API_BASE_URL}/api/pets/${petId}`)
      if (response.ok) {
        const data = await response.json()
        setPetData(data)
        
        // Generate initial emoji message if pet doesn't have one
        if (!data.current_emoji_message) {
          setPetResponse('👋😊') // Default greeting
        } else {
          setPetResponse(data.current_emoji_message)
        }
      }
    } catch (error) {
      console.error('Failed to fetch pet data:', error)
    } finally {
      setIsLoading(false)
    }
  }, [availablePetId, getAvailablePetId])

  // Send emoji interaction to backend
  const sendEmojiInteraction = useCallback(async (emojiSequence: string) => {
    if (!emojiSequence.trim()) return

    // Get available pet ID if we don't have one
    let petId = availablePetId
    if (!petId) {
      petId = await getAvailablePetId()
      if (!petId) {
        console.error('No pets available for interaction')
        return
      }
    }

    try {
      setIsLoading(true)
      
      const response = await fetch(`${API_BASE_URL}/api/pets/emoji`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          pet_id: petId,
          emojis: emojiSequence,
          user_id: 'frontend_user',
          context: { source: 'frontend' }
        }),
      })

      if (response.ok) {
        const result = await response.json()
        
        // Update pet response
        setPetResponse(result.emoji_response || result.pet_response || result.response || '🤔')
        
        // Add to interaction history
        const newInteraction: InteractionResult = {
          userEmojis: emojiSequence,
          petResponse: result.emoji_response || result.pet_response || result.response || '🤔',
          surpriseLevel: result.surprise_level || 0,
          responseConfidence: result.response_confidence || result.confidence || 0.5,
          timestamp: Date.now()
        }
        
        setInteractionHistory(prev => {
          const updated = [...prev, newInteraction]
          return updated
        })
        
        // Update pet data if available
        if (result.pet_state) {
          setPetData(prev => prev ? { ...prev, ...result.pet_state } : null)
        }
        
        return result
      } else {
        const errorText = await response.text()
        console.error('Failed to send emoji interaction:', response.status, errorText)
      }
    } catch (error) {
      console.error('Error sending emoji interaction:', error)
    } finally {
      setIsLoading(false)
    }
  }, [availablePetId, getAvailablePetId])

  // Initialize pet data on mount
  useEffect(() => {
    refreshPetState()
  }, [refreshPetState])

  // Load interaction history from localStorage
  useEffect(() => {
    const savedHistory = localStorage.getItem('emoji-pet-history')
    if (savedHistory) {
      try {
        setInteractionHistory(JSON.parse(savedHistory))
      } catch (error) {
        console.error('Failed to load interaction history:', error)
      }
    }
  }, [])

  // Save interaction history to localStorage
  useEffect(() => {
    if (interactionHistory.length > 0) {
      localStorage.setItem('emoji-pet-history', JSON.stringify(interactionHistory.slice(-50))) // Keep last 50
    }
  }, [interactionHistory])

  return {
    petData,
    isLoading,
    petResponse,
    interactionHistory,
    petName,
    updatePetName,
    sendEmojiInteraction,
    refreshPetState,
  }
}
