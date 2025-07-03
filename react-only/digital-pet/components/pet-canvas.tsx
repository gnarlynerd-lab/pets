"use client"

import { useEffect, useRef, useState } from "react"

declare global {
  interface Window {
    p5: any
  }
}

export default function PetCanvas() {
  const canvasRef = useRef<HTMLDivElement>(null)
  const [isP5Ready, setIsP5Ready] = useState(false)

  // Load p5 from CDN to avoid gifenc ESM issue
  useEffect(() => {
    if (typeof window === "undefined") return

    if (window.p5) {
      setIsP5Ready(true)
      return
    }

    const script = document.createElement("script")
    script.src = "https://cdn.jsdelivr.net/npm/p5@1.9.0/lib/p5.min.js"
    script.async = true
    script.onload = () => setIsP5Ready(true)
    document.body.appendChild(script)

    return () => {
      if (document.body.contains(script)) {
        document.body.removeChild(script)
      }
    }
  }, [])

  // Create the p5 sketch
  useEffect(() => {
    if (!isP5Ready || !canvasRef.current) return
    const p5 = window.p5 as any

    // Clear any existing canvas
    while (canvasRef.current.firstChild) {
      canvasRef.current.removeChild(canvasRef.current.firstChild)
    }

    const sketch = (p: any) => {
      p.setup = () => {
        const width = Math.min(600, canvasRef.current?.clientWidth || 600)
        const height = Math.min(400, width * 0.67)
        p.createCanvas(width, height)
      }

      p.draw = () => {
        // Laboratory environment background
        p.background(47, 79, 79, 200)

        // Add subtle grid pattern
        p.stroke(70, 130, 180, 30)
        p.strokeWeight(0.5)
        for (let i = 0; i < p.width; i += 20) {
          p.line(i, 0, i, p.height)
        }
        for (let i = 0; i < p.height; i += 20) {
          p.line(0, i, p.width, i)
        }

        // Laboratory specimen platform
        p.fill(138, 108, 60, 100)
        p.noStroke()
        p.ellipse(p.width / 2, p.height - 30, p.width * 0.8, 20)

        // Placeholder for pet rendering - this is where PetRenderer would be used
        p.fill(70, 130, 180, 150)
        p.noStroke()
        p.ellipse(p.width / 2, p.height / 2 + 20, 150, 150)

        // Add some simple animation for the placeholder
        const breathe = p.sin(p.frameCount * 0.05) * 10
        p.fill(255, 99, 71, 120)
        p.ellipse(p.width / 2, p.height / 2 + 20, 100 + breathe, 100 + breathe)

        // Simple eyes with laboratory glow
        p.fill(255, 255, 255, 200)
        p.ellipse(p.width / 2 - 20, p.height / 2 + 10, 20, 20)
        p.ellipse(p.width / 2 + 20, p.height / 2 + 10, 20, 20)

        p.fill(70, 130, 180)
        p.ellipse(p.width / 2 - 20, p.height / 2 + 10, 8, 8)
        p.ellipse(p.width / 2 + 20, p.height / 2 + 10, 8, 8)

        // Laboratory particle effects
        p.fill(255, 99, 71, 100)
        for (let i = 0; i < 5; i++) {
          const x = p.width / 2 + p.sin(p.frameCount * 0.02 + i) * 80
          const y = p.height / 2 + p.cos(p.frameCount * 0.03 + i) * 60
          p.ellipse(x, y, 3, 3)
        }
      }

      p.windowResized = () => {
        if (!canvasRef.current) return
        const width = Math.min(600, canvasRef.current.clientWidth)
        const height = Math.min(400, width * 0.67)
        p.resizeCanvas(width, height)
      }
    }

    const instance = new p5(sketch, canvasRef.current)

    return () => {
      instance.remove()
    }
  }, [isP5Ready])

  return (
    <div className="p-8">
      <div ref={canvasRef} className="w-full h-full flex items-center justify-center" style={{ minHeight: "300px" }} />
    </div>
  )
}
