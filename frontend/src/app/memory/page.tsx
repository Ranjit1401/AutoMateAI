'use client'

import { useEffect, useState, type FormEvent } from 'react'
import { Brain, MessageSquare, Plus, Trash2 } from 'lucide-react'
import { memoryApi, chatApi, type MemoryEntry, type Conversation } from '@/lib/api'

function formatDate(iso: string) {
  return new Date(iso).toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' })
}

export default function Memory() {
  const [memories, setMemories] = useState<MemoryEntry[]>([])
  const [conversations, setConversations] = useState<Conversation[]>([])
  const [loading, setLoading] = useState(true)
  const [newFact, setNewFact] = useState('')
  const [adding, setAdding] = useState(false)

  useEffect(() => {
    Promise.all([memoryApi.list(), chatApi.listConversations()])
      .then(([m, c]) => {
        setMemories(m)
        setConversations(c)
      })
      .finally(() => setLoading(false))
  }, [])

  const handleAdd = async (e: FormEvent) => {
    e.preventDefault()
    if (!newFact.trim()) return
    setAdding(true)
    try {
      const created = await memoryApi.create(newFact.trim())
      setMemories((prev) => [created, ...prev])
      setNewFact('')
    } finally {
      setAdding(false)
    }
  }

  const handleDelete = async (id: string) => {
    setMemories((prev) => prev.filter((m) => m.id !== id))
    await memoryApi.remove(id)
  }

  return (
    <div style={{ position: 'relative', zIndex: 1, minHeight: '100vh', paddingTop: 100, paddingBottom: 80 }}>
      <div style={{ maxWidth: 800, margin: '0 auto', padding: '24px' }}>
        <div style={{ marginBottom: 32 }}>
          <h1 style={{ fontSize: 28, fontWeight: 700, color: 'white', letterSpacing: '-0.5px', margin: '0 0 8px' }}>
            Memory
          </h1>
          <p style={{ fontSize: 14, color: '#52525b', margin: 0 }}>
            Durable facts AutoMateAI remembers about you, and your past conversations
          </p>
        </div>

        {/* Long-term memory */}
        <div style={{ marginBottom: 36 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 14 }}>
            <Brain size={15} color="#a855f7" />
            <h2 style={{ fontSize: 15, fontWeight: 600, color: 'white', margin: 0 }}>Remembered facts</h2>
          </div>

          <form onSubmit={handleAdd} className="glass" style={{ display: 'flex', gap: 10, padding: 10, marginBottom: 14 }}>
            <input
              value={newFact}
              onChange={(e) => setNewFact(e.target.value)}
              placeholder="Add something for AutoMateAI to remember (e.g. I prefer window seats)"
              style={{
                flex: 1,
                padding: '8px 10px',
                borderRadius: 8,
                border: '1px solid rgba(255,255,255,0.08)',
                background: 'rgba(255,255,255,0.03)',
                color: 'white',
                fontSize: 13,
                outline: 'none',
                fontFamily: 'inherit',
              }}
            />
            <button type="submit" className="btn-primary" disabled={adding} style={{ padding: '8px 14px', fontSize: 13, display: 'flex', alignItems: 'center', gap: 6 }}>
              <Plus size={14} /> Add
            </button>
          </form>

          {loading ? (
            <div className="glass" style={{ padding: 24, textAlign: 'center', fontSize: 13, color: '#52525b' }}>
              Loading…
            </div>
          ) : memories.length === 0 ? (
            <div className="glass" style={{ padding: 24, textAlign: 'center', fontSize: 13, color: '#52525b' }}>
              Nothing remembered yet. Facts you mention in chat get picked up automatically too.
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
              {memories.map((m) => (
                <div key={m.id} className="glass" style={{ padding: '12px 14px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: 10 }}>
                  <div>
                    <div style={{ fontSize: 13, color: 'white' }}>{m.content}</div>
                    <div style={{ fontSize: 11, color: '#52525b', marginTop: 3 }}>
                      {m.category} · {formatDate(m.created_at)}
                    </div>
                  </div>
                  <button
                    onClick={() => handleDelete(m.id)}
                    style={{ background: 'transparent', border: 'none', cursor: 'pointer', padding: 6, flexShrink: 0 }}
                  >
                    <Trash2 size={14} color="#52525b" />
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Conversation history */}
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 14 }}>
            <MessageSquare size={15} color="#a855f7" />
            <h2 style={{ fontSize: 15, fontWeight: 600, color: 'white', margin: 0 }}>Past conversations</h2>
          </div>

          {!loading && conversations.length === 0 ? (
            <div className="glass" style={{ padding: 24, textAlign: 'center', fontSize: 13, color: '#52525b' }}>
              No conversations yet.
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
              {conversations.map((c) => (
                <div key={c.id} className="glass" style={{ padding: '12px 14px' }}>
                  <div style={{ fontSize: 13, color: 'white' }}>{c.title}</div>
                  <div style={{ fontSize: 11, color: '#52525b', marginTop: 3 }}>Updated {formatDate(c.updated_at)}</div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
