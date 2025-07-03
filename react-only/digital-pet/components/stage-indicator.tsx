"use client"

import { Star, Beaker, Microscope, Atom, Dna } from "lucide-react"

interface StageIndicatorProps {
  stage: number
}

export default function StageIndicator({ stage }: StageIndicatorProps) {
  const maxStage = 4
  const stageNames = ["EMBRYONIC", "JUVENILE", "ADOLESCENT", "MATURE", "EVOLVED"]
  const stageIcons = [Beaker, Microscope, Atom, Dna, Star]

  return (
    <div className="bg-gradient-to-br from-[#2F4F4F] to-[#1a2f2f] p-6 rounded-2xl shadow-2xl border-2 border-[#8A6C3C] font-mono">
      <h2 className="text-lg font-bold mb-6 text-[#FF6347] flex items-center">
        <Dna className="h-5 w-5 mr-2" />
        DEVELOPMENT PHASE
      </h2>

      <div className="flex items-center justify-between mb-6">
        <span className="text-sm font-bold text-[#4682B4]">{stageNames[stage]}</span>
        <span className="text-xs text-[#8A6C3C] bg-[#1a2f2f] px-2 py-1 rounded border border-[#8A6C3C]">
          PHASE {stage} / {maxStage}
        </span>
      </div>

      <div className="flex justify-between items-center">
        {Array.from({ length: maxStage + 1 }).map((_, index) => {
          const IconComponent = stageIcons[index]
          return (
            <div key={index} className="flex items-center">
              <div
                className={`relative flex items-center justify-center w-12 h-12 rounded-full transition-all duration-500 border-2 ${
                  index <= stage
                    ? "bg-gradient-to-br from-[#FF6347] to-[#8A6C3C] text-white border-[#FF6347] scale-110 shadow-lg"
                    : "bg-[#1a2f2f] text-[#4682B4] border-[#8A6C3C]"
                }`}
              >
                <IconComponent className="w-6 h-6" />
                {index <= stage && (
                  <div className="absolute inset-0 rounded-full bg-gradient-to-t from-white/20 to-transparent"></div>
                )}
              </div>
              {index < maxStage && (
                <div className="flex items-center mx-2">
                  <div
                    className={`h-1 w-8 transition-all duration-500 ${
                      index < stage ? "bg-gradient-to-r from-[#FF6347] to-[#8A6C3C]" : "bg-[#8A6C3C]/30"
                    }`}
                  />
                  {/* Laboratory connection nodes */}
                  <div
                    className={`w-2 h-2 rounded-full mx-1 ${index < stage ? "bg-[#FF6347]" : "bg-[#8A6C3C]/30"}`}
                  ></div>
                  <div
                    className={`h-1 w-8 transition-all duration-500 ${
                      index < stage ? "bg-gradient-to-r from-[#8A6C3C] to-[#FF6347]" : "bg-[#8A6C3C]/30"
                    }`}
                  />
                </div>
              )}
            </div>
          )
        })}
      </div>

      {/* Laboratory measurement display */}
      <div className="mt-6 p-3 bg-[#1a2f2f] rounded border border-[#8A6C3C] text-xs">
        <div className="flex justify-between text-[#4682B4]">
          <span>COMPLEXITY INDEX:</span>
          <span className="text-[#FF6347] font-bold">{((stage + 1) * 20).toFixed(1)}%</span>
        </div>
        <div className="flex justify-between text-[#4682B4] mt-1">
          <span>NEURAL PATHWAYS:</span>
          <span className="text-[#FF6347] font-bold">{Math.pow(2, stage + 1)} ACTIVE</span>
        </div>
      </div>
    </div>
  )
}
