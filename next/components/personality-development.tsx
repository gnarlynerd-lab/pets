"use client"

import { useEffect, useRef, useState } from 'react'

interface PersonalityTrait {
  name: string
  value: number
  category: 'core' | 'secondary'
  connections: string[]
}

interface PersonalityNetwork {
  traits: Record<string, PersonalityTrait>
  dominantTrait: string
  recentChanges: Array<{
    trait: string
    delta: number
    timestamp: number
  }>
}

interface PersonalityDevelopmentProps {
  personality: PersonalityNetwork | null
  history?: Array<{
    timestamp: number
    traits: Record<string, number>
  }>
}

export default function PersonalityDevelopment({ personality, history = [] }: PersonalityDevelopmentProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const [tick, setTick] = useState(0)
  const [selectedTrait, setSelectedTrait] = useState<string | null>(null)

  useEffect(() => {
    const interval = setInterval(() => setTick(t => t + 1), 100)
    return () => clearInterval(interval)
  }, [])

  useEffect(() => {
    drawPersonalityNetwork()
  }, [personality, tick, selectedTrait])

  const getTraitPosition = (traitName: string, index: number, total: number) => {
    // Core traits in inner circle, secondary traits in outer circle
    const trait = personality?.traits[traitName]
    if (!trait) return { x: 200, y: 150 }

    const isCore = trait.category === 'core'
    const radius = isCore ? 60 : 100
    const angle = (index / total) * Math.PI * 2 - Math.PI / 2

    return {
      x: 200 + Math.cos(angle) * radius,
      y: 150 + Math.sin(angle) * radius
    }
  }

  const getTraitColor = (trait: PersonalityTrait) => {
    const colors: Record<string, { h: number; s: number; l: number }> = {
      // Core traits - Big Five
      openness: { h: 280, s: 60, l: 60 },
      conscientiousness: { h: 220, s: 60, l: 60 },
      extraversion: { h: 40, s: 70, l: 60 },
      agreeableness: { h: 120, s: 60, l: 60 },
      neuroticism: { h: 0, s: 60, l: 60 },
      // Secondary traits
      curiosity: { h: 260, s: 50, l: 65 },
      playfulness: { h: 30, s: 60, l: 65 },
      social: { h: 200, s: 50, l: 65 },
      affection: { h: 340, s: 60, l: 65 },
      stubbornness: { h: 20, s: 50, l: 55 }
    }
    return colors[trait.name] || { h: 180, s: 40, l: 60 }
  }

  const drawPersonalityNetwork = () => {
    const canvas = canvasRef.current
    if (!canvas || !personality) return

    const ctx = canvas.getContext('2d')
    if (!ctx) return

    ctx.clearRect(0, 0, canvas.width, canvas.height)

    // Draw background
    const bgGradient = ctx.createRadialGradient(200, 150, 0, 200, 150, 150)
    bgGradient.addColorStop(0, 'rgba(20, 20, 40, 0.2)')
    bgGradient.addColorStop(1, 'rgba(0, 0, 0, 0.4)')
    ctx.fillStyle = bgGradient
    ctx.fillRect(0, 0, canvas.width, canvas.height)

    const traits = Object.entries(personality.traits)
    const coreTraits = traits.filter(([_, t]) => t.category === 'core')
    const secondaryTraits = traits.filter(([_, t]) => t.category === 'secondary')

    // Draw connections first
    traits.forEach(([name, trait], i) => {
      const pos1 = getTraitPosition(name, 
        trait.category === 'core' ? coreTraits.findIndex(([n]) => n === name) : secondaryTraits.findIndex(([n]) => n === name),
        trait.category === 'core' ? coreTraits.length : secondaryTraits.length
      )

      trait.connections.forEach(connName => {
        const connTrait = personality.traits[connName]
        if (!connTrait) return

        const pos2 = getTraitPosition(connName,
          connTrait.category === 'core' ? coreTraits.findIndex(([n]) => n === connName) : secondaryTraits.findIndex(([n]) => n === connName),
          connTrait.category === 'core' ? coreTraits.length : secondaryTraits.length
        )

        // Connection strength based on both trait values
        const strength = (trait.value + connTrait.value) / 2
        
        // Draw connection
        ctx.beginPath()
        ctx.moveTo(pos1.x, pos1.y)
        
        // Curved connection for visual appeal
        const cpx = (pos1.x + pos2.x) / 2 + (pos1.y - pos2.y) * 0.2
        const cpy = (pos1.y + pos2.y) / 2 + (pos2.x - pos1.x) * 0.2
        ctx.quadraticCurveTo(cpx, cpy, pos2.x, pos2.y)
        
        ctx.strokeStyle = `rgba(150, 150, 200, ${strength * 0.3})`
        ctx.lineWidth = strength * 2
        ctx.stroke()
      })
    })

    // Draw trait nodes
    const allTraits = [...coreTraits, ...secondaryTraits]
    allTraits.forEach(([name, trait], globalIndex) => {
      const index = trait.category === 'core' ? 
        coreTraits.findIndex(([n]) => n === name) : 
        secondaryTraits.findIndex(([n]) => n === name)
      const total = trait.category === 'core' ? coreTraits.length : secondaryTraits.length
      const pos = getTraitPosition(name, index, total)
      const color = getTraitColor(trait)
      const isSelected = name === selectedTrait
      const isDominant = name === personality.dominantTrait

      // Trait influence aura
      const auraSize = 20 + trait.value * 30
      const auraGradient = ctx.createRadialGradient(pos.x, pos.y, 0, pos.x, pos.y, auraSize)
      auraGradient.addColorStop(0, `hsla(${color.h}, ${color.s}%, ${color.l}%, ${trait.value * 0.3})`)
      auraGradient.addColorStop(1, 'transparent')
      ctx.fillStyle = auraGradient
      ctx.fillRect(pos.x - auraSize, pos.y - auraSize, auraSize * 2, auraSize * 2)

      // Trait node
      const nodeSize = 8 + trait.value * 12 + (isSelected ? 3 : 0) + (isDominant ? 5 : 0)
      
      // Pulsing effect for dominant trait
      if (isDominant) {
        const pulseSize = nodeSize + Math.sin(tick * 0.05) * 3
        ctx.beginPath()
        ctx.arc(pos.x, pos.y, pulseSize, 0, Math.PI * 2)
        ctx.strokeStyle = `hsla(${color.h}, ${color.s + 20}%, ${color.l + 10}%, ${0.5 + Math.sin(tick * 0.05) * 0.3})`
        ctx.lineWidth = 2
        ctx.stroke()
      }

      // Main node
      ctx.beginPath()
      ctx.arc(pos.x, pos.y, nodeSize, 0, Math.PI * 2)
      
      const gradient = ctx.createRadialGradient(pos.x, pos.y, 0, pos.x, pos.y, nodeSize)
      gradient.addColorStop(0, `hsla(${color.h}, ${color.s}%, ${color.l + 20}%, 0.9)`)
      gradient.addColorStop(0.7, `hsla(${color.h}, ${color.s}%, ${color.l}%, 0.8)`)
      gradient.addColorStop(1, `hsla(${color.h}, ${color.s - 10}%, ${color.l - 10}%, 0.7)`)
      
      ctx.fillStyle = gradient
      ctx.fill()

      // Node border
      ctx.strokeStyle = isSelected ? 
        `hsla(${color.h}, ${color.s + 20}%, ${color.l + 20}%, 0.9)` :
        `hsla(${color.h}, ${color.s}%, ${color.l}%, 0.5)`
      ctx.lineWidth = isSelected ? 2 : 1
      ctx.stroke()

      // Trait label
      ctx.font = trait.category === 'core' ? 'bold 11px monospace' : '10px monospace'
      ctx.textAlign = 'center'
      ctx.textBaseline = 'middle'
      
      // Text background for readability
      const metrics = ctx.measureText(name)
      ctx.fillStyle = 'rgba(0, 0, 0, 0.7)'
      ctx.fillRect(pos.x - metrics.width / 2 - 3, pos.y + nodeSize + 5, metrics.width + 6, 14)
      
      // Text
      ctx.fillStyle = `hsla(${color.h}, ${color.s}%, ${color.l + 30}%, 0.9)`
      ctx.fillText(name, pos.x, pos.y + nodeSize + 12)

      // Value indicator
      ctx.font = '9px monospace'
      ctx.fillStyle = 'rgba(255, 255, 255, 0.7)'
      ctx.fillText(`${Math.round(trait.value * 100)}%`, pos.x, pos.y)

      // Recent change indicator
      const recentChange = personality.recentChanges.find(c => c.trait === name)
      if (recentChange && Date.now() - recentChange.timestamp < 10000) {
        const changeAlpha = 1 - (Date.now() - recentChange.timestamp) / 10000
        ctx.fillStyle = recentChange.delta > 0 ? 
          `rgba(100, 255, 100, ${changeAlpha})` : 
          `rgba(255, 100, 100, ${changeAlpha})`
        ctx.fillText(
          recentChange.delta > 0 ? `+${Math.round(recentChange.delta * 100)}` : `${Math.round(recentChange.delta * 100)}`,
          pos.x + nodeSize + 5,
          pos.y - nodeSize - 5
        )
      }
    })

    // Draw personality core
    ctx.beginPath()
    ctx.arc(200, 150, 20, 0, Math.PI * 2)
    const coreGradient = ctx.createRadialGradient(200, 150, 0, 200, 150, 20)
    coreGradient.addColorStop(0, 'rgba(255, 255, 255, 0.3)')
    coreGradient.addColorStop(1, 'rgba(200, 200, 255, 0.1)')
    ctx.fillStyle = coreGradient
    ctx.fill()
  }

  const handleCanvasClick = (e: React.MouseEvent<HTMLCanvasElement>) => {
    const canvas = canvasRef.current
    if (!canvas || !personality) return

    const rect = canvas.getBoundingClientRect()
    const x = e.clientX - rect.left
    const y = e.clientY - rect.top

    // Find clicked trait
    let clickedTrait: string | null = null
    Object.entries(personality.traits).forEach(([name, trait]) => {
      const index = trait.category === 'core' ? 
        Object.entries(personality.traits).filter(([_, t]) => t.category === 'core').findIndex(([n]) => n === name) :
        Object.entries(personality.traits).filter(([_, t]) => t.category === 'secondary').findIndex(([n]) => n === name)
      const total = Object.values(personality.traits).filter(t => t.category === trait.category).length
      const pos = getTraitPosition(name, index, total)
      
      const distance = Math.sqrt((x - pos.x) ** 2 + (y - pos.y) ** 2)
      if (distance < 20) {
        clickedTrait = name
      }
    })

    setSelectedTrait(clickedTrait)
  }

  return (
    <div className="bg-gray-800 border border-gray-700 p-4 font-mono">
      <h3 className="text-sm font-bold text-green-400 mb-3">[PERSONALITY] Trait Network</h3>
      
      <div className="bg-black border border-gray-600 p-3 mb-3">
        <canvas
          ref={canvasRef}
          width={400}
          height={300}
          className="w-full cursor-pointer"
          onClick={handleCanvasClick}
        />
      </div>

      <div className="space-y-2 text-xs">
        {personality?.dominantTrait && (
          <div className="flex justify-between">
            <span className="text-purple-400">DOMINANT TRAIT:</span>
            <span className="text-gray-300 uppercase">{personality.dominantTrait}</span>
          </div>
        )}

        {selectedTrait && personality?.traits[selectedTrait] && (
          <div className="bg-gray-900 border border-gray-600 p-2 mt-2">
            <div className="text-yellow-400 mb-1">{selectedTrait.toUpperCase()}</div>
            <div className="text-gray-400">
              Value: {Math.round(personality.traits[selectedTrait].value * 100)}%
            </div>
            {personality.traits[selectedTrait].connections.length > 0 && (
              <div className="text-gray-400 mt-1">
                Influences: {personality.traits[selectedTrait].connections.join(', ')}
              </div>
            )}
          </div>
        )}

        <div className="text-gray-500 mt-2">
          Click traits to explore • Size = strength • Glow = influence
        </div>
      </div>
    </div>
  )
}