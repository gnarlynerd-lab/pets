"use client"

import { useState, useEffect, createContext, useContext } from 'react'
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog'

interface DemoAuthContextType {
  isAuthenticated: boolean
  authenticate: (password: string) => boolean
}

const DemoAuthContext = createContext<DemoAuthContextType>({
  isAuthenticated: false,
  authenticate: () => false
})

export const useDemoAuth = () => useContext(DemoAuthContext)

export function DemoAuthProvider({ children }: { children: React.ReactNode }) {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [showPasswordModal, setShowPasswordModal] = useState(false)
  
  // Check if demo mode is enabled
  const isDemoMode = process.env.NEXT_PUBLIC_DEMO_MODE === 'true'
  const demoPassword = process.env.NEXT_PUBLIC_DEMO_PASSWORD || 'AFFINITY2024'
  
  useEffect(() => {
    if (!isDemoMode) {
      setIsAuthenticated(true)
      return
    }
    
    // Check if already authenticated in this session
    const sessionAuth = sessionStorage.getItem('demo_authenticated')
    if (sessionAuth === 'true') {
      setIsAuthenticated(true)
    } else {
      setShowPasswordModal(true)
    }
  }, [isDemoMode])
  
  const authenticate = (password: string): boolean => {
    if (password === demoPassword) {
      setIsAuthenticated(true)
      sessionStorage.setItem('demo_authenticated', 'true')
      setShowPasswordModal(false)
      return true
    }
    return false
  }
  
  if (!isDemoMode || isAuthenticated) {
    return (
      <DemoAuthContext.Provider value={{ isAuthenticated: true, authenticate }}>
        {children}
      </DemoAuthContext.Provider>
    )
  }
  
  return (
    <DemoAuthContext.Provider value={{ isAuthenticated, authenticate }}>
      <DemoPasswordModal 
        open={showPasswordModal} 
        onAuthenticate={authenticate}
      />
      {isAuthenticated && children}
    </DemoAuthContext.Provider>
  )
}

function DemoPasswordModal({ 
  open, 
  onAuthenticate 
}: { 
  open: boolean
  onAuthenticate: (password: string) => boolean 
}) {
  const [password, setPassword] = useState('')
  const [error, setError] = useState(false)
  const [showPassword, setShowPassword] = useState(false)
  
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!onAuthenticate(password)) {
      setError(true)
      setTimeout(() => setError(false), 2000)
    }
  }
  
  return (
    <Dialog open={open} onOpenChange={() => {}}>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle>Welcome to AFFINITY Demo</DialogTitle>
        </DialogHeader>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="password" className="text-sm font-medium">
              Please enter the demo password
            </label>
            <div className="relative">
              <input
                id="password"
                type={showPassword ? "text" : "password"}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className={`
                  mt-2 w-full px-3 py-2 pr-10 border rounded-md
                  ${error ? 'border-red-500' : 'border-gray-300'}
                  focus:outline-none focus:ring-2 focus:ring-black
                  text-gray-900 placeholder-gray-400
                `}
                placeholder="Enter password"
                autoFocus
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-2 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-700"
              >
                {showPassword ? (
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
                  </svg>
                ) : (
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                  </svg>
                )}
              </button>
            </div>
            {error && (
              <p className="mt-1 text-sm text-red-500">
                Incorrect password. Please try again.
              </p>
            )}
          </div>
          <button
            type="submit"
            className="w-full py-2 bg-black text-white rounded-md hover:bg-gray-800 transition-colors"
          >
            Enter Demo
          </button>
        </form>
        <p className="text-xs text-gray-500 text-center mt-4">
          This is an early preview of AFFINITY. 
          Contact the team for access credentials.
        </p>
      </DialogContent>
    </Dialog>
  )
}