"use client"

import { useState, useCallback } from "react"
import { Download, FileArchive, RotateCcw, AlertCircle } from "lucide-react"
import { FileDropZone } from "./file-drop-zone"
import {
  StatsDisplay,
  buildCompressStats,
  buildDecompressStats,
} from "./stats-display"
import pako from "pako"

// ============== CCC2 CODEC (inlined) ==============

const MAGIC = new Uint8Array([0x43, 0x43, 0x43, 0x32]) // "CCC2"
const HEADER_SIZE = 9 // 4 magic + 4 length + 1 multiplier

export interface CompressResult {
  data: Uint8Array
  fileName: string
  originalSize: number
  compressedSize: number
  multiplier: number
  ratio: number
}

export interface DecompressResult {
  data: Uint8Array
  fileName: string
  originalSize: number
  compressedSize: number
  multiplier: number
}

function findBestMultiplier(data: Uint8Array): number {
  if (data.length === 0) return 1

  let bestMultiplier = 1
  let bestScore = 0

  for (let m = 1; m <= 255; m++) {
    const transformed = new Uint8Array(data.length)
    for (let i = 0; i < data.length; i++) {
      transformed[i] = (data[i] * m) & 0xff
    }

    const freqs = new Map<number, number>()
    for (const b of transformed) {
      freqs.set(b, (freqs.get(b) || 0) + 1)
    }

    let entropy = 0
    for (const count of freqs.values()) {
      const p = count / data.length
      entropy -= p * Math.log2(p)
    }

    const score = 8 - entropy
    if (score > bestScore) {
      bestScore = score
      bestMultiplier = m
    }
  }

  return bestMultiplier
}

function modInverse(a: number, m: number): number {
  a = ((a % m) + m) % m
  for (let x = 1; x < m; x++) {
    if ((a * x) % m === 1) return x
  }
  return 1
}

function applyMultiplier(data: Uint8Array, multiplier: number): Uint8Array {
  const result = new Uint8Array(data.length)
  for (let i = 0; i < data.length; i++) {
    result[i] = (data[i] * multiplier) & 0xff
  }
  return result
}

function reverseMultiplier(data: Uint8Array, multiplier: number): Uint8Array {
  const inverse = modInverse(multiplier, 256)
  const result = new Uint8Array(data.length)
  for (let i = 0; i < data.length; i++) {
    result[i] = (data[i] * inverse) & 0xff
  }
  return result
}

export function compressToCC(data: Uint8Array, fileName: string): CompressResult {
  const multiplier = findBestMultiplier(data)
  const transformed = applyMultiplier(data, multiplier)
  const compressed = pako.deflate(transformed, { level: 9 })

  const output = new Uint8Array(HEADER_SIZE + compressed.length)
  output.set(MAGIC, 0)

  const lengthView = new DataView(output.buffer)
  lengthView.setUint32(4, data.length, true)
  output[8] = multiplier
  output.set(compressed, HEADER_SIZE)

  return {
    data: output,
    fileName: `${fileName}.cc`,
    originalSize: data.length,
    compressedSize: output.length,
    multiplier,
    ratio: output.length / data.length,
  }
}

export function decompressFromCC(data: Uint8Array, fileName: string): DecompressResult {
  if (!isCCFile(data)) {
    throw new Error("Invalid CCC2 file: missing magic bytes")
  }

  const view = new DataView(data.buffer, data.byteOffset)
  const originalLength = view.getUint32(4, true)
  const multiplier = data[8]

  const compressedPayload = data.slice(HEADER_SIZE)
  const decompressed = pako.inflate(compressedPayload)
  const restored = reverseMultiplier(decompressed, multiplier)

  if (restored.length !== originalLength) {
    throw new Error(
      `Length mismatch: expected ${originalLength}, got ${restored.length}`
    )
  }

  const outputName = fileName.endsWith(".cc")
    ? fileName.slice(0, -3)
    : `${fileName}.restored`

  return {
    data: restored,
    fileName: outputName,
    originalSize: restored.length,
    compressedSize: data.length,
    multiplier,
  }
}

export function isCCFile(data: Uint8Array): boolean {
  if (data.length < HEADER_SIZE) return false
  return (
    data[0] === MAGIC[0] &&
    data[1] === MAGIC[1] &&
    data[2] === MAGIC[2] &&
    data[3] === MAGIC[3]
  )
}

// ============== CONVERTER COMPONENT ==============

type Mode = "compress" | "restore"

