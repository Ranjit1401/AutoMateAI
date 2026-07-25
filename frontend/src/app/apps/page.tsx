'use client'

import { useState } from 'react'
import { CheckCircle, Plus } from 'lucide-react'

const apps = [
  { name: 'Gmail', category: 'Email', color: '#EA4335', letter: 'G', connected: true, uses: 234, desc: 'Read, compose and send emails' },
  { name: 'Google Drive', category: 'Storage', color: '#4285F4', letter: 'D', connected: true, uses: 89, desc: 'Access and manage documents' },
  { name: 'Slack', category: 'Messaging', color: '#E01E5A', letter: 'S', connected: true, uses: 56, desc: 'Send messages and notifications' },
  { name: 'Notion', category: 'Notes', color: '#ffffff', letter: 'N', connected: true, uses: 120, desc: 'Read and write workspace content' },
  { name: 'GitHub', category: 'Code', color: '#6e40c9', letter: 'Gh', connected: true, uses: 44, desc: 'Manage repos, issues and PRs' },
  { name: 'Spotify', category: 'Music', color: '#1DB954', letter: 'Sp', connected: true, uses: 12, desc: 'Control playback and playlists' },
  { name: 'Google Calendar', category: 'Calendar', color: '#0F9D58', letter: 'C', connected: true, uses: 198, desc: 'Schedule and manage events' },
  { name: 'Zoom', category: 'Meetings', color: '#2D8CFF', letter: 'Zo', connected: false, uses: 0, desc: 'Join and schedule video calls' },
  { name: 'WhatsApp', category: 'Messaging', color: '#25D366', letter: 'W', connected: false, uses: 0, desc: 'Send WhatsApp messages' },
  { name: 'Google Maps', category: 'Navigation', color: '#F4B400', letter: 'M', connected: false, uses: 0, desc: 'Search places and get directions' },
  { name: 'Stripe', category: 'Payments', color: '#635BFF', letter: 'St', connected: false, uses: 0, desc: 'Manage payments and invoices' },
  { name: 'Linear', category: 'Project', color: '#5E6AD2', letter: 'Li', connected: false, uses: 0, desc: 'Manage issues and projects' },
]

const ORBIT_APPS = apps.slice(0, 8)

function OrbitalCore() {
  return (
    <div
      style={{
        position: 'relative',
        width: 480,
        height: 480,
        margin: '0 auto 40px',
        flexShrink: 0,
      }}
    >
      {/* Outer orbit ring */}
      <div
        style={{
          position: 'absolute',
          inset: 0,
          borderRadius: '50%',
          border: '1px solid rgba(255,255,255,0.04)',
        }}
      />
      {/* Inner orbit ring */}
      <div
        style={{
          position: 'absolute',
          inset: 60,
          borderRadius: '50%',
          border: '1px solid rgba(168,85,247,0.08)',
        }}
      />

      {/* Core */}
      <div
        style={{
          position: 'absolute',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          width: 90,
          height: 90,
          borderRadius: '50%',
          background: 'linear-gradient(135deg, rgba(168,85,247,0.3), rgba(99,102,241,0.2))',
          border: '1px solid rgba(168,85,247,0.4)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          boxShadow:
            '0 0 60px rgba(168,85,247,0.3), 0 0 120px rgba(168,85,247,0.1), inset 0 0 30px rgba(168,85,247,0.1)',
          backdropFilter: 'blur(12px)',
          animation: 'pulse-glow 3s ease-in-out infinite',
          zIndex: 2,
        }}
      >
        <div
          style={{
            fontSize: 11,
            fontWeight: 700,
            color: '#c4b5fd',
            textAlign: 'center',
            letterSpacing: '0.5px',
          }}
        >
          <div style={{ fontSize: 18 }}>AI</div>
          <div style={{ opacity: 0.7, fontSize: 9 }}>CORE</div>
        </div>
      </div>

      {/* Orbiting apps */}
      {ORBIT_APPS.map((app, i) => {
        const angle = (i / ORBIT_APPS.length) * 360
        const rad = (angle * Math.PI) / 180
        const r = 180
        const x = 240 + r * Math.cos(rad) - 22
        const y = 240 + r * Math.sin(rad) - 22
        return (
          <div
            key={app.name}
            title={app.name}
            style={{
              position: 'absolute',
              left: x,
              top: y,
              width: 44,
              height: 44,
              borderRadius: '50%',
              background: `${app.color}20`,
              border: `2px solid ${app.color}50`,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: 11,
              fontWeight: 700,
              color: app.color === '#ffffff' ? '#a1a1aa' : app.color,
              cursor: 'pointer',
              transition: 'transform 0.3s ease, box-shadow 0.3s ease',
              boxShadow: `0 0 16px ${app.color}30`,
              backdropFilter: 'blur(8px)',
              animation: `float-gentle ${4 + i * 0.5}s ease-in-out ${i * 0.3}s infinite`,
              zIndex: 1,
            }}
            onMouseEnter={e => {
              const el = e.currentTarget as HTMLDivElement
              el.style.transform = 'scale(1.2)'
              el.style.boxShadow = `0 0 30px ${app.color}60`
            }}
            onMouseLeave={e => {
              const el = e.currentTarget as HTMLDivElement
              el.style.transform = 'scale(1)'
              el.style.boxShadow = `0 0 16px ${app.color}30`
            }}
          >
            {app.letter}
          </div>
        )
      })}

      {/* Connection lines */}
      <svg
        style={{ position: 'absolute', inset: 0, pointerEvents: 'none' }}
        width="480"
        height="480"
      >
        {ORBIT_APPS.filter(a => a.connected).map((app, i) => {
          const angle = (i / ORBIT_APPS.length) * 360
          const rad = (angle * Math.PI) / 180
          const r = 180
          const x = 240 + r * Math.cos(rad)
          const y = 240 + r * Math.sin(rad)
          return (
            <line
              key={app.name}
              x1={240}
              y1={240}
              x2={x}
              y2={y}
              stroke={`${app.color}20`}
              strokeWidth={1}
              strokeDasharray="4 6"
            />
          )
        })}
      </svg>
    </div>
  )
}

export default function ConnectedApps() {
  const [filter, setFilter] = useState<'all' | 'connected' | 'available'>('all')

  const filtered = apps.filter(a =>
    filter === 'connected' ? a.connected : filter === 'available' ? !a.connected : true
  )

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
            {apps.filter(a => a.connected).length} apps connected · AutoMateAI orchestrates them all
          </p>
        </div>

        {/* Orbital visualization */}
        <div style={{ animation: 'fade-in 0.8s ease 0.2s both' }}>
          <OrbitalCore />
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
      </div>
    </div>
  )
}
