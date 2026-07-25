'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import {
  Sparkles,
  Mic,
  Paperclip,
  MapPin,
  Hotel,
  Search,
  Mail,
  Calendar,
  FileText,
  BarChart3,
  Plug,
  CheckCircle,
} from 'lucide-react'

const quickActions = [
  { icon: MapPin, label: 'Plan Trip', color: '#a855f7', desc: 'Research & book travel' },
  { icon: Hotel, label: 'Book Hotel', color: '#8b5cf6', desc: 'Find & reserve stays' },
  { icon: Search, label: 'Research Topic', color: '#6366f1', desc: 'Deep-dive analysis' },
  { icon: Mail, label: 'Send Email', color: '#ec4899', desc: 'Draft & send messages' },
  { icon: Calendar, label: 'Schedule Meeting', color: '#06b6d4', desc: 'Manage your calendar' },
  { icon: FileText, label: 'Analyze Document', color: '#10b981', desc: 'Extract key insights' },
  { icon: BarChart3, label: 'Generate Report', color: '#f59e0b', desc: 'Data-driven reports' },
  { icon: Plug, label: 'Connect Apps', color: '#a855f7', desc: 'Integrate services' },
]

interface RecentTask {
  icon: React.ElementType
  title: string
  status: string
  time: string
  color: string
}

interface ConnectedAppEntry {
  name: string
  color: string
  letter: string
}

// Populated once the backend is connected.
const recentTasks: RecentTask[] = []

// Populated once the backend is connected.
const connectedApps: ConnectedAppEntry[] = []

function StatusDot({ status }: { status: string }) {
  if (status === 'completed') {
    return <CheckCircle size={14} color="#10b981" />
  }
  if (status === 'running') {
    return (
      <div
        style={{
          width: 8,
          height: 8,
          borderRadius: '50%',
          background: '#a855f7',
          animation: 'status-pulse 1.5s ease-in-out infinite',
          boxShadow: '0 0 8px rgba(168,85,247,0.6)',
        }}
      />
    )
  }
  return (
    <div
      style={{
        width: 8,
        height: 8,
        borderRadius: '50%',
        background: '#52525b',
      }}
    />
  )
}

function StatusLabel({ status }: { status: string }) {
  const map: Record<string, { color: string; label: string }> = {
    completed: { color: '#10b981', label: 'Completed' },
    running: { color: '#a855f7', label: 'Running' },
    waiting: { color: '#52525b', label: 'Waiting' },
  }
  const { color, label } = map[status] || map.waiting
  return (
    <span
      style={{
        fontSize: 11,
        fontWeight: 500,
        color,
        background: `${color}18`,
        padding: '3px 10px',
        borderRadius: 100,
        border: `1px solid ${color}30`,
        letterSpacing: '0.1px',
      }}
    >
      {label}
    </span>
  )
}

