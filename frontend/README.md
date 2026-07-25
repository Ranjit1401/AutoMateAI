# AutoMateAI

Next.js + TypeScript + Tailwind CSS v4 conversion of the AutoMateAI Figma Make export.

## Stack

- [Next.js 15](https://nextjs.org) (App Router)
- TypeScript
- Tailwind CSS v4
- [lucide-react](https://lucide.dev) for icons

## Getting started

```bash
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

## Structure

The original single-page app (which used local React state to switch between
"pages") has been converted into real routes using the Next.js App Router:

| Original page      | Route         |
| ------------------- | ------------- |
| `Home`               | `/`           |
| `Chat`                | `/chat`       |
| `Tasks`               | `/tasks`      |
| `Memory`              | `/memory`     |
| `ConnectedApps`      | `/apps`       |
| `Logs`                | `/logs`       |
| `Settings`           | `/settings`   |

- `src/app/layout.tsx` — root layout, loads fonts (`next/font/google`), and
  renders the shared `Aurora` background and `Nav` bar around every page.
- `src/components/Nav.tsx` — top navigation bar, now using `next/link` and
  `usePathname()` for active-route highlighting instead of local state.
- `src/components/Aurora.tsx` — animated background blobs (unchanged).
- `src/app/globals.css` — Tailwind v4 theme tokens + all custom animations /
  utility classes from the original `index.css`.

All page components are marked `'use client'` since they rely on local
component state (`useState`, `useRef`, etc.) from the original design.

## Build

```bash
npm run build
npm start
```
