'use client'

import { useState, useRef, useEffect } from 'react'
import { Sparkles, User, Loader2 } from 'lucide-react'
import { chatApi, ApiError } from '@/lib/api'

interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
}

const NODE_LABELS: Record<string, string> = {
  router: 'Classifying your request…',
  planner: 'Planning the steps…',
  supervisor: 'Assigning specialized agents…',
  execute_agents: 'Running agents (weather, flights, maps, etc.)…',
  response: 'Putting the answer together…',
}

function MessageContent({ content }: { content: string }) {
  const lines = content.split('\n')
  return (
    <div style={{ lineHeight: 1.75 }}>
      {lines.map((line, i) => {
        const boldProcessed = line.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        return (
          <p
            key={i}
            style={{ margin: '2px 0', fontSize: 14, color: 'white' }}
            dangerouslySetInnerHTML={{ __html: boldProcessed || '&nbsp;' }}
          />
        )
      })}
    </div>
  )
}

function StatusIndicator({ label }: { label: string }) {
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: 8, padding: '8px 0' }}>
      <Loader2 size={13} color="#a855f7" style={{ animation: 'spin 1s linear infinite' }} />
      <span style={{ fontSize: 13, color: '#a1a1aa' }}>{label}</span>
    </div>
  )
}

export default function Chat() {
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [input, setInput] = useState('')
  const [statusLabel, setStatusLabel] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [conversationId, setConversationId] = useState<string | undefined>(undefined)
  const endRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLTextAreaElement>(null)

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, statusLabel])

  const handleSend = async () => {
    const text = input.trim()
    if (!text || statusLabel) return

    setMessages((prev) => [...prev, { role: 'user', content: text }])
    setInput('')
    setError(null)
    setStatusLabel('Thinking…')

    try {
      await chatApi.stream(text, conversationId, (event, data) => {
        if (event === 'start') {
          setConversationId(data.conversation_id)
        } else if (event === 'progress') {
          setStatusLabel(NODE_LABELS[data.node] || 'Working…')
        } else if (event === 'error') {
          setError(data.detail || 'Something went wrong.')
          setStatusLabel(null)
        } else if (event === 'done') {
          setMessages((prev) => [...prev, { role: 'assistant', content: data.response }])
          setStatusLabel(null)
        }
      })
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Failed to reach AutoMateAI. Please try again.')
      setStatusLabel(null)
    }
  }

  return (
    <div
      style={{
        position: 'relative',
        zIndex: 1,
        height: '100vh',
        display: 'flex',
        flexDirection: 'column',
        paddingTop: 80,
      }}
    >
      {/* Messages */}
      <div style={{ flex: 1, overflowY: 'auto', padding: '24px 24px 8px' }}>
        <div style={{ maxWidth: 720, margin: '0 auto' }}>
          {messages.length === 0 && !statusLabel && (
            <div style={{ textAlign: 'center', padding: '80px 24px', color: '#52525b', fontSize: 14 }}>
              No messages yet. Start a conversation below.
            </div>
          )}
          {messages.map((msg, i) => (
            <div
              key={i}
              style={{
                display: 'flex',
                gap: 12,
                marginBottom: 24,
                justifyContent: msg.role === 'user' ? 'flex-end' : 'flex-start',
                animation: 'slide-up 0.4s cubic-bezier(0.16,1,0.3,1) both',
              }}
            >
              {msg.role === 'assistant' && (
                <div
                  style={{
                    width: 30,
                    height: 30,
                    borderRadius: '50%',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    flexShrink: 0,
                    marginTop: 2,
                    filter: 'drop-shadow(0 0 8px rgba(168,85,247,0.4))',
                  }}
                >
                  {/* eslint-disable-next-line @next/next/no-img-element */}
                  <img src="/logo.png" alt="AutoMateAI" style={{ width: 26, height: 26, objectFit: 'contain' }} />
                </div>
              )}

              <div
                style={{
                  maxWidth: msg.role === 'user' ? '70%' : '85%',
                  background:
                    msg.role === 'user'
                      ? 'linear-gradient(135deg, rgba(168,85,247,0.2), rgba(99,102,241,0.15))'
                      : 'rgba(255,255,255,0.04)',
                  border: msg.role === 'user' ? '1px solid rgba(168,85,247,0.25)' : '1px solid rgba(255,255,255,0.07)',
                  borderRadius: msg.role === 'user' ? '18px 18px 4px 18px' : '4px 18px 18px 18px',
                  padding: '12px 16px',
                  backdropFilter: 'blur(12px)',
                  whiteSpace: 'pre-wrap',
                }}
              >
                <MessageContent content={msg.content} />
              </div>

              {msg.role === 'user' && (
                <div
                  style={{
                    width: 30,
                    height: 30,
                    borderRadius: '50%',
                    background: 'rgba(255,255,255,0.08)',
                    border: '1px solid rgba(255,255,255,0.14)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    flexShrink: 0,
                    marginTop: 2,
                  }}
                >
                  <User size={13} color="white" />
                </div>
              )}
            </div>
          ))}

          {statusLabel && (
            <div style={{ display: 'flex', gap: 12, marginBottom: 24 }}>
              <div
                style={{
                  width: 30,
                  height: 30,
                  borderRadius: '50%',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  flexShrink: 0,
                  filter: 'drop-shadow(0 0 8px rgba(168,85,247,0.4))',
                }}
              >
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img src="/logo.png" alt="AutoMateAI" style={{ width: 26, height: 26, objectFit: 'contain' }} />
              </div>
              <div
                style={{
                  background: 'rgba(255,255,255,0.04)',
                  border: '1px solid rgba(255,255,255,0.07)',
                  borderRadius: '4px 18px 18px 18px',
                  padding: '10px 16px',
                }}
              >
                <StatusIndicator label={statusLabel} />
              </div>
            </div>
          )}

          {error && (
            <div style={{ color: '#f87171', fontSize: 13, marginBottom: 16, textAlign: 'center' }}>{error}</div>
          )}

          <div ref={endRef} />
        </div>
      </div>

      {/* Input */}
      <div style={{ padding: '12px 24px 20px', backdropFilter: 'blur(24px)', borderTop: '1px solid rgba(255,255,255,0.06)' }}>
        <div style={{ maxWidth: 720, margin: '0 auto' }}>
          <div
            className="glass"
            style={{
              display: 'flex',
              alignItems: 'flex-end',
              padding: '12px 16px',
              gap: 12,
              boxShadow: '0 0 0 1px rgba(168,85,247,0.12), 0 20px 60px rgba(0,0,0,0.5)',
            }}
          >
            <Sparkles size={16} color="#a855f7" style={{ flexShrink: 0, marginBottom: 2 }} />
            <textarea
              ref={inputRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault()
                  handleSend()
                }
              }}
              placeholder="Ask AutoMateAI anything... (e.g. Plan a 3-day trip from Mumbai to Goa)"
              rows={1}
              style={{
                flex: 1,
                fontSize: 15,
                fontFamily: 'inherit',
                border: 'none',
                background: 'transparent',
                color: 'white',
                outline: 'none',
                resize: 'none',
                lineHeight: 1.5,
                maxHeight: 120,
                overflow: 'auto',
              }}
            />
            <div style={{ display: 'flex', gap: 6, flexShrink: 0 }}>
              <button className="btn-primary" style={{ padding: '8px 14px', fontSize: 13 }} onClick={handleSend} disabled={!!statusLabel}>
                Send
              </button>
            </div>
          </div>
          <p style={{ textAlign: 'center', fontSize: 11, color: '#3f3f46', marginTop: 8 }}>
            AutoMateAI can make mistakes. Verify important information.
          </p>
        </div>
      </div>
    </div>
  )
}
