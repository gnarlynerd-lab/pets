"use client"

import { useState, useEffect, useRef } from 'react'
import BlobPetDisplay from '@/components/blob-pet-display'
import EmojiInteraction from '@/components/emoji-interaction'
import UserInsightsPanel from '@/components/user-insights-panel'
import { usePetState } from '@/hooks/use-pet-state'

export default function Home() {
  const {
    petData,
    isLoading,
    sendEmojiInteraction,
    petResponse,
    interactionHistory,
    petName,
    updatePetName,
    refreshPetState
  } = usePetState()

  const [isEditingName, setIsEditingName] = useState(false)
  const [tempPetName, setTempPetName] = useState(petName || '')
  const [userInsights, setUserInsights] = useState(null)
  const [showUserInsights, setShowUserInsights] = useState(false)

  // Update tempPetName when petName changes
  useEffect(() => {
    setTempPetName(petName || '')
  }, [petName])
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
    <main className="min-h-screen bg-gradient-to-br from-pink-50 to-purple-50">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl md:text-6xl font-bold text-pink-700 mb-2 font-sans">
            Digital Pets
          </h1>
          <p className="text-purple-600 text-lg font-sans">
            Chat with your blob friend using emojis
          </p>
        </div>

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
              <div className="bg-white/90 backdrop-blur-sm rounded-3xl shadow-lg border-2 border-pink-200 p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-pink-700 font-sans">Chat History</h3>
              
              {/* Pet Name Editor */}
              <div className="flex items-center gap-2">
                {isEditingName ? (
                  <>
                    <input
                      type="text"
                      value={tempPetName}
                      onChange={(e) => setTempPetName(e.target.value)}
                      className="text-sm px-2 py-1 border border-pink-300 rounded-md focus:outline-none focus:ring-2 focus:ring-pink-500"
                      placeholder="Pet name..."
                      maxLength={20}
                    />
                    <button
                      onClick={handleNameSave}
                      className="bg-pink-500 hover:bg-pink-600 text-white text-xs px-2 py-1 rounded"
                    >
                      Save
                    </button>
                    <button
                      onClick={handleNameCancel}
                      className="border border-pink-300 text-pink-600 text-xs px-2 py-1 rounded"
                    >
                      Cancel
                    </button>
                  </>
                ) : (
                  <button
                    onClick={() => setIsEditingName(true)}
                    className="text-pink-600 hover:bg-pink-50 text-xs px-2 py-1 rounded"
                  >
                    {petName ? `Name: ${petName}` : 'Name Pet'}
                  </button>
                )}
              </div>
            </div>
            
            <div 
              ref={chatContainerRef}
              className="bg-pink-50/70 rounded-2xl p-4 h-48 overflow-y-auto space-y-3 scrollbar-thin scrollbar-thumb-pink-300 scrollbar-track-pink-100"
            >
              {interactionHistory.length === 0 ? (
                <div className="text-center text-pink-600 text-sm font-sans py-8">
                  No conversations yet. Start chatting! 👋
                </div>
              ) : (
                <>
                  {interactionHistory.slice(-20).map((interaction, index) => (
                    <div key={`${interaction.timestamp || index}-${index}`} className="space-y-2">
                      {/* User message */}
                      <div className="flex justify-end">
                        <div className="bg-purple-100 rounded-2xl px-3 py-2 max-w-xs shadow-sm">
                          <div className="text-lg">
                            {interaction.userEmojis}
                          </div>
                          <div className="text-xs text-purple-600 mt-1">You</div>
                        </div>
                      </div>
                      
                      {/* Pet response */}
                      <div className="flex justify-start">
                        <div className="bg-pink-100 rounded-2xl px-3 py-2 max-w-xs shadow-sm">
                          <div className="text-lg">
                            {interaction.petResponse}
                          </div>
                          <div className="text-xs text-pink-600 mt-1">{petName || 'Pet'}</div>
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
                userId="frontend_user"
                userInsights={userInsights}
                onRefresh={() => {
                  // Could implement refresh logic here
                  console.log('Refreshing user insights...')
                }}
              />
              
              {/* Relationship Toggle */}
              <div className="bg-white/90 backdrop-blur-sm rounded-xl p-4 border border-pink-200 shadow-lg">
                <div className="flex items-center justify-between">
                  <h3 className="text-lg font-semibold text-pink-700 font-sans">
                    Relationship Features
                  </h3>
                  <button
                    onClick={() => setShowUserInsights(!showUserInsights)}
                    className="text-sm text-pink-600 hover:bg-pink-50 px-3 py-1 rounded-md border border-pink-200"
                  >
                    {showUserInsights ? 'Hide' : 'Show'} Insights
                  </button>
                </div>
                <p className="text-sm text-pink-600 mt-2">
                  Your pet learns about you and adapts to your communication style! 💕
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  )
}
