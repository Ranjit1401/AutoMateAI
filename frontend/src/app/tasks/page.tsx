'use client'

import { CheckCircle, Loader2, Clock, Zap, Activity } from 'lucide-react'

interface TaskStep {
  label: string
  status: string
  tool: string
  result: string | null
}

interface Task {
  id: string
  title: string
  status: string
  startedAt: string
  duration: string
  icon: React.ElementType
  color: string
  steps: TaskStep[]
}

// Populated once the backend is connected.
const tasks: Task[] = []

type StepStatus = 'done' | 'running' | 'waiting'

function StepRow({ step }: { step: { label: string; status: string; tool: string; result: string | null } }) {
  const st = step.status as StepStatus
  return (
    <div
      style={{
        display: 'flex',
        alignItems: 'flex-start',
        gap: 10,
        paddingLeft: 20,
        position: 'relative',
      }}
    >
      {/* Timeline dot */}
      <div
        style={{
          position: 'absolute',
          left: 0,
          top: 10,
          width: 8,
          height: 8,
          borderRadius: '50%',
          background:
            st === 'done' ? '#10b981' : st === 'running' ? '#a855f7' : '#3f3f46',
          boxShadow:
            st === 'running' ? '0 0 8px rgba(168,85,247,0.6)' : 'none',
          animation: st === 'running' ? 'status-pulse 1.5s ease-in-out infinite' : 'none',
          flexShrink: 0,
          zIndex: 1,
        }}
      />

      <div
        style={{
          flex: 1,
          padding: '8px 12px',
          borderRadius: 10,
          background: st === 'waiting' ? 'transparent' : 'rgba(255,255,255,0.03)',
          border: `1px solid ${st === 'waiting' ? 'transparent' : 'rgba(255,255,255,0.06)'}`,
          marginBottom: 6,
          opacity: st === 'waiting' ? 0.4 : 1,
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
            {st === 'running' ? (
              <Loader2 size={12} color="#a855f7" style={{ animation: 'spin 1s linear infinite' }} />
            ) : st === 'done' ? (
              <CheckCircle size={12} color="#10b981" />
            ) : (
              <Clock size={12} color="#52525b" />
            )}
            <span style={{ fontSize: 13, fontWeight: 500, color: 'white' }}>{step.label}</span>
          </div>
          <span
            style={{
              fontSize: 10,
              color: '#52525b',
              fontFamily: 'JetBrains Mono, monospace',
              background: 'rgba(255,255,255,0.04)',
              padding: '2px 6px',
              borderRadius: 4,
            }}
          >
            {step.tool}
          </span>
        </div>
        {step.result && (
          <p style={{ margin: '4px 0 0 20px', fontSize: 11, color: '#52525b' }}>{step.result}</p>
        )}
      </div>
    </div>
  )
}

export default function Tasks() {
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
      <div style={{ maxWidth: 800, margin: '0 auto', padding: '24px' }}>
        <div style={{ marginBottom: 32, animation: 'slide-up 0.5s cubic-bezier(0.16,1,0.3,1) both' }}>
          <h1
            style={{ fontSize: 28, fontWeight: 700, color: 'white', letterSpacing: '-0.5px', margin: '0 0 8px' }}
          >
            Task Execution
          </h1>
          <p style={{ fontSize: 14, color: '#52525b', margin: 0 }}>
            Real-time view of all running and completed autonomous tasks
          </p>
        </div>

        {/* Stats row */}
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(4, 1fr)',
            gap: 10,
            marginBottom: 28,
            animation: 'slide-up 0.5s cubic-bezier(0.16,1,0.3,1) 0.05s both',
          }}
        >
          {[
            {
              label: 'Running',
              value: String(tasks.filter(t => t.status === 'running').length),
              color: '#a855f7',
              icon: Activity,
            },
            {
              label: 'Completed Today',
              value: String(tasks.filter(t => t.status === 'completed').length),
              color: '#10b981',
              icon: CheckCircle,
            },
            {
              label: 'Waiting',
              value: String(tasks.filter(t => t.status === 'waiting').length),
              color: '#52525b',
              icon: Clock,
            },
            { label: 'Avg Duration', value: '—', color: '#06b6d4', icon: Zap },
          ].map(({ label, value, color, icon: Icon }) => (
            <div
              key={label}
              className="glass"
              style={{ padding: '14px 16px' }}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginBottom: 8 }}>
                <Icon size={12} color={color} />
                <span style={{ fontSize: 11, color: '#52525b', fontWeight: 500 }}>{label}</span>
              </div>
              <div
                style={{
                  fontSize: 24,
                  fontWeight: 700,
                  color: 'white',
                  fontFamily: 'JetBrains Mono, monospace',
                }}
              >
                {value}
              </div>
            </div>
          ))}
        </div>

        {/* Task cards */}
        {tasks.length === 0 ? (
          <div
            className="glass"
            style={{
              padding: '40px 24px',
              textAlign: 'center',
              fontSize: 13,
              color: '#52525b',
            }}
          >
            No tasks yet. Waiting for backend connection.
          </div>
        ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
          {tasks.map((task, idx) => {
            const Icon = task.icon
            const progress = task.steps.filter(s => s.status === 'done').length / task.steps.length
            return (
              <div
                key={task.id}
                className="glass"
                style={{
                  padding: 24,
                  animation: `slide-up 0.5s cubic-bezier(0.16,1,0.3,1) ${0.1 + idx * 0.05}s both`,
                }}
              >
                {/* Header */}
                <div
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: 12,
                    marginBottom: 20,
                  }}
                >
                  <div
                    style={{
                      width: 36,
                      height: 36,
                      borderRadius: 10,
                      background: `${task.color}18`,
                      border: `1px solid ${task.color}30`,
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                    }}
                  >
                    <Icon size={16} color={task.color} />
                  </div>
                  <div style={{ flex: 1 }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                      <span style={{ fontSize: 15, fontWeight: 600, color: 'white' }}>{task.title}</span>
                      <span
                        style={{
                          fontSize: 11,
                          fontFamily: 'JetBrains Mono, monospace',
                          color: '#52525b',
                        }}
                      >
                        {task.id}
                      </span>
                    </div>
                    <div
                      style={{
                        fontSize: 12,
                        color: '#52525b',
                        marginTop: 2,
                        display: 'flex',
                        gap: 12,
                      }}
                    >
                      <span>Started {task.startedAt}</span>
                      {task.duration !== '—' && <span>Duration: {task.duration}</span>}
                    </div>
                  </div>
                  <span
                    style={{
                      fontSize: 11,
                      fontWeight: 500,
                      padding: '4px 10px',
                      borderRadius: 8,
                      background:
                        task.status === 'completed'
                          ? '#10b98118'
                          : task.status === 'running'
                          ? 'rgba(168,85,247,0.15)'
                          : '#3f3f4618',
                      color:
                        task.status === 'completed'
                          ? '#10b981'
                          : task.status === 'running'
                          ? '#c4b5fd'
                          : '#71717a',
                      border: `1px solid ${
                        task.status === 'completed'
                          ? '#10b98130'
                          : task.status === 'running'
                          ? 'rgba(168,85,247,0.3)'
                          : '#3f3f4630'
                      }`,
                    }}
                  >
                    {task.status === 'running' && (
                      <Loader2 size={10} style={{ display: 'inline', marginRight: 4, animation: 'spin 1s linear infinite' }} />
                    )}
                    {task.status.charAt(0).toUpperCase() + task.status.slice(1)}
                  </span>
                </div>

                {/* Progress bar */}
                <div
                  style={{
                    height: 3,
                    background: 'rgba(255,255,255,0.06)',
                    borderRadius: 2,
                    marginBottom: 16,
                    overflow: 'hidden',
                  }}
                >
                  <div
                    style={{
                      height: '100%',
                      width: `${progress * 100}%`,
                      background: `linear-gradient(90deg, ${task.color}, ${task.color}aa)`,
                      borderRadius: 2,
                      transition: 'width 1s ease',
                    }}
                  />
                </div>

                {/* Steps */}
                <div
                  style={{
                    position: 'relative',
                    paddingLeft: 4,
                  }}
                >
                  {/* Vertical line */}
                  <div
                    style={{
                      position: 'absolute',
                      left: 3,
                      top: 14,
                      bottom: 14,
                      width: 1,
                      background: 'rgba(255,255,255,0.06)',
                    }}
                  />
                  {task.steps.map((step, j) => (
                    <StepRow key={j} step={step} />
                  ))}
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
