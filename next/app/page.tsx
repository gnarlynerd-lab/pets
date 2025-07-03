"use client"

import { useState, useEffect } from 'react'
import PetDisplay from '@/components/pet-display'
import EmojiInteraction from '@/components/emoji-interaction'
import PetStats from '@/components/pet-stats'
import { usePetState } from '@/hooks/use-pet-state'

export default function Home() {
  const {
    petData,
    isLoading,
    sendEmojiInteraction,
    petResponse,
    interactionHistory,
    refreshPetState
  } = usePetState()

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 relative overflow-hidden">
      {/* Animated background grid */}
      <div className="absolute inset-0 opacity-20">
        <div
          className="w-full h-full"
          style={{
            backgroundImage: `
              linear-gradient(rgba(147, 197, 253, 0.1) 1px, transparent 1px),
              linear-gradient(90deg, rgba(147, 197, 253, 0.1) 1px, transparent 1px)
            `,
            backgroundSize: "50px 50px",
          }}
        />
      </div>

      <div className="relative z-10 container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl md:text-6xl font-bold bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 bg-clip-text text-transparent mb-2">
            DKS Emoji Pet
          </h1>
          <p className="text-slate-300 text-lg">
            Your digital companion that speaks in emojis
          </p>
        </div>

        {/* Main content grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 max-w-6xl mx-auto">
          
          {/* Pet Display - Main area */}
          <div className="lg:col-span-2">
            <PetDisplay 
              petData={petData}
              petResponse={petResponse}
              isLoading={isLoading}
            />
          </div>

          {/* Side panel - Stats and controls */}
          <div className="space-y-6">
            <PetStats petData={petData} />
            
            {/* Interaction history */}
            <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-4 border border-slate-700">
              <h3 className="text-lg font-semibold text-white mb-3">Recent Interactions</h3>
              <div className="space-y-2 max-h-40 overflow-y-auto">
                {interactionHistory.slice(-5).reverse().map((interaction, index) => (
                  <div key={index} className="flex items-center justify-between text-sm">
                    <span className="text-slate-300">You: {interaction.userEmojis}</span>
                    <span className="text-blue-400">Pet: {interaction.petResponse}</span>
                  </div>
                ))}
                {interactionHistory.length === 0 && (
                  <p className="text-slate-500 text-sm italic">No interactions yet...</p>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Emoji interaction panel - Bottom */}
        <div className="mt-8">
          <EmojiInteraction 
            onSendEmoji={sendEmojiInteraction}
            isLoading={isLoading}
          />
        </div>
      </div>
    </main>
  )
}
