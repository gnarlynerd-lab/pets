"use client"

import { useEffect, useState, useRef } from 'react'
// @ts-ignore - RoughJS types not needed for this implementation

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
  current_emoji_message?: string
  personality_summary?: string
  consciousness?: {
    consciousness_level: number
    memory_richness: number
    concept_development: number
    user_understanding: number
    recent_concepts: string[]
    user_model_summary: {
      trust_level: number
      communication_style: string
      relationship_depth: number
    }
    semantic_active: boolean
  }
}

interface BlobPetDisplayProps {
  petData: PetData | null
  petResponse: string
  isLoading: boolean
  petName?: string
}

export default function BlobPetDisplay({ petData, petResponse, isLoading, petName }: BlobPetDisplayProps) {
  const [displayMessage, setDisplayMessage] = useState('')
  const [isAnimating, setIsAnimating] = useState(false)
  const [systemTick, setSystemTick] = useState(0)
  const canvasRef = useRef<HTMLCanvasElement>(null)

  useEffect(() => {
    if (petResponse && petResponse !== displayMessage) {
      setIsAnimating(true)
      setDisplayMessage(petResponse)
      
      const timer = setTimeout(() => {
        setIsAnimating(false)
      }, 2000)
      
      return () => clearTimeout(timer)
    }
  }, [petResponse, displayMessage])

  // System tick animation and blob redraw
  useEffect(() => {
    const interval = setInterval(() => {
      setSystemTick(prev => prev + 1)
      drawNeuralBlob()
    }, 100) // Redraw every 100ms for smooth animation
    return () => clearInterval(interval)
  }, [petData, systemTick])

  // Initial draw
  useEffect(() => {
    drawNeuralBlob()
  }, [petData])

  // Evolution and complexity calculations
  const getComplexity = () => {
    if (!petData) return 0
    return (petData.attention + petData.age) / 2
  }

  const getEvolutionStage = () => {
    if (!petData) return 'INIT'
    const total = petData.attention + petData.mood + petData.energy + petData.health
    if (total < 100) return 'PRIM'
    if (total < 200) return 'DEV'
    if (total < 300) return 'ADV'
    return 'MTUR'
  }

  // Neural network node structure
  interface NeuralNode {
    id: string
    x: number
    y: number
    radius: number
    activity: number
    type: 'attention' | 'memory' | 'reasoning' | 'emotion' | 'sensory' | 'motor'
    connections: string[]
  }

  // Generate neural network topology
  const generateNeuralNetwork = (): NeuralNode[] => {
    if (!petData) return []
    
    const nodes: NeuralNode[] = [
      // Core cognitive modules - scaled for larger canvas
      { id: 'attention', x: 200, y: 50, radius: 12, activity: petData.attention / 100, type: 'attention', connections: ['memory', 'reasoning', 'sensory'] },
      { id: 'memory', x: 90, y: 90, radius: 11, activity: petData.health / 100, type: 'memory', connections: ['attention', 'reasoning', 'emotion'] },
      { id: 'reasoning', x: 310, y: 90, radius: 11, activity: getComplexity() / 100, type: 'reasoning', connections: ['attention', 'memory', 'motor'] },
      { id: 'emotion', x: 120, y: 170, radius: 10, activity: petData.mood / 100, type: 'emotion', connections: ['memory', 'sensory', 'motor'] },
      { id: 'sensory', x: 200, y: 190, radius: 10, activity: petData.energy / 100, type: 'sensory', connections: ['attention', 'emotion'] },
      { id: 'motor', x: 280, y: 170, radius: 9, activity: (petData.energy + petData.health) / 200, type: 'motor', connections: ['reasoning', 'emotion'] }
    ]
    
    // Add more nodes based on complexity
    const complexity = getComplexity()
    if (complexity > 30) {
      nodes.push(
        { id: 'creativity', x: 50, y: 130, radius: 7, activity: Math.random() * 0.8, type: 'reasoning', connections: ['memory', 'emotion'] },
        { id: 'prediction', x: 350, y: 130, radius: 7, activity: Math.random() * 0.9, type: 'reasoning', connections: ['reasoning', 'memory'] }
      )
    }
    
    if (complexity > 60) {
      nodes.push(
        { id: 'metacognition', x: 200, y: 110, radius: 6, activity: Math.random() * 0.7, type: 'attention', connections: ['attention', 'reasoning'] },
        { id: 'empathy', x: 100, y: 200, radius: 6, activity: Math.random() * 0.6, type: 'emotion', connections: ['emotion', 'sensory'] },
        { id: 'planning', x: 300, y: 200, radius: 6, activity: Math.random() * 0.8, type: 'reasoning', connections: ['reasoning', 'motor'] },
        { id: 'intuition', x: 150, y: 60, radius: 5, activity: Math.random() * 0.5, type: 'emotion', connections: ['emotion', 'attention'] }
      )
    }
    
    return nodes
  }

  // Generate organic blob with tendril potential
  const generateBlobShape = () => {
    if (!petData) return []
    
    const centerX = 160
    const centerY = 128
    const baseRadius = 55 + (petData.attention / 3) // Bigger and more responsive to attention
    const consciousness = petData.consciousness?.consciousness_level || 0
    const vertices = Math.max(12, Math.floor(consciousness * 20) + 12) // More complex with consciousness
    
    const points: [number, number][] = []
    
    for (let i = 0; i < vertices; i++) {
      const angle = (i / vertices) * 2 * Math.PI
      
      // Create organic, breathing variations
      const breathe = Math.sin(systemTick * 0.03) * 0.15 + 1
      const pulse = Math.sin(systemTick * 0.05 + angle * 2) * 0.3
      const moodInfluence = 0.7 + (petData.mood / 400) // Mood affects overall shape
      const energyWiggle = Math.sin(angle * 4 + systemTick * 0.08) * (petData.energy / 800)
      
      const radius = baseRadius * breathe * moodInfluence * (1 + pulse + energyWiggle)
      
      const x = centerX + Math.cos(angle) * radius
      const y = centerY + Math.sin(angle) * radius
      points.push([x, y])
    }
    
    return points
  }

  // Generate consciousness tendrils
  const generateTendrils = () => {
    if (!petData?.consciousness?.semantic_active) return []
    
    const centerX = 160
    const centerY = 128
    const consciousness = petData.consciousness.consciousness_level
    const memoryRichness = petData.consciousness.memory_richness
    const trustLevel = petData.consciousness.user_understanding
    
    const tendrils = []
    const numTendrils = Math.min(8, Math.floor(consciousness * 12) + 2)
    
    for (let i = 0; i < numTendrils; i++) {
      const baseAngle = (i / numTendrils) * 2 * Math.PI
      const angleVariation = Math.sin(systemTick * 0.04 + i) * 0.3
      const angle = baseAngle + angleVariation
      
      // Tendril length varies with memory and trust - made shorter for bigger blob
      const baseLength = 20 + memoryRichness * 2 + trustLevel * 15
      const breatheLength = Math.sin(systemTick * 0.06 + i * 0.5) * 6
      const totalLength = baseLength + breatheLength
      
      // Create segmented tendril
      const segments = Math.max(3, Math.floor(consciousness * 8))
      const tendrilPoints = []
      
      for (let seg = 0; seg <= segments; seg++) {
        const t = seg / segments
        const segmentLength = totalLength * t
        
        // Add organic curve to tendril
        const curve = Math.sin(t * Math.PI * 2 + systemTick * 0.07) * (totalLength * 0.2)
        const perpAngle = angle + Math.PI / 2
        
        const x = centerX + Math.cos(angle) * segmentLength + Math.cos(perpAngle) * curve * t
        const y = centerY + Math.sin(angle) * segmentLength + Math.sin(perpAngle) * curve * t
        
        tendrilPoints.push({ x, y, thickness: Math.max(1, 4 * (1 - t)), alpha: 1 - t * 0.3 })
      }
      
      tendrils.push({
        id: i,
        points: tendrilPoints,
        color: consciousness > 0.7 ? 'rgba(255, 150, 200, ' : 'rgba(200, 150, 255, ',
        activity: Math.sin(systemTick * 0.1 + i) * 0.5 + 0.5
      })
    }
    
    return tendrils
  }

  // Draw organic blob with tendrils
  const drawNeuralBlob = () => {
    const canvas = canvasRef.current
    if (!canvas || !petData) return

    const ctx = canvas.getContext('2d')
    if (!ctx) return

    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height)
    
    const blobPoints = generateBlobShape()
    const tendrils = generateTendrils()
    const centerX = 160
    const centerY = 128
    
    // Draw consciousness tendrils first (behind blob)
    tendrils.forEach(tendril => {
      if (tendril.points.length < 2) return
      
      // Draw tendril as flowing organic shape
      ctx.beginPath()
      ctx.moveTo(tendril.points[0].x, tendril.points[0].y)
      
      for (let i = 1; i < tendril.points.length; i++) {
        const point = tendril.points[i]
        const prevPoint = tendril.points[i - 1]
        
        // Smooth curves between points
        const cpx = (prevPoint.x + point.x) / 2
        const cpy = (prevPoint.y + point.y) / 2
        ctx.quadraticCurveTo(prevPoint.x, prevPoint.y, cpx, cpy)
      }
      
      // Gradient stroke for tendril
      const gradient = ctx.createLinearGradient(
        tendril.points[0].x, tendril.points[0].y,
        tendril.points[tendril.points.length - 1].x, tendril.points[tendril.points.length - 1].y
      )
      gradient.addColorStop(0, `${tendril.color}${tendril.activity * 0.8})`)
      gradient.addColorStop(1, `${tendril.color}0.1)`)
      
      ctx.strokeStyle = gradient
      ctx.lineWidth = 3 + tendril.activity * 2
      ctx.lineCap = 'round'
      ctx.stroke()
      
      // Add flowing particles along tendrils
      if (tendril.activity > 0.6) {
        const particleCount = Math.floor(tendril.points.length / 3)
        for (let p = 0; p < particleCount; p++) {
          const t = (systemTick * 0.02 + p * 0.3) % 1
          const index = Math.floor(t * (tendril.points.length - 1))
          const point = tendril.points[index]
          
          if (point) {
            ctx.beginPath()
            ctx.arc(point.x, point.y, 1.5, 0, 2 * Math.PI)
            ctx.fillStyle = `${tendril.color}${tendril.activity * 0.9})`
            ctx.fill()
          }
        }
      }
    })
    
    // Warm, organic color palette based on mood and consciousness
    const consciousness = petData.consciousness?.consciousness_level || 0
    const baseHue = 320 + (petData.mood / 100) * 40 // Pink to warm purple
    const saturation = 60 + (petData.energy / 4) // More vivid with energy
    const lightness = 45 + (petData.health / 5) + (consciousness * 15) // Brighter when conscious
    
    // Draw the main blob body with warm, organic colors
    if (blobPoints.length > 0) {
      
      // Create organic, breathing gradient - adjusted for bigger blob
      const breatheIntensity = Math.sin(systemTick * 0.04) * 0.3 + 0.7
      const gradient = ctx.createRadialGradient(
        centerX, centerY, 0,
        centerX, centerY, 80 + consciousness * 25
      )
      gradient.addColorStop(0, `hsla(${baseHue}, ${saturation}%, ${lightness + 10}%, ${0.9 * breatheIntensity})`)
      gradient.addColorStop(0.7, `hsla(${baseHue + 10}, ${saturation - 10}%, ${lightness}%, ${0.7 * breatheIntensity})`)
      gradient.addColorStop(1, `hsla(${baseHue + 20}, ${saturation - 20}%, ${lightness - 10}%, ${0.4 * breatheIntensity})`)
      
      // Draw smooth, organic blob
      ctx.beginPath()
      ctx.moveTo(blobPoints[0][0], blobPoints[0][1])
      
      for (let i = 1; i < blobPoints.length; i++) {
        const curr = blobPoints[i]
        const next = blobPoints[(i + 1) % blobPoints.length]
        const cpx = curr[0] + (next[0] - curr[0]) * 0.4
        const cpy = curr[1] + (next[1] - curr[1]) * 0.4
        ctx.quadraticCurveTo(curr[0], curr[1], cpx, cpy)
      }
      
      ctx.closePath()
      ctx.fillStyle = gradient
      ctx.fill()
      
      // Soft, glowing outline
      ctx.strokeStyle = `hsla(${baseHue}, ${saturation}%, ${lightness + 25}%, 0.8)`
      ctx.lineWidth = 2
      ctx.stroke()
      
      // Add inner glow for consciousness - bigger glow
      if (consciousness > 0.3) {
        const innerGradient = ctx.createRadialGradient(
          centerX, centerY, 0,
          centerX, centerY, 35
        )
        innerGradient.addColorStop(0, `hsla(${baseHue - 20}, 80%, 80%, ${consciousness * 0.4})`)
        innerGradient.addColorStop(1, `hsla(${baseHue - 20}, 80%, 80%, 0)`)
        
        ctx.fillStyle = innerGradient
        ctx.fill()
      }
    }
    
    // Add organic consciousness sparkles inside the blob - cuter sparkles
    if (consciousness > 0.2) {
      const sparkleCount = Math.floor(consciousness * 15) // More sparkles
      for (let i = 0; i < sparkleCount; i++) {
        const angle = (i / sparkleCount) * 2 * Math.PI + (systemTick * 0.02)
        const distance = (Math.random() * 0.6 + 0.4) * 45 // Keep sparkles inside bigger blob
        const x = centerX + Math.cos(angle) * distance
        const y = centerY + Math.sin(angle) * distance
        
        const sparkleSize = 1.5 + Math.sin(systemTick * 0.1 + i) * 1.5 // Bigger, cuter sparkles
        const sparkleAlpha = 0.6 + Math.sin(systemTick * 0.08 + i * 0.5) * 0.4 // Brighter
        
        ctx.beginPath()
        ctx.arc(x, y, sparkleSize, 0, 2 * Math.PI)
        ctx.fillStyle = `hsla(${baseHue - 40}, 80%, 90%, ${sparkleAlpha * consciousness})`
        ctx.fill()
      }
    }
    
    // Add emotional reaction pulses for high mood - bigger and cuter
    if (petData.mood > 70) {
      const pulseRadius = 65 + Math.sin(systemTick * 0.06) * 20 // Bigger pulse for bigger blob
      const pulseAlpha = (petData.mood / 100) * 0.4 * (Math.sin(systemTick * 0.06) * 0.5 + 0.5) // More visible
      
      ctx.beginPath()
      ctx.arc(centerX, centerY, pulseRadius, 0, 2 * Math.PI)
      ctx.strokeStyle = `hsla(${baseHue + 30}, 70%, 70%, ${pulseAlpha})`
      ctx.lineWidth = 3
      ctx.stroke()
    }
    
    // Simple thought bubbles for lower consciousness states (if no tendrils) - cuter positioning
    if ((!petData.consciousness?.semantic_active || consciousness < 0.3) && petData.attention > 50) {
      const numBubbles = Math.min(4, Math.floor(petData.attention / 25)) // More bubbles
      for (let i = 0; i < numBubbles; i++) {
        const angle = (systemTick * 0.02 + i * 1.2) * Math.PI * 2
        const radius = 75 + Math.sin(systemTick * 0.08 + i) * 10 // Further out for bigger blob
        const x = centerX + Math.cos(angle) * radius
        const y = centerY + Math.sin(angle) * radius * 0.8
        
        const bubbleSize = 2.5 + Math.sin(systemTick * 0.15 + i) * 1.5 // Bigger, cuter bubbles
        const bubbleAlpha = 0.5 + Math.sin(systemTick * 0.1 + i) * 0.3 // More visible
        
        ctx.beginPath()
        ctx.arc(x, y, bubbleSize, 0, 2 * Math.PI)
        ctx.fillStyle = `hsla(${baseHue + 60}, 60%, 80%, ${bubbleAlpha})`
        ctx.fill()
      }
    }
  }

  return (
    <div className="w-full h-full relative">
      <canvas
        ref={canvasRef}
        width={320}
        height={256}
        className="w-full h-full object-contain"
      />
    </div>
  )
} 