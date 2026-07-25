'use client'

import { Brain, MessageSquare, User, Trash2, Search } from 'lucide-react'
import { useState } from 'react'

interface Preference {
  key: string
  value: string
  icon: string
}

interface MemoryEntry {
  id: number
  type: string
  content: string
  source: string
  savedAt: string
  icon: string
}

interface Conversation {
  title: string
  messages: number
  date: string
  preview: string
}

// Populated once the backend is connected.
const preferences: Preference[] = []

// Populated once the backend is connected.
const memories: MemoryEntry[] = []

// Populated once the backend is connected.
const conversations: Conversation[] = []

export default function Memory() {
  const [search, setSearch] = useState('')

  const filteredMemories = memories.filter(m =>
    m.content.toLowerCase().includes(search.toLowerCase())
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
      <div style={{ maxWidth: 900, margin: '0 auto', padding: '24px' }}>
        <div
          style={{
            marginBottom: 32,
            animation: 'slide-up 0.5s cubic-bezier(0.16,1,0.3,1) both',
          }}
        >
          <h1
            style={{ fontSize: 28, fontWeight: 700, color: 'white', letterSpacing: '-0.5px', margin: '0 0 8px' }}
          >
            Memory
          </h1>
          <p style={{ fontSize: 14, color: '#52525b', margin: 0 }}>
            Everything AutoMateAI knows about you and your preferences
          </p>
        </div>

        {/* Search */}
        <div
          className="glass"
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: 10,
            padding: '10px 16px',
            marginBottom: 24,
            animation: 'slide-up 0.5s cubic-bezier(0.16,1,0.3,1) 0.05s both',
          }}
        >
          <Search size={15} color="#52525b" />
          <input
            value={search}
            onChange={e => setSearch(e.target.value)}
            placeholder="Search memories..."
            style={{
              flex: 1,
              fontSize: 14,
              fontFamily: 'inherit',
              border: 'none',
              background: 'transparent',
              color: 'white',
              outline: 'none',
            }}
          />
        </div>

        <div
          style={{
            display: 'grid',
            gridTemplateColumns: '1fr 1fr',
            gap: 16,
            animation: 'slide-up 0.5s cubic-bezier(0.16,1,0.3,1) 0.1s both',
          }}
        >
          {/* User Preferences */}
          <div>
            <div className="glass" style={{ padding: 20, marginBottom: 16 }}>
              <div
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: 8,
                  marginBottom: 16,
                }}
              >
                <User size={14} color="#a855f7" />
                <span
                  style={{
                    fontSize: 11,
                    color: '#52525b',
                    fontWeight: 600,
                    letterSpacing: '0.08em',
                    textTransform: 'uppercase',
                  }}
                >
                  User Preferences
                </span>
              </div>
              {preferences.length === 0 ? (
                <div style={{ padding: '16px 10px', fontSize: 12, color: '#52525b' }}>
                  No preferences learned yet.
                </div>
              ) : (
                <div style={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                  {preferences.map(pref => (
                    <div
                      key={pref.key}
                      style={{
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'space-between',
                        padding: '8px 10px',
                        borderRadius: 8,
                        transition: 'background 0.2s ease',
                        cursor: 'default',
                      }}
                      onMouseEnter={e => {
                        (e.currentTarget as HTMLDivElement).style.background = 'rgba(255,255,255,0.04)'
                      }}
                      onMouseLeave={e => {
                        (e.currentTarget as HTMLDivElement).style.background = 'transparent'
                      }}
                    >
                      <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                        <span style={{ fontSize: 13 }}>{pref.icon}</span>
                        <span style={{ fontSize: 12, color: '#71717a' }}>{pref.key}</span>
                      </div>
                      <span style={{ fontSize: 12, fontWeight: 500, color: 'white' }}>{pref.value}</span>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Conversation History */}
            <div className="glass" style={{ padding: 20 }}>
              <div
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: 8,
                  marginBottom: 16,
                }}
              >
                <MessageSquare size={14} color="#06b6d4" />
                <span
                  style={{
                    fontSize: 11,
                    color: '#52525b',
                    fontWeight: 600,
                    letterSpacing: '0.08em',
                    textTransform: 'uppercase',
                  }}
                >
                  Conversation History
                </span>
              </div>
              {conversations.length === 0 ? (
                <div style={{ padding: '16px 10px', fontSize: 12, color: '#52525b' }}>
                  No conversation history yet.
                </div>
              ) : (
                <div style={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                  {conversations.map((conv, i) => (
                    <div
                      key={i}
                      style={{
                        padding: '10px',
                        borderRadius: 10,
                        cursor: 'pointer',
                        transition: 'background 0.2s ease',
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
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'space-between',
                          marginBottom: 3,
                        }}
                      >
                        <span style={{ fontSize: 13, fontWeight: 500, color: 'white' }}>{conv.title}</span>
                        <span style={{ fontSize: 10, color: '#3f3f46' }}>{conv.messages} msgs</span>
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
                        {conv.preview}
                      </p>
                      <span style={{ fontSize: 10, color: '#3f3f46', marginTop: 4, display: 'block' }}>
                        {conv.date}
                      </span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* Saved Memories */}
          <div className="glass" style={{ padding: 20 }}>
            <div
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: 8,
                marginBottom: 16,
              }}
            >
              <Brain size={14} color="#a855f7" />
              <span
                style={{
                  fontSize: 11,
                  color: '#52525b',
                  fontWeight: 600,
                  letterSpacing: '0.08em',
                  textTransform: 'uppercase',
                }}
              >
                AI Knowledge
              </span>
              <span
                style={{
                  marginLeft: 'auto',
                  fontSize: 11,
                  color: '#52525b',
                  background: 'rgba(255,255,255,0.06)',
                  padding: '2px 8px',
                  borderRadius: 6,
                }}
              >
                {filteredMemories.length} entries
              </span>
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
              {filteredMemories.length === 0 ? (
                <div style={{ padding: '16px 10px', fontSize: 12, color: '#52525b' }}>
                  No memories yet.
                </div>
              ) : (
                filteredMemories.map(mem => (
                <div
                  key={mem.id}
                  style={{
                    padding: '12px 14px',
                    borderRadius: 12,
                    background: 'rgba(255,255,255,0.03)',
                    border: '1px solid rgba(255,255,255,0.06)',
                    transition: 'border-color 0.2s ease',
                    cursor: 'default',
                    position: 'relative',
                  }}
                  onMouseEnter={e => {
                    (e.currentTarget as HTMLDivElement).style.borderColor = 'rgba(168,85,247,0.2)'
                  }}
                  onMouseLeave={e => {
                    (e.currentTarget as HTMLDivElement).style.borderColor = 'rgba(255,255,255,0.06)'
                  }}
                >
                  <div
                    style={{
                      display: 'flex',
                      alignItems: 'flex-start',
                      gap: 10,
                    }}
                  >
                    <span style={{ fontSize: 16, lineHeight: 1, flexShrink: 0 }}>{mem.icon}</span>
                    <div style={{ flex: 1 }}>
                      <p
                        style={{
                          margin: '0 0 6px',
                          fontSize: 13,
                          color: '#d4d4d8',
                          lineHeight: 1.5,
                        }}
                      >
                        {mem.content}
                      </p>
                      <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                        <span
                          style={{
                            fontSize: 10,
                            color: '#52525b',
                            background: 'rgba(255,255,255,0.04)',
                            padding: '2px 6px',
                            borderRadius: 4,
                          }}
                        >
                          {mem.source}
                        </span>
                        <span style={{ fontSize: 10, color: '#3f3f46' }}>{mem.savedAt}</span>
                      </div>
                    </div>
                    <button
                      style={{
                        background: 'none',
                        border: 'none',
                        cursor: 'pointer',
                        color: '#3f3f46',
                        padding: 2,
                        flexShrink: 0,
                        transition: 'color 0.2s ease',
                      }}
                      onMouseEnter={e => {
                        (e.currentTarget as HTMLButtonElement).style.color = '#ef4444'
                      }}
                      onMouseLeave={e => {
                        (e.currentTarget as HTMLButtonElement).style.color = '#3f3f46'
                      }}
                    >
                      <Trash2 size={12} />
                    </button>
                  </div>
                </div>
                ))
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
