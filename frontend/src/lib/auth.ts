import { authApi, setStoredToken, clearStoredToken, User } from '@/lib/api'

export type StoredUser = User

export function setUser(user: StoredUser): void {
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

export function removeUser(): void {
  if (typeof window === 'undefined') return
  localStorage.removeItem('user')
}

export async function signupAndStore(
  name: string,
  email: string,
  password: string,
): Promise<StoredUser> {
  const data = await authApi.signup(email, password, name)
  // Store the token BEFORE calling /auth/me so the Bearer header is sent
  setStoredToken(data.access_token)

  const user = await authApi.me()
  setUser(user)

  return user
}

export async function loginAndStore(
  email: string,
  password: string,
): Promise<StoredUser> {
  // Capture the response — it contains the access_token we need to store
  const data = await authApi.login(email, password)
  // Store token so subsequent /auth/me call includes the Bearer header
  setStoredToken(data.access_token)

  const user = await authApi.me()
  setUser(user)

  return user
}

export async function logout(): Promise<void> {
  clearStoredToken()
  removeUser()

  try {
    await authApi.logout()
  } catch {}

  if (typeof window !== 'undefined') {
    window.location.href = '/login'
  }
}

export async function isAuthenticated(): Promise<boolean> {
  try {
    const user = await authApi.me()
    setUser(user)
    return true
  } catch {
    clearStoredToken()
    removeUser()
    return false
  }
}