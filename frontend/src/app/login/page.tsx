'use client'

import { Suspense, useState, type FormEvent } from 'react'
import Link from 'next/link'
import { useRouter, useSearchParams } from 'next/navigation'
import { LogIn } from 'lucide-react'
import { useAuth } from '@/contexts/AuthContext'
import { ApiError } from '@/lib/api'

function LoginForm() {
  const router = useRouter()
  const searchParams = useSearchParams()
  const { login } = useAuth()

  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    setError(null)
    setLoading(true)
    try {
      await login(email, password)
      router.push(searchParams.get('next') || '/chat')
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Something went wrong. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="glass"
      style={{ width: '100%', maxWidth: 380, padding: 32, borderRadius: 20 }}
    >
      <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 24 }}>
        <div
          style={{
            width: 36,
            height: 36,
            borderRadius: 10,
            background: 'linear-gradient(135deg, rgba(168,85,247,0.3), rgba(99,102,241,0.3))',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
          }}
        >
          <LogIn size={17} color="white" />
        </div>
        <h1 style={{ fontSize: 19, fontWeight: 600, color: 'white', margin: 0 }}>Welcome back</h1>
      </div>

      <Field label="Email" type="email" value={email} onChange={setEmail} placeholder="you@example.com" required />
      <Field label="Password" type="password" value={password} onChange={setPassword} placeholder="••••••••" required />

      {error && <div style={{ color: '#f87171', fontSize: 13, marginBottom: 14, marginTop: -6 }}>{error}</div>}

      <button
        type="submit"
        disabled={loading}
        style={{
          width: '100%',
          padding: '11px 0',
          borderRadius: 10,
          border: 'none',
          background: 'linear-gradient(135deg, #a855f7, #6366f1)',
          color: 'white',
          fontSize: 14,
          fontWeight: 600,
          cursor: loading ? 'default' : 'pointer',
          opacity: loading ? 0.7 : 1,
          marginTop: 4,
        }}
      >
        {loading ? 'Signing in…' : 'Sign in'}
      </button>

      <p style={{ marginTop: 18, fontSize: 13, color: 'rgba(255,255,255,0.55)', textAlign: 'center' }}>
        Don&apos;t have an account?{' '}
        <Link href="/signup" style={{ color: '#c4b5fd' }}>
          Sign up
        </Link>
      </p>
    </form>
  )
}

export default function LoginPage() {
  return (
    <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: 24 }}>
      <Suspense fallback={null}>
        <LoginForm />
      </Suspense>
    </div>
  )
}

function Field({
  label,
  type,
  value,
  onChange,
  placeholder,
  required,
}: {
  label: string
  type: string
  value: string
  onChange: (v: string) => void
  placeholder: string
  required?: boolean
}) {
  return (
    <div style={{ marginBottom: 16 }}>
      <label style={{ display: 'block', fontSize: 12, color: 'rgba(255,255,255,0.6)', marginBottom: 6 }}>{label}</label>
      <input
        type={type}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        required={required}
        style={{
          width: '100%',
          padding: '10px 12px',
          borderRadius: 10,
          border: '1px solid rgba(255,255,255,0.1)',
          background: 'rgba(255,255,255,0.04)',
          color: 'white',
          fontSize: 14,
          fontFamily: 'inherit',
          outline: 'none',
        }}
      />
    </div>
  )
}
