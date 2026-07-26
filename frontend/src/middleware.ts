import { NextResponse, type NextRequest } from 'next/server'

// Must match backend AUTH_COOKIE_NAME
const SESSION_COOKIE = 'automateai_session'

const PROTECTED_PREFIXES = [
  '/chat',
  '/tasks',
  '/apps',
  '/memory',
  '/logs',
  '/settings',
]

const AUTH_PAGES = ['/login', '/signup']

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl

  // ===== DEBUG LOGS =====
  console.log('==============================')
  console.log('Path:', pathname)
  console.log(
    'All Cookies:',
    request.cookies.getAll().map((c) => ({
      name: c.name,
      value: c.value.substring(0, 20) + '...',
    }))
  )

  const sessionCookie = request.cookies.get(SESSION_COOKIE)

  console.log(
    'Session Cookie:',
    sessionCookie ? 'FOUND ✅' : 'NOT FOUND ❌'
  )
  console.log('==============================')
  // ======================

  const hasSession = Boolean(sessionCookie)

  const isProtected = PROTECTED_PREFIXES.some((p) =>
    pathname.startsWith(p)
  )

  const isAuthPage = AUTH_PAGES.some((p) =>
    pathname.startsWith(p)
  )

  if (isProtected && !hasSession) {
    console.log('➡ Redirecting to /login')

    const loginUrl = new URL('/login', request.url)
    loginUrl.searchParams.set('next', pathname)

    return NextResponse.redirect(loginUrl)
  }

  if (isAuthPage && hasSession) {
    console.log('➡ Redirecting to /chat')
    return NextResponse.redirect(new URL('/chat', request.url))
  }

  console.log('➡ Allow request')

  return NextResponse.next()
}

export const config = {
  matcher: [
    '/chat/:path*',
    '/tasks/:path*',
    '/apps/:path*',
    '/memory/:path*',
    '/logs/:path*',
    '/settings/:path*',
    '/login',
    '/signup',
  ],
}