export function ConverterPanel() {
  const [mode, setMode] = useState<Mode>("compress")
  const [processing, setProcessing] = useState(false)
  const [fileName, setFileName] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [compressResult, setCompressResult] = useState<
    (CompressResult & { outputName: string }) | null
  >(null)
  const [decompressResult, setDecompressResult] = useState<
    (DecompressResult & { outputName: string }) | null
  >(null)

  const reset = useCallback(() => {
    setFileName(null)
    setError(null)
    setCompressResult(null)
    setDecompressResult(null)
  }, [])

  const switchMode = useCallback(
    (newMode: Mode) => {
      if (newMode !== mode) {
        reset()
        setMode(newMode)
      }
    },
    [mode, reset]
  )

  const handleCompress = useCallback(async (file: File) => {
    setProcessing(true)
    setError(null)
    setCompressResult(null)
    setFileName(file.name)

    try {
      const buffer = await file.arrayBuffer()
      const data = new Uint8Array(buffer)
      const result = compressToCC(data, file.name)
      setCompressResult({ ...result, outputName: result.fileName })
    } catch (err) {
      setError(err instanceof Error ? err.message : "Compression failed")
    } finally {
      setProcessing(false)
    }
  }, [])

  const handleRestore = useCallback(async (file: File) => {
    setProcessing(true)
    setError(null)
    setDecompressResult(null)
    setFileName(file.name)

    try {
      const buffer = await file.arrayBuffer()
      const data = new Uint8Array(buffer)

      if (!isCCFile(data)) {
        throw new Error("Not a valid .cc file (missing CCC2 magic bytes)")
      }

      const result = decompressFromCC(data, file.name)
      setDecompressResult({ ...result, outputName: result.fileName })
    } catch (err) {
      setError(err instanceof Error ? err.message : "Decompression failed")
    } finally {
      setProcessing(false)
    }
  }, [])

  const downloadResult = useCallback(
    (data: Uint8Array, filename: string) => {
      const blob = new Blob([data])
      const url = URL.createObjectURL(blob)
      const a = document.createElement("a")
      a.href = url
      a.download = filename
      a.click()
      URL.revokeObjectURL(url)
    },
    []
  )

  const result = mode === "compress" ? compressResult : decompressResult

  return (
    <div className="flex w-full max-w-xl flex-col gap-6">
      {/* Mode tabs */}
      <div className="flex rounded-lg bg-muted p-1">
        <button
          onClick={() => switchMode("compress")}
          className={`flex flex-1 items-center justify-center gap-2 rounded-md px-4 py-2.5 text-sm font-medium transition-all ${
            mode === "compress"
              ? "bg-background text-foreground shadow-sm"
              : "text-muted-foreground hover:text-foreground"
          }`}
        >
          <FileArchive className="h-4 w-4" />
          Compress to .cc
        </button>
        <button
          onClick={() => switchMode("restore")}
          className={`flex flex-1 items-center justify-center gap-2 rounded-md px-4 py-2.5 text-sm font-medium transition-all ${
            mode === "restore"
              ? "bg-background text-foreground shadow-sm"
              : "text-muted-foreground hover:text-foreground"
          }`}
        >
          <RotateCcw className="h-4 w-4" />
          Restore from .cc
        </button>
      </div>

      {/* Drop zone */}
      <FileDropZone
        onFileSelected={mode === "compress" ? handleCompress : handleRestore}
        accept={mode === "restore" ? ".cc" : undefined}
        label={
          mode === "compress"
            ? "Drop any file to compress"
            : "Drop a .cc file to restore"
        }
        sublabel={
          mode === "compress"
            ? "Produces a lossless .cc archive using CCC2 format"
            : "Recovers the original file from CCC2 compressed data"
        }
        disabled={processing}
      />

      {/* Processing state */}
      {processing && (
        <div className="flex items-center justify-center gap-3 py-4">
          <div className="h-4 w-4 animate-spin rounded-full border-2 border-primary border-t-transparent" />
          <span className="text-sm text-muted-foreground">
            {mode === "compress" ? "Compressing" : "Restoring"} {fileName}...
          </span>
        </div>
      )}

      {/* Error */}
      {error && (
        <div className="animate-fade-in flex items-start gap-3 rounded-lg border border-destructive/30 bg-destructive/10 px-4 py-3">
          <AlertCircle className="mt-0.5 h-4 w-4 shrink-0 text-destructive" />
          <div className="flex flex-col gap-1">
            <span className="text-sm font-medium text-destructive">
              {mode === "compress" ? "Compression" : "Restoration"} failed
            </span>
            <span className="text-xs text-muted-foreground">{error}</span>
          </div>
        </div>
      )}

      {/* Result */}
      {result && !processing && (
        <div className="animate-fade-in flex flex-col gap-4">
          {/* File info */}
          <div className="flex items-center justify-between rounded-lg border border-border bg-card px-4 py-3">
            <div className="flex flex-col gap-0.5">
              <span className="text-xs text-muted-foreground">
                {mode === "compress" ? "Input" : "Restored from"}
              </span>
              <span className="font-mono text-sm text-foreground">
                {fileName}
              </span>
            </div>
            <div className="flex flex-col items-end gap-0.5">
              <span className="text-xs text-muted-foreground">Output</span>
              <span className="font-mono text-sm text-primary">
                {"outputName" in result
                  ? (result as { outputName: string }).outputName
                  : "output"}
              </span>
            </div>
          </div>

          {/* Stats */}
          <StatsDisplay
            stats={
              mode === "compress"
                ? buildCompressStats(compressResult!)
                : buildDecompressStats(decompressResult!)
            }
          />

          {/* Download button */}
          <button
            onClick={() =>
              downloadResult(
                result.data,
                "outputName" in result
                  ? (result as { outputName: string }).outputName
                  : "output"
              )
            }
            className="flex items-center justify-center gap-2 rounded-lg bg-primary px-4 py-3 text-sm font-semibold text-primary-foreground transition-opacity hover:opacity-90 active:opacity-80"
          >
            <Download className="h-4 w-4" />
            Download{" "}
            {"outputName" in result
              ? (result as { outputName: string }).outputName
              : "output"}
          </button>
        </div>
      )}
    </div>
  )
}
