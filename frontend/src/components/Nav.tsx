'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { Sparkles, Home, MessageSquare, Brain, Plug, ScrollText, Settings } from 'lucide-react'
import type { ElementType } from 'react'

const navItems: { href: string; label: string; icon: ElementType }[] = [
  { href: '/', label: 'Home', icon: Home },
  { href: '/chat', label: 'Chat', icon: MessageSquare },
  { href: '/memory', label: 'Memory', icon: Brain },
  { href: '/apps', label: 'Connected Apps', icon: Plug },
  { href: '/logs', label: 'Logs', icon: ScrollText },
  { href: '/settings', label: 'Settings', icon: Settings },
]

export default function Nav() {
  const pathname = usePathname()

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
              background: 'linear-gradient(135deg, #a855f7, #6366f1)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              boxShadow: '0 0 12px rgba(168,85,247,0.5)',
            }}
          >
            <Sparkles size={14} color="white" />
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
                  color: isActive ? '#c4b5fd' : '#71717a',
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
        <div
          style={{
            width: 32,
            height: 32,
            borderRadius: '50%',
            background: 'linear-gradient(135deg, #a855f7, #ec4899)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontSize: 12,
            fontWeight: 700,
            color: 'white',
            cursor: 'pointer',
            boxShadow: '0 0 12px rgba(168,85,247,0.4)',
            flexShrink: 0,
            marginLeft: 8,
          }}
        >
          N
        </div>
      </div>
    </header>
  )
}
