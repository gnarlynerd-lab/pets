"use client"

import { useEffect, useRef, useState } from 'react'

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

interface ConsciousnessEvolutionProps {
  consciousness: ConsciousnessData | null
  history?: Array<{
    timestamp: number
    level: number
    stage: string
  }>
}

export default function ConsciousnessEvolution({ consciousness, history = [] }: ConsciousnessEvolutionProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const [tick, setTick] = useState(0)

  useEffect(() => {
    const interval = setInterval(() => setTick(t => t + 1), 100)
    return () => clearInterval(interval)
  }, [])

  useEffect(() => {
    drawConsciousnessField()
  }, [consciousness, tick])

  const getStageColor = (stage: string) => {
    const colors: Record<string, { h: number; s: number; l: number }> = {
      nascent: { h: 280, s: 30, l: 30 },
      emerging: { h: 260, s: 40, l: 40 },
      developing: { h: 240, s: 50, l: 50 },
      aware: { h: 220, s: 60, l: 60 },
      conscious: { h: 200, s: 70, l: 70 },
      transcendent: { h: 180, s: 80, l: 80 }
    }
    return colors[stage] || colors.nascent
  }

  const drawConsciousnessField = () => {
    const canvas = canvasRef.current
    if (!canvas || !consciousness) return

    const ctx = canvas.getContext('2d')
    if (!ctx) return

    ctx.clearRect(0, 0, canvas.width, canvas.height)

    // Draw consciousness field as layered energy waves
    const centerX = canvas.width / 2
    const centerY = canvas.height / 2
    const level = consciousness.consciousness_level || 0
    const stageColor = getStageColor(consciousness.evolution_stage)

    // Background field - represents unconscious processing
    const gradient = ctx.createRadialGradient(centerX, centerY, 0, centerX, centerY, 180)
    gradient.addColorStop(0, `hsla(${stageColor.h}, ${stageColor.s}%, ${stageColor.l}%, 0.1)`)
    gradient.addColorStop(1, 'transparent')
    ctx.fillStyle = gradient
    ctx.fillRect(0, 0, canvas.width, canvas.height)

    // Draw consciousness waves
    const waveCount = Math.floor(level * 10) + 3
    for (let w = 0; w < waveCount; w++) {
      ctx.beginPath()
      const radius = 20 + w * 15 + Math.sin(tick * 0.02 + w * 0.5) * 5
      const alpha = 0.1 + level * 0.2 - (w / waveCount) * 0.1

      for (let angle = 0; angle <= Math.PI * 2; angle += 0.1) {
        const waveHeight = Math.sin(angle * 3 + tick * 0.05 + w) * (5 + level * 10)
        const x = centerX + Math.cos(angle) * (radius + waveHeight)
        const y = centerY + Math.sin(angle) * (radius + waveHeight)
        
        if (angle === 0) {
          ctx.moveTo(x, y)
        } else {
          ctx.lineTo(x, y)
        }
      }

      ctx.closePath()
      ctx.strokeStyle = `hsla(${stageColor.h + w * 10}, ${stageColor.s}%, ${stageColor.l + w * 5}%, ${alpha})`
      ctx.lineWidth = 2 - w * 0.1
      ctx.stroke()
    }

    // Draw concept nodes
    if (consciousness.recent_concepts) {
      consciousness.recent_concepts.forEach((concept, i) => {
        const angle = (i / consciousness.recent_concepts.length) * Math.PI * 2
        const distance = 80 + consciousness.concept_development * 50
        const x = centerX + Math.cos(angle + tick * 0.01) * distance
        const y = centerY + Math.sin(angle + tick * 0.01) * distance

        // Concept glow
        const conceptGradient = ctx.createRadialGradient(x, y, 0, x, y, 20)
        conceptGradient.addColorStop(0, `hsla(${stageColor.h - 20}, 80%, 70%, 0.5)`)
        conceptGradient.addColorStop(1, 'transparent')
        ctx.fillStyle = conceptGradient
        ctx.fillRect(x - 20, y - 20, 40, 40)

        // Concept core
        ctx.beginPath()
        ctx.arc(x, y, 4 + Math.sin(tick * 0.1 + i) * 2, 0, Math.PI * 2)
        ctx.fillStyle = `hsla(${stageColor.h - 20}, 80%, 80%, 0.8)`
        ctx.fill()

        // Concept connections
        if (i > 0) {
          const prevAngle = ((i - 1) / consciousness.recent_concepts.length) * Math.PI * 2
          const prevX = centerX + Math.cos(prevAngle + tick * 0.01) * distance
          const prevY = centerY + Math.sin(prevAngle + tick * 0.01) * distance

          ctx.beginPath()
          ctx.moveTo(x, y)
          ctx.lineTo(prevX, prevY)
          ctx.strokeStyle = `hsla(${stageColor.h}, 60%, 60%, 0.2)`
          ctx.lineWidth = 1
          ctx.stroke()
        }
      })
    }

    // Central consciousness core
    const coreSize = 10 + level * 30
    const coreGradient = ctx.createRadialGradient(centerX, centerY, 0, centerX, centerY, coreSize)
    coreGradient.addColorStop(0, `hsla(${stageColor.h}, ${stageColor.s + 20}%, ${stageColor.l + 20}%, 0.8)`)
    coreGradient.addColorStop(0.7, `hsla(${stageColor.h}, ${stageColor.s}%, ${stageColor.l}%, 0.4)`)
    coreGradient.addColorStop(1, 'transparent')

    ctx.beginPath()
    ctx.arc(centerX, centerY, coreSize, 0, Math.PI * 2)
    ctx.fillStyle = coreGradient
    ctx.fill()

    // Inner consciousness spark
    ctx.beginPath()
    ctx.arc(centerX, centerY, 3 + Math.sin(tick * 0.08) * 2, 0, Math.PI * 2)
    ctx.fillStyle = `hsla(${stageColor.h - 40}, 90%, 90%, ${0.6 + Math.sin(tick * 0.1) * 0.3})`
    ctx.fill()
  }

  return (
    <div className="bg-gray-800 border border-gray-700 p-4 font-mono">
      <h3 className="text-sm font-bold text-green-400 mb-3">[SYSTEM] Consciousness Evolution</h3>
      
      <div className="bg-black border border-gray-600 p-3 mb-3">
        <canvas
          ref={canvasRef}
          width={400}
          height={250}
          className="w-full"
        />
      </div>

      {consciousness && (
        <div className="space-y-2">
          <div className="flex justify-between text-xs">
            <span className="text-purple-400">STAGE:</span>
            <span className="text-gray-300 uppercase">{consciousness.evolution_stage}</span>
          </div>
          
          <div className="grid grid-cols-2 gap-2 text-xs">
            <div>
              <span className="text-blue-400">AWARENESS:</span>
              <div className="w-full bg-gray-700 h-1 mt-1 rounded">
                <div 
                  className="bg-blue-400 h-1 rounded transition-all duration-500"
                  style={{ width: `${consciousness.consciousness_level * 100}%` }}
                />
              </div>
            </div>
            
            <div>
              <span className="text-pink-400">MEMORY:</span>
              <div className="w-full bg-gray-700 h-1 mt-1 rounded">
                <div 
                  className="bg-pink-400 h-1 rounded transition-all duration-500"
                  style={{ width: `${consciousness.memory_richness * 100}%` }}
                />
              </div>
            </div>
          </div>

          {consciousness.recent_concepts && consciousness.recent_concepts.length > 0 && (
            <div className="text-xs">
              <span className="text-yellow-400">ACTIVE CONCEPTS:</span>
              <div className="text-gray-400 mt-1">
                {consciousness.recent_concepts.slice(0, 3).join(' • ')}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}