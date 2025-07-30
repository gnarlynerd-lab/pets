"use client"

import { useState, useEffect, useRef } from 'react'
import { useAuthenticatedPetState } from '@/hooks/use-authenticated-pet-state'
import { AuthDialog } from '@/components/auth/auth-dialog'
import { UserMenu } from '@/components/auth/user-menu'
import { ClientOnly } from '@/components/client-only'
import { useAuth } from '@/contexts/auth-context'
import { DemoBanner } from '@/components/demo-banner'
import EmojiPicker from 'emoji-picker-react'

export default function Home() {
  const { user } = useAuth()
  const {
    petData,
    isLoading,
    sendEmojiInteraction,
    petResponse,
    interactionHistory,
    petName,
    updatePetName,
    isAuthenticated,
    sessionId,
    migrateAnonymousData
  } = useAuthenticatedPetState()

  const [currentEmoji, setCurrentEmoji] = useState('')
  const [showEmojiPicker, setShowEmojiPicker] = useState(false)
  const [isEditingName, setIsEditingName] = useState(false)
  const [tempPetName, setTempPetName] = useState(petName || '')
  const [authDialogOpen, setAuthDialogOpen] = useState(false)
  const [migrationStatus, setMigrationStatus] = useState<{ 
    isComplete: boolean
    message?: string 
  }>({ isComplete: false })
  
  const chatContainerRef = useRef<HTMLDivElement>(null)
  const emojiPickerRef = useRef<HTMLDivElement>(null)

  // Update tempPetName when petName changes
  useEffect(() => {
    setTempPetName(petName || '')
  }, [petName])

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    setTimeout(() => {
      if (chatContainerRef.current) {
        chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight
      }
    }, 100)
  }, [interactionHistory])

  // Close emoji picker when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (emojiPickerRef.current && !emojiPickerRef.current.contains(event.target as Node)) {
        setShowEmojiPicker(false)
      }
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  // Auto-migrate anonymous data when user authenticates
  useEffect(() => {
    if (isAuthenticated && sessionId && !migrationStatus.isComplete) {
      const performMigration = async () => {
        const result = await migrateAnonymousData()
        if (result.success) {
          setMigrationStatus({ 
            isComplete: true, 
            message: `Successfully saved your companion! ${result.interactionsMigrated} interactions migrated.` 
          })
        }
      }
      performMigration()
    }
  }, [isAuthenticated, sessionId, migrationStatus.isComplete, migrateAnonymousData])

  const handleEmojiSend = () => {
    if (currentEmoji.trim()) {
      sendEmojiInteraction(currentEmoji.trim())
      setCurrentEmoji('')
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleEmojiSend()
    }
  }

  const handleNameSave = () => {
    if (tempPetName.trim()) {
      updatePetName(tempPetName.trim())
    }
    setIsEditingName(false)
  }

  const handleNameCancel = () => {
    setTempPetName(petName || '')
    setIsEditingName(false)
  }

  const onEmojiClick = (emojiObject: any) => {
    setCurrentEmoji(prev => prev + emojiObject.emoji)
  }

  const quickEmojis = ['👋', '❤️', '😊', '🤔', '👍', '😴', '🍎', '🎮']
  const companionName = petName || 'Companion'

  return (
    <div className="min-h-screen bg-white text-black font-mono">
      {/* Demo Banner */}
      <DemoBanner 
        interactionCount={interactionHistory.length}
        maxInteractions={50}
      />
      
      <div className="max-w-4xl mx-auto p-8 pt-12">
        
        {/* Header with Auth */}
        <div className="border-b border-black pb-4 mb-8">
          <div className="flex justify-between items-center">
            <div>
              {isEditingName ? (
                <div className="flex items-center gap-2">
                  <input
                    type="text"
                    value={tempPetName}
                    onChange={(e) => setTempPetName(e.target.value)}
                    className="text-2xl font-bold tracking-tight px-2 py-1 border border-black focus:outline-none"
                    placeholder="Companion name..."
                    maxLength={20}
                  />
                  <button
                    onClick={handleNameSave}
                    className="px-3 py-1 bg-black text-white text-sm hover:bg-gray-800"
                  >
                    Save
                  </button>
                  <button
                    onClick={handleNameCancel}
                    className="px-3 py-1 border border-black text-sm hover:bg-gray-100"
                  >
                    Cancel
                  </button>
                </div>
              ) : (
                <h1 
                  className="text-2xl font-bold tracking-tight cursor-pointer hover:text-gray-600"
                  onClick={() => setIsEditingName(true)}
                >
                  {companionName}
                </h1>
              )}
            </div>
            
            {/* User Menu - Hide in demo mode */}
            {process.env.NEXT_PUBLIC_DEMO_MODE !== 'true' && (
              <UserMenu onOpenAuth={() => setAuthDialogOpen(true)} />
            )}
          </div>
        </div>

        {/* Auth Dialog */}
        <AuthDialog 
          open={authDialogOpen} 
          onOpenChange={setAuthDialogOpen}
        />

        {/* Main Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-12">
          
          {/* Left: Companion Display */}
          <div className="space-y-6">
            {/* Companion Visual */}
            <div className="border border-black h-64 overflow-hidden relative bg-black flex items-center justify-center">
              {/* Companion Name */}
              <div className="absolute top-4 left-4 z-10">
                <div className="text-white font-bold text-sm">
                  {companionName}
                </div>
              </div>
              
              {/* Large Emoji Display */}
              <div className="text-center">
                <div className="text-8xl animate-pulse">
                  {isLoading ? '💭' : (petResponse || '😊')}
                </div>
              </div>
              
              {/* Custom CSS for breathing animation */}
              <style jsx>{`
                @keyframes breathe {
                  0%, 100% { transform: scale(1); }
                  50% { transform: scale(1.05); }
                }
              `}</style>
            </div>

            {/* Status */}
            <div className="border border-black p-4 space-y-2 text-sm">
              <div className="grid grid-cols-2 gap-4">
                <div>Energy: {Math.round(petData?.energy || 0)}%</div>
                <div>Mood: {Math.round(petData?.mood || 0)}%</div>
                <div>Health: {Math.round(petData?.health || 0)}%</div>
                <div>Attention: {Math.round(petData?.attention || 0)}%</div>
              </div>
            </div>
          </div>

          {/* Right: Communication */}
          <div className="space-y-6">
            
            {/* Conversation */}
            <div className="border border-black h-64 overflow-hidden">
              <div className="border-b border-black p-2 text-sm font-bold">
                Conversation
              </div>
              <div 
                ref={chatContainerRef}
                className="p-4 h-48 overflow-y-auto space-y-3 text-sm"
              >
                {interactionHistory.length === 0 ? (
                  <div className="text-gray-600 italic">
                    Start a conversation...
                  </div>
                ) : (
                  interactionHistory.slice(-10).map((interaction, index) => (
                    <div key={index} className="space-y-1">
                      <div className="flex gap-2">
                        <span className="font-bold">You:</span>
                        <span>{interaction.userEmojis}</span>
                      </div>
                      <div className="flex gap-2">
                        <span className="font-bold">{companionName}:</span>
                        <span>{interaction.petResponse}</span>
                      </div>
                    </div>
                  ))
                )}
              </div>
            </div>

            {/* Input and Controls */}
            <div className="space-y-3">
              {/* Input with emoji picker */}
              <div className="border border-black relative">
                <input
                  type="text"
                  value={currentEmoji}
                  onChange={(e) => setCurrentEmoji(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="Type emojis here..."
                  className="w-full p-4 pr-12 text-lg font-mono bg-white border-none outline-none"
                  disabled={isLoading}
                />
                
                {/* Emoji Picker Button */}
                <div className="absolute right-2 top-1/2 -translate-y-1/2" ref={emojiPickerRef}>
                  <button
                    onClick={() => setShowEmojiPicker(!showEmojiPicker)}
                    className="w-8 h-8 bg-gray-500 hover:bg-gray-600 rounded-full flex items-center justify-center transition-colors"
                    title="Emoji picker"
                  >
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                      <circle cx="12" cy="12" r="10"/>
                      <path d="M8 14s1.5 2 4 2 4-2 4-2"/>
                      <circle cx="9" cy="9" r="1" fill="white"/>
                      <circle cx="15" cy="9" r="1" fill="white"/>
                    </svg>
                  </button>
                  {showEmojiPicker && (
                    <div className="absolute bottom-full mb-2 right-0 z-[9999] shadow-2xl">
                      <EmojiPicker
                        onEmojiClick={onEmojiClick}
                        height={250}
                        width={250}
                        searchDisabled={true}
                        skinTonesDisabled={true}
                        previewConfig={{ showPreview: false }}
                        lazyLoadEmojis={true}
                        emojiStyle="native"
                        categories={[
                          'smileys_people',
                          'animals_nature',
                          'food_drink',
                          'activities'
                        ]}
                      />
                    </div>
                  )}
                </div>
              </div>

              
              {/* Send button */}
              <button
                onClick={handleEmojiSend}
                disabled={!currentEmoji.trim() || isLoading}
                className="w-full py-3 bg-black text-white rounded-full hover:bg-gray-800 transition-colors disabled:opacity-50 disabled:cursor-not-allowed font-bold text-lg"
              >
                {isLoading ? 'Sending...' : 'Send'}
              </button>
            </div>

            {/* Stats */}
            <div className="border border-black p-4 text-xs space-y-2">
              <div>Total interactions: {interactionHistory.length}</div>
              <div>Session: {process.env.NEXT_PUBLIC_DEMO_MODE === 'true' ? 'Demo' : (isAuthenticated ? 'Authenticated' : 'Anonymous')}</div>
              <div>Connection: Active</div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="border-t border-gray-300 pt-8 mt-16">
          <div className="text-left">
            <div className="text-xs font-mono tracking-wide mb-1" style={{ color: '#006666' }}>
              AFFINITY v0.1
            </div>
            <div className="text-xs text-gray-400">
              Interactive Companion Platform
            </div>
          </div>
        </div>
      </div>


      {/* Migration Success Notification */}
      <ClientOnly>
        {migrationStatus.isComplete && migrationStatus.message && (
          <div className="fixed top-4 right-4 max-w-sm animate-slide-up">
            <div className="bg-black text-white p-4 shadow-lg">
              <div className="flex items-start gap-2">
                <div className="text-xl">✨</div>
                <div className="flex-1">
                  <h3 className="font-semibold text-sm mb-1">Migration Complete!</h3>
                  <p className="text-xs">{migrationStatus.message}</p>
                </div>
                <button
                  onClick={() => setMigrationStatus(prev => ({ ...prev, message: undefined }))}
                  className="text-gray-300 hover:text-white text-xl leading-none"
                >
                  ×
                </button>
              </div>
            </div>
          </div>
        )}
      </ClientOnly>
    </div>
  )
}