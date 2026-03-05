"use client"

import { formatBytes } from "@/lib/cc-codec"

interface Stat {
  label: string
  value: string
}

interface StatsDisplayProps {
  stats: Stat[]
}

export function StatsDisplay({ stats }: StatsDisplayProps) {
  return (
    <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
      {stats.map((stat) => (
        <div
          key={stat.label}
          className="flex flex-col gap-1 rounded-md bg-[hsl(var(--muted))] px-3 py-2.5"
        >
          <span className="text-[11px] font-medium uppercase tracking-wider text-[hsl(var(--muted-foreground))]">
            {stat.label}
          </span>
          <span className="font-mono text-sm font-semibold text-[hsl(var(--foreground))]">
            {stat.value}
          </span>
        </div>
      ))}
    </div>
  )
}

export function buildCompressStats(result: {
  originalLength: number
  compressedLength: number
  multiplier: number
  compressionRatio: number
}): Stat[] {
  return [
    { label: "Original", value: formatBytes(result.originalLength) },
    { label: "Compressed", value: formatBytes(result.compressedLength) },
    { label: "Ratio", value: `${result.compressionRatio.toFixed(1)}%` },
    { label: "Multiplier", value: `x${result.multiplier}` },
  ]
}

export function buildDecompressStats(result: {
  originalLength: number
  compressedLength: number
  multiplier: number
  recoveredLength: number
}): Stat[] {
  return [
    { label: "Compressed", value: formatBytes(result.compressedLength) },
    { label: "Recovered", value: formatBytes(result.recoveredLength) },
    { label: "Multiplier", value: `x${result.multiplier}` },
    {
      label: "Verified",
      value:
        result.recoveredLength === result.originalLength ? "Yes" : "Mismatch",
    },
  ]
}
