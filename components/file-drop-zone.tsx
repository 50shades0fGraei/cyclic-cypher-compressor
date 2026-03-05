"use client"

import { useCallback, useState, useRef } from "react"
import { Upload } from "lucide-react"
import { cn } from "@/lib/utils"

interface FileDropZoneProps {
  onFileSelected: (file: File) => void
  accept?: string
  label: string
  sublabel: string
  disabled?: boolean
}

export function FileDropZone({
  onFileSelected,
  accept,
  label,
  sublabel,
  disabled = false,
}: FileDropZoneProps) {
  const [isDragOver, setIsDragOver] = useState(false)
  const inputRef = useRef<HTMLInputElement>(null)

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault()
      setIsDragOver(false)
      if (disabled) return
      const file = e.dataTransfer.files?.[0]
      if (file) onFileSelected(file)
    },
    [onFileSelected, disabled]
  )

  const handleDragOver = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault()
      if (!disabled) setIsDragOver(true)
    },
    [disabled]
  )

  const handleDragLeave = useCallback(() => {
    setIsDragOver(false)
  }, [])

  const handleClick = () => {
    if (!disabled) inputRef.current?.click()
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) onFileSelected(file)
    // Reset so the same file can be selected again
    e.target.value = ""
  }

  return (
    <button
      type="button"
      onClick={handleClick}
      onDrop={handleDrop}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      disabled={disabled}
      className={cn(
        "relative flex w-full cursor-pointer flex-col items-center justify-center gap-3 rounded-lg border-2 border-dashed px-6 py-12 transition-all",
        "hover:border-[hsl(var(--primary))] hover:bg-[hsl(var(--primary)/0.04)]",
        "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[hsl(var(--ring))]",
        isDragOver &&
          "border-[hsl(var(--primary))] bg-[hsl(var(--primary)/0.08)]",
        !isDragOver && "border-[hsl(var(--border))]",
        disabled && "pointer-events-none opacity-50"
      )}
    >
      <div
        className={cn(
          "flex h-12 w-12 items-center justify-center rounded-full transition-colors",
          isDragOver
            ? "bg-[hsl(var(--primary)/0.15)] text-[hsl(var(--primary))]"
            : "bg-[hsl(var(--muted))] text-[hsl(var(--muted-foreground))]"
        )}
      >
        <Upload className="h-5 w-5" />
      </div>
      <div className="flex flex-col items-center gap-1">
        <span className="text-sm font-medium text-[hsl(var(--foreground))]">
          {label}
        </span>
        <span className="text-xs text-[hsl(var(--muted-foreground))]">
          {sublabel}
        </span>
      </div>
      <input
        ref={inputRef}
        type="file"
        accept={accept}
        onChange={handleChange}
        className="sr-only"
        tabIndex={-1}
        aria-hidden="true"
      />
    </button>
  )
}
