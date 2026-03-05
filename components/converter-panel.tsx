"use client"

import { useState, useCallback } from "react"
import { Download, FileArchive, RotateCcw, AlertCircle } from "lucide-react"
import { FileDropZone } from "./file-drop-zone"
import {
  StatsDisplay,
  buildCompressStats,
  buildDecompressStats,
} from "./stats-display"
import {
  compressToCC,
  decompressFromCC,
  isCCFile,
  type CompressResult,
  type DecompressResult,
} from "@/lib/cc-codec"

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
      const result = compressToCC(data)
      setCompressResult({ ...result, outputName: `${file.name}.cc` })
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
        throw new Error(
          "Not a valid .cc file (missing CCC2 magic bytes)"
        )
      }

      const result = decompressFromCC(data)
      // Strip .cc extension for the output name
      const outputName = file.name.endsWith(".cc")
        ? file.name.slice(0, -3)
        : `${file.name}.restored`
      setDecompressResult({ ...result, outputName })
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
      <div className="flex rounded-lg bg-[hsl(var(--muted))] p-1">
        <button
          onClick={() => switchMode("compress")}
          className={`flex flex-1 items-center justify-center gap-2 rounded-md px-4 py-2.5 text-sm font-medium transition-all ${
            mode === "compress"
              ? "bg-[hsl(var(--background))] text-[hsl(var(--foreground))] shadow-sm"
              : "text-[hsl(var(--muted-foreground))] hover:text-[hsl(var(--foreground))]"
          }`}
        >
          <FileArchive className="h-4 w-4" />
          Compress to .cc
        </button>
        <button
          onClick={() => switchMode("restore")}
          className={`flex flex-1 items-center justify-center gap-2 rounded-md px-4 py-2.5 text-sm font-medium transition-all ${
            mode === "restore"
              ? "bg-[hsl(var(--background))] text-[hsl(var(--foreground))] shadow-sm"
              : "text-[hsl(var(--muted-foreground))] hover:text-[hsl(var(--foreground))]"
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
          <div className="h-4 w-4 animate-spin rounded-full border-2 border-[hsl(var(--primary))] border-t-transparent" />
          <span className="text-sm text-[hsl(var(--muted-foreground))]">
            {mode === "compress" ? "Compressing" : "Restoring"} {fileName}...
          </span>
        </div>
      )}

      {/* Error */}
      {error && (
        <div className="animate-fade-in flex items-start gap-3 rounded-lg border border-[hsl(var(--destructive)/0.3)] bg-[hsl(var(--destructive)/0.08)] px-4 py-3">
          <AlertCircle className="mt-0.5 h-4 w-4 shrink-0 text-[hsl(var(--destructive))]" />
          <div className="flex flex-col gap-1">
            <span className="text-sm font-medium text-[hsl(var(--destructive))]">
              {mode === "compress" ? "Compression" : "Restoration"} failed
            </span>
            <span className="text-xs text-[hsl(var(--muted-foreground))]">
              {error}
            </span>
          </div>
        </div>
      )}

      {/* Result */}
      {result && !processing && (
        <div className="animate-fade-in flex flex-col gap-4">
          {/* File info */}
          <div className="flex items-center justify-between rounded-lg bg-[hsl(var(--card))] border border-[hsl(var(--border))] px-4 py-3">
            <div className="flex flex-col gap-0.5">
              <span className="text-xs text-[hsl(var(--muted-foreground))]">
                {mode === "compress" ? "Input" : "Restored from"}
              </span>
              <span className="font-mono text-sm text-[hsl(var(--foreground))]">
                {fileName}
              </span>
            </div>
            <div className="flex flex-col items-end gap-0.5">
              <span className="text-xs text-[hsl(var(--muted-foreground))]">
                Output
              </span>
              <span className="font-mono text-sm text-[hsl(var(--primary))]">
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
            className="flex items-center justify-center gap-2 rounded-lg bg-[hsl(var(--primary))] px-4 py-3 text-sm font-semibold text-[hsl(var(--primary-foreground))] transition-opacity hover:opacity-90 active:opacity-80"
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
