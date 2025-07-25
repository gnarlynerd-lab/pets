"use client"

import { useEffect, useRef, useState } from 'react'

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

interface MemoryCluster {
  id: string
  concept: string
  memories: string[]
  strength: number
  color: string
}

interface MemoryVisualizationProps {
  memories: Memory[]
  clusters?: MemoryCluster[]
  activeMemoryId?: string
}

export default function MemoryVisualization({ memories, clusters = [], activeMemoryId }: MemoryVisualizationProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const [tick, setTick] = useState(0)
  const [hoveredMemory, setHoveredMemory] = useState<string | null>(null)

  useEffect(() => {
    const interval = setInterval(() => setTick(t => t + 1), 50)
    return () => clearInterval(interval)
  }, [])

  useEffect(() => {
    drawMemoryNetwork()
  }, [memories, clusters, tick, hoveredMemory])

  const getMemoryPosition = (memory: Memory, index: number) => {
    // Position memories based on temporal and semantic properties
    const age = Date.now() - memory.timestamp
    const maxAge = Math.max(...memories.map(m => Date.now() - m.timestamp))
    const normalizedAge = age / maxAge

    // Use emotional valence and arousal for spatial distribution
    const angle = (memory.emotional_context.valence + 1) * Math.PI
    const radius = 50 + (1 - normalizedAge) * 100 + memory.emotional_context.arousal * 30

    return {
      x: 200 + Math.cos(angle) * radius,
      y: 150 + Math.sin(angle) * radius * 0.7
    }
  }

  const drawMemoryNetwork = () => {
    const canvas = canvasRef.current
    if (!canvas || !memories.length) return

    const ctx = canvas.getContext('2d')
    if (!ctx) return

    ctx.clearRect(0, 0, canvas.width, canvas.height)

    // Draw background gradient representing time
    const timeGradient = ctx.createLinearGradient(0, 0, canvas.width, 0)
    timeGradient.addColorStop(0, 'rgba(40, 40, 80, 0.2)')
    timeGradient.addColorStop(1, 'rgba(20, 20, 40, 0.2)')
    ctx.fillStyle = timeGradient
    ctx.fillRect(0, 0, canvas.width, canvas.height)

    // Draw cluster regions
    clusters.forEach(cluster => {
      const clusterMemories = memories.filter(m => cluster.memories.includes(m.id))
      if (clusterMemories.length === 0) return

      // Calculate cluster center
      let centerX = 0, centerY = 0
      clusterMemories.forEach((memory, i) => {
        const pos = getMemoryPosition(memory, memories.indexOf(memory))
        centerX += pos.x
        centerY += pos.y
      })
      centerX /= clusterMemories.length
      centerY /= clusterMemories.length

      // Draw cluster aura
      const gradient = ctx.createRadialGradient(centerX, centerY, 0, centerX, centerY, 80)
      gradient.addColorStop(0, `${cluster.color}22`)
      gradient.addColorStop(1, 'transparent')
      ctx.fillStyle = gradient
      ctx.fillRect(centerX - 80, centerY - 80, 160, 160)
    })

    // Draw associations (connections between memories)
    memories.forEach((memory, i) => {
      const pos1 = getMemoryPosition(memory, i)
      
      memory.associations.forEach(assocId => {
        const assocMemory = memories.find(m => m.id === assocId)
        if (!assocMemory) return
        
        const pos2 = getMemoryPosition(assocMemory, memories.indexOf(assocMemory))
        
        // Draw connection line
        ctx.beginPath()
        ctx.moveTo(pos1.x, pos1.y)
        ctx.lineTo(pos2.x, pos2.y)
        
        const strength = memory.significance * assocMemory.significance
        ctx.strokeStyle = `rgba(150, 150, 255, ${strength * 0.3})`
        ctx.lineWidth = strength * 2
        ctx.stroke()
      })
    })

    // Draw memory nodes
    memories.forEach((memory, i) => {
      const pos = getMemoryPosition(memory, i)
      const age = Date.now() - memory.timestamp
      const maxAge = Math.max(...memories.map(m => Date.now() - m.timestamp))
      const ageRatio = age / maxAge

      // Memory fading effect
      const opacity = 0.3 + (1 - ageRatio) * 0.7
      const size = 3 + memory.significance * 7 + (memory.id === hoveredMemory ? 3 : 0)

      // Memory glow based on emotional intensity
      const emotionalIntensity = Math.abs(memory.emotional_context.valence) + memory.emotional_context.arousal
      if (emotionalIntensity > 0.5) {
        const glowGradient = ctx.createRadialGradient(pos.x, pos.y, 0, pos.x, pos.y, size * 3)
        const hue = memory.emotional_context.valence > 0 ? 120 : 0 // Green for positive, red for negative
        glowGradient.addColorStop(0, `hsla(${hue}, 70%, 60%, ${opacity * 0.3})`)
        glowGradient.addColorStop(1, 'transparent')
        ctx.fillStyle = glowGradient
        ctx.fillRect(pos.x - size * 3, pos.y - size * 3, size * 6, size * 6)
      }

      // Memory core
      ctx.beginPath()
      ctx.arc(pos.x, pos.y, size, 0, Math.PI * 2)
      
      // Color based on memory type and emotion
      const hue = 200 + memory.emotional_context.valence * 60
      const sat = 40 + memory.emotional_context.arousal * 40
      ctx.fillStyle = `hsla(${hue}, ${sat}%, 60%, ${opacity})`
      ctx.fill()

      // Active memory highlight
      if (memory.id === activeMemoryId) {
        ctx.strokeStyle = `hsla(60, 80%, 70%, ${0.8 + Math.sin(tick * 0.1) * 0.2})`
        ctx.lineWidth = 2
        ctx.stroke()
      }

      // Memory decay particles
      if (ageRatio > 0.7) {
        const particleCount = Math.floor((ageRatio - 0.7) * 10)
        for (let p = 0; p < particleCount; p++) {
          const particleAngle = (p / particleCount) * Math.PI * 2 + tick * 0.02
          const particleRadius = size + 5 + Math.sin(tick * 0.05 + p) * 3
          const px = pos.x + Math.cos(particleAngle) * particleRadius
          const py = pos.y + Math.sin(particleAngle) * particleRadius
          
          ctx.beginPath()
          ctx.arc(px, py, 1, 0, Math.PI * 2)
          ctx.fillStyle = `hsla(${hue}, ${sat}%, 70%, ${opacity * 0.5 * (1 - ageRatio)})`
          ctx.fill()
        }
      }
    })

    // Draw semantic tags for hovered memory
    if (hoveredMemory) {
      const memory = memories.find(m => m.id === hoveredMemory)
      if (memory) {
        const pos = getMemoryPosition(memory, memories.indexOf(memory))
        
        ctx.font = '10px monospace'
        ctx.textAlign = 'center'
        memory.semantic_tags.forEach((tag, i) => {
          const tagY = pos.y - 20 - i * 12
          
          // Tag background
          const metrics = ctx.measureText(tag)
          ctx.fillStyle = 'rgba(0, 0, 0, 0.8)'
          ctx.fillRect(pos.x - metrics.width / 2 - 4, tagY - 8, metrics.width + 8, 12)
          
          // Tag text
          ctx.fillStyle = 'rgba(200, 200, 255, 0.9)'
          ctx.fillText(tag, pos.x, tagY)
        })
      }
    }
  }

  const handleCanvasClick = (e: React.MouseEvent<HTMLCanvasElement>) => {
    const canvas = canvasRef.current
    if (!canvas) return

    const rect = canvas.getBoundingClientRect()
    const x = e.clientX - rect.left
    const y = e.clientY - rect.top

    // Find clicked memory
    let clickedMemory: string | null = null
    memories.forEach((memory, i) => {
      const pos = getMemoryPosition(memory, i)
      const distance = Math.sqrt((x - pos.x) ** 2 + (y - pos.y) ** 2)
      if (distance < 10) {
        clickedMemory = memory.id
      }
    })

    setHoveredMemory(clickedMemory)
  }

  return (
    <div className="bg-gray-800 border border-gray-700 p-4 font-mono">
      <h3 className="text-sm font-bold text-green-400 mb-3">[MEMORY] Semantic Network</h3>
      
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
        <div className="flex justify-between">
          <span className="text-purple-400">TOTAL MEMORIES:</span>
          <span className="text-gray-300">{memories.length}</span>
        </div>
        
        {clusters.length > 0 && (
          <div className="flex justify-between">
            <span className="text-blue-400">CONCEPT CLUSTERS:</span>
            <span className="text-gray-300">{clusters.length}</span>
          </div>
        )}

        <div className="text-gray-500 mt-2">
          Click memories to explore • Brightness = recency • Size = significance
        </div>
      </div>
    </div>
  )
}