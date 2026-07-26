'use client'

import { useEffect, useState } from 'react'
import { CheckCircle, Mail, Calendar, HardDrive, Sheet, Phone, Mic } from 'lucide-react'
import GoogleConnect from '@/components/GoogleConnect'
import { googleApi } from '@/lib/api'

const GOOGLE_SERVICES = [
  { name: 'Gmail', icon: Mail, desc: 'Send emails through your Gmail account' },
  { name: 'Calendar', icon: Calendar, desc: 'Create events on your Google Calendar' },
  { name: 'Drive', icon: HardDrive, desc: 'Upload files to your Google Drive' },
  { name: 'Sheets', icon: Sheet, desc: 'Append rows to your Google Sheets' },
]

export default function ConnectedApps() {
  const [googleConnected, setGoogleConnected] = useState<boolean | null>(null)

  useEffect(() => {
    googleApi
      .status()
      .then((s) => setGoogleConnected(s.connected))
      .catch(() => setGoogleConnected(false))
  }, [])

  return (
    <div style={{ position: 'relative', zIndex: 1, minHeight: '100vh', paddingTop: 100, paddingBottom: 80 }}>
      <div style={{ maxWidth: 800, margin: '0 auto', padding: '24px' }}>
        <div style={{ marginBottom: 32, textAlign: 'center' }}>
          <h1 style={{ fontSize: 28, fontWeight: 700, color: 'white', letterSpacing: '-0.5px', margin: '0 0 8px' }}>
            Connected Apps
          </h1>
          <p style={{ fontSize: 14, color: '#52525b', margin: 0 }}>
            Link your Google account so agents can send email, book calendar events, and more
          </p>
        </div>

        {/* Google connection */}
        <div className="glass" style={{ padding: 24, marginBottom: 20 }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 18, flexWrap: 'wrap', gap: 12 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img src="/logo.png" alt="" style={{ width: 32, height: 32, objectFit: 'contain', opacity: 0 }} />
              <div>
                <div style={{ fontSize: 15, fontWeight: 600, color: 'white' }}>Google Workspace</div>
                <div style={{ fontSize: 12, color: '#52525b' }}>
                  {googleConnected === null ? 'Checking status…' : googleConnected ? 'Connected' : 'Not connected'}
                </div>
              </div>
            </div>
            {googleConnected ? (
              <span style={{ display: 'flex', alignItems: 'center', gap: 6, color: '#10b981', fontSize: 13 }}>
                <CheckCircle size={15} /> Connected
              </span>
            ) : (
              <GoogleConnect />
            )}
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(160px, 1fr))', gap: 10 }}>
            {GOOGLE_SERVICES.map(({ name, icon: Icon, desc }) => (
              <div key={name} style={{ padding: '12px 14px', borderRadius: 10, background: 'rgba(255,255,255,0.03)', border: '1px solid rgba(255,255,255,0.06)' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 6 }}>
                  <Icon size={14} color="#a855f7" />
                  <span style={{ fontSize: 13, fontWeight: 500, color: 'white' }}>{name}</span>
                </div>
                <div style={{ fontSize: 11, color: '#52525b' }}>{desc}</div>
              </div>
            ))}
          </div>
        </div>

        {/* Server-configured integrations */}
        <div className="glass" style={{ padding: 24 }}>
          <div style={{ fontSize: 13, fontWeight: 600, color: 'white', marginBottom: 4 }}>Voice &amp; SMS</div>
          <div style={{ fontSize: 12, color: '#52525b', marginBottom: 16 }}>
            Configured by the server via API keys — no per-user connection needed
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(160px, 1fr))', gap: 10 }}>
            <div style={{ padding: '12px 14px', borderRadius: 10, background: 'rgba(255,255,255,0.03)', border: '1px solid rgba(255,255,255,0.06)' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 6 }}>
                <Phone size={14} color="#a855f7" />
                <span style={{ fontSize: 13, fontWeight: 500, color: 'white' }}>Twilio</span>
              </div>
              <div style={{ fontSize: 11, color: '#52525b' }}>Outbound calls &amp; SMS</div>
            </div>
            <div style={{ padding: '12px 14px', borderRadius: 10, background: 'rgba(255,255,255,0.03)', border: '1px solid rgba(255,255,255,0.06)' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 6 }}>
                <Mic size={14} color="#a855f7" />
                <span style={{ fontSize: 13, fontWeight: 500, color: 'white' }}>Vapi</span>
              </div>
              <div style={{ fontSize: 11, color: '#52525b' }}>Voice AI sessions</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
