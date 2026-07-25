'use client'

import { useState } from 'react'
import { CheckCircle, Plus } from 'lucide-react'

interface AppEntry {
  name: string
  category: string
  color: string
  letter: string
  connected: boolean
  uses: number
  desc: string
}

// Populated once the backend is connected.
const apps: AppEntry[] = []

// Reserved space for the Orbit component (to be added later). Keeping the
// same dimensions here means dropping the real component in won't shift
// the rest of the page layout.
function OrbitPlaceholder() {
  return (
    <div
      style={{
        position: 'relative',
        width: 480,
        height: 480,
        maxWidth: '100%',
        margin: '0 auto 40px',
        flexShrink: 0,
      }}
    />
  )
}

export default function ConnectedApps() {
  const [filter, setFilter] = useState<'all' | 'connected' | 'available'>('all')

  const filtered = apps.filter(a =>
    filter === 'connected' ? a.connected : filter === 'available' ? !a.connected : true
  )

  const connectedCount = apps.filter(a => a.connected).length

  return (
    <div
      style={{
        position: 'relative',
        zIndex: 1,
        minHeight: '100vh',
        paddingTop: 100,
        paddingBottom: 80,
      }}
    >
      <div style={{ maxWidth: 960, margin: '0 auto', padding: '24px' }}>
        <div
          style={{
            marginBottom: 40,
            textAlign: 'center',
            animation: 'slide-up 0.5s cubic-bezier(0.16,1,0.3,1) both',
          }}
        >
          <h1
            style={{ fontSize: 28, fontWeight: 700, color: 'white', letterSpacing: '-0.5px', margin: '0 0 8px' }}
          >
            Connected Apps
          </h1>
          <p style={{ fontSize: 14, color: '#52525b', margin: 0 }}>
            {connectedCount > 0
              ? `${connectedCount} apps connected · AutoMateAI orchestrates them all`
              : 'No connected apps. Waiting for backend connection.'}
          </p>
        </div>

        {/* Orbit visualization — reserved space, component added later */}
        <div style={{ animation: 'fade-in 0.8s ease 0.2s both' }}>
          <OrbitPlaceholder />
        </div>

        {/* Filter tabs */}
        <div
          style={{
            display: 'flex',
            justifyContent: 'center',
            gap: 6,
            marginBottom: 24,
          }}
        >
          {(['all', 'connected', 'available'] as const).map(f => (
            <button
              key={f}
              onClick={() => setFilter(f)}
              style={{
                padding: '7px 16px',
                borderRadius: 10,
                border: 'none',
                fontSize: 13,
                fontWeight: 500,
                fontFamily: 'inherit',
                cursor: 'pointer',
                background:
                  filter === f
                    ? 'linear-gradient(135deg, rgba(168,85,247,0.2), rgba(99,102,241,0.15))'
                    : 'rgba(255,255,255,0.04)',
                color: filter === f ? '#c4b5fd' : '#52525b',
                boxShadow: filter === f ? 'inset 0 0 0 1px rgba(168,85,247,0.25)' : 'none',
                transition: 'all 0.2s ease',
              }}
            >
              {f.charAt(0).toUpperCase() + f.slice(1)}
            </button>
          ))}
        </div>

        {/* Apps grid */}
        {filtered.length === 0 ? (
          <div
            className="glass"
            style={{
              padding: '40px 24px',
              textAlign: 'center',
              fontSize: 13,
              color: '#52525b',
            }}
          >
            No connected apps.
          </div>
        ) : (
          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(3, 1fr)',
              gap: 10,
            }}
          >
            {filtered.map((app, i) => (
              <div
                key={app.name}
                className="glass glass-hover"
                style={{
                  padding: '16px',
                  display: 'flex',
                  alignItems: 'center',
                  gap: 12,
                  cursor: 'pointer',
                  animation: `slide-up 0.4s cubic-bezier(0.16,1,0.3,1) ${i * 0.03}s both`,
                }}
              >
                <div
                  style={{
                    width: 40,
                    height: 40,
                    borderRadius: '50%',
                    background: `${app.color}15`,
                    border: `1.5px solid ${app.color}40`,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontSize: 12,
                    fontWeight: 700,
                    color: app.color === '#ffffff' ? '#a1a1aa' : app.color,
                    flexShrink: 0,
                    boxShadow: `0 0 12px ${app.color}20`,
                  }}
                >
                  {app.letter}
                </div>
                <div style={{ flex: 1, minWidth: 0 }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginBottom: 2 }}>
                    <span style={{ fontSize: 13, fontWeight: 600, color: 'white' }}>{app.name}</span>
                    {app.connected && <CheckCircle size={11} color="#10b981" />}
                  </div>
                  <p
                    style={{
                      margin: 0,
                      fontSize: 11,
                      color: '#52525b',
                      overflow: 'hidden',
                      textOverflow: 'ellipsis',
                      whiteSpace: 'nowrap',
                    }}
                  >
                    {app.desc}
                  </p>
                  {app.connected && (
                    <span style={{ fontSize: 10, color: '#3f3f46', marginTop: 2, display: 'block' }}>
                      Used {app.uses} times
                    </span>
                  )}
                </div>
                {app.connected ? (
                  <span
                    style={{
                      fontSize: 10,
                      fontWeight: 500,
                      color: '#10b981',
                      background: '#10b98115',
                      padding: '3px 8px',
                      borderRadius: 6,
                      border: '1px solid #10b98125',
                      flexShrink: 0,
                    }}
                  >
                    Active
                  </span>
                ) : (
                  <button
                    className="btn-glass"
                    style={{ padding: '4px 10px', fontSize: 11, flexShrink: 0 }}
                  >
                    <Plus size={10} style={{ display: 'inline', marginRight: 3 }} />
                    Connect
                  </button>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
