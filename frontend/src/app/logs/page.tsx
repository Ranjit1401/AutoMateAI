'use client'

import { useEffect, useState } from 'react'
import { Info, AlertTriangle, XCircle, ScrollText } from 'lucide-react'
import { logsApi, type LogEntry } from '@/lib/api'

const LEVEL_CONFIG: Record<LogEntry['level'], { color: string; icon: React.ElementType }> = {
  info: { color: '#60a5fa', icon: Info },
  warning: { color: '#fbbf24', icon: AlertTriangle },
  error: { color: '#f87171', icon: XCircle },
}

function formatTime(iso: string) {
  return new Date(iso).toLocaleString(undefined, { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit', second: '2-digit' })
}

export default function Logs() {
  const [logs, setLogs] = useState<LogEntry[]>([])
  const [filter, setFilter] = useState<'all' | LogEntry['level']>('all')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    logsApi
      .list()
      .then(setLogs)
      .finally(() => setLoading(false))
  }, [])

  const filtered = filter === 'all' ? logs : logs.filter((l) => l.level === filter)

  return (
    <div style={{ position: 'relative', zIndex: 1, minHeight: '100vh', paddingTop: 100, paddingBottom: 80 }}>
      <div style={{ maxWidth: 800, margin: '0 auto', padding: '24px' }}>
        <div style={{ marginBottom: 24, display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: 12 }}>
          <div>
            <h1 style={{ fontSize: 28, fontWeight: 700, color: 'white', letterSpacing: '-0.5px', margin: '0 0 8px' }}>
              Logs
            </h1>
            <p style={{ fontSize: 14, color: '#52525b', margin: 0 }}>System and agent activity, most recent first</p>
          </div>

          <div style={{ display: 'flex', gap: 6 }}>
            {(['all', 'info', 'warning', 'error'] as const).map((level) => (
              <button
                key={level}
                onClick={() => setFilter(level)}
                className={filter === level ? '' : 'glass-hover'}
                style={{
                  padding: '6px 12px',
                  borderRadius: 8,
                  fontSize: 12,
                  fontWeight: 500,
                  cursor: 'pointer',
                  textTransform: 'capitalize',
                  border: '1px solid rgba(255,255,255,0.08)',
                  background: filter === level ? 'rgba(168,85,247,0.18)' : 'rgba(255,255,255,0.03)',
                  color: filter === level ? 'white' : '#a1a1aa',
                }}
              >
                {level}
              </button>
            ))}
          </div>
        </div>

        {loading ? (
          <div className="glass" style={{ padding: 40, textAlign: 'center', fontSize: 13, color: '#52525b' }}>
            Loading logs…
          </div>
        ) : filtered.length === 0 ? (
          <div className="glass" style={{ padding: 40, textAlign: 'center', fontSize: 13, color: '#52525b' }}>
            <ScrollText size={20} color="#3f3f46" style={{ marginBottom: 8 }} />
            <div>No logs yet.</div>
          </div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
            {filtered.map((log) => {
              const { color, icon: Icon } = LEVEL_CONFIG[log.level]
              return (
                <div key={log.id} className="glass" style={{ padding: '10px 14px', display: 'flex', gap: 10, alignItems: 'flex-start' }}>
                  <Icon size={13} color={color} style={{ marginTop: 2, flexShrink: 0 }} />
                  <div style={{ flex: 1, minWidth: 0 }}>
                    <div style={{ fontSize: 13, color: 'white' }}>{log.message}</div>
                    <div style={{ fontSize: 11, color: '#52525b', marginTop: 3 }}>
                      {log.source} · {formatTime(log.created_at)}
                    </div>
                  </div>
                </div>
              )
            })}
          </div>
        )}
      </div>
    </div>
  )
}
