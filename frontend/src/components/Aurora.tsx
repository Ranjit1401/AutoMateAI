'use client'

import { usePathname } from 'next/navigation'
import ColorBends from './ColorBends'

export default function Aurora() {
  const pathname = usePathname()

  // Connected Apps page uses a plain dark background — the orbit
  // visualization is the main visual element there, so Aurora is skipped.
  if (pathname === '/apps') return null

  return (
    <div className="aurora-container">
      <ColorBends
        colors={['#6d28d9', '#a855f7', '#c026d3']}
        transparent
        speed={0.16}
        scale={1.45}
        frequency={1.1}
        warpStrength={1.3}
        mouseInfluence={0.5}
        parallax={0.3}
        noise={0.06}
        iterations={2}
        intensity={1.25}
        bandWidth={5.5}
        rotation={100}
        autoRotate={0.5}
      />
    </div>
  )
}
