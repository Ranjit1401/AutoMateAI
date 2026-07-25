'use client'

import { useState } from 'react'
import { ChevronDown, ChevronRight, CheckCircle, Loader2, AlertCircle, Clock } from 'lucide-react'

interface LogEntry {
  id: string
  timestamp: string
  level: 'info' | 'success' | 'warning' | 'error' | 'running'
  message: string
  source: string
  details?: string[]
  expanded?: boolean
}

// Populated once the backend is connected.
const allLogs: LogEntry[] = []

const levelConfig = {
  success: { color: '#10b981', bg: '#10b98115', border: '#10b98125', icon: CheckCircle, label: 'Success' },
  running: { color: '#a855f7', bg: 'rgba(168,85,247,0.12)', border: 'rgba(168,85,247,0.25)', icon: Loader2, label: 'Running' },
  warning: { color: '#f59e0b', bg: '#f59e0b15', border: '#f59e0b25', icon: AlertCircle, label: 'Warning' },
  error: { color: '#ef4444', bg: '#ef444415', border: '#ef444425', icon: AlertCircle, label: 'Error' },
  info: { color: '#06b6d4', bg: '#06b6d415', border: '#06b6d425', icon: Clock, label: 'Info' },
}

export default function Logs() {
  const [expanded, setExpanded] = useState<Set<string>>(new Set())
  const [filter, setFilter] = useState<string>('all')

  const filtered = allLogs.filter(l => filter === 'all' || l.level === filter)

  const toggle = (id: string) => {
    setExpanded(prev => {
      const next = new Set(prev)
      next.has(id) ? next.delete(id) : next.add(id)
      return next
    })
  }

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
      <div style={{ maxWidth: 860, margin: '0 auto', padding: '24px' }}>
        <div
          style={{
            display: 'flex',
            alignItems: 'flex-end',
            justifyContent: 'space-between',
            marginBottom: 28,
            animation: 'slide-up 0.5s cubic-bezier(0.16,1,0.3,1) both',
          }}
        >
          <div>
            <h1
              style={{ fontSize: 28, fontWeight: 700, color: 'white', letterSpacing: '-0.5px', margin: '0 0 8px' }}
            >
              Execution Logs
            </h1>
            <p style={{ fontSize: 14, color: '#52525b', margin: 0 }}>
              Full audit trail of every action AutoMateAI takes
            </p>
          </div>
          <div
            style={{
              fontSize: 11,
              fontFamily: 'JetBrains Mono, monospace',
              color: '#52525b',
              background: 'rgba(255,255,255,0.04)',
              border: '1px solid rgba(255,255,255,0.08)',
              padding: '6px 12px',
              borderRadius: 8,
            }}
          >
            {allLogs.length} entries today
          </div>
        </div>

        {/* Filters */}
        <div
          style={{
            display: 'flex',
            gap: 6,
            marginBottom: 20,
            flexWrap: 'wrap',
            animation: 'slide-up 0.5s cubic-bezier(0.16,1,0.3,1) 0.05s both',
          }}
        >
          {['all', 'running', 'success', 'warning', 'error', 'info'].map(f => {
            const cfg = f !== 'all' ? levelConfig[f as keyof typeof levelConfig] : null
            return (
              <button
                key={f}
                onClick={() => setFilter(f)}
                style={{
                  padding: '6px 12px',
                  borderRadius: 8,
                  border: filter === f && cfg ? `1px solid ${cfg.border}` : '1px solid transparent',
                  fontSize: 12,
                  fontWeight: 500,
                  fontFamily: 'inherit',
                  cursor: 'pointer',
                  background: filter === f ? (cfg ? cfg.bg : 'rgba(255,255,255,0.08)') : 'rgba(255,255,255,0.04)',
                  color: filter === f ? (cfg ? cfg.color : 'white') : '#52525b',
                  transition: 'all 0.2s ease',
                }}
              >
                {f.charAt(0).toUpperCase() + f.slice(1)}
              </button>
            )
          })}
        </div>

        {/* Log entries */}
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
            No logs yet. Waiting for backend connection.
          </div>
        ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
          {filtered.map((log, i) => {
            const cfg = levelConfig[log.level]
            const Icon = cfg.icon
            const isOpen = expanded.has(log.id)

            return (
              <div
                key={log.id}
                className="glass"
                style={{
                  overflow: 'hidden',
                  animation: `slide-up 0.4s cubic-bezier(0.16,1,0.3,1) ${i * 0.04}s both`,
                  borderColor: isOpen ? cfg.border : 'rgba(255,255,255,0.08)',
                  transition: 'border-color 0.2s ease',
                }}
              >
                <button
                  onClick={() => toggle(log.id)}
                  style={{
                    width: '100%',
                    padding: '14px 16px',
                    display: 'flex',
                    alignItems: 'center',
                    gap: 12,
                    background: 'none',
                    border: 'none',
                    cursor: 'pointer',
                    fontFamily: 'inherit',
                    textAlign: 'left',
                  }}
                >
                  {isOpen ? (
                    <ChevronDown size={14} color="#52525b" style={{ flexShrink: 0 }} />
                  ) : (
                    <ChevronRight size={14} color="#52525b" style={{ flexShrink: 0 }} />
                  )}

                  <div
                    style={{
                      width: 28,
                      height: 28,
                      borderRadius: 8,
                      background: cfg.bg,
                      border: `1px solid ${cfg.border}`,
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      flexShrink: 0,
                    }}
                  >
                    <Icon
                      size={13}
                      color={cfg.color}
                      style={{
                        animation:
                          log.level === 'running'
                            ? 'spin 1s linear infinite'
                            : undefined,
                      }}
                    />
                  </div>

                  <div style={{ flex: 1, minWidth: 0 }}>
                    <div style={{ fontSize: 13, fontWeight: 500, color: 'white' }}>{log.message}</div>
                    <div
                      style={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: 10,
                        marginTop: 2,
                      }}
                    >
                      <span
                        style={{
                          fontSize: 10,
                          fontFamily: 'JetBrains Mono, monospace',
                          color: '#3f3f46',
                        }}
                      >
                        {log.timestamp}
                      </span>
                      <span
                        style={{
                          fontSize: 10,
                          color: '#52525b',
                          background: 'rgba(255,255,255,0.04)',
                          padding: '1px 6px',
                          borderRadius: 4,
                        }}
                      >
                        {log.source}
                      </span>
                    </div>
                  </div>

                  <span
                    style={{
                      fontSize: 11,
                      fontWeight: 500,
                      color: cfg.color,
                      background: cfg.bg,
                      padding: '3px 8px',
                      borderRadius: 6,
                      border: `1px solid ${cfg.border}`,
                      flexShrink: 0,
                    }}
                  >
                    {cfg.label}
                  </span>
                </button>

                {isOpen && log.details && (
                  <div
                    style={{
                      padding: '0 16px 14px 58px',
                      borderTop: '1px solid rgba(255,255,255,0.04)',
                    }}
                  >
                    <div
                      style={{
                        background: 'rgba(0,0,0,0.3)',
                        borderRadius: 10,
                        padding: '12px 14px',
                        marginTop: 12,
                        border: '1px solid rgba(255,255,255,0.05)',
                      }}
                    >
                      {log.details.map((line, j) => (
                        <div
                          key={j}
                          style={{
                            fontSize: 12,
                            fontFamily: 'JetBrains Mono, monospace',
                            color: line.startsWith('✗') ? '#ef4444' : line.startsWith('⟳') ? '#a855f7' : '#71717a',
                            lineHeight: 1.8,
                          }}
                        >
                          {line}
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )
          })}
        </div>
        )}
      </div>
    </div>
  )
}
