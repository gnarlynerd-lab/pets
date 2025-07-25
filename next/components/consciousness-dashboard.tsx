"use client"

import { useState } from 'react'
import ConsciousnessEvolution from './consciousness-evolution'
import MemoryVisualization from './memory-visualization'
import PersonalityDevelopment from './personality-development'
import { Button } from '@/components/ui/button'

interface ConsciousnessData {
  consciousness_level: number
  memory_richness: number
  concept_development: number
  user_understanding: number
  attention_span: number
  recent_concepts: string[]
  semantic_active: boolean
  evolution_stage: 'nascent' | 'emerging' | 'developing' | 'aware' | 'conscious' | 'transcendent'
}

interface Memory {
  id: string
  timestamp: number
  interaction_type: string
  content: string
  semantic_tags: string[]
  emotional_context: {
    valence: number
    arousal: number
    dominance: number
  }
  significance: number
  associations: string[]
  cluster_id?: string
}

interface PersonalityTrait {
  name: string
  value: number
  category: 'core' | 'secondary'
  connections: string[]
}

interface ConsciousnessDashboardProps {
  petData: any
  memories?: Memory[]
}

export default function ConsciousnessDashboard({ petData, memories = [] }: ConsciousnessDashboardProps) {
  const [activeView, setActiveView] = useState<'evolution' | 'memory' | 'personality'>('evolution')

  // Transform pet data into visualization formats
  const getConsciousnessData = (): ConsciousnessData | null => {
    if (!petData?.consciousness) return null

    // Determine evolution stage based on consciousness level
    const level = petData.consciousness.consciousness_level || 0
    let stage: ConsciousnessData['evolution_stage'] = 'nascent'
    
    if (level >= 0.8) stage = 'transcendent'
    else if (level >= 0.6) stage = 'conscious'
    else if (level >= 0.4) stage = 'aware'
    else if (level >= 0.25) stage = 'developing'
    else if (level >= 0.1) stage = 'emerging'

    return {
      consciousness_level: level,
      memory_richness: petData.consciousness.memory_richness || 0,
      concept_development: petData.consciousness.concept_development || 0,
      user_understanding: petData.consciousness.user_understanding || 0,
      attention_span: petData.attention / 100 || 0,
      recent_concepts: petData.consciousness.recent_concepts || [],
      semantic_active: petData.consciousness.semantic_active || false,
      evolution_stage: stage
    }
  }

  const getPersonalityNetwork = () => {
    if (!petData?.traits) return null

    // Convert traits to network format
    const traits: Record<string, PersonalityTrait> = {}
    
    // Core traits (Big Five)
    const coreTraitNames = ['openness', 'conscientiousness', 'extraversion', 'agreeableness', 'neuroticism']
    const secondaryTraitNames = ['curiosity', 'playfulness', 'social', 'affection', 'stubbornness']
    
    // Add core traits
    coreTraitNames.forEach(name => {
      if (petData.traits[name] !== undefined) {
        traits[name] = {
          name,
          value: petData.traits[name] / 100,
          category: 'core',
          connections: getTraitConnections(name)
        }
      }
    })

    // Add secondary traits
    secondaryTraitNames.forEach(name => {
      if (petData.traits[name] !== undefined) {
        traits[name] = {
          name,
          value: petData.traits[name] / 100,
          category: 'secondary',
          connections: getTraitConnections(name)
        }
      }
    })

    // Find dominant trait
    let dominantTrait = ''
    let maxValue = 0
    Object.entries(traits).forEach(([name, trait]) => {
      if (trait.value > maxValue) {
        maxValue = trait.value
        dominantTrait = name
      }
    })

    return {
      traits,
      dominantTrait,
      recentChanges: [] // Could be populated from history if available
    }
  }

  const getTraitConnections = (traitName: string): string[] => {
    // Define trait influence relationships
    const connections: Record<string, string[]> = {
      openness: ['curiosity', 'playfulness'],
      conscientiousness: ['stubbornness'],
      extraversion: ['social', 'playfulness'],
      agreeableness: ['affection', 'social'],
      neuroticism: ['stubbornness'],
      curiosity: ['openness', 'playfulness'],
      playfulness: ['openness', 'extraversion', 'curiosity'],
      social: ['extraversion', 'agreeableness'],
      affection: ['agreeableness'],
      stubbornness: ['conscientiousness', 'neuroticism']
    }
    return connections[traitName] || []
  }

  // Generate sample memories if none provided
  const getSampleMemories = (): Memory[] => {
    if (memories.length > 0) return memories

    // Generate memories based on pet's history
    const now = Date.now()
    const sampleMemories: Memory[] = []
    
    // Create some sample memories based on pet state
    if (petData?.consciousness?.semantic_active) {
      sampleMemories.push({
        id: 'mem_1',
        timestamp: now - 1000 * 60 * 5, // 5 minutes ago
        interaction_type: 'emoji',
        content: 'User sent heart emoji',
        semantic_tags: ['affection', 'positive', 'bonding'],
        emotional_context: { valence: 0.8, arousal: 0.6, dominance: 0.5 },
        significance: 0.8,
        associations: []
      })
    }

    return sampleMemories
  }

  const consciousnessData = getConsciousnessData()
  const personalityNetwork = getPersonalityNetwork()
  const memoryData = getSampleMemories()

  return (
    <div className="bg-gray-800 border border-gray-700 p-4 font-mono space-y-4">
      <div className="mb-4">
        <h2 className="text-lg font-bold text-green-400 mb-3">[CONSCIOUSNESS] Analysis Dashboard</h2>
        <div className="flex flex-wrap gap-2 justify-center">
          <Button
            variant={activeView === 'evolution' ? 'default' : 'outline'}
            size="sm"
            onClick={() => setActiveView('evolution')}
            className="font-mono text-xs flex-shrink-0"
          >
            Evolution
          </Button>
          <Button
            variant={activeView === 'memory' ? 'default' : 'outline'}
            size="sm"
            onClick={() => setActiveView('memory')}
            className="font-mono text-xs flex-shrink-0"
          >
            Memory
          </Button>
          <Button
            variant={activeView === 'personality' ? 'default' : 'outline'}
            size="sm"
            onClick={() => setActiveView('personality')}
            className="font-mono text-xs flex-shrink-0"
          >
            Personality
          </Button>
        </div>
      </div>

      <div className="min-h-[400px]">
        {activeView === 'evolution' && (
          <ConsciousnessEvolution 
            consciousness={consciousnessData}
            history={[]} // Could be populated from backend
          />
        )}
        
        {activeView === 'memory' && (
          <MemoryVisualization 
            memories={memoryData}
            clusters={[]} // Could be populated from semantic clustering
            activeMemoryId={undefined}
          />
        )}
        
        {activeView === 'personality' && (
          <PersonalityDevelopment 
            personality={personalityNetwork}
            history={[]} // Could be populated from trait history
          />
        )}
      </div>

      {/* Quick stats footer */}
      <div className="grid grid-cols-3 gap-2 text-xs pt-4 border-t border-gray-600">
        <div className="text-center">
          <div className="text-purple-400">AWARENESS</div>
          <div className="text-2xl text-gray-300">
            {consciousnessData ? Math.round(consciousnessData.consciousness_level * 100) : 0}%
          </div>
        </div>
        <div className="text-center">
          <div className="text-blue-400">MEMORIES</div>
          <div className="text-2xl text-gray-300">
            {memoryData.length}
          </div>
        </div>
        <div className="text-center">
          <div className="text-pink-400">DOMINANT</div>
          <div className="text-lg text-gray-300 uppercase">
            {personalityNetwork?.dominantTrait || 'none'}
          </div>
        </div>
      </div>
    </div>
  )
}