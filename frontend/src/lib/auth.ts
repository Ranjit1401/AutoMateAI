import { authApi, User } from '@/lib/api'

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
  await authApi.signup(email, password, name)

  const user = await authApi.me()
  setUser(user)

  return user
}

export async function loginAndStore(
  email: string,
  password: string,
): Promise<StoredUser> {
  await authApi.login(email, password)

  const user = await authApi.me()
  setUser(user)

  return user
}

export async function logout(): Promise<void> {
  try {
    await authApi.logout()
  } catch {}

  removeUser()

  if (typeof window !== 'undefined') {
    window.location.href = '/auth/login'
  }
}

export async function isAuthenticated(): Promise<boolean> {
  try {
    const user = await authApi.me()
    setUser(user)
    return true
  } catch {
    removeUser()
    return false
  }
}
