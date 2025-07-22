"use client"

import { useAuth } from '@/contexts/auth-context'
import { Button } from '@/components/ui/button'
import { User, LogOut, Coins } from 'lucide-react'

interface UserMenuProps {
  onOpenAuth: () => void
}

export function UserMenu({ onOpenAuth }: UserMenuProps) {
  const { user, logout, isLoading } = useAuth()

  if (isLoading) {
    return (
      <div className="flex items-center gap-2">
        <div className="w-8 h-8 bg-pink-200 rounded-full animate-pulse"></div>
        <div className="w-20 h-4 bg-pink-200 rounded animate-pulse"></div>
      </div>
    )
  }

  if (!user) {
    return (
      <Button
        onClick={onOpenAuth}
        variant="outline"
        size="sm"
        className="border-pink-300 text-pink-700 hover:bg-pink-50"
      >
        <User className="w-4 h-4 mr-2" />
        Sign In
      </Button>
    )
  }

  return (
    <div className="flex items-center gap-4">
      {/* Token Balance */}
      <div className="flex items-center gap-1 bg-yellow-100 px-2 py-1 rounded-full">
        <Coins className="w-4 h-4 text-yellow-600" />
        <span className="text-sm font-medium text-yellow-700">
          {user.token_balance.toLocaleString()}
        </span>
      </div>

      {/* User Info */}
      <div className="flex items-center gap-2">
        <div className="w-8 h-8 bg-pink-500 rounded-full flex items-center justify-center">
          <span className="text-white text-sm font-semibold">
            {user.username.charAt(0).toUpperCase()}
          </span>
        </div>
        <div className="text-sm">
          <div className="font-medium text-pink-700">{user.username}</div>
          <div className="text-pink-500 text-xs">{user.email}</div>
        </div>
      </div>

      {/* Logout Button */}
      <Button
        onClick={logout}
        variant="outline"
        size="sm"
        className="border-pink-300 text-pink-700 hover:bg-pink-50"
      >
        <LogOut className="w-4 h-4" />
      </Button>
    </div>
  )
}