export default function Home() {
  const router = useRouter()
  const [prompt, setPrompt] = useState('')

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
      <div
        style={{
          maxWidth: 860,
          margin: '0 auto',
          padding: '0 24px',
        }}
      >
        {/* Hero */}
        <div
          style={{
            textAlign: 'center',
            paddingTop: 60,
            paddingBottom: 48,
            animation: 'slide-up 0.6s cubic-bezier(0.16,1,0.3,1) both',
          }}
        >
          <div
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: 6,
              padding: '6px 14px',
              borderRadius: 100,
              background: 'rgba(255,255,255,0.05)',
              border: '1px solid rgba(255,255,255,0.1)',
              fontSize: 12,
              color: '#a1a1aa',
              fontWeight: 500,
              marginBottom: 32,
              letterSpacing: '0.3px',
            }}
          >
            <div
              style={{
                width: 6,
                height: 6,
                borderRadius: '50%',
                background: '#52525b',
              }}
            />
            Waiting for backend connection
          </div>

          <p
            style={{
              fontSize: 18,
              color: '#71717a',
              fontWeight: 400,
              margin: '0 0 12px',
              letterSpacing: '-0.1px',
            }}
          >
            Good afternoon.
          </p>

          <h1
            style={{
              fontSize: 'clamp(32px, 5vw, 52px)',
              fontWeight: 700,
              lineHeight: 1.15,
              letterSpacing: '-1.5px',
              margin: '0 0 20px',
              color: 'white',
            }}
            className="text-gradient"
          >
            What would you like me to<br />accomplish today?
          </h1>

          <p
            style={{
              fontSize: 16,
              color: '#52525b',
              lineHeight: 1.7,
              maxWidth: 580,
              margin: '0 auto',
              fontWeight: 400,
            }}
          >
            I can plan trips, book flights, reserve hotels, manage emails, schedule
            meetings, research topics, automate workflows and complete multi-step
            tasks autonomously.
          </p>
        </div>

        {/* Prompt input */}
        <div
          style={{
            animation: 'slide-up 0.6s cubic-bezier(0.16,1,0.3,1) 0.1s both',
            marginBottom: 40,
          }}
        >
          <div
            className="glass"
            style={{
              display: 'flex',
              alignItems: 'center',
              padding: '14px 16px',
              gap: 12,
              boxShadow: '0 0 0 1px rgba(168,85,247,0.12), 0 20px 60px rgba(0,0,0,0.5)',
              transition: 'box-shadow 0.3s ease',
            }}
            onFocus={() => {}}
          >
            <Sparkles size={18} color="#a855f7" style={{ flexShrink: 0 }} />
            <input
              value={prompt}
              onChange={e => setPrompt(e.target.value)}
              onKeyDown={e => {
                if (e.key === 'Enter' && prompt.trim()) router.push('/chat')
              }}
              placeholder="Ask AutoMateAI anything..."
              style={{
                flex: 1,
                fontSize: 16,
                fontFamily: 'inherit',
                border: 'none',
                background: 'transparent',
                color: 'white',
                outline: 'none',
              }}
            />
            <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
              <button
                className="btn-glass"
                style={{ padding: '6px', borderRadius: 8 }}
                title="Attach file"
              >
                <Paperclip size={15} color="#52525b" />
              </button>
              <button
                className="btn-glass"
                style={{ padding: '6px', borderRadius: 8 }}
                title="Voice input"
              >
                <Mic size={15} color="#52525b" />
              </button>
              <button
                className="btn-primary"
                style={{ padding: '8px 16px', fontSize: 13 }}
                onClick={() => { if (prompt.trim()) router.push('/chat') }}
              >
                <Sparkles size={13} style={{ display: 'inline', marginRight: 6 }} />
                Send
              </button>
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div
          style={{
            animation: 'slide-up 0.6s cubic-bezier(0.16,1,0.3,1) 0.15s both',
            marginBottom: 56,
          }}
        >
          <p
            style={{
              fontSize: 11,
              color: '#52525b',
              fontWeight: 600,
              letterSpacing: '0.08em',
              textTransform: 'uppercase',
              marginBottom: 14,
            }}
          >
            Quick Actions
          </p>
          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(4, 1fr)',
              gap: 10,
            }}
          >
            {quickActions.map(({ icon: Icon, label, desc }) => (
              <button
                key={label}
                onClick={() => router.push('/chat')}
                className="glass glass-hover"
                style={{
                  padding: '16px',
                  border: '1px solid rgba(255,255,255,0.08)',
                  cursor: 'pointer',
                  textAlign: 'left',
                  background:
                    'radial-gradient(120% 120% at 12% 0%, rgba(168,85,247,0.16) 0%, rgba(168,85,247,0) 55%), rgba(255,255,255,0.035)',
                  fontFamily: 'inherit',
                }}
              >
                <div
                  style={{
                    width: 32,
                    height: 32,
                    borderRadius: 10,
                    background: 'rgba(255,255,255,0.08)',
                    border: '1px solid rgba(255,255,255,0.14)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    marginBottom: 10,
                  }}
                >
                  <Icon size={15} color="#ffffff" />
                </div>
                <div style={{ fontSize: 13, fontWeight: 600, color: 'white', marginBottom: 3 }}>
                  {label}
                </div>
                <div style={{ fontSize: 11, color: '#a1a1aa' }}>{desc}</div>
              </button>
            ))}
          </div>
        </div>

        {/* Bottom grid: Recent Tasks + AI Status + Connected Apps */}
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: '1fr 260px',
            gap: 16,
            animation: 'slide-up 0.6s cubic-bezier(0.16,1,0.3,1) 0.2s both',
          }}
        >
          {/* Recent Tasks */}
          <div
            className="glass"
            style={{
              padding: 24,
              background:
                'radial-gradient(150% 150% at 100% 0%, rgba(168,85,247,0.06) 0%, rgba(168,85,247,0) 55%), rgba(255,255,255,0.035)',
            }}
          >
            <div
              style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                marginBottom: 20,
              }}
            >
              <p
                style={{
                  fontSize: 11,
                  color: '#52525b',
                  fontWeight: 600,
                  letterSpacing: '0.08em',
                  textTransform: 'uppercase',
                  margin: 0,
                }}
              >
                Recent Tasks
              </p>
              <button
                className="btn-glass"
                style={{ padding: '4px 10px', fontSize: 11 }}
                onClick={() => router.push('/tasks')}
              >
                View all
              </button>
            </div>

            {recentTasks.length === 0 ? (
              <div
                style={{
                  padding: '32px 12px',
                  textAlign: 'center',
                  fontSize: 13,
                  color: '#52525b',
                }}
              >
                No recent tasks.
              </div>
            ) : (
              <div style={{ display: 'flex', flexDirection: 'column' }}>
                {recentTasks.map((task, i) => {
                  const Icon = task.icon
                  return (
                    <div
                      key={i}
                      style={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: 12,
                        padding: '11px 12px',
                        borderRadius: 12,
                        borderBottom:
                          i < recentTasks.length - 1 ? '1px solid rgba(255,255,255,0.05)' : 'none',
                        transition: 'background 0.2s ease',
                        cursor: 'pointer',
                      }}
                      onMouseEnter={e => {
                        (e.currentTarget as HTMLDivElement).style.background = 'rgba(255,255,255,0.04)'
                      }}
                      onMouseLeave={e => {
                        (e.currentTarget as HTMLDivElement).style.background = 'transparent'
                      }}
                    >
                      <div
                        style={{
                          width: 30,
                          height: 30,
                          borderRadius: 8,
                          background: `${task.color}15`,
                          border: `1px solid ${task.color}25`,
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          flexShrink: 0,
                        }}
                      >
                        <Icon size={13} color={task.color} />
                      </div>
                      <div style={{ flex: 1, minWidth: 0 }}>
                        <div
                          style={{
                            fontSize: 13,
                            fontWeight: 500,
                            color: 'white',
                            overflow: 'hidden',
                            textOverflow: 'ellipsis',
                            whiteSpace: 'nowrap',
                          }}
                        >
                          {task.title}
                        </div>
                        <div style={{ fontSize: 11, color: '#52525b', marginTop: 2 }}>
                          {task.time}
                        </div>
                      </div>
                      <div style={{ display: 'flex', alignItems: 'center', gap: 8, flexShrink: 0 }}>
                        <StatusDot status={task.status} />
                        <StatusLabel status={task.status} />
                      </div>
                    </div>
                  )
                })}
              </div>
            )}
          </div>

          {/* Right column */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
            {/* AI Status Card */}
            <div
              className="glass"
              style={{
                padding: 20,
                background:
                  'radial-gradient(150% 150% at 0% 0%, rgba(168,85,247,0.10) 0%, rgba(99,102,241,0.05) 35%, rgba(168,85,247,0) 60%), rgba(255,255,255,0.035)',
                boxShadow: '0 0 30px rgba(168,85,247,0.06)',
              }}
            >
              <div
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: 8,
                  marginBottom: 16,
                }}
              >
                <div
                  style={{
                    width: 8,
                    height: 8,
                    borderRadius: '50%',
                    background: '#52525b',
                  }}
                />
                <span style={{ fontSize: 13, fontWeight: 600, color: 'white' }}>Backend Offline</span>
              </div>

              <div
                style={{
                  padding: '12px 0',
                  fontSize: 12,
                  color: '#52525b',
                  lineHeight: 1.6,
                }}
              >
                Waiting for backend connection.
              </div>
            </div>

            {/* Connected Apps mini */}
            <div
              className="glass"
              style={{
                padding: 20,
                background:
                  'radial-gradient(150% 150% at 100% 100%, rgba(6,182,212,0.06) 0%, rgba(6,182,212,0) 55%), rgba(255,255,255,0.035)',
              }}
            >
              <p
                style={{
                  fontSize: 11,
                  color: '#52525b',
                  fontWeight: 600,
                  letterSpacing: '0.08em',
                  textTransform: 'uppercase',
                  margin: '0 0 14px',
                }}
              >
                Connected Apps
              </p>
              {connectedApps.length === 0 ? (
                <div
                  style={{
                    padding: '20px 8px',
                    textAlign: 'center',
                    fontSize: 12,
                    color: '#52525b',
                  }}
                >
                  No connected apps.
                </div>
              ) : (
                <div
                  style={{
                    display: 'grid',
                    gridTemplateColumns: 'repeat(4, 1fr)',
                    gap: 8,
                  }}
                >
                  {connectedApps.map(app => (
                    <div
                      key={app.name}
                      title={app.name}
                      style={{
                        width: '100%',
                        aspectRatio: '1',
                        borderRadius: 10,
                        background: `${app.color}18`,
                        border: `1px solid ${app.color}30`,
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        fontSize: 11,
                        fontWeight: 700,
                        color: app.color === '#FFFFFF' ? '#a1a1aa' : app.color,
                        cursor: 'pointer',
                        transition: 'transform 0.2s ease, box-shadow 0.2s ease',
                      }}
                      onMouseEnter={e => {
                        (e.currentTarget as HTMLDivElement).style.transform = 'scale(1.1)'
                        ;(e.currentTarget as HTMLDivElement).style.boxShadow = `0 0 12px ${app.color}40`
                      }}
                      onMouseLeave={e => {
                        (e.currentTarget as HTMLDivElement).style.transform = 'scale(1)'
                        ;(e.currentTarget as HTMLDivElement).style.boxShadow = 'none'
                      }}
                    >
                      {app.letter}
                    </div>
                  ))}
                </div>
              )}
              <button
                className="btn-glass"
                style={{ width: '100%', marginTop: 12, padding: '8px', fontSize: 12 }}
                onClick={() => router.push('/apps')}
              >
                Manage Apps
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
