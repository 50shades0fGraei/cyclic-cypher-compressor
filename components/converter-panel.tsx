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
} from "./cc-codec"

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
                {result.outputName}
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
            onClick={() => downloadResult(result.data, result.outputName)}
            className="flex items-center justify-center gap-2 rounded-lg bg-primary px-4 py-3 text-sm font-semibold text-primary-foreground transition-opacity hover:opacity-90 active:opacity-80"
          >
            <Download className="h-4 w-4" />
            Download {result.outputName}
          </button>
        </div>
      )}
    </div>
  )
}
