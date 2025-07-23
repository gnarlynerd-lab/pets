"use client"

import { useState, useEffect, useRef } from 'react'
import BlobPetDisplay from '@/components/blob-pet-display'
import EmojiInteraction from '@/components/emoji-interaction'
import UserInsightsPanel from '@/components/user-insights-panel'
import { AuthDialog } from '@/components/auth/auth-dialog'
import { UserMenu } from '@/components/auth/user-menu'
import { SaveCompanionBanner } from '@/components/save-companion-banner'
import { SessionInfo } from '@/components/session-info'
import { ClientOnly } from '@/components/client-only'
import { EnvironmentStatus } from '@/components/environment-status'
import { CompanionAutonomy } from '@/components/companion-autonomy'
import { useAuthenticatedPetState } from '@/hooks/use-authenticated-pet-state'
import { useAuth } from '@/contexts/auth-context'

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
    refreshPetState,
    userPets,
    isAuthenticated,
    sessionId,
    migrateAnonymousData
  } = useAuthenticatedPetState()

  const [isEditingName, setIsEditingName] = useState(false)
  const [tempPetName, setTempPetName] = useState(petName || '')
  const [userInsights, setUserInsights] = useState(null)
  const [showUserInsights, setShowUserInsights] = useState(false)
  const [authDialogOpen, setAuthDialogOpen] = useState(false)
  const [migrationStatus, setMigrationStatus] = useState<{ 
    isComplete: boolean
    message?: string 
  }>({ isComplete: false })

  // Update tempPetName when petName changes
  useEffect(() => {
    setTempPetName(petName || '')
  }, [petName])

  // Auto-migrate anonymous data when user authenticates
  useEffect(() => {
    if (isAuthenticated && sessionId && !migrationStatus.isComplete) {
      const performMigration = async () => {
        console.log('Attempting to migrate anonymous data...', { sessionId })
        const result = await migrateAnonymousData()
        
        if (result.success) {
          setMigrationStatus({ 
            isComplete: true, 
            message: `Successfully saved your companion! ${result.interactionsMigrated} interactions migrated.` 
          })
          console.log('Migration successful:', result)
        } else {
          console.error('Migration failed:', result.error)
          setMigrationStatus({ 
            isComplete: true, 
            message: `Failed to migrate data: ${result.error}` 
          })
        }
      }
      
      performMigration()
    }
  }, [isAuthenticated, sessionId, migrationStatus.isComplete, migrateAnonymousData])
  const chatEndRef = useRef<HTMLDivElement>(null)
  const chatContainerRef = useRef<HTMLDivElement>(null)

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    // Use setTimeout to ensure DOM is updated before scrolling
    setTimeout(() => {
      if (chatContainerRef.current) {
        chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight
      }
    }, 100)
  }, [interactionHistory])

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

  // Enhanced emoji interaction handler to capture user insights
  const handleEmojiInteraction = async (emojiSequence: string) => {
    const result = await sendEmojiInteraction(emojiSequence)
    if (result && result.user_insights) {
      setUserInsights(result.user_insights)
      setShowUserInsights(true)
    }
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-50 to-indigo-50">
      <div className="container mx-auto px-4 py-8">
        {/* Header with Auth */}
        <div className="flex justify-between items-start mb-8">
          <div className="text-center flex-1">
            <h1 className="text-4xl md:text-6xl font-bold text-indigo-700 mb-2 font-sans">
              Digital Ecosystem
            </h1>
            <p className="text-slate-600 text-lg font-sans">
              Connect with autonomous digital companions
            </p>
          </div>
          
          {/* User Menu */}
          <div className="flex-shrink-0 ml-4">
            <UserMenu onOpenAuth={() => setAuthDialogOpen(true)} />
          </div>
        </div>

        {/* Auth Dialog */}
        <AuthDialog 
          open={authDialogOpen} 
          onOpenChange={setAuthDialogOpen}
        />

        {/* Main content */}
        <div className="max-w-7xl mx-auto">
          {/* Three Column Layout: Pet, Chat, and Insights */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Pet Display Area */}
            <div className="flex justify-center">
              <BlobPetDisplay 
                petData={petData}
                petResponse={petResponse}
                isLoading={isLoading}
                petName={petName}
              />
            </div>

            {/* Chat and Interaction Area */}
            <div className="space-y-6">
              {/* Chat History */}
              <div className="bg-white/95 backdrop-blur-sm rounded-2xl shadow-xl border border-slate-200/50 p-6 hover:shadow-2xl transition-all duration-300">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-xl font-semibold text-indigo-700 font-sans">Conversation</h3>
              
              {/* Pet Name Editor */}
              <div className="flex items-center gap-2">
                {isEditingName ? (
                  <>
                    <input
                      type="text"
                      value={tempPetName}
                      onChange={(e) => setTempPetName(e.target.value)}
                      className="text-sm px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                      placeholder="Companion name..."
                      maxLength={20}
                    />
                    <button
                      onClick={handleNameSave}
                      className="bg-gradient-to-r from-indigo-500 to-indigo-600 hover:from-indigo-600 hover:to-indigo-700 text-white text-sm px-4 py-2 rounded-lg font-medium transition-all duration-200 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 active:translate-y-0"
                    >
                      Save
                    </button>
                    <button
                      onClick={handleNameCancel}
                      className="border border-slate-300 hover:border-slate-400 text-slate-600 hover:text-slate-700 text-sm px-4 py-2 rounded-lg font-medium transition-all duration-200 hover:bg-slate-50 shadow-md hover:shadow-lg transform hover:-translate-y-0.5 active:translate-y-0"
                    >
                      Cancel
                    </button>
                  </>
                ) : (
                  <button
                    onClick={() => setIsEditingName(true)}
                    className="text-indigo-600 hover:text-indigo-700 hover:bg-indigo-50 text-sm px-3 py-2 rounded-lg font-medium transition-all duration-200 hover:shadow-md transform hover:-translate-y-0.5 active:translate-y-0"
                  >
                    {petName ? `Companion: ${petName}` : 'Meet Companion'}
                  </button>
                )}
              </div>
            </div>
            
            <div 
              ref={chatContainerRef}
              className="bg-slate-50/70 rounded-2xl p-6 h-96 overflow-y-auto space-y-4 scrollbar-thin scrollbar-thumb-slate-300 scrollbar-track-slate-100"
            >
              {interactionHistory.length === 0 ? (
                <div className="text-center text-slate-500 text-sm font-sans py-12">
                  No conversations yet. Connect with your companion! 👋
                </div>
              ) : (
                <>
                  {interactionHistory.slice(-20).map((interaction, index) => (
                    <div key={`${interaction.timestamp || index}-${index}`} className="space-y-2">
                      {/* User message */}
                      <div className="flex justify-end">
                        <div className="bg-gradient-to-br from-indigo-100 to-indigo-200 rounded-2xl px-4 py-3 max-w-xs shadow-lg border border-indigo-200/30 hover:shadow-xl transition-all duration-200">
                          <div className="text-xl">
                            {interaction.userEmojis}
                          </div>
                          <div className="text-xs text-indigo-600 mt-1 font-medium">You</div>
                        </div>
                      </div>
                      
                      {/* Pet response */}
                      <div className="flex justify-start">
                        <div className="bg-gradient-to-br from-slate-100 to-slate-200 rounded-2xl px-4 py-3 max-w-xs shadow-lg border border-slate-200/30 hover:shadow-xl transition-all duration-200">
                          <div className="text-xl">
                            {interaction.petResponse}
                          </div>
                          <div className="text-xs text-slate-600 mt-1 font-medium">{petName || 'Companion'}</div>
                        </div>
                      </div>
                    </div>
                  ))}

                </>
              )}
            </div>
          </div>

              {/* Emoji Communication Interface */}
              <div>
                <EmojiInteraction 
                  onSendEmoji={handleEmojiInteraction}
                  isLoading={isLoading}
                />
              </div>
            </div>

            {/* User Insights Panel */}
            <div className="space-y-6">
              <UserInsightsPanel
                petId={petData?.id || ''}
                userId={user?.user_id || "frontend_user"}
                userInsights={userInsights}
                onRefresh={() => {
                  // Could implement refresh logic here
                  console.log('Refreshing user insights...')
                }}
              />
              
              {/* Session Status */}
              <ClientOnly fallback={
                <div className="bg-gradient-to-r from-gray-50 to-gray-100 rounded-xl p-3 border border-gray-200">
                  <div className="flex items-center gap-2">
                    <div className="w-4 h-4 bg-gray-300 rounded-full animate-pulse"></div>
                    <div className="flex-1">
                      <div className="w-20 h-4 bg-gray-300 rounded animate-pulse mb-1"></div>
                      <div className="w-32 h-3 bg-gray-200 rounded animate-pulse"></div>
                    </div>
                  </div>
                </div>
              }>
                <SessionInfo
                  isAuthenticated={isAuthenticated}
                  sessionId={sessionId}
                  petName={petName}
                  interactionCount={interactionHistory.length}
                  onSignIn={() => setAuthDialogOpen(true)}
                />
              </ClientOnly>

              {/* Environment Intelligence */}
              <ClientOnly fallback={
                <div className="bg-white/90 backdrop-blur-sm rounded-xl p-4 border border-indigo-200 shadow-lg">
                  <div className="flex items-center gap-2 mb-3">
                    <div className="w-6 h-6 bg-indigo-100 rounded-full animate-pulse"></div>
                    <div className="w-24 h-5 bg-indigo-100 rounded animate-pulse"></div>
                  </div>
                  <div className="space-y-2">
                    <div className="w-full h-3 bg-indigo-50 rounded animate-pulse"></div>
                    <div className="w-3/4 h-3 bg-indigo-50 rounded animate-pulse"></div>
                  </div>
                </div>
              }>
                <EnvironmentStatus
                  companionCount={petData ? 1 : 0}
                  activeConnections={interactionHistory.length > 0 ? 1 : 0}
                />
              </ClientOnly>

              {/* Companion Autonomy */}
              <ClientOnly fallback={
                <div className="bg-white/90 backdrop-blur-sm rounded-xl p-4 border border-emerald-200 shadow-lg">
                  <div className="flex items-center gap-2 mb-3">
                    <div className="w-6 h-6 bg-emerald-100 rounded-full animate-pulse"></div>
                    <div className="w-32 h-5 bg-emerald-100 rounded animate-pulse"></div>
                  </div>
                  <div className="space-y-2">
                    <div className="w-full h-3 bg-emerald-50 rounded animate-pulse"></div>
                    <div className="w-2/3 h-3 bg-emerald-50 rounded animate-pulse"></div>
                  </div>
                </div>
              }>
                <CompanionAutonomy
                  petData={petData}
                  interactionCount={interactionHistory.length}
                />
              </ClientOnly>

              {/* Peer Relationship Status */}
              <div className="bg-white/95 backdrop-blur-sm rounded-2xl p-6 border border-amber-200/30 shadow-xl hover:shadow-2xl transition-all duration-300">
                <h3 className="text-lg font-semibold text-amber-700 font-sans mb-3">
                  Peer Connection
                </h3>
                <p className="text-sm text-amber-600 leading-relaxed">
                  Your companion learns and grows through authentic interaction! We're building relationships together. 🤝
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Save Companion Banner for anonymous users */}
      <ClientOnly>
        {!isAuthenticated && (
          <SaveCompanionBanner
            onSignIn={() => setAuthDialogOpen(true)}
            petName={petName}
            interactionCount={interactionHistory.length}
          />
        )}
      </ClientOnly>

      {/* Migration Success Notification */}
      <ClientOnly>
        {migrationStatus.isComplete && migrationStatus.message && (
          <div className="fixed top-4 right-4 max-w-sm animate-slide-up">
            <div className="bg-green-600 text-white rounded-xl p-4 shadow-xl">
              <div className="flex items-start gap-2">
                <div className="text-2xl">✨</div>
                <div className="flex-1">
                  <h3 className="font-semibold text-sm mb-1">Migration Complete!</h3>
                  <p className="text-xs text-green-100">{migrationStatus.message}</p>
                </div>
                <button
                  onClick={() => setMigrationStatus(prev => ({ ...prev, message: undefined }))}
                  className="text-green-200 hover:text-white text-xl leading-none"
                >
                  ×
                </button>
              </div>
            </div>
          </div>
        )}
      </ClientOnly>
    </main>
  )
}
