"use client"
import PetCanvas from "@/components/pet-canvas"
import EmojiCommunication from "@/components/emoji-communication"
import InteractionControls from "@/components/interaction-controls"
import StatDisplay from "@/components/stat-display"
import StageIndicator from "@/components/stage-indicator"
import { usePetState } from "@/hooks/use-pet-state"
import UserEmojiInput from "@/components/user-emoji-input"

export default function Home() {
  const {
    petStats,
    petStage,
    relationshipStrength,
    currentMessage,
    handleFeed,
    handlePlay,
    handlePet,
    handleUserEmoji,
    emojiHistory,
    petResponse,
  } = usePetState()

  return (
    <main className="min-h-screen p-4 md:p-8 bg-gradient-to-b from-[#1a2f2f] to-[#2F4F4F] relative overflow-hidden">
      {/* Laboratory Grid Background */}
      <div className="absolute inset-0 opacity-10">
        <div
          className="w-full h-full"
          style={{
            backgroundImage: `
            linear-gradient(rgba(70, 130, 180, 0.3) 1px, transparent 1px),
            linear-gradient(90deg, rgba(70, 130, 180, 0.3) 1px, transparent 1px)
          `,
            backgroundSize: "20px 20px",
          }}
        ></div>
      </div>

      <div className="max-w-5xl mx-auto relative z-10">
        <h1 className="text-4xl font-bold text-center mb-8 text-[#4682B4] font-mono tracking-wider">
          <span className="bg-gradient-to-r from-[#4682B4] to-[#FF6347] bg-clip-text text-transparent">
            DKS LABORATORY
          </span>
          <div className="text-sm font-normal text-[#8A6C3C] mt-2">Digital Kinetic Systems Research Facility</div>
        </h1>

        <div className="flex flex-col lg:flex-row gap-8">
          <div className="flex-1 flex flex-col">
            {/* Laboratory Container */}
            <div className="relative bg-gradient-to-b from-[#2F4F4F] to-[#1a2f2f] rounded-2xl shadow-2xl border-4 border-[#8A6C3C] overflow-hidden">
              {/* Container Frame with Measurements */}
              <div className="absolute inset-0 border-8 border-[#8A6C3C] rounded-2xl pointer-events-none">
                {/* Measurement Markings */}
                <div className="absolute left-2 top-4 bottom-4 w-4 flex flex-col justify-between text-xs text-[#8A6C3C] font-mono">
                  {Array.from({ length: 11 }).map((_, i) => (
                    <div key={i} className="flex items-center">
                      <div className="w-2 h-px bg-[#8A6C3C]"></div>
                      <span className="ml-1">{100 - i * 10}</span>
                    </div>
                  ))}
                </div>
                <div className="absolute bottom-2 left-8 right-8 h-4 flex justify-between text-xs text-[#8A6C3C] font-mono">
                  {Array.from({ length: 11 }).map((_, i) => (
                    <div key={i} className="flex flex-col items-center">
                      <div className="w-px h-2 bg-[#8A6C3C]"></div>
                      <span className="mt-1">{i * 10}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Glass Effect Overlay */}
              <div className="absolute inset-4 bg-gradient-to-br from-white/10 via-transparent to-white/5 rounded-xl pointer-events-none"></div>
              <div className="absolute top-4 left-4 w-16 h-32 bg-gradient-to-br from-white/20 to-transparent rounded-lg blur-sm pointer-events-none"></div>

              <EmojiCommunication
                message={currentMessage}
                petStage={petStage}
                relationshipStrength={relationshipStrength}
              />
              <PetCanvas />

              {/* Bubble Effects */}
              <div className="absolute inset-0 pointer-events-none">
                {Array.from({ length: 3 }).map((_, i) => (
                  <div
                    key={i}
                    className="absolute w-2 h-2 bg-[#4682B4]/30 rounded-full animate-bounce"
                    style={{
                      left: `${20 + i * 30}%`,
                      bottom: "10%",
                      animationDelay: `${i * 0.5}s`,
                      animationDuration: "3s",
                    }}
                  ></div>
                ))}
              </div>
            </div>

            <UserEmojiInput onSendEmoji={handleUserEmoji} emojiHistory={emojiHistory} petResponse={petResponse} />

            <InteractionControls onFeed={handleFeed} onPlay={handlePlay} onPet={handlePet} />
          </div>

          <div className="w-full lg:w-80 space-y-6">
            <StatDisplay stats={petStats} relationshipStrength={relationshipStrength} />
            <StageIndicator stage={petStage} />
          </div>
        </div>
      </div>
    </main>
  )
}
