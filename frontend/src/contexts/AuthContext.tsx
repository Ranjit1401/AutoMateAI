'use client'

import { createContext, useCallback, useContext, useEffect, useRef, useState, type ReactNode } from 'react'
import { authApi, setStoredToken, clearStoredToken, getStoredToken, type User } from '@/lib/api'

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
const SILENT_REFRESH_INTERVAL_MS = 20 * 60 * 1000

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
        const data = await authApi.refresh()
        // Refresh returns a new token — update localStorage so subsequent
        // requests use the fresh token.
        setStoredToken(data.access_token)
      } catch {
        clearStoredToken()
        setUser(null)
        stopSilentRefresh()
      }
    }, SILENT_REFRESH_INTERVAL_MS)
  }, [stopSilentRefresh])

  // On mount: check if there's a stored token and validate it with /auth/me.
  const refresh = useCallback(async () => {
    try {
      const me = await authApi.me()
      setUser(me)
    } catch {
      // Token expired or invalid — clear it so the middleware redirects to login.
      clearStoredToken()
      setUser(null)
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    // Only attempt /auth/me if we have a stored token (avoids unnecessary 401
    // on every page load for non-logged-in users).
    if (getStoredToken()) {
      refresh()
    } else {
      setLoading(false)
    }
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
    const data = await authApi.login(email, password)
    // Store the JWT returned in the response body — this is the Bearer token
    // used for cross-origin requests where cookies are blocked.
    setStoredToken(data.access_token)
    setUser(data.user)
  }, [])

  const signup = useCallback(async (email: string, password: string, fullName?: string) => {
    const data = await authApi.signup(email, password, fullName)
    setStoredToken(data.access_token)
    setUser(data.user)
  }, [])

  const logout = useCallback(async () => {
    stopSilentRefresh()
    clearStoredToken()
    try {
      await authApi.logout()
    } catch {
      // Even if the server call fails, we clear the local token.
    }
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
