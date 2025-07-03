"use client"

import { Button } from "@/components/ui/button"
import { Heart, Utensils, Gamepad2, Zap, Activity, Search } from "lucide-react"

interface InteractionControlsProps {
  onFeed: () => void
  onPlay: () => void
  onPet: () => void
}

export default function InteractionControls({ onFeed, onPlay, onPet }: InteractionControlsProps) {
  return (
    <div className="mt-6 grid grid-cols-3 gap-4">
      <Button
        onClick={onFeed}
        className="flex flex-col items-center justify-center py-8 bg-gradient-to-br from-[#2F4F4F] to-[#1a2f2f] hover:from-[#4682B4] hover:to-[#2F4F4F] transition-all duration-300 shadow-2xl gap-2 border-2 border-[#8A6C3C] font-mono group relative overflow-hidden"
      >
        {/* Laboratory equipment styling */}
        <div className="absolute inset-0 bg-gradient-to-r from-transparent via-[#8A6C3C]/10 to-transparent transform -skew-x-12 group-hover:translate-x-full transition-transform duration-700"></div>

        <div className="relative z-10 flex flex-col items-center gap-2">
          <div className="relative">
            <Utensils className="h-8 w-8 text-[#FF6347]" />
            <Zap className="absolute -top-1 -right-1 h-4 w-4 text-[#8A6C3C] animate-pulse" />
          </div>
          <div className="text-center">
            <div className="text-sm font-bold text-[#FF6347]">NUTRITIONAL</div>
            <div className="text-xs text-[#4682B4]">CALIBRATION</div>
          </div>
        </div>

        {/* Equipment details */}
        <div className="absolute bottom-1 left-1 text-xs text-[#8A6C3C] opacity-60">NUT-01</div>
      </Button>

      <Button
        onClick={onPlay}
        className="flex flex-col items-center justify-center py-8 bg-gradient-to-br from-[#2F4F4F] to-[#1a2f2f] hover:from-[#4682B4] hover:to-[#2F4F4F] transition-all duration-300 shadow-2xl gap-2 border-2 border-[#8A6C3C] font-mono group relative overflow-hidden"
      >
        <div className="absolute inset-0 bg-gradient-to-r from-transparent via-[#8A6C3C]/10 to-transparent transform -skew-x-12 group-hover:translate-x-full transition-transform duration-700"></div>

        <div className="relative z-10 flex flex-col items-center gap-2">
          <div className="relative">
            <Gamepad2 className="h-8 w-8 text-[#FF6347]" />
            <Activity className="absolute -top-1 -right-1 h-4 w-4 text-[#8A6C3C] animate-pulse" />
          </div>
          <div className="text-center">
            <div className="text-sm font-bold text-[#FF6347]">ENVIRONMENTAL</div>
            <div className="text-xs text-[#4682B4]">STIMULATION</div>
          </div>
        </div>

        <div className="absolute bottom-1 left-1 text-xs text-[#8A6C3C] opacity-60">ENV-02</div>
      </Button>

      <Button
        onClick={onPet}
        className="flex flex-col items-center justify-center py-8 bg-gradient-to-br from-[#2F4F4F] to-[#1a2f2f] hover:from-[#4682B4] hover:to-[#2F4F4F] transition-all duration-300 shadow-2xl gap-2 border-2 border-[#8A6C3C] font-mono group relative overflow-hidden"
      >
        <div className="absolute inset-0 bg-gradient-to-r from-transparent via-[#8A6C3C]/10 to-transparent transform -skew-x-12 group-hover:translate-x-full transition-transform duration-700"></div>

        <div className="relative z-10 flex flex-col items-center gap-2">
          <div className="relative">
            <Heart className="h-8 w-8 text-[#FF6347]" />
            <Search className="absolute -top-1 -right-1 h-4 w-4 text-[#8A6C3C] animate-pulse" />
          </div>
          <div className="text-center">
            <div className="text-sm font-bold text-[#FF6347]">SPECIMEN</div>
            <div className="text-xs text-[#4682B4]">ANALYSIS</div>
          </div>
        </div>

        <div className="absolute bottom-1 left-1 text-xs text-[#8A6C3C] opacity-60">SPC-03</div>
      </Button>
    </div>
  )
}
