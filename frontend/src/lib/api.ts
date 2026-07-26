/**
 * Typed backend API client. Cookie-based auth (the httpOnly session cookie
 * set by the backend on login/signup is sent automatically via
 * `credentials: 'include'`) — the frontend never touches a raw JWT.
 *
 * Replaces the old services/api.ts, which only had one function that was
 * never actually imported anywhere and didn't match the backend's request
 * shape.
 */
export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export class ApiError extends Error {
  status: number
  constructor(status: number, message: string) {
    super(message)
    this.status = status
  }
}

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  })

  if (!response.ok) {
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

export const authApi = {
  signup: (email: string, password: string, full_name?: string) =>
    request<{ user: User; access_token_expires_in_minutes: number }>('/auth/signup', {
      method: 'POST',
      body: JSON.stringify({ email, password, full_name }),
    }),
  login: (email: string, password: string) =>
    request<{ user: User; access_token_expires_in_minutes: number }>('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    }),
  logout: () => request<void>('/auth/logout', { method: 'POST' }),
  me: () => request<User>('/auth/me'),
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

  /** Streams pipeline progress via SSE (fetch + ReadableStream, since
   * EventSource can't send cookies cross-origin reliably with POST bodies). */
  stream: async (
    message: string,
    conversation_id: string | undefined,
    onEvent: (event: string, data: any) => void,
  ) => {
    const response = await fetch(`${API_BASE_URL}/chat/stream`, {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message, conversation_id }),
    })

    if (!response.ok || !response.body) {
      throw new ApiError(response.status, 'Failed to start chat stream')
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
