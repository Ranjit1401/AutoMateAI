'use client'

import { createContext, useCallback, useContext, useEffect, useRef, useState, type ReactNode } from 'react'
import { authApi, type User } from '@/lib/api'

interface AuthContextValue {
  user: User | null
  loading: boolean
  login: (email: string, password: string) => Promise<void>
  signup: (email: string, password: string, fullName?: string) => Promise<void>
  logout: () => Promise<void>
  refresh: () => Promise<void>
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined)

// Silent-refresh interval: call /auth/refresh every 20 minutes while logged in.
// This slides the cookie expiry forward so the session persists across long
// browser sessions without requiring the user to log in again.
const SILENT_REFRESH_INTERVAL_MS = 20 * 60 * 1000 // 20 minutes

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)
  const silentRefreshTimer = useRef<ReturnType<typeof setInterval> | null>(null)

  const stopSilentRefresh = useCallback(() => {
    if (silentRefreshTimer.current) {
      clearInterval(silentRefreshTimer.current)
      silentRefreshTimer.current = null
    }
  }, [])

  const startSilentRefresh = useCallback(() => {
    stopSilentRefresh()
    silentRefreshTimer.current = setInterval(async () => {
      try {
        // /auth/refresh re-issues the session cookie, extending its expiry.
        // If the cookie is already expired this will 401 — that's fine, we
        // just clear the user state so the UI redirects to login.
        await authApi.refresh()
      } catch {
        setUser(null)
        stopSilentRefresh()
      }
    }, SILENT_REFRESH_INTERVAL_MS)
  }, [stopSilentRefresh])

  const refresh = useCallback(async () => {
    try {
      const me = await authApi.me()
      setUser(me)
    } catch {
      setUser(null)
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    refresh()
  }, [refresh])

  // Start/stop the silent-refresh timer whenever the user changes.
  useEffect(() => {
    if (user) {
      startSilentRefresh()
    } else {
      stopSilentRefresh()
    }
    return stopSilentRefresh
  }, [user, startSilentRefresh, stopSilentRefresh])

  const login = useCallback(async (email: string, password: string) => {
    const { user: loggedInUser } = await authApi.login(email, password)
    setUser(loggedInUser)
  }, [])

  const signup = useCallback(async (email: string, password: string, fullName?: string) => {
    const { user: newUser } = await authApi.signup(email, password, fullName)
    setUser(newUser)
  }, [])

  const logout = useCallback(async () => {
    stopSilentRefresh()
    await authApi.logout()
    setUser(null)
  }, [stopSilentRefresh])

  return (
    <AuthContext.Provider value={{ user, loading, login, signup, logout, refresh }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used within an AuthProvider')
  return ctx
}
