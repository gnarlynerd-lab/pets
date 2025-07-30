import './globals.css'
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import { AuthProvider } from '@/contexts/auth-context'
import { DemoAuthProvider } from '@/components/demo-auth'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Affinity - Interactive Companion Platform',
  description: 'Digital companion that communicates through emojis and evolves based on your interactions',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <DemoAuthProvider>
          <AuthProvider>
            {children}
          </AuthProvider>
        </DemoAuthProvider>
      </body>
    </html>
  )
}
