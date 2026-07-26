/**
 * Auth utilities — wraps localStorage token management and provides
 * a reactive way to check auth state across the app.
 */

import {
  auth as authApi,
  setTokens,
  clearTokens,
  getAccessToken,
  TokenResponse,
  UserProfile,
} from '@/lib/api'

export interface StoredUser {
  id: string
  name: string
  email: string
  created_at: string
}

// ─── Persist / retrieve user profile ─────────────────────────────────────────

export function setUser(user: UserProfile): void {
  if (typeof window === 'undefined') return
  localStorage.setItem('user', JSON.stringify(user))
}

export function getUser(): StoredUser | null {
  if (typeof window === 'undefined') return null
  try {
    const raw = localStorage.getItem('user')
    return raw ? (JSON.parse(raw) as StoredUser) : null
  } catch {
    return null
  }
}

export function isAuthenticated(): boolean {
  return Boolean(getAccessToken())
}

// ─── Auth actions ─────────────────────────────────────────────────────────────

export async function signupAndStore(
  name: string,
  email: string,
  password: string,
): Promise<StoredUser> {
  const tokens: TokenResponse = await authApi.signup(name, email, password)
  setTokens(tokens.access_token, tokens.refresh_token)
  const user = await authApi.me()
  setUser(user)
  return user
}

export async function loginAndStore(
  email: string,
  password: string,
): Promise<StoredUser> {
  const tokens: TokenResponse = await authApi.login(email, password)
  setTokens(tokens.access_token, tokens.refresh_token)
  const user = await authApi.me()
  setUser(user)
  return user
}

export function logout(): void {
  clearTokens()
  if (typeof window !== 'undefined') window.location.href = '/auth/login'
}
