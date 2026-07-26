import { NextResponse, type NextRequest } from 'next/server'

// Must match backend AUTH_COOKIE_NAME (app/core/config.py). Checking for the
// cookie's presence here is a fast, no-flash redirect; the pages themselves
// still verify the session is actually valid via AuthContext (a present but
// expired/tampered cookie is rejected server-side on the first API call).
const SESSION_COOKIE = 'automateai_session'

const PROTECTED_PREFIXES = ['/chat', '/tasks', '/apps', '/memory', '/logs', '/settings']
const AUTH_PAGES = ['/login', '/signup']

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl
  const hasSession = Boolean(request.cookies.get(SESSION_COOKIE))

  const isProtected = PROTECTED_PREFIXES.some((p) => pathname.startsWith(p))
  const isAuthPage = AUTH_PAGES.some((p) => pathname.startsWith(p))

  if (isProtected && !hasSession) {
    const loginUrl = new URL('/login', request.url)
    loginUrl.searchParams.set('next', pathname)
    return NextResponse.redirect(loginUrl)
  }

  if (isAuthPage && hasSession) {
    return NextResponse.redirect(new URL('/chat', request.url))
  }

  return NextResponse.next()
}

export const config = {
  matcher: ['/chat/:path*', '/tasks/:path*', '/apps/:path*', '/memory/:path*', '/logs/:path*', '/settings/:path*', '/login', '/signup'],
}
