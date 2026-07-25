'use client'

import { useState } from 'react'
import {
  User,
  Palette,
  Cpu,
  Key,
  Bell,
  Plug,
  Shield,
  Check,
  Eye,
  EyeOff,
  Moon,
} from 'lucide-react'

const sections = [
  { id: 'profile', label: 'Profile', icon: User },
  { id: 'theme', label: 'Appearance', icon: Palette },
  { id: 'llm', label: 'LLM Provider', icon: Cpu },
  { id: 'keys', label: 'API Keys', icon: Key },
  { id: 'notifications', label: 'Notifications', icon: Bell },
  { id: 'integrations', label: 'Connected Apps', icon: Plug },
  { id: 'privacy', label: 'Privacy', icon: Shield },
]

function Toggle({ on, onChange }: { on: boolean; onChange: (v: boolean) => void }) {
  return (
    <button
      onClick={() => onChange(!on)}
      style={{
        width: 40,
        height: 22,
        borderRadius: 11,
        background: on ? 'linear-gradient(135deg, #a855f7, #8b5cf6)' : 'rgba(255,255,255,0.1)',
        border: 'none',
        cursor: 'pointer',
        position: 'relative',
        transition: 'background 0.3s ease',
        flexShrink: 0,
      }}
    >
      <div
        style={{
          position: 'absolute',
          top: 3,
          left: on ? 21 : 3,
          width: 16,
          height: 16,
          borderRadius: '50%',
          background: 'white',
          transition: 'left 0.3s ease',
          boxShadow: '0 1px 4px rgba(0,0,0,0.3)',
        }}
      />
    </button>
  )
}

function SettingRow({
  label,
  desc,
  children,
}: {
  label: string
  desc?: string
  children: React.ReactNode
}) {
  return (
    <div
      style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        gap: 16,
        padding: '14px 0',
        borderBottom: '1px solid rgba(255,255,255,0.05)',
      }}
    >
      <div>
        <div style={{ fontSize: 13, fontWeight: 500, color: 'white' }}>{label}</div>
        {desc && <div style={{ fontSize: 12, color: '#52525b', marginTop: 2 }}>{desc}</div>}
      </div>
      {children}
    </div>
  )
}

function ProfileSection() {
  return (
    <div>
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: 16,
          padding: '20px 0',
          borderBottom: '1px solid rgba(255,255,255,0.05)',
          marginBottom: 8,
        }}
      >
        <div
          style={{
            width: 60,
            height: 60,
            borderRadius: '50%',
            background: 'linear-gradient(135deg, #a855f7, #ec4899)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontSize: 22,
            fontWeight: 700,
            color: 'white',
            boxShadow: '0 0 20px rgba(168,85,247,0.4)',
          }}
        >
          N
        </div>
        <div>
          <div style={{ fontSize: 16, fontWeight: 600, color: 'white' }}>Nikita</div>
          <div style={{ fontSize: 13, color: '#52525b' }}>nikita@company.com</div>
          <div
            style={{
              fontSize: 11,
              color: '#a855f7',
              marginTop: 4,
              background: 'rgba(168,85,247,0.12)',
              display: 'inline-block',
              padding: '2px 8px',
              borderRadius: 6,
            }}
          >
            Pro Plan
          </div>
        </div>
        <button className="btn-glass" style={{ marginLeft: 'auto', padding: '8px 14px', fontSize: 12 }}>
          Edit Profile
        </button>
      </div>
      <SettingRow label="Display Name" desc="How AutoMateAI addresses you">
        <input
          defaultValue="Nikita"
          style={{
            background: 'rgba(255,255,255,0.06)',
            border: '1px solid rgba(255,255,255,0.1)',
            borderRadius: 8,
            padding: '7px 12px',
            fontSize: 13,
            color: 'white',
            fontFamily: 'inherit',
            width: 200,
          }}
        />
      </SettingRow>
      <SettingRow label="Timezone" desc="Used for scheduling tasks">
        <select
          defaultValue="America/New_York"
          style={{
            background: 'rgba(255,255,255,0.06)',
            border: '1px solid rgba(255,255,255,0.1)',
            borderRadius: 8,
            padding: '7px 12px',
            fontSize: 13,
            color: 'white',
            fontFamily: 'inherit',
            width: 200,
          }}
        >
          <option value="America/New_York">Eastern Time (ET)</option>
          <option value="America/Los_Angeles">Pacific Time (PT)</option>
          <option value="Europe/London">London (GMT)</option>
        </select>
      </SettingRow>
    </div>
  )
}

