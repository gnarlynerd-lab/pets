"use client"

import { Progress } from '@/components/ui/progress'

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
}

interface PetStatsProps {
  petData: PetData | null
}

export default function PetStats({ petData }: PetStatsProps) {
  if (!petData) {
    return (
      <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-4 border border-slate-700">
        <h3 className="text-lg font-semibold text-white mb-3">Pet Stats</h3>
        <div className="text-slate-400 text-sm">Loading...</div>
      </div>
    )
  }

  const vitalStats = [
    { name: 'Mood', value: petData.mood / 100.0, color: 'bg-blue-500', emoji: '😊' },
    { name: 'Energy', value: petData.energy / 100.0, color: 'bg-yellow-500', emoji: '⚡' },
    { name: 'Health', value: petData.health / 100.0, color: 'bg-green-500', emoji: '❤️' },
    { name: 'Hunger', value: 1 - (petData.needs.hunger / 100.0), color: 'bg-orange-500', emoji: '🍎' },
  ]

  const personalityTraits = Object.entries(petData.traits).slice(0, 5)

  return (
    <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-4 border border-slate-700">
      <h3 className="text-lg font-semibold text-white mb-4">Pet Stats</h3>
      
      {/* Vital Stats */}
      <div className="space-y-3 mb-6">
        {vitalStats.map((stat) => (
          <div key={stat.name} className="space-y-1">
            <div className="flex items-center justify-between text-sm">
              <span className="flex items-center gap-2 text-slate-300">
                <span>{stat.emoji}</span>
                {stat.name}
              </span>
              <span className="text-white font-medium">
                {Math.round(stat.value * 100)}%
              </span>
            </div>
            <Progress 
              value={stat.value * 100} 
              className="h-2"
            />
          </div>
        ))}
      </div>

      {/* Personality Traits */}
      <div>
        <h4 className="text-sm font-medium text-slate-300 mb-3">Personality</h4>
        <div className="space-y-2">
          {personalityTraits.map(([trait, value]) => (
            <div key={trait} className="flex items-center justify-between text-xs">
              <span className="text-slate-400 capitalize">
                {trait.replace('_', ' ')}
              </span>
              <div className="flex items-center gap-1">
                <div className="w-16 bg-slate-700 rounded-full h-1.5">
                  <div 
                    className="h-full bg-gradient-to-r from-indigo-400 to-indigo-500 rounded-full transition-all duration-300"
                    style={{ width: `${Math.round(value * 100)}%` }}
                  />
                </div>
                <span className="text-slate-300 w-8 text-right">
                  {Math.round(value * 100)}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
