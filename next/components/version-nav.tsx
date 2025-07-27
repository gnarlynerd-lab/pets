"use client"

import Link from 'next/link'
import { usePathname } from 'next/navigation'

export function VersionNav() {
  const pathname = usePathname()
  
  const versions = [
    { path: '/', label: 'Minimal' },
    { path: '/full', label: 'Full' }
  ]

  return (
    <div className="fixed top-4 left-4 z-50">
      <div className="bg-white border border-black shadow-lg">
        <div className="text-xs uppercase tracking-wider text-gray-600 p-2 border-b border-gray-300">
          Interface
        </div>
        <div className="space-y-1 p-2">
          {versions.map((version) => (
            <Link
              key={version.path}
              href={version.path}
              className={`block px-3 py-1 text-sm transition-colors ${
                pathname === version.path
                  ? 'bg-black text-white'
                  : 'hover:bg-gray-100'
              }`}
            >
              {version.label}
            </Link>
          ))}
        </div>
      </div>
    </div>
  )
}