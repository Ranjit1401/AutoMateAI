'use client'

import { useEffect, useState } from 'react'
import { Settings as SettingsIcon, Save, Check } from 'lucide-react'
import { settingsApi, type Preferences } from '@/lib/api'
import { useAuth } from '@/contexts/AuthContext'

const MODEL_OPTIONS = ['llama-3.3-70b-versatile', 'llama-3.1-8b-instant', 'mixtral-8x7b-32768']

function Toggle({ checked, onChange }: { checked: boolean; onChange: (v: boolean) => void }) {
  return (
    <button
      onClick={() => onChange(!checked)}
      style={{
        width: 40,
        height: 22,
        borderRadius: 999,
        border: 'none',
        cursor: 'pointer',
        background: checked ? 'linear-gradient(135deg, #a855f7, #6366f1)' : 'rgba(255,255,255,0.1)',
        position: 'relative',
        transition: 'background 0.2s ease',
        flexShrink: 0,
      }}
    >
      <div
        style={{
          width: 16,
          height: 16,
          borderRadius: '50%',
          background: 'white',
          position: 'absolute',
          top: 3,
          left: checked ? 21 : 3,
          transition: 'left 0.2s ease',
        }}
      />
    </button>
  )
}

export default function SettingsPage() {
  const { user } = useAuth()
  const [prefs, setPrefs] = useState<Preferences | null>(null)
  const [saving, setSaving] = useState(false)
  const [saved, setSaved] = useState(false)

  useEffect(() => {
    settingsApi.get().then(setPrefs)
  }, [])

  const update = (patch: Partial<Preferences>) => {
    setPrefs((prev) => (prev ? { ...prev, ...patch } : prev))
    setSaved(false)
  }

  const handleSave = async () => {
    if (!prefs) return
    setSaving(true)
    try {
      const updated = await settingsApi.update({
        preferred_model: prefs.preferred_model,
        theme: prefs.theme,
        notifications_enabled: prefs.notifications_enabled,
      })
      setPrefs(updated)
      setSaved(true)
    } finally {
      setSaving(false)
    }
  }

  return (
    <div style={{ position: 'relative', zIndex: 1, minHeight: '100vh', paddingTop: 100, paddingBottom: 80 }}>
      <div style={{ maxWidth: 640, margin: '0 auto', padding: '24px' }}>
        <div style={{ marginBottom: 32, display: 'flex', alignItems: 'center', gap: 10 }}>
          <SettingsIcon size={20} color="#a855f7" />
          <h1 style={{ fontSize: 28, fontWeight: 700, color: 'white', letterSpacing: '-0.5px', margin: 0 }}>Settings</h1>
        </div>

        {/* Profile */}
        <div className="glass" style={{ padding: 20, marginBottom: 16 }}>
          <h2 style={{ fontSize: 14, fontWeight: 600, color: 'white', margin: '0 0 12px' }}>Profile</h2>
          <div style={{ fontSize: 13, color: '#a1a1aa' }}>
            <div>Name: {user?.full_name || '—'}</div>
            <div style={{ marginTop: 4 }}>Email: {user?.email}</div>
          </div>
        </div>

        {!prefs ? (
          <div className="glass" style={{ padding: 24, textAlign: 'center', fontSize: 13, color: '#52525b' }}>
            Loading preferences…
          </div>
        ) : (
          <>
            {/* Model */}
            <div className="glass" style={{ padding: 20, marginBottom: 16 }}>
              <h2 style={{ fontSize: 14, fontWeight: 600, color: 'white', margin: '0 0 12px' }}>Model</h2>
              <select
                value={prefs.preferred_model}
                onChange={(e) => update({ preferred_model: e.target.value })}
                style={{
                  width: '100%',
                  padding: '10px 12px',
                  borderRadius: 10,
                  border: '1px solid rgba(255,255,255,0.1)',
                  background: 'rgba(255,255,255,0.04)',
                  color: 'white',
                  fontSize: 13,
                  fontFamily: 'inherit',
                  outline: 'none',
                }}
              >
                {MODEL_OPTIONS.map((m) => (
                  <option key={m} value={m} style={{ background: '#18181b' }}>
                    {m}
                  </option>
                ))}
              </select>
            </div>

            {/* Preferences */}
            <div className="glass" style={{ padding: 20, marginBottom: 16 }}>
              <h2 style={{ fontSize: 14, fontWeight: 600, color: 'white', margin: '0 0 16px' }}>Preferences</h2>

              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 14 }}>
                <div>
                  <div style={{ fontSize: 13, color: 'white' }}>Theme</div>
                  <div style={{ fontSize: 11, color: '#52525b' }}>Dark or light interface</div>
                </div>
                <select
                  value={prefs.theme}
                  onChange={(e) => update({ theme: e.target.value })}
                  style={{
                    padding: '6px 10px',
                    borderRadius: 8,
                    border: '1px solid rgba(255,255,255,0.1)',
                    background: 'rgba(255,255,255,0.04)',
                    color: 'white',
                    fontSize: 12,
                    fontFamily: 'inherit',
                  }}
                >
                  <option value="dark" style={{ background: '#18181b' }}>Dark</option>
                  <option value="light" style={{ background: '#18181b' }}>Light</option>
                </select>
              </div>

              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <div>
                  <div style={{ fontSize: 13, color: 'white' }}>Notifications</div>
                  <div style={{ fontSize: 11, color: '#52525b' }}>Task completion and error alerts</div>
                </div>
                <Toggle checked={prefs.notifications_enabled} onChange={(v) => update({ notifications_enabled: v })} />
              </div>
            </div>

            <button
              onClick={handleSave}
              disabled={saving}
              className="btn-primary"
              style={{ display: 'flex', alignItems: 'center', gap: 8, padding: '10px 18px', fontSize: 13 }}
            >
              {saved ? <Check size={14} /> : <Save size={14} />}
              {saving ? 'Saving…' : saved ? 'Saved' : 'Save changes'}
            </button>
          </>
        )}
      </div>
    </div>
  )
}
