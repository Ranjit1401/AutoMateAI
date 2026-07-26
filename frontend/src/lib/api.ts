/**
 * Typed backend API client.
 *
 * Auth strategy — dual transport to handle cross-origin browser cookie blocking:
 *
 * 1. The backend sets an httpOnly session cookie on login/signup (works for
 *    same-origin local dev).
 * 2. The backend ALSO returns the JWT in the response body.  The frontend
 *    stores it in localStorage and attaches it as "Authorization: Bearer <token>"
 *    on every request.  This is the path that works in production where browsers
 *    (Chrome Privacy Sandbox, Safari ITP, Firefox ETP) block third-party cookies
 *    even when SameSite=None; Secure is set.
 *
 * Both transports are sent simultaneously — the backend accepts whichever it sees.
 */

export const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || 'https://automateai-ugwf.onrender.com'

// ---------------------------------------------------------------------------
// Token storage — localStorage for cross-origin Bearer auth
// ---------------------------------------------------------------------------

const TOKEN_KEY = 'automateai_token'

export function getStoredToken(): string | null {
  if (typeof window === 'undefined') return null
  return localStorage.getItem(TOKEN_KEY)
}

export function setStoredToken(token: string): void {
  if (typeof window === 'undefined') return
  localStorage.setItem(TOKEN_KEY, token)
}

export function clearStoredToken(): void {
  if (typeof window === 'undefined') return
  localStorage.removeItem(TOKEN_KEY)
}

// ---------------------------------------------------------------------------
// Core fetch wrapper
// ---------------------------------------------------------------------------

export class ApiError extends Error {
  status: number
  constructor(status: number, message: string) {
    super(message)
    this.status = status
  }
}

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const token = getStoredToken()

  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(options.headers as Record<string, string>),
  }

  // Always send Bearer header when we have a token — this is the primary auth
  // transport for cross-origin production (Vercel → Render).
  if (token) {
    headers['Authorization'] = `Bearer ${token}`
  }

  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    // Also send cookies for same-origin local dev compatibility.
    credentials: 'include',
    headers,
  })

  if (!response.ok) {
    // If we get 401, clear the stored token so the user is redirected to login.
    if (response.status === 401) {
      clearStoredToken()
    }

    let detail = response.statusText
    try {
      const body = await response.json()
      detail = body.detail || detail
    } catch {
      // response had no JSON body
    }
    throw new ApiError(response.status, detail)
  }

  if (response.status === 204) return undefined as T
  return response.json() as Promise<T>
}

// ---------------------------------------------------------------------------
// Auth
// ---------------------------------------------------------------------------

export interface User {
  id: string
  email: string
  full_name: string | null
  created_at: string
}

export interface AuthResponse {
  user: User
  access_token: string
  access_token_expires_in_minutes: number
}

export const authApi = {
  signup: async (email: string, password: string, full_name?: string) => {
    const data = await request<AuthResponse>('/auth/signup', {
      method: 'POST',
      body: JSON.stringify({ email, password, full_name }),
    });

    setStoredToken(data.access_token);
    return data;
    },

  login: async (email: string, password: string) => {
    const data = await request<AuthResponse>('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });

    setStoredToken(data.access_token);
    return data;
    },
  logout: () => {
    clearStoredToken()
    return request<void>('/auth/logout', { method: 'POST' })
  },
  me: () => request<User>('/auth/me'),
  /** Re-issues the session cookie + token, extending the sliding expiry. */
  refresh: () =>
    request<AuthResponse>('/auth/refresh', {
      method: 'POST',
    }),
}

// ---------------------------------------------------------------------------
// Chat
// ---------------------------------------------------------------------------

export interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  created_at: string
}

export interface Conversation {
  id: string
  title: string
  created_at: string
  updated_at: string
}

export interface ConversationDetail extends Conversation {
  messages: Message[]
}

export const chatApi = {
  send: (message: string, conversation_id?: string) =>
    request<{ conversation_id: string; response: string }>('/chat', {
      method: 'POST',
      body: JSON.stringify({ message, conversation_id }),
    }),
  listConversations: () => request<Conversation[]>('/chat/conversations'),
  getConversation: (id: string) => request<ConversationDetail>(`/chat/conversations/${id}`),

  /** Streams pipeline progress via SSE. */
  stream: async (
    message: string,
    conversation_id: string | undefined,
    onEvent: (event: string, data: any) => void,
  ) => {
    const token = getStoredToken()
    const headers: Record<string, string> = { 'Content-Type': 'application/json' }
    if (token) headers['Authorization'] = `Bearer ${token}`

    const response = await fetch(`${API_BASE_URL}/chat/stream`, {
      method: 'POST',
      credentials: 'include',
      headers,
      body: JSON.stringify({ message, conversation_id }),
    })

    if (!response.ok || !response.body) {
      throw new ApiError(response.status, 'Please Login Before Start , use profile tab to get login  || For admin use email = admin@gmail.com and password = admin')
    }

    const reader = response.body.getReader()
    const decoder = new TextDecoder()
    let buffer = ''

    while (true) {
      const { done, value } = await reader.read()
      if (done) break
      buffer += decoder.decode(value, { stream: true })

      const chunks = buffer.split('\n\n')
      buffer = chunks.pop() || ''

      for (const chunk of chunks) {
        const eventLine = chunk.split('\n').find((l) => l.startsWith('event:'))
        const dataLine = chunk.split('\n').find((l) => l.startsWith('data:'))
        if (!eventLine || !dataLine) continue

        const eventName = eventLine.replace('event:', '').trim()
        const data = JSON.parse(dataLine.replace('data:', '').trim())
        onEvent(eventName, data)
      }
    }
  },
}

// ---------------------------------------------------------------------------
// Tasks / Memory / Logs / Settings
// ---------------------------------------------------------------------------

export interface Task {
  id: string
  title: string
  agent: string
  action: string
  status: 'pending' | 'running' | 'done' | 'failed'
  result: Record<string, any> | null
  error: string | null
  created_at: string
  started_at: string | null
  finished_at: string | null
}

export const tasksApi = {
  list: () => request<Task[]>('/tasks'),
}

export interface MemoryEntry {
  id: string
  category: string
  content: string
  created_at: string
}

export const memoryApi = {
  list: () => request<MemoryEntry[]>('/memory'),
  create: (content: string, category = 'general') =>
    request<MemoryEntry>('/memory', { method: 'POST', body: JSON.stringify({ content, category }) }),
  remove: (id: string) => request<void>(`/memory/${id}`, { method: 'DELETE' }),
}

export interface LogEntry {
  id: string
  level: 'info' | 'warning' | 'error'
  source: string
  message: string
  meta: Record<string, any> | null
  created_at: string
}

export const logsApi = {
  list: () => request<LogEntry[]>('/logs'),
}

export interface Preferences {
  preferred_model: string
  theme: string
  notifications_enabled: boolean
  extra: Record<string, any> | null
}

export const settingsApi = {
  get: () => request<Preferences>('/settings/preferences'),
  update: (payload: Partial<Preferences>) =>
    request<Preferences>('/settings/preferences', { method: 'PUT', body: JSON.stringify(payload) }),
}

// ---------------------------------------------------------------------------
// Google connected apps
// ---------------------------------------------------------------------------

export const googleApi = {
  status: () => request<{ connected: boolean }>('/google/status'),
  connectUrl: () => `${API_BASE_URL}/google/auth`,
}
