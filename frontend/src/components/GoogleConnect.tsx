'use client'

import { googleApi } from '@/lib/api'

export default function GoogleConnect() {
  const connectGoogle = () => {
    // Fixed: this used to point at /google/login, which doesn't exist on
    // the backend (the real route is /google/auth) — the button was a 404.
    window.location.href = googleApi.connectUrl()
  }

  return (
    <button onClick={connectGoogle} className="btn-primary" style={{ padding: '8px 16px', fontSize: 13 }}>
      Connect Google
    </button>
  )
}
