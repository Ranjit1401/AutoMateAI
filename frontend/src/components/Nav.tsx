'use client'

import Link from 'next/link'
import { usePathname, useRouter } from 'next/navigation'
import { Home, MessageSquare, Brain, Plug, ScrollText, Settings, User, LogOut, ListChecks } from 'lucide-react'
import { useState, type ElementType } from 'react'
import { useAuth } from '@/contexts/AuthContext'

const navItems: { href: string; label: string; icon: ElementType }[] = [
  { href: '/', label: 'Home', icon: Home },
  { href: '/chat', label: 'Chat', icon: MessageSquare },
  { href: '/tasks', label: 'Tasks', icon: ListChecks },
  { href: '/memory', label: 'Memory', icon: Brain },
  { href: '/apps', label: 'Connected Apps', icon: Plug },
  { href: '/logs', label: 'Logs', icon: ScrollText },
  { href: '/settings', label: 'Settings', icon: Settings },
]

export default function Nav() {
  const pathname = usePathname()
  const router = useRouter()
  const { user, logout } = useAuth()
  const [menuOpen, setMenuOpen] = useState(false)

  const handleLogout = async () => {
    setMenuOpen(false)
    await logout()
    router.push('/login')
  }

  return (
    <header
      style={{
        position: 'fixed',
        top: 20,
        left: '50%',
        transform: 'translateX(-50%)',
        zIndex: 100,
        width: 'calc(100% - 48px)',
        maxWidth: 900,
      }}
    >
      <div
        className="glass"
        style={{
          display: 'flex',
          alignItems: 'center',
          padding: '10px 16px',
          gap: 4,
          boxShadow: '0 8px 32px rgba(0,0,0,0.4), 0 0 0 1px rgba(255,255,255,0.06) inset',
        }}
      >
        {/* Logo */}
        <Link
          href="/"
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: 8,
            padding: '6px 12px',
            borderRadius: 12,
            textDecoration: 'none',
            marginRight: 8,
          }}
        >
          <div
            style={{
              width: 28,
              height: 28,
              borderRadius: 8,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              filter: 'drop-shadow(0 0 8px rgba(168,85,247,0.5))',
            }}
          >
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img src="/logo.png" alt="AutoMateAI" style={{ width: 26, height: 26, objectFit: 'contain' }} />
          </div>
          <span
            style={{
              fontSize: 15,
              fontWeight: 600,
              color: 'white',
              letterSpacing: '-0.3px',
            }}
          >
            AutoMateAI
          </span>
        </Link>

        {/* Divider */}
        <div
          style={{
            width: 1,
            height: 20,
            background: 'rgba(255,255,255,0.1)',
            margin: '0 8px',
          }}
        />

        {/* Nav items */}
        <nav style={{ display: 'flex', alignItems: 'center', gap: 2, flex: 1 }}>
          {navItems.map(({ href, label, icon: Icon }) => {
            const isActive = pathname === href
            return (
              <Link
                key={href}
                href={href}
                className="nav-link"
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: 6,
                  padding: '7px 12px',
                  borderRadius: 10,
                  cursor: 'pointer',
                  fontSize: 13,
                  fontWeight: 500,
                  fontFamily: 'inherit',
                  textDecoration: 'none',
                  background: isActive
                    ? 'linear-gradient(135deg, rgba(168,85,247,0.2), rgba(99,102,241,0.15))'
                    : 'transparent',
                  color: isActive ? '#ffffff' : 'rgba(255,255,255,0.85)',
                  transition: 'all 0.2s ease',
                  whiteSpace: 'nowrap',
                  boxShadow: isActive ? 'inset 0 0 0 1px rgba(168,85,247,0.25)' : 'none',
                }}
              >
                <Icon size={13} />
                <span className="nav-link-label">{label}</span>
              </Link>
            )
          })}
        </nav>

        {/* User avatar */}
        <div style={{ position: 'relative', marginLeft: 8 }}>
          <button
            onClick={() => setMenuOpen((open) => !open)}
            style={{
              width: 32,
              height: 32,
              borderRadius: '50%',
              background: 'rgba(255,255,255,0.08)',
              border: '1px solid rgba(255,255,255,0.14)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              cursor: 'pointer',
              flexShrink: 0,
              padding: 0,
            }}
          >
            <User size={15} color="white" />
          </button>

          {menuOpen && (
            <div
              className="glass"
              style={{
                position: 'absolute',
                top: 42,
                right: 0,
                minWidth: 200,
                padding: 10,
                borderRadius: 12,
                boxShadow: '0 8px 32px rgba(0,0,0,0.5)',
              }}
            >
              {user ? (
                <>
                  <div style={{ padding: '6px 8px 10px', fontSize: 12, color: 'rgba(255,255,255,0.6)' }}>
                    Signed in as
                    <div style={{ color: 'white', fontSize: 13, fontWeight: 500, marginTop: 2 }}>{user.email}</div>
                  </div>
                  <button
                    onClick={handleLogout}
                    style={{
                      width: '100%',
                      display: 'flex',
                      alignItems: 'center',
                      gap: 8,
                      padding: '8px 8px',
                      borderRadius: 8,
                      background: 'transparent',
                      border: 'none',
                      color: 'rgba(255,255,255,0.85)',
                      fontSize: 13,
                      cursor: 'pointer',
                      fontFamily: 'inherit',
                    }}
                  >
                    <LogOut size={14} /> Log out
                  </button>
                </>
              ) : (
                <Link
                  href="/login"
                  onClick={() => setMenuOpen(false)}
                  style={{
                    display: 'block',
                    padding: '8px 8px',
                    borderRadius: 8,
                    color: 'white',
                    fontSize: 13,
                    textDecoration: 'none',
                  }}
                >
                  Sign in
                </Link>
              )}
            </div>
          )}
        </div>
      </div>
    </header>
  )
}
