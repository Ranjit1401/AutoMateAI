'use client'

import { useState, useRef, useEffect } from 'react'
import { Sparkles, Mic, Paperclip, CheckCircle, Loader2, User } from 'lucide-react'

interface Message {
  role: 'user' | 'assistant'
  content: string
  tools?: ToolCard[]
  streaming?: boolean
}

interface ToolCard {
  name: string
  status: 'running' | 'done'
  result?: string
  icon: React.ElementType
  color: string
}

const INITIAL_MESSAGES: Message[] = []

function ToolExecCard({ tool }: { tool: ToolCard }) {
  const Icon = tool.icon
  return (
    <div
      style={{
        display: 'flex',
        alignItems: 'center',
        gap: 10,
        padding: '8px 12px',
        borderRadius: 10,
        background: 'rgba(255,255,255,0.03)',
        border: '1px solid rgba(255,255,255,0.06)',
        marginBottom: 6,
      }}
    >
      <div
        style={{
          width: 24,
          height: 24,
          borderRadius: 6,
          background: `${tool.color}18`,
          border: `1px solid ${tool.color}30`,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          flexShrink: 0,
        }}
      >
        {tool.status === 'running' ? (
          <Loader2 size={11} color={tool.color} style={{ animation: 'spin 1s linear infinite' }} />
        ) : (
          <Icon size={11} color={tool.color} />
        )}
      </div>
      <div style={{ flex: 1, minWidth: 0 }}>
        <div style={{ fontSize: 12, color: '#a1a1aa', fontWeight: 500 }}>{tool.name}</div>
        {tool.result && (
          <div style={{ fontSize: 11, color: '#52525b', marginTop: 2 }}>{tool.result}</div>
        )}
      </div>
      {tool.status === 'done' && <CheckCircle size={13} color="#10b981" />}
    </div>
  )
}

function TypingIndicator() {
  return (
    <div style={{ display: 'flex', gap: 4, alignItems: 'center', padding: '8px 0' }}>
      {[0, 1, 2].map(i => (
        <div
          key={i}
          style={{
            width: 6,
            height: 6,
            borderRadius: '50%',
            background: '#a855f7',
            animation: `typing-dot 1.4s ease-in-out ${i * 0.2}s infinite`,
          }}
        />
      ))}
    </div>
  )
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
            style={{ margin: '2px 0', fontSize: 14, color: i === 0 && line === '' ? undefined : 'white' }}
            dangerouslySetInnerHTML={{ __html: boldProcessed || '&nbsp;' }}
          />
        )
      })}
    </div>
  )
}

export default function Chat() {
  const [messages, setMessages] = useState<Message[]>(INITIAL_MESSAGES)
  const [input, setInput] = useState('')
  const [isTyping, setIsTyping] = useState(false)
  const endRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLTextAreaElement>(null)

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, isTyping])

  const handleSend = () => {
    if (!input.trim()) return
    const userMsg: Message = { role: 'user', content: input }
    setMessages(prev => [...prev, userMsg])
    setInput('')
    setIsTyping(true)
    setTimeout(() => {
      setIsTyping(false)
      setMessages(prev => [
        ...prev,
        {
          role: 'assistant',
          content: 'Waiting for backend connection.',
        },
      ])
    }, 800)
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
      <div
        style={{
          flex: 1,
          overflowY: 'auto',
          padding: '24px 24px 8px',
        }}
      >
        <div style={{ maxWidth: 720, margin: '0 auto' }}>
          {messages.length === 0 && !isTyping && (
            <div
              style={{
                textAlign: 'center',
                padding: '80px 24px',
                color: '#52525b',
                fontSize: 14,
              }}
            >
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
                  border:
                    msg.role === 'user'
                      ? '1px solid rgba(168,85,247,0.25)'
                      : '1px solid rgba(255,255,255,0.07)',
                  borderRadius: msg.role === 'user' ? '18px 18px 4px 18px' : '4px 18px 18px 18px',
                  padding: '12px 16px',
                  backdropFilter: 'blur(12px)',
                }}
              >
                {msg.tools && msg.tools.length > 0 && (
                  <div style={{ marginBottom: 12 }}>
                    {msg.tools.map((tool, j) => (
                      <ToolExecCard key={j} tool={tool} />
                    ))}
                  </div>
                )}
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

          {isTyping && (
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
                  padding: '12px 16px',
                }}
              >
                <TypingIndicator />
              </div>
            </div>
          )}

          <div ref={endRef} />
        </div>
      </div>

      {/* Input */}
      <div
        style={{
          padding: '12px 24px 20px',
          backdropFilter: 'blur(24px)',
          borderTop: '1px solid rgba(255,255,255,0.06)',
        }}
      >
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
              onChange={e => setInput(e.target.value)}
              onKeyDown={e => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault()
                  handleSend()
                }
              }}
              placeholder="Ask AutoMateAI anything..."
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
              <button className="btn-glass" style={{ padding: '6px', borderRadius: 8 }}>
                <Paperclip size={14} color="#52525b" />
              </button>
              <button className="btn-glass" style={{ padding: '6px', borderRadius: 8 }}>
                <Mic size={14} color="#52525b" />
              </button>
              <button className="btn-primary" style={{ padding: '8px 14px', fontSize: 13 }} onClick={handleSend}>
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
