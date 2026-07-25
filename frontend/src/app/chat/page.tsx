'use client'

import { useState, useRef, useEffect } from 'react'
import { Sparkles, Mic, Paperclip, MapPin, CheckCircle, Loader2, Globe, Calendar } from 'lucide-react'

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

const INITIAL_MESSAGES: Message[] = [
  {
    role: 'user',
    content: 'Plan a 7-day trip to Tokyo for two people in September. Include flights from New York, hotels near Shinjuku, and a daily itinerary.',
  },
  {
    role: 'assistant',
    content: "I'll plan a comprehensive 7-day Tokyo trip for you. Let me search for flights, hotels, and build a detailed itinerary right now.",
    tools: [
      { name: 'Searching flights JFK → TYO', status: 'done', result: 'Found 12 options · Best: $890/person on ANA', icon: Globe, color: '#a855f7' },
      { name: 'Finding hotels near Shinjuku', status: 'done', result: '8 hotels matched · Rec: Hyatt Regency ¥28,000/night', icon: MapPin, color: '#06b6d4' },
      { name: 'Building daily itinerary', status: 'done', result: '7-day plan created with 42 activities', icon: Calendar, color: '#10b981' },
    ],
  },
  {
    role: 'assistant',
    content: `Here's your complete **Tokyo trip plan** for September:

**✈️ Flights**
- Outbound: ANA NH009 · JFK → NRT · Sep 1, 11:00am · $890/person
- Return: ANA NH010 · NRT → JFK · Sep 8, 1:10pm · $910/person
- Total flights: $3,600

**🏨 Hotel**
- Hyatt Regency Tokyo, Shinjuku · 7 nights · $1,540 total
- Superior Room with city views · Breakfast included

**📅 Highlights**
- Day 1: Shinjuku exploration, Omoide Yokocho
- Day 2: Tsukiji Market, Odaiba, teamLab Borderless
- Day 3: Harajuku, Meiji Shrine, Shibuya Crossing
- Day 4: Day trip to Nikko
- Day 5: Asakusa, Ueno, Akihabara
- Day 6: Ginza, Tokyo Tower, Roppongi
- Day 7: Farewell brunch, Narita Express

**💰 Total estimated cost: ~$7,200 for two**

Would you like me to proceed with booking the flights and hotel?`,
  },
]

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
          content: "I'm on it! Let me process your request and get back to you with a comprehensive response. I'll use my connected tools to find the best information available.",
        },
      ])
    }, 2200)
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
                    background: 'linear-gradient(135deg, #a855f7, #6366f1)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    flexShrink: 0,
                    marginTop: 2,
                    boxShadow: '0 0 12px rgba(168,85,247,0.4)',
                  }}
                >
                  <Sparkles size={13} color="white" />
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
                    background: 'linear-gradient(135deg, #a855f7, #ec4899)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    flexShrink: 0,
                    marginTop: 2,
                    fontSize: 12,
                    fontWeight: 700,
                    color: 'white',
                  }}
                >
                  N
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
                  background: 'linear-gradient(135deg, #a855f7, #6366f1)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  flexShrink: 0,
                  boxShadow: '0 0 12px rgba(168,85,247,0.4)',
                }}
              >
                <Sparkles size={13} color="white" />
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