function LLMSection() {
  const [selected, setSelected] = useState('claude-sonnet-4-6')

  const models = [
    { id: 'claude-opus-4-8', label: 'Claude Opus 4.8', desc: 'Most capable, slower', badge: 'Best' },
    { id: 'claude-sonnet-4-6', label: 'Claude Sonnet 4.6', desc: 'Balanced speed & quality', badge: 'Recommended' },
    { id: 'claude-haiku-4-5', label: 'Claude Haiku 4.5', desc: 'Fast, lightweight tasks', badge: '' },
    { id: 'gpt-4o', label: 'GPT-4o', desc: 'OpenAI flagship model', badge: '' },
  ]

  return (
    <div>
      <p style={{ fontSize: 13, color: '#52525b', marginBottom: 16, lineHeight: 1.6 }}>
        Choose which language model powers AutoMateAI. Each model has different strengths.
      </p>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
        {models.map(m => (
          <button
            key={m.id}
            onClick={() => setSelected(m.id)}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: 12,
              padding: '14px 16px',
              borderRadius: 12,
              border: `1px solid ${selected === m.id ? 'rgba(168,85,247,0.4)' : 'rgba(255,255,255,0.07)'}`,
              background: selected === m.id ? 'rgba(168,85,247,0.08)' : 'rgba(255,255,255,0.03)',
              cursor: 'pointer',
              fontFamily: 'inherit',
              textAlign: 'left',
              transition: 'all 0.2s ease',
            }}
          >
            <div
              style={{
                width: 18,
                height: 18,
                borderRadius: '50%',
                border: `2px solid ${selected === m.id ? '#a855f7' : 'rgba(255,255,255,0.2)'}`,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                flexShrink: 0,
              }}
            >
              {selected === m.id && (
                <div
                  style={{
                    width: 8,
                    height: 8,
                    borderRadius: '50%',
                    background: '#a855f7',
                  }}
                />
              )}
            </div>
            <div style={{ flex: 1 }}>
              <div style={{ fontSize: 13, fontWeight: 500, color: 'white', display: 'flex', alignItems: 'center', gap: 8 }}>
                {m.label}
                {m.badge && (
                  <span
                    style={{
                      fontSize: 10,
                      color: '#a855f7',
                      background: 'rgba(168,85,247,0.15)',
                      padding: '1px 6px',
                      borderRadius: 4,
                    }}
                  >
                    {m.badge}
                  </span>
                )}
              </div>
              <div style={{ fontSize: 12, color: '#52525b', marginTop: 2 }}>{m.desc}</div>
            </div>
          </button>
        ))}
      </div>
    </div>
  )
}

function APIKeysSection() {
  const [show, setShow] = useState<Record<string, boolean>>({})

  const keys = [
    { name: 'Anthropic API Key', placeholder: 'sk-ant-...', set: true },
    { name: 'OpenAI API Key', placeholder: 'sk-...', set: false },
    { name: 'Serper API Key', placeholder: 'Serper search key', set: true },
  ]

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
      {keys.map(k => (
        <div key={k.name}>
          <div style={{ fontSize: 12, color: '#71717a', marginBottom: 6, fontWeight: 500 }}>{k.name}</div>
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: 8,
              background: 'rgba(255,255,255,0.04)',
              border: '1px solid rgba(255,255,255,0.08)',
              borderRadius: 10,
              padding: '8px 12px',
            }}
          >
            <input
              type={show[k.name] ? 'text' : 'password'}
              defaultValue={k.set ? '••••••••••••••••••••••' : ''}
              placeholder={k.placeholder}
              style={{
                flex: 1,
                fontSize: 13,
                fontFamily: k.set ? 'JetBrains Mono, monospace' : 'inherit',
                border: 'none',
                background: 'transparent',
                color: 'white',
                outline: 'none',
              }}
            />
            <button
              onClick={() => setShow(s => ({ ...s, [k.name]: !s[k.name] }))}
              style={{ background: 'none', border: 'none', cursor: 'pointer', color: '#52525b', padding: 2 }}
            >
              {show[k.name] ? <EyeOff size={14} /> : <Eye size={14} />}
            </button>
            {k.set && <Check size={14} color="#10b981" />}
          </div>
        </div>
      ))}
    </div>
  )
}

