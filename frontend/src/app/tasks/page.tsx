'use client'

import { useEffect, useState } from 'react'
import { CheckCircle, Loader2, Clock, XCircle, Activity } from 'lucide-react'
import { tasksApi, type Task } from '@/lib/api'

const STATUS_COLOR: Record<Task['status'], string> = {
  pending: '#52525b',
  running: '#a855f7',
  done: '#10b981',
  failed: '#f87171',
}

const STATUS_ICON: Record<Task['status'], React.ElementType> = {
  pending: Clock,
  running: Loader2,
  done: CheckCircle,
  failed: XCircle,
}

function formatTime(iso: string) {
  return new Date(iso).toLocaleString(undefined, { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })
}

export default function Tasks() {
  const [tasks, setTasks] = useState<Task[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    tasksApi
      .list()
      .then(setTasks)
      .catch(() => setError('Could not load tasks.'))
      .finally(() => setLoading(false))
  }, [])

  const counts = {
    running: tasks.filter((t) => t.status === 'running' || t.status === 'pending').length,
    done: tasks.filter((t) => t.status === 'done').length,
    failed: tasks.filter((t) => t.status === 'failed').length,
  }

  return (
    <div style={{ position: 'relative', zIndex: 1, minHeight: '100vh', paddingTop: 100, paddingBottom: 80 }}>
      <div style={{ maxWidth: 800, margin: '0 auto', padding: '24px' }}>
        <div style={{ marginBottom: 32, animation: 'slide-up 0.5s cubic-bezier(0.16,1,0.3,1) both' }}>
          <h1 style={{ fontSize: 28, fontWeight: 700, color: 'white', letterSpacing: '-0.5px', margin: '0 0 8px' }}>
            Task Execution
          </h1>
          <p style={{ fontSize: 14, color: '#52525b', margin: 0 }}>
            Every agent action run by the chat pipeline, in order
          </p>
        </div>

        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(3, 1fr)',
            gap: 10,
            marginBottom: 28,
            animation: 'slide-up 0.5s cubic-bezier(0.16,1,0.3,1) 0.05s both',
          }}
        >
          {[
            { label: 'In Progress', value: counts.running, color: '#a855f7', icon: Activity },
            { label: 'Completed', value: counts.done, color: '#10b981', icon: CheckCircle },
            { label: 'Failed', value: counts.failed, color: '#f87171', icon: XCircle },
          ].map(({ label, value, color, icon: Icon }) => (
            <div key={label} className="glass" style={{ padding: '14px 16px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginBottom: 8 }}>
                <Icon size={12} color={color} />
                <span style={{ fontSize: 11, color: '#52525b', fontWeight: 500 }}>{label}</span>
              </div>
              <div style={{ fontSize: 24, fontWeight: 700, color: 'white', fontFamily: 'JetBrains Mono, monospace' }}>
                {value}
              </div>
            </div>
          ))}
        </div>

        {loading ? (
          <div className="glass" style={{ padding: '40px 24px', textAlign: 'center', fontSize: 13, color: '#52525b' }}>
            Loading tasks…
          </div>
        ) : error ? (
          <div className="glass" style={{ padding: '40px 24px', textAlign: 'center', fontSize: 13, color: '#f87171' }}>
            {error}
          </div>
        ) : tasks.length === 0 ? (
          <div className="glass" style={{ padding: '40px 24px', textAlign: 'center', fontSize: 13, color: '#52525b' }}>
            No tasks yet. Send a message in Chat to run the agent pipeline.
          </div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
            {tasks.map((task) => {
              const Icon = STATUS_ICON[task.status]
              const color = STATUS_COLOR[task.status]
              return (
                <div key={task.id} className="glass" style={{ padding: '16px 18px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 12 }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 10, minWidth: 0 }}>
                      <Icon
                        size={14}
                        color={color}
                        style={{ animation: task.status === 'running' ? 'spin 1s linear infinite' : 'none', flexShrink: 0 }}
                      />
                      <div style={{ minWidth: 0 }}>
                        <div style={{ fontSize: 13.5, fontWeight: 500, color: 'white', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                          {task.title}
                        </div>
                        <div style={{ fontSize: 11, color: '#52525b', marginTop: 2 }}>{formatTime(task.created_at)}</div>
                      </div>
                    </div>
                    <span
                      style={{
                        fontSize: 10,
                        fontFamily: 'JetBrains Mono, monospace',
                        color,
                        background: `${color}18`,
                        border: `1px solid ${color}30`,
                        padding: '3px 8px',
                        borderRadius: 6,
                        flexShrink: 0,
                        textTransform: 'uppercase',
                      }}
                    >
                      {task.agent}
                    </span>
                  </div>
                  {task.error && <p style={{ margin: '10px 0 0', fontSize: 12, color: '#f87171' }}>{task.error}</p>}
                </div>
              )
            })}
          </div>
        )}
      </div>
    </div>
  )
}
