"use client"

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react'

interface User {
  user_id: string
  username: string
  email: string
  token_balance: number
  created_at: string
  last_login?: string
}

interface AuthContextType {
  user: User | null
  token: string | null
  login: (email: string, password: string) => Promise<boolean>
  register: (username: string, email: string, password: string) => Promise<boolean>
  logout: () => void
  isLoading: boolean
  error: string | null
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}

interface AuthProviderProps {
  children: ReactNode
}

export function AuthProvider({ children }: AuthProviderProps) {
  const [user, setUser] = useState<User | null>(null)
  const [token, setToken] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [isClient, setIsClient] = useState(false)

  const API_BASE = 'http://localhost:8000'

  // Initialize client state for Safari compatibility
  useEffect(() => {
    setIsClient(true)
  }, [])

  // Load token from localStorage on mount
  useEffect(() => {
    // Only run on client side with proper Safari checks
    if (!isClient || typeof window === 'undefined') {
      setIsLoading(false)
      return
    }
    
    const savedToken = localStorage.getItem('auth_token')
    if (savedToken) {
      setToken(savedToken)
      fetchUserInfo(savedToken)
    } else {
      setIsLoading(false)
    }
  }, [isClient])

  const fetchUserInfo = async (authToken: string) => {
    try {
      const response = await fetch(`${API_BASE}/auth/me`, {
        headers: {
          'Authorization': `Bearer ${authToken}`
        }
      })
      
      if (response.ok) {
        const userData = await response.json()
        setUser(userData)
      } else {
        // Token might be expired
        if (typeof window !== 'undefined') {
          localStorage.removeItem('auth_token')
        }
        setToken(null)
      }
    } catch (error) {
      console.error('Failed to fetch user info:', error)
      if (typeof window !== 'undefined') {
        localStorage.removeItem('auth_token')
      }
      setToken(null)
    } finally {
      setIsLoading(false)
    }
  }

  const login = async (email: string, password: string): Promise<boolean> => {
    setIsLoading(true)
    setError(null)
    
    try {
      const response = await fetch(`${API_BASE}/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
      })

      if (response.ok) {
        const data = await response.json()
        const authToken = data.access_token
        
        setToken(authToken)
        if (typeof window !== 'undefined') {
          localStorage.setItem('auth_token', authToken)
        }
        
        // Fetch user info
        await fetchUserInfo(authToken)
        return true
      } else {
        const errorData = await response.json()
        setError(errorData.detail || 'Login failed')
        return false
      }
    } catch (error) {
      setError('Network error. Please try again.')
      return false
    } finally {
      setIsLoading(false)
    }
  }

  const register = async (username: string, email: string, password: string): Promise<boolean> => {
    setIsLoading(true)
    setError(null)
    
    try {
      const response = await fetch(`${API_BASE}/auth/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, email, password })
      })

      if (response.ok) {
        // Auto-login after successful registration
        return await login(email, password)
      } else {
        const errorData = await response.json()
        setError(errorData.detail || 'Registration failed')
        return false
      }
    } catch (error) {
      setError('Network error. Please try again.')
      return false
    } finally {
      setIsLoading(false)
    }
  }

  const logout = () => {
    setUser(null)
    setToken(null)
    if (typeof window !== 'undefined') {
      localStorage.removeItem('auth_token')
    }
    setError(null)
  }

  const value: AuthContextType = {
    user,
    token,
    login,
    register,
    logout,
    isLoading,
    error
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}