function NotificationsSection() {
  const [prefs, setPrefs] = useState({
    taskComplete: true,
    taskFailed: true,
    weeklySummary: false,
    emailDigest: true,
    slackAlerts: false,
  })

  return (
    <div>
      {[
        { key: 'taskComplete', label: 'Task completed', desc: 'Notify when autonomous tasks finish' },
        { key: 'taskFailed', label: 'Task failed', desc: 'Alert on errors or failures' },
        { key: 'weeklySummary', label: 'Weekly summary', desc: 'Digest of tasks and usage every Monday' },
        { key: 'emailDigest', label: 'Email digest', desc: 'Daily email of completed tasks' },
        { key: 'slackAlerts', label: 'Slack alerts', desc: 'Push notifications to your Slack' },
      ].map(({ key, label, desc }) => (
        <SettingRow key={key} label={label} desc={desc}>
          <Toggle
            on={prefs[key as keyof typeof prefs]}
            onChange={v => setPrefs(p => ({ ...p, [key]: v }))}
          />
        </SettingRow>
      ))}
    </div>
  )
}

function PrivacySection() {
  const [prefs, setPrefs] = useState({
    saveHistory: true,
    learnPrefs: true,
    shareAnalytics: false,
    storeFiles: true,
  })

  return (
    <div>
      {[
        { key: 'saveHistory', label: 'Save conversation history', desc: 'Store past chats for context' },
        { key: 'learnPrefs', label: 'Learn my preferences', desc: 'AutoMateAI adapts to your style over time' },
        { key: 'shareAnalytics', label: 'Share usage analytics', desc: 'Help improve AutoMateAI (anonymous)' },
        { key: 'storeFiles', label: 'Store processed files', desc: 'Keep copies of analyzed documents' },
      ].map(({ key, label, desc }) => (
        <SettingRow key={key} label={label} desc={desc}>
          <Toggle
            on={prefs[key as keyof typeof prefs]}
            onChange={v => setPrefs(p => ({ ...p, [key]: v }))}
          />
        </SettingRow>
      ))}
      <div style={{ marginTop: 20 }}>
        <button
          style={{
            background: 'rgba(239,68,68,0.1)',
            border: '1px solid rgba(239,68,68,0.2)',
            color: '#ef4444',
            padding: '8px 16px',
            borderRadius: 10,
            fontSize: 13,
            fontWeight: 500,
            cursor: 'pointer',
            fontFamily: 'inherit',
            transition: 'all 0.2s ease',
          }}
          onMouseEnter={e => {
            (e.currentTarget as HTMLButtonElement).style.background = 'rgba(239,68,68,0.15)'
          }}
          onMouseLeave={e => {
            (e.currentTarget as HTMLButtonElement).style.background = 'rgba(239,68,68,0.1)'
          }}
        >
          Delete all conversation data
        </button>
      </div>
    </div>
  )
}

