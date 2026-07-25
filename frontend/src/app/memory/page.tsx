'use client'

import { Brain, MessageSquare, User, Trash2, Search } from 'lucide-react'
import { useState } from 'react'

const preferences = [
  { key: 'Preferred airline', value: 'ANA / JAL', icon: '✈️' },
  { key: 'Hotel tier', value: 'Luxury / 5-star', icon: '🏨' },
  { key: 'Dietary preference', value: 'Vegetarian friendly', icon: '🥗' },
  { key: 'Timezone', value: 'America/New_York', icon: '🕐' },
  { key: 'Currency', value: 'USD', icon: '💵' },
  { key: 'Calendar', value: 'Google Calendar', icon: '📅' },
  { key: 'Email provider', value: 'Gmail', icon: '📧' },
  { key: 'Language', value: 'English', icon: '🌐' },
]

const memories = [
  {
    id: 1,
    type: 'preference',
    content: 'Nikita prefers window seats on flights and usually books business class for international trips over 8 hours.',
    source: 'Flight booking task',
    savedAt: '2 days ago',
    icon: '✈️',
  },
  {
    id: 2,
    type: 'fact',
    content: 'Team standup is every Monday, Wednesday, Friday at 10:00 AM EST with 6 participants.',
    source: 'Calendar access',
    savedAt: '5 days ago',
    icon: '📅',
  },
  {
    id: 3,
    type: 'preference',
    content: "Nikita's writing style is concise, professional, and avoids jargon. Emails should be under 200 words.",
    source: 'Email drafting session',
    savedAt: '1 week ago',
    icon: '✍️',
  },
  {
    id: 4,
    type: 'fact',
    content: 'Company headquarters: San Francisco, CA. Remote-first policy. Team of 24 across 8 time zones.',
    source: 'Notion workspace',
    savedAt: '2 weeks ago',
    icon: '🏢',
  },
  {
    id: 5,
    type: 'task',
    content: 'Tokyo trip planned for September 1-8. Two travelers. Budget $7,200. Hyatt Regency booked.',
    source: 'Trip planning task',
    savedAt: '3 days ago',
    icon: '🗺️',
  },
  {
    id: 6,
    type: 'preference',
    content: 'Preferred meeting length: 30 minutes max. No back-to-back meetings. Buffer 15 min between calls.',
    source: 'Calendar analysis',
    savedAt: '1 week ago',
    icon: '⏱️',
  },
]

const conversations = [
  { title: 'Tokyo trip planning', messages: 12, date: 'Today, 2:14 PM', preview: 'Plan a 7-day trip to Tokyo for two people...' },
  { title: 'Q3 investor email draft', messages: 8, date: 'Today, 9:02 AM', preview: 'Draft the Q3 update email for investors...' },
  { title: 'Competitor pricing analysis', messages: 5, date: 'Yesterday, 4:30 PM', preview: 'Research our top 5 competitors pricing...' },
  { title: 'Team standup automation', messages: 15, date: 'Jul 22, 11:00 AM', preview: 'Set up recurring standup meeting reminders...' },
]

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
              {filteredMemories.map(mem => (
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
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
