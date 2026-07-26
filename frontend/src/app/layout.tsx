import type { Metadata } from 'next'
import Aurora from '@/components/Aurora'
import Nav from '@/components/Nav'
import { AuthProvider } from '@/contexts/AuthContext'
import './globals.css'

export const metadata: Metadata = {
  title: 'AutoMateAI',
  description: 'AutoMateAI web application',
  icons: {
    icon: '/logo.png',
  },
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en">
      <body
        style={{
          minHeight: '100vh',
          background: '#09090b',
          position: 'relative',
          overflowX: 'hidden',
        }}
      >
        <AuthProvider>
          <Aurora />
          <Nav />
          <main style={{ position: 'relative', zIndex: 1 }}>{children}</main>
        </AuthProvider>
      </body>
    </html>
  )
}
