"use client"

import { useState, useEffect, useCallback } from 'react'
import { useAuth } from '@/contexts/auth-context'
import { getApiHeaders, getApiUrl } from '@/lib/api-client'

interface CompanionData {
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
  companionResponse: string
  surpriseLevel: number
  responseConfidence: number
  timestamp: number
  user_insights?: any
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export function useAuthenticatedCompanionState() {
  const { user, token } = useAuth()
  const [companionData, setCompanionData] = useState<CompanionData | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [companionResponse, setCompanionResponse] = useState<string>('')
  const [interactionHistory, setInteractionHistory] = useState<InteractionResult[]>([])
  const [availableCompanionId, setAvailableCompanionId] = useState<string | null>(null)
  const [companionName, setCompanionName] = useState<string>('')
  const [userCompanions, setUserCompanions] = useState<CompanionData[]>([])
  const [sessionId, setSessionId] = useState<string | null>(null)
  const [sessionToken, setSessionToken] = useState<string | null>(null)
  const [isClient, setIsClient] = useState(false)

  // Initialize client state
  useEffect(() => {
    setIsClient(true)
  }, [])

  // Load session ID and companion name from localStorage for anonymous users
  useEffect(() => {
    // Only run on client side with proper checks for Safari
    if (!isClient || typeof window === 'undefined') return
    
    if (!user) {
      // Load or create session ID and token
      const savedSessionId = localStorage.getItem('emoji-companion-session-id')
      const savedSessionToken = localStorage.getItem('emoji-companion-session-token')
      if (savedSessionId && savedSessionToken) {
        setSessionId(savedSessionId)
        setSessionToken(savedSessionToken)
      }
      
      // Load companion name
      const savedName = localStorage.getItem('emoji-companion-name')
      if (savedName) {
        setCompanionName(savedName)
      }
    }
  }, [user, isClient])

  // Save companion name to localStorage for anonymous users
  const updateCompanionName = useCallback((name: string) => {
    setCompanionName(name)
    if (!user && typeof window !== 'undefined') {
      localStorage.setItem('emoji-companion-name', name)
    }
    // TODO: For authenticated users, save to backend
  }, [user])

  // Create anonymous session
  const createAnonymousSession = useCallback(async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/simple/session/create`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        }
      })
      
      if (response.ok) {
        const data = await response.json()
        setSessionId(data.session_id)
        setSessionToken(data.token)
        
        if (typeof window !== 'undefined') {
          localStorage.setItem('emoji-companion-session-id', data.session_id)
          localStorage.setItem('emoji-companion-session-token', data.token)
        }
        
        if (data.companion) {
          setCompanionData(data.companion)
          setCompanionName(data.companion.name || '')
          
          if (typeof window !== 'undefined') {
            localStorage.setItem('emoji-companion-name', data.companion.name || '')
          }
          
          setCompanionResponse(data.companion.current_emoji_message || '👋😊')
        }
        
        return data.session_id
      } else {
        console.error('Failed to create anonymous session:', response.status, response.statusText)
      }
    } catch (error) {
      console.error('Failed to create anonymous session:', error)
      // Return null to indicate failure, but don't throw to prevent app crashes
    }
    return null
  }, [])

  // Get user's companions if authenticated
  const getUserCompanions = useCallback(async () => {
    if (!user || !token) return []

    try {
      const response = await fetch(`${API_BASE_URL}/api/users/companions`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      
      if (response.ok) {
        const data = await response.json()
        setUserPets(data.companions || [])
        return data.companions || []
      }
    } catch (error) {
      console.error('Failed to get user companions:', error)
    }
    return []
  }, [user, token])

  // Get any available companion (for anonymous users)
  const getAvailableCompanionId = useCallback(async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/companions`)
      if (response.ok) {
        const data = await response.json()
        if (data.companions && data.companions.length > 0) {
          const companionId = data.companions[0].id
          setAvailablePetId(companionId)
          return companionId
        }
      }
    } catch (error) {
      console.error('Failed to get available companions:', error)
    }
    return null
  }, [])

  // Load companion data from backend
  const refreshCompanionState = useCallback(async () => {
    try {
      setIsLoading(true)

      // If authenticated, get user's companions
      if (user && token) {
        const companions = await getUserCompanions()
        if (companions.length > 0) {
          const companionId = companions[0].id
          setAvailablePetId(companionId)
          
          const response = await fetch(`${API_BASE_URL}/api/companions/${companionId}`)
          if (response.ok) {
            const data = await response.json()
            setCompanionData(data)
            setCompanionResponse(data.current_emoji_message || '👋😊')
          }
        } else {
          // User has no companions, create one (optional, or show create companion UI)
          console.log('User has no companions')
        }
      } else {
        // Anonymous user - use session-based companion
        if (!sessionId) {
          // Create new session if needed
          const newSessionId = await createAnonymousSession()
          if (!newSessionId) {
            console.error('Failed to create anonymous session')
            return
          }
        } else {
          // Load existing session companion
          const response = await fetch(`${API_BASE_URL}/api/simple/companions/${sessionId}`, {
            headers: {
              'X-Session-Token': sessionToken || ''
            }
          })
          if (response.ok) {
            const data = await response.json()
            setCompanionData(data)
            setCompanionResponse(data.current_emoji_message || '👋😊')
            if (data.name) {
              setCompanionName(data.name)
            }
          } else if (response.status === 404) {
            // Session companion not found, create new session
            console.log('Session companion not found, creating new session')
            await createAnonymousSession()
          }
        }
      }
    } catch (error) {
      console.error('Failed to fetch companion data:', error)
    } finally {
      setIsLoading(false)
    }
  }, [user, token, sessionId, sessionToken, getUserCompanions, createAnonymousSession])

  // Send emoji interaction to backend
  const sendEmojiInteraction = useCallback(async (emojiSequence: string) => {
    if (!emojiSequence.trim()) return

    try {
      setIsLoading(true)
      
      let response: Response
      
      if (user && token) {
        // Authenticated user
        if (!availableCompanionId) {
          console.error('No companion available for authenticated user')
          return
        }
        
        const requestBody = {
          companion_id: availableCompanionId,
          emojis: emojiSequence,
          context: { source: 'frontend' }
        }
        
        response = await fetch(`${API_BASE_URL}/api/companions/emoji`, {
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
        
        response = await fetch(`${API_BASE_URL}/api/simple/companions/${sessionId}/emoji`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-Session-Token': sessionToken || ''
          },
          body: JSON.stringify(requestBody),
        })
      }

      if (response.ok) {
        const result = await response.json()
        
        // Update companion response
        setCompanionResponse(result.emoji_response || result.companion_response || result.response || '🤔')
        
        // Add to interaction history
        const newInteraction: InteractionResult = {
          userEmojis: emojiSequence,
          companionResponse: result.emoji_response || result.companion_response || result.response || '🤔',
          surpriseLevel: result.surprise_level || 0,
          responseConfidence: result.response_confidence || result.confidence || 0.5,
          timestamp: Date.now(),
          user_insights: result.user_insights
        }
        
        setInteractionHistory(prev => {
          const updated = [...prev, newInteraction]
          return updated
        })
        
        // Update companion data if available
        if (result.companion_state) {
          setCompanionData(prev => prev ? { ...prev, ...result.companion_state } : null)
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
  }, [availableCompanionId, sessionId, sessionToken, user, token])

  // Initialize companion data on mount and when auth state changes
  useEffect(() => {
    refreshCompanionState()
  }, [refreshCompanionState])

  // Load interaction history from localStorage (for anonymous users)
  useEffect(() => {
    // Only run on client side with proper Safari checks
    if (!isClient || typeof window === 'undefined') return
    
    if (!user) {
      const savedHistory = localStorage.getItem('emoji-companion-history')
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
      localStorage.setItem('emoji-companion-history', JSON.stringify(interactionHistory.slice(-50))) // Keep last 50
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
          localStorage.removeItem('emoji-companion-session-id')
          localStorage.removeItem('emoji-companion-session-token')
          localStorage.removeItem('emoji-companion-name')
          localStorage.removeItem('emoji-companion-history')
        }
        
        // Clear anonymous state
        setSessionId(null)
        setSessionToken(null)
        setInteractionHistory([])
        
        // Refresh companion state to get the migrated data
        await refreshCompanionState()
        
        console.log(`Migration successful: ${result.interactions_migrated} interactions migrated`)
        return { 
          success: true, 
          companion: result.companion, 
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
  }, [user, token, sessionId, isClient, refreshCompanionState])

  // Fetch memories for consciousness visualization
  const fetchMemories = useCallback(async () => {
    try {
      let response: Response
      
      if (user && token && availableCompanionId) {
        // Authenticated user
        response = await fetch(`${API_BASE_URL}/api/companions/${availableCompanionId}/memories`, {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        })
      } else if (sessionId) {
        // Anonymous user
        response = await fetch(`${API_BASE_URL}/api/anonymous/companions/${sessionId}/memories`, {
          headers: {
            'X-Session-Token': sessionToken || ''
          }
        })
      } else {
        return []
      }
      
      if (response.ok) {
        const data = await response.json()
        return data.memories || []
      } else if (response.status === 404) {
        // Pet/session doesn't exist yet - this is normal for new sessions
        return []
      } else {
        console.error('Failed to fetch memories:', response.status)
        return []
      }
    } catch (error) {
      console.error('Error fetching memories:', error)
      return []
    }
  }, [user, token, availableCompanionId, sessionId, sessionToken])

  return {
    companionData,
    isLoading,
    companionResponse,
    interactionHistory,
    companionName,
    updateCompanionName,
    sendEmojiInteraction,
    refreshCompanionState,
    userCompanions,
    isAuthenticated: !!user,
    sessionId,
    migrateAnonymousData,
    fetchMemories,
  }
}