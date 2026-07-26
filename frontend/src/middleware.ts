import { NextResponse, type NextRequest } from 'next/server'

// The middleware does a fast, optimistic check for the httpOnly session cookie
// set by the backend.  In cross-origin production deployments (Vercel → Render)
// the cookie may be blocked by the browser's third-party cookie policy, so the
// frontend falls back to Bearer token auth stored in localStorage.
//
// localStorage is NOT accessible in middleware (it runs in the Edge runtime).
// We therefore treat the cookie absence as "possibly not authenticated, let the
// page decide" rather than "definitely logged out" — the AuthContext on the
// client re-validates via /auth/me with the Bearer header and redirects to
// /login if the session is actually invalid.
//
// The ONLY hard redirect from middleware is when we're confident the user is
// already authenticated (cookie IS present) and they try to visit login/signup
// — we send them to /chat to avoid a flash of the login page.

const SESSION_COOKIE = 'automateai_session'
const AUTH_PAGES = ['/login', '/signup']

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl
  const hasSessionCookie = Boolean(request.cookies.get(SESSION_COOKIE))
  const isAuthPage = AUTH_PAGES.some((p) => pathname.startsWith(p))

  // If the user has a valid cookie AND is on an auth page, redirect to /chat.
  // (This prevents a flash of the login form for already-logged-in users.)
  if (isAuthPage && hasSessionCookie) {
    return NextResponse.redirect(new URL('/chat', request.url))
  }

  // For protected routes: we do NOT block here because the cookie may be
  // absent even for authenticated users (Bearer-only cross-origin flow).
  // Each protected page's AuthContext will call /auth/me and redirect to
  // /login client-side if the session is truly invalid.

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