const sectionContent: Record<string, React.ReactNode> = {
  profile: <ProfileSection />,
  theme: (
    <div>
      <SettingRow label="Color theme" desc="AutoMateAI is dark mode only">
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: 8,
            padding: '6px 12px',
            borderRadius: 8,
            background: 'rgba(255,255,255,0.06)',
            border: '1px solid rgba(255,255,255,0.1)',
            fontSize: 13,
            color: '#c4b5fd',
          }}
        >
          <Moon size={13} color="#a855f7" />
          Dark Mode
        </div>
      </SettingRow>
      <SettingRow label="Accent color" desc="Primary brand color throughout the interface">
        <div style={{ display: 'flex', gap: 6 }}>
          {['#a855f7', '#6366f1', '#ec4899', '#06b6d4', '#10b981'].map(c => (
            <div
              key={c}
              style={{
                width: 24,
                height: 24,
                borderRadius: '50%',
                background: c,
                cursor: 'pointer',
                border: c === '#a855f7' ? '2px solid white' : '2px solid transparent',
                boxShadow: c === '#a855f7' ? `0 0 10px ${c}` : 'none',
                transition: 'all 0.2s ease',
              }}
            />
          ))}
        </div>
      </SettingRow>
      <SettingRow label="Reduce motion" desc="Minimize animations across the interface">
        <Toggle on={false} onChange={() => {}} />
      </SettingRow>
      <SettingRow label="Glass blur intensity" desc="Backdrop blur strength for panels">
        <input
          type="range"
          min={0}
          max={100}
          defaultValue={75}
          style={{ width: 120, accentColor: '#a855f7' }}
        />
      </SettingRow>
    </div>
  ),
  llm: <LLMSection />,
  keys: <APIKeysSection />,
  notifications: <NotificationsSection />,
  integrations: (
    <div>
      <p style={{ fontSize: 13, color: '#52525b', marginBottom: 16 }}>
        Manage your connected apps from the Connected Apps page.
      </p>
      <button className="btn-primary" style={{ fontSize: 13, padding: '10px 20px' }}>
        Manage Integrations
      </button>
    </div>
  ),
  privacy: <PrivacySection />,
}

export default function Settings() {
  const [active, setActive] = useState('profile')

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
      <div style={{ maxWidth: 860, margin: '0 auto', padding: '24px' }}>
        <div
          style={{
            marginBottom: 28,
            animation: 'slide-up 0.5s cubic-bezier(0.16,1,0.3,1) both',
          }}
        >
          <h1
            style={{ fontSize: 28, fontWeight: 700, color: 'white', letterSpacing: '-0.5px', margin: '0 0 8px' }}
          >
            Settings
          </h1>
          <p style={{ fontSize: 14, color: '#52525b', margin: 0 }}>
            Customize your AutoMateAI experience
          </p>
        </div>

        <div
          style={{
            display: 'grid',
            gridTemplateColumns: '200px 1fr',
            gap: 16,
            animation: 'slide-up 0.5s cubic-bezier(0.16,1,0.3,1) 0.08s both',
          }}
        >
          {/* Sidebar */}
          <div className="glass" style={{ padding: 8, alignSelf: 'start' }}>
            {sections.map(({ id, label, icon: Icon }) => {
              const isActive = active === id
              return (
                <button
                  key={id}
                  onClick={() => setActive(id)}
                  style={{
                    width: '100%',
                    display: 'flex',
                    alignItems: 'center',
                    gap: 10,
                    padding: '9px 12px',
                    borderRadius: 10,
                    border: 'none',
                    background: isActive
                      ? 'linear-gradient(135deg, rgba(168,85,247,0.15), rgba(99,102,241,0.1))'
                      : 'transparent',
                    color: isActive ? '#c4b5fd' : '#71717a',
                    fontSize: 13,
                    fontWeight: isActive ? 500 : 400,
                    fontFamily: 'inherit',
                    cursor: 'pointer',
                    textAlign: 'left',
                    transition: 'all 0.2s ease',
                    boxShadow: isActive ? 'inset 0 0 0 1px rgba(168,85,247,0.2)' : 'none',
                  }}
                  onMouseEnter={e => {
                    if (!isActive) (e.currentTarget as HTMLButtonElement).style.background = 'rgba(255,255,255,0.04)'
                  }}
                  onMouseLeave={e => {
                    if (!isActive) (e.currentTarget as HTMLButtonElement).style.background = 'transparent'
                  }}
                >
                  <Icon size={14} />
                  {label}
                </button>
              )
            })}
          </div>

          {/* Content */}
          <div className="glass" style={{ padding: 24 }}>
            <h2
              style={{
                fontSize: 16,
                fontWeight: 600,
                color: 'white',
                margin: '0 0 20px',
                paddingBottom: 16,
                borderBottom: '1px solid rgba(255,255,255,0.06)',
              }}
            >
              {sections.find(s => s.id === active)?.label}
            </h2>
            {sectionContent[active]}
          </div>
        </div>
      </div>
    </div>
  )
}
