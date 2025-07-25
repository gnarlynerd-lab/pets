"use client"

import { useState, useEffect, useCallback } from 'react'
import { useAuth } from '@/contexts/auth-context'

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
  consciousness?: {
    consciousness_level: number
    memory_richness: number
    concept_development: number
    user_understanding: number
    recent_concepts: string[]
    user_model_summary: {
      trust_level: number
      communication_style: string
      relationship_depth: number
    }
    semantic_active: boolean
  }
}

interface InteractionResult {
  userEmojis: string
  petResponse: string
  surpriseLevel: number
  responseConfidence: number
  timestamp: number
  user_insights?: any
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export function useAuthenticatedPetState() {
  const { user, token } = useAuth()
  const [petData, setPetData] = useState<PetData | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [petResponse, setPetResponse] = useState<string>('')
  const [interactionHistory, setInteractionHistory] = useState<InteractionResult[]>([])
  const [availablePetId, setAvailablePetId] = useState<string | null>(null)
  const [petName, setPetName] = useState<string>('')
  const [userPets, setUserPets] = useState<PetData[]>([])
  const [sessionId, setSessionId] = useState<string | null>(null)
  const [isClient, setIsClient] = useState(false)

  // Initialize client state
  useEffect(() => {
    setIsClient(true)
  }, [])

  // Load session ID and pet name from localStorage for anonymous users
  useEffect(() => {
    // Only run on client side with proper checks for Safari
    if (!isClient || typeof window === 'undefined') return
    
    if (!user) {
      // Load or create session ID
      const savedSessionId = localStorage.getItem('emoji-pet-session-id')
      if (savedSessionId) {
        setSessionId(savedSessionId)
      }
      
      // Load pet name
      const savedName = localStorage.getItem('emoji-pet-name')
      if (savedName) {
        setPetName(savedName)
      }
    }
  }, [user, isClient])

  // Save pet name to localStorage for anonymous users
  const updatePetName = useCallback((name: string) => {
    setPetName(name)
    if (!user && typeof window !== 'undefined') {
      localStorage.setItem('emoji-pet-name', name)
    }
    // TODO: For authenticated users, save to backend
  }, [user])

  // Create anonymous session
  const createAnonymousSession = useCallback(async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/anonymous/session/create`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        }
      })
      
      if (response.ok) {
        const data = await response.json()
        setSessionId(data.session_id)
        
        if (typeof window !== 'undefined') {
          localStorage.setItem('emoji-pet-session-id', data.session_id)
        }
        
        if (data.pet) {
          setPetData(data.pet)
          setPetName(data.pet.name || '')
          
          if (typeof window !== 'undefined') {
            localStorage.setItem('emoji-pet-name', data.pet.name || '')
          }
          
          setPetResponse(data.pet.current_emoji_message || '👋😊')
        }
        
        return data.session_id
      }
    } catch (error) {
      console.error('Failed to create anonymous session:', error)
    }
    return null
  }, [])

  // Get user's pets if authenticated
  const getUserPets = useCallback(async () => {
    if (!user || !token) return []

    try {
      const response = await fetch(`${API_BASE_URL}/api/users/pets`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      
      if (response.ok) {
        const data = await response.json()
        setUserPets(data.pets || [])
        return data.pets || []
      }
    } catch (error) {
      console.error('Failed to get user pets:', error)
    }
    return []
  }, [user, token])

  // Get any available pet (for anonymous users)
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

      // If authenticated, get user's pets
      if (user && token) {
        const pets = await getUserPets()
        if (pets.length > 0) {
          const petId = pets[0].id
          setAvailablePetId(petId)
          
          const response = await fetch(`${API_BASE_URL}/api/pets/${petId}`)
          if (response.ok) {
            const data = await response.json()
            setPetData(data)
            setPetResponse(data.current_emoji_message || '👋😊')
          }
        } else {
          // User has no pets, create one (optional, or show create pet UI)
          console.log('User has no pets')
        }
      } else {
        // Anonymous user - use session-based pet
        if (!sessionId) {
          // Create new session if needed
          const newSessionId = await createAnonymousSession()
          if (!newSessionId) {
            console.error('Failed to create anonymous session')
            return
          }
        } else {
          // Load existing session pet
          const response = await fetch(`${API_BASE_URL}/api/anonymous/pets/${sessionId}`)
          if (response.ok) {
            const data = await response.json()
            setPetData(data)
            setPetResponse(data.current_emoji_message || '👋😊')
            if (data.name) {
              setPetName(data.name)
            }
          } else if (response.status === 404) {
            // Session pet not found, create new session
            console.log('Session pet not found, creating new session')
            await createAnonymousSession()
          }
        }
      }
    } catch (error) {
      console.error('Failed to fetch pet data:', error)
    } finally {
      setIsLoading(false)
    }
  }, [user, token, sessionId, getUserPets, createAnonymousSession])

  // Send emoji interaction to backend
  const sendEmojiInteraction = useCallback(async (emojiSequence: string) => {
    if (!emojiSequence.trim()) return

    try {
      setIsLoading(true)
      
      let response: Response
      
      if (user && token) {
        // Authenticated user
        if (!availablePetId) {
          console.error('No pet available for authenticated user')
          return
        }
        
        const requestBody = {
          pet_id: availablePetId,
          emojis: emojiSequence,
          context: { source: 'frontend' }
        }
        
        response = await fetch(`${API_BASE_URL}/api/pets/emoji`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify(requestBody),
        })
      } else {
        // Anonymous user
        if (!sessionId) {
          console.error('No session available for anonymous user')
          return
        }
        
        const requestBody = {
          emojis: emojiSequence,
          context: { source: 'frontend' }
        }
        
        response = await fetch(`${API_BASE_URL}/api/anonymous/pets/${sessionId}/emoji`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(requestBody),
        })
      }

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
          timestamp: Date.now(),
          user_insights: result.user_insights
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
  }, [availablePetId, sessionId, user, token])

  // Initialize pet data on mount and when auth state changes
  useEffect(() => {
    refreshPetState()
  }, [refreshPetState])

  // Load interaction history from localStorage (for anonymous users)
  useEffect(() => {
    // Only run on client side with proper Safari checks
    if (!isClient || typeof window === 'undefined') return
    
    if (!user) {
      const savedHistory = localStorage.getItem('emoji-pet-history')
      if (savedHistory) {
        try {
          setInteractionHistory(JSON.parse(savedHistory))
        } catch (error) {
          console.error('Failed to load interaction history:', error)
        }
      }
    }
    // TODO: For authenticated users, load from backend
  }, [user, isClient])

  // Save interaction history to localStorage (for anonymous users)
  useEffect(() => {
    // Only run on client side
    if (typeof window === 'undefined') return
    
    if (!user && interactionHistory.length > 0) {
      localStorage.setItem('emoji-pet-history', JSON.stringify(interactionHistory.slice(-50))) // Keep last 50
    }
    // TODO: For authenticated users, save to backend
  }, [interactionHistory, user])

  // Migrate anonymous data to authenticated account
  const migrateAnonymousData = useCallback(async () => {
    if (!user || !token || !sessionId) {
      console.error('Cannot migrate: missing user, token, or sessionId')
      return { success: false, error: 'Missing required data for migration' }
    }

    try {
      const response = await fetch(`${API_BASE_URL}/auth/migrate-anonymous-data`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          session_id: sessionId
        })
      })

      if (response.ok) {
        const result = await response.json()
        
        // Clear anonymous data from localStorage after successful migration
        if (isClient && typeof window !== 'undefined') {
          localStorage.removeItem('emoji-pet-session-id')
          localStorage.removeItem('emoji-pet-name')
          localStorage.removeItem('emoji-pet-history')
        }
        
        // Clear anonymous state
        setSessionId(null)
        setInteractionHistory([])
        
        // Refresh pet state to get the migrated data
        await refreshPetState()
        
        console.log(`Migration successful: ${result.interactions_migrated} interactions migrated`)
        return { 
          success: true, 
          pet: result.pet, 
          interactionsMigrated: result.interactions_migrated 
        }
        
      } else {
        const errorData = await response.json()
        console.error('Migration failed:', errorData)
        return { success: false, error: errorData.detail || 'Migration failed' }
      }
      
    } catch (error) {
      console.error('Error during migration:', error)
      return { success: false, error: 'Network error during migration' }
    }
  }, [user, token, sessionId, isClient, refreshPetState])

  return {
    petData,
    isLoading,
    petResponse,
    interactionHistory,
    petName,
    updatePetName,
    sendEmojiInteraction,
    refreshPetState,
    userPets,
    isAuthenticated: !!user,
    sessionId,
    migrateAnonymousData,
  }
}