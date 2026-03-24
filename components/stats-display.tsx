"use client"

import { formatBytes } from "./cc-codec"

interface Stat {
  label: string
  value: string
}

interface StatsDisplayProps {
  stats: Stat[]
}

export function StatsDisplay({ stats }: StatsDisplayProps) {
  return (
    <div className="grid grid-cols-2 gap-3 sm:grid-cols-3">
      {stats.map((stat) => (
        <div
          key={stat.label}
          className="flex flex-col gap-1 rounded-md bg-muted px-3 py-2.5"
        >
          <span className="text-[11px] font-medium uppercase tracking-wider text-muted-foreground">
            {stat.label}
          </span>
          <span className="font-mono text-sm font-semibold text-foreground">
            {stat.value}
          </span>
        </div>
      ))}
    </div>
  )
}

export function buildCompressStats(result: {
  originalSize: number
  compressedSize: number
  multiplier: number
  alignmentCount: number
  totalBits: number
  ratio: number
}): Stat[] {
  const ratioPercent = (result.ratio * 100).toFixed(1)
  const alignPct = result.totalBits > 0 
    ? ((result.alignmentCount / result.totalBits) * 100).toFixed(1)
    : "0"
  return [
    { label: "Original", value: formatBytes(result.originalSize) },
    { label: "Compressed", value: formatBytes(result.compressedSize) },
    { label: "Ratio", value: `${ratioPercent}%` },
    { label: "Multiplier", value: `x${result.multiplier}` },
    { label: "Alignments", value: `${alignPct}%` },
    { label: "Total Bits", value: result.totalBits.toLocaleString() },
  ]
}

export function buildDecompressStats(result: {
  originalSize: number
  compressedSize: number
  multiplier: number
}): Stat[] {
  return [
    { label: "Compressed", value: formatBytes(result.compressedSize) },
    { label: "Recovered", value: formatBytes(result.originalSize) },
    { label: "Multiplier", value: `x${result.multiplier}` },
    { label: "Verified", value: "Yes" },
  ]
}
