"use client"
import { Heart, Brain, Sparkles, Users, Activity, Zap } from "lucide-react"

interface PetStats {
  energy: number
  mood: number
  attention: number
  evolutionProgress: number
}

interface StatDisplayProps {
  stats: PetStats
  relationshipStrength: number
}

export default function StatDisplay({ stats, relationshipStrength }: StatDisplayProps) {
  const getRelationshipLabel = (strength: number) => {
    if (strength >= 80) return "SYMBIOTIC"
    if (strength >= 60) return "BONDED"
    if (strength >= 40) return "RESPONSIVE"
    if (strength >= 20) return "OBSERVED"
    return "SPECIMEN"
  }

  return (
    <div className="bg-gradient-to-br from-[#2F4F4F] to-[#1a2f2f] p-6 rounded-2xl shadow-2xl border-2 border-[#8A6C3C] font-mono">
      <h2 className="text-lg font-bold mb-6 text-[#FF6347] flex items-center">
        <Activity className="h-5 w-5 mr-2" />
        MONITORING SYSTEMS
      </h2>

      <div className="space-y-6">
        {/* Energy - Fluid Tube */}
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <Zap className="w-4 h-4 mr-2 text-[#FF6347]" />
              <span className="text-sm font-bold text-[#4682B4]">ENERGY LEVELS</span>
            </div>
            <span className="text-xs text-[#8A6C3C]">{stats.energy}%</span>
          </div>
          <div className="relative h-6 bg-[#1a2f2f] rounded-full border border-[#8A6C3C] overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-[#4682B4] to-[#FF6347] transition-all duration-500 relative"
              style={{ width: `${stats.energy}%` }}
            >
              <div className="absolute inset-0 bg-gradient-to-t from-white/20 to-transparent"></div>
              {/* Bubble effect */}
              <div className="absolute top-1 left-2 w-2 h-2 bg-white/40 rounded-full animate-pulse"></div>
            </div>
            {/* Measurement marks */}
            {Array.from({ length: 5 }).map((_, i) => (
              <div
                key={i}
                className="absolute top-0 bottom-0 w-px bg-[#8A6C3C]/50"
                style={{ left: `${i * 25}%` }}
              ></div>
            ))}
          </div>
        </div>

        {/* Mood - Oscilloscope */}
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <Heart className="w-4 h-4 mr-2 text-[#FF6347]" />
              <span className="text-sm font-bold text-[#4682B4]">MOOD FREQUENCY</span>
            </div>
            <span className="text-xs text-[#8A6C3C]">{stats.mood}%</span>
          </div>
          <div className="h-12 bg-[#1a2f2f] rounded border border-[#8A6C3C] relative overflow-hidden">
            <svg className="w-full h-full" viewBox="0 0 200 48">
              <path
                d={`M 0 24 ${Array.from({ length: 20 })
                  .map((_, i) => `L ${i * 10} ${24 - Math.sin(i * 0.5 + Date.now() * 0.01) * (stats.mood / 100) * 20}`)
                  .join(" ")}`}
                stroke="#FF6347"
                strokeWidth="2"
                fill="none"
                className="animate-pulse"
              />
              <defs>
                <linearGradient id="waveGlow" x1="0%" y1="0%" x2="100%" y2="0%">
                  <stop offset="0%" stopColor="#FF6347" stopOpacity="0.8" />
                  <stop offset="100%" stopColor="#4682B4" stopOpacity="0.3" />
                </linearGradient>
              </defs>
            </svg>
          </div>
        </div>

        {/* Attention - Laboratory Graph */}
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <Brain className="w-4 h-4 mr-2 text-[#FF6347]" />
              <span className="text-sm font-bold text-[#4682B4]">ATTENTION MATRIX</span>
            </div>
            <span className="text-xs text-[#8A6C3C]">{stats.attention}%</span>
          </div>
          <div className="h-8 bg-[#1a2f2f] rounded border border-[#8A6C3C] relative overflow-hidden flex items-end justify-center">
            {Array.from({ length: 10 }).map((_, i) => (
              <div
                key={i}
                className="w-3 bg-gradient-to-t from-[#4682B4] to-[#FF6347] mx-px transition-all duration-300"
                style={{
                  height: `${Math.min(100, stats.attention + (Math.random() - 0.5) * 20)}%`,
                  opacity: i < stats.attention / 10 ? 1 : 0.3,
                }}
              ></div>
            ))}
          </div>
        </div>

        {/* Evolution - DNA Strand */}
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <Sparkles className="w-4 h-4 mr-2 text-[#FF6347]" />
              <span className="text-sm font-bold text-[#4682B4]">EVOLUTION SEQUENCE</span>
            </div>
            <span className="text-xs text-[#8A6C3C]">{stats.evolutionProgress}%</span>
          </div>
          <div className="h-8 bg-[#1a2f2f] rounded border border-[#8A6C3C] relative overflow-hidden">
            <div className="absolute inset-0 flex items-center">
              <svg className="w-full h-6" viewBox="0 0 200 24">
                <path
                  d="M 0 12 Q 25 6 50 12 T 100 12 T 150 12 T 200 12"
                  stroke="#FF6347"
                  strokeWidth="2"
                  fill="none"
                  strokeDasharray={`${stats.evolutionProgress * 2} ${200 - stats.evolutionProgress * 2}`}
                  className="animate-pulse"
                />
                <path
                  d="M 0 12 Q 25 18 50 12 T 100 12 T 150 12 T 200 12"
                  stroke="#4682B4"
                  strokeWidth="2"
                  fill="none"
                  strokeDasharray={`${stats.evolutionProgress * 2} ${200 - stats.evolutionProgress * 2}`}
                  className="animate-pulse"
                />
              </svg>
            </div>
          </div>
        </div>

        {/* Relationship Strength */}
        <div className="pt-4 border-t border-[#8A6C3C]/30">
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <Users className="w-4 h-4 mr-2 text-[#FF6347]" />
                <span className="text-sm font-bold text-[#4682B4]">BOND ANALYSIS</span>
              </div>
              <span className="text-xs text-[#8A6C3C] font-bold">{getRelationshipLabel(relationshipStrength)}</span>
            </div>
            <div className="relative h-4 bg-[#1a2f2f] rounded border border-[#8A6C3C] overflow-hidden">
              <div
                className="h-full bg-gradient-to-r from-[#8A6C3C] to-[#FF6347] transition-all duration-500"
                style={{ width: `${relationshipStrength}%` }}
              ></div>
              <div className="absolute inset-0 flex justify-between items-center px-1">
                {Array.from({ length: 5 }).map((_, i) => (
                  <div key={i} className="w-px h-2 bg-[#8A6C3C]"></div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
