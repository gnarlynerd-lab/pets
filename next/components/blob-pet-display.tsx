"use client"

import { useEffect, useState, useRef } from 'react'
import rough from 'roughjs/bundled/rough.esm'

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

  // Generate organic blob shape
  const generateBlobShape = () => {
    if (!petData) return []
    
    const centerX = 160
    const centerY = 90
    const baseRadius = 45 + (petData.attention / 5) // Size based on attention
    const complexity = getComplexity()
    const vertices = Math.max(8, Math.floor(complexity / 8) + 8) // More complex with growth
    
    const points: [number, number][] = []
    
    for (let i = 0; i < vertices; i++) {
      const angle = (i / vertices) * 2 * Math.PI
      // Create organic variations
      const noiseScale = 0.3 + (petData.energy / 500) // Energy affects dynamism
      const radiusVariation = 1 + Math.sin(angle * 3 + systemTick * 0.05) * noiseScale
      const moodInfluence = 0.8 + (petData.mood / 250) // Mood affects overall shape
      const radius = baseRadius * radiusVariation * moodInfluence
      
      const x = centerX + Math.cos(angle) * radius
      const y = centerY + Math.sin(angle) * radius
      points.push([x, y])
    }
    
    return points
  }

  // Draw neural-influenced blob
  const drawNeuralBlob = () => {
    const canvas = canvasRef.current
    if (!canvas || !petData) return

    const ctx = canvas.getContext('2d')
    if (!ctx) return

    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height)
    
    const blobPoints = generateBlobShape()
    const nodes = generateNeuralNetwork()
    
    // Draw the blob body
    if (blobPoints.length > 0) {
      // Main blob gradient based on mood and energy
      const hue = (petData.mood / 100) * 60 // Red to yellow spectrum
      const saturation = 30 + (petData.energy / 5) // More vivid with energy
      const lightness = 20 + (petData.health / 5) // Brighter when healthy
      
      const gradient = ctx.createRadialGradient(200, 120, 0, 200, 120, 80)
      gradient.addColorStop(0, `hsla(${hue}, ${saturation}%, ${lightness + 15}%, 0.8)`)
      gradient.addColorStop(1, `hsla(${hue}, ${saturation}%, ${lightness}%, 0.4)`)
      
      // Draw blob outline
      ctx.beginPath()
      ctx.moveTo(blobPoints[0][0], blobPoints[0][1])
      
      for (let i = 1; i < blobPoints.length; i++) {
        const curr = blobPoints[i]
        const next = blobPoints[(i + 1) % blobPoints.length]
        const cpx = curr[0] + (next[0] - curr[0]) * 0.5
        const cpy = curr[1] + (next[1] - curr[1]) * 0.5
        ctx.quadraticCurveTo(curr[0], curr[1], cpx, cpy)
      }
      
      ctx.closePath()
      ctx.fillStyle = gradient
      ctx.fill()
      
      // Subtle outline
      ctx.strokeStyle = `hsla(${hue}, ${saturation}%, ${lightness + 30}%, 0.6)`
      ctx.lineWidth = 1
      ctx.stroke()
    }
    
    // Draw neural activity INSIDE the blob
    const centerX = 200
    const centerY = 120
    
    // Internal neural connections - more organic
    nodes.forEach(node => {
      // Scale nodes to fit inside blob
      const scaledNode = {
        ...node,
        x: centerX + (node.x - 200) * 0.5, // Scale to fit inside larger blob
        y: centerY + (node.y - 120) * 0.5,
        radius: node.radius * 0.8
      }
      
      // Draw neural pathways as organic tendrils
      node.connections.forEach(connId => {
        const connNode = nodes.find(n => n.id === connId)
        if (!connNode) return
        
        const scaledConn = {
          x: centerX + (connNode.x - 200) * 0.5,
          y: centerY + (connNode.y - 120) * 0.5
        }
        
        const strength = (node.activity + connNode.activity) / 2
        if (strength > 0.2) {
          // Draw wavy neural pathways
          ctx.beginPath()
          ctx.moveTo(scaledNode.x, scaledNode.y)
          
          const midX = (scaledNode.x + scaledConn.x) / 2
          const midY = (scaledNode.y + scaledConn.y) / 2
          const waveOffset = Math.sin(systemTick * 0.1 + node.x) * 8
          
          ctx.quadraticCurveTo(
            midX + waveOffset, midY + waveOffset,
            scaledConn.x, scaledConn.y
          )
          
          const opacity = 0.3 + (strength * 0.4)
          ctx.strokeStyle = `rgba(100, 255, 200, ${opacity})`
          ctx.lineWidth = 1 + strength
          ctx.stroke()
          
          // Flowing energy particles
          if (strength > 0.5) {
            const t = (systemTick * 0.02) % 1
            const particleX = scaledNode.x + (scaledConn.x - scaledNode.x) * t
            const particleY = scaledNode.y + (scaledConn.y - scaledNode.y) * t + Math.sin(t * Math.PI * 2) * 3
            
            ctx.beginPath()
            ctx.arc(particleX, particleY, 1.5, 0, 2 * Math.PI)
            ctx.fillStyle = `rgba(150, 255, 150, ${opacity})`
            ctx.fill()
          }
        }
      })
    })
    
    // Draw neural nodes as brain regions inside blob
    nodes.forEach(node => {
      const scaledNode = {
        x: centerX + (node.x - 200) * 0.5,
        y: centerY + (node.y - 120) * 0.5,
        radius: (node.radius * 0.8) + (node.activity * 3)
      }
      
      const activity = node.activity + Math.sin(systemTick * 0.15 + node.x) * 0.1
      
      if (activity > 0.3) {
        // Pulsing neural centers
        ctx.beginPath()
        ctx.arc(scaledNode.x, scaledNode.y, scaledNode.radius, 0, 2 * Math.PI)
        
        const intensity = 0.4 + (activity * 0.6)
        ctx.fillStyle = `rgba(200, 255, 200, ${intensity})`
        ctx.fill()
        
        // Extra glow for high activity
        if (activity > 0.7) {
          ctx.beginPath()
          ctx.arc(scaledNode.x, scaledNode.y, scaledNode.radius + 3, 0, 2 * Math.PI)
          ctx.fillStyle = `rgba(255, 255, 255, ${(activity - 0.7) * 0.3})`
          ctx.fill()
        }
      }
    })
    
    // Draw "thought bubbles" or consciousness patterns
    if (petData.attention > 70) {
      const numBubbles = Math.floor(petData.attention / 25)
      for (let i = 0; i < numBubbles; i++) {
        const angle = (systemTick * 0.02 + i) * Math.PI * 2
        const radius = 25 + Math.sin(systemTick * 0.1 + i) * 10
        const x = centerX + Math.cos(angle) * radius
        const y = centerY + Math.sin(angle) * radius * 0.8
        
        ctx.beginPath()
        ctx.arc(x, y, 2 + Math.sin(systemTick * 0.2 + i) * 1, 0, 2 * Math.PI)
        ctx.fillStyle = `rgba(255, 255, 255, ${0.3 + Math.sin(systemTick * 0.1 + i) * 0.2})`
        ctx.fill()
      }
    }
  }

  return (
    <div className="bg-gray-800 border border-gray-700 p-4 min-h-[450px] flex flex-col items-center justify-start w-full font-mono">
      {/* Loading overlay */}
      {isLoading && (
        <div className="absolute inset-0 bg-black/50 z-20 flex items-center justify-center">
          <div className="text-green-400 text-sm">PROCESSING...</div>
        </div>
      )}

      {/* Evolving Blob Canvas */}
      <div className="w-full h-64 mb-4 bg-black border border-gray-600 p-3 relative">
        <div className="text-green-400 text-xs mb-2">[CONSCIOUSNESS] Neural-Biological Entity</div>
        
        <canvas
          ref={canvasRef}
          width={320}
          height={180}
          className="bg-black border border-gray-700"
        />
        
        {/* Status readout overlay */}
        <div className="absolute bottom-3 left-3 right-3">
          <div className="grid grid-cols-4 gap-2 text-xs">
            <div>
              <span className="text-green-400">VITAL:</span> 
              <span className="text-gray-300">{Math.round((petData?.health || 0))}%</span>
            </div>
            <div>
              <span className="text-blue-400">AWARE:</span> 
              <span className="text-gray-300">{Math.round((petData?.attention || 0))}%</span>
            </div>
            <div>
              <span className="text-purple-400">THINK:</span> 
              <span className="text-gray-300">{Math.round(getComplexity())}%</span>
            </div>
            <div>
              <span className="text-yellow-400">FEEL:</span> 
              <span className="text-gray-300">{Math.round((petData?.mood || 0))}%</span>
            </div>
          </div>
        </div>
      </div>

      {/* Last Response Terminal Output */}
      {displayMessage && (
        <div className="bg-black border border-green-400 px-3 py-2 mb-4 font-mono">
          <div className="text-green-400 text-xs mb-1">[OUTPUT] Last Response:</div>
          <div className={`text-yellow-400 text-sm ${isAnimating ? 'animate-pulse' : ''}`}>
            {displayMessage}
          </div>
        </div>
      )}

      {/* Pet name and status */}
      <div className="text-center">
        <div className="text-green-400 text-sm mb-1">[PROCESS] {petName || petData?.id || 'companion_001'}</div>
        <div className="text-blue-400 text-xs font-mono mb-2">
          {petData?.personality_summary || 'INITIALIZING_PERSONALITY_MATRIX...'}
        </div>
        <div className="text-gray-500 text-xs">
          Last ping: {systemTick}s ago | Status: ACTIVE
        </div>
      </div>

      {/* Interaction hints */}
      {!displayMessage && (
        <div className="text-center mt-4">
          <div className="flex items-center justify-center gap-2 text-xs">
            <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
            <span className="text-gray-500 font-mono">[SYSTEM] Awaiting I/O</span>
          </div>
        </div>
      )}
    </div>
  )
} 