/**
 * CCC2 Binary Codec - TypeScript port of cyclic_hybrid.py
 * 
 * Binary format:
 * - 4 bytes: Magic "CCC2"
 * - 4 bytes: Original file length (big-endian)
 * - 1 byte: Cyclic multiplier used
 * - N bytes: zlib-compressed data
 */

import pako from "pako"

// Magic bytes for CCC2 format
const MAGIC = new Uint8Array([0x43, 0x43, 0x43, 0x32]) // "CCC2"

export interface CompressResult {
  data: Uint8Array
  originalSize: number
  compressedSize: number
  multiplier: number
  ratio: number
  fileName: string
}

export interface DecompressResult {
  data: Uint8Array
  originalSize: number
  compressedSize: number
  multiplier: number
  fileName: string
}

/**
 * Format bytes to human readable string
 */
export function formatBytes(bytes: number): string {
  if (bytes === 0) return "0 B"
  const k = 1024
  const sizes = ["B", "KB", "MB", "GB"]
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return `${parseFloat((bytes / Math.pow(k, i)).toFixed(2))} ${sizes[i]}`
}

/**
 * Apply cyclic multiplier transformation
 */
function applyCyclicMultiplier(data: Uint8Array, multiplier: number): Uint8Array {
  const result = new Uint8Array(data.length)
  for (let i = 0; i < data.length; i++) {
    result[i] = (data[i] * multiplier) & 0xff
  }
  return result
}

/**
 * Reverse cyclic multiplier transformation using modular inverse
 */
function reverseCyclicMultiplier(data: Uint8Array, multiplier: number): Uint8Array {
  // Find modular inverse of multiplier mod 256
  const inverse = modularInverse(multiplier, 256)
  const result = new Uint8Array(data.length)
  for (let i = 0; i < data.length; i++) {
    result[i] = (data[i] * inverse) & 0xff
  }
  return result
}

/**
 * Extended Euclidean Algorithm to find modular inverse
 */
function modularInverse(a: number, m: number): number {
  let [old_r, r] = [a, m]
  let [old_s, s] = [1, 0]
  
  while (r !== 0) {
    const quotient = Math.floor(old_r / r)
    ;[old_r, r] = [r, old_r - quotient * r]
    ;[old_s, s] = [s, old_s - quotient * s]
  }
  
  return ((old_s % m) + m) % m
}

/**
 * Find optimal cyclic multiplier for compression
 * Tests odd multipliers (coprime to 256) and picks the one with best compression
 */
function findOptimalMultiplier(data: Uint8Array): number {
  let bestMultiplier = 1
  let bestSize = Infinity
  
  // Test odd multipliers from 1 to 255 (coprime to 256)
  for (let mult = 1; mult < 256; mult += 2) {
    const transformed = applyCyclicMultiplier(data, mult)
    try {
      const compressed = pako.deflate(transformed, { level: 9 })
      if (compressed.length < bestSize) {
        bestSize = compressed.length
        bestMultiplier = mult
      }
    } catch {
      // Skip if compression fails
    }
  }
  
  return bestMultiplier
}

/**
 * Compress data to CCC2 format
 */
export function compressToCC(data: Uint8Array, fileName: string): CompressResult {
  const originalSize = data.length
  
  // Find optimal multiplier
  const multiplier = findOptimalMultiplier(data)
  
  // Apply transformation and compress
  const transformed = applyCyclicMultiplier(data, multiplier)
  const compressed = pako.deflate(transformed, { level: 9 })
  
  // Build CCC2 binary format
  const header = new Uint8Array(9)
  header.set(MAGIC, 0)
  
  // Write original length as 4-byte big-endian
  header[4] = (originalSize >> 24) & 0xff
  header[5] = (originalSize >> 16) & 0xff
  header[6] = (originalSize >> 8) & 0xff
  header[7] = originalSize & 0xff
  
  // Write multiplier
  header[8] = multiplier
  
  // Combine header and compressed data
  const result = new Uint8Array(header.length + compressed.length)
  result.set(header, 0)
  result.set(compressed, header.length)
  
  const compressedSize = result.length
  const ratio = compressedSize / originalSize
  
  return {
    data: result,
    originalSize,
    compressedSize,
    multiplier,
    ratio,
    fileName: `${fileName}.cc`,
  }
}

/**
 * Check if data is a valid CCC2 file
 */
export function isCCFile(data: Uint8Array): boolean {
  if (data.length < 9) return false
  return (
    data[0] === MAGIC[0] &&
    data[1] === MAGIC[1] &&
    data[2] === MAGIC[2] &&
    data[3] === MAGIC[3]
  )
}

/**
 * Decompress CCC2 format back to original data
 */
export function decompressFromCC(data: Uint8Array, fileName: string): DecompressResult {
  if (!isCCFile(data)) {
    throw new Error("Invalid CCC2 file: missing magic bytes")
  }
  
  // Read original length (4-byte big-endian)
  const originalSize =
    (data[4] << 24) | (data[5] << 16) | (data[6] << 8) | data[7]
  
  // Read multiplier
  const multiplier = data[8]
  
  // Extract compressed payload
  const compressedPayload = data.slice(9)
  
  // Decompress
  const decompressed = pako.inflate(compressedPayload)
  
  // Reverse the cyclic transformation
  const restored = reverseCyclicMultiplier(decompressed, multiplier)
  
  // Verify length
  if (restored.length !== originalSize) {
    throw new Error(
      `Size mismatch: expected ${originalSize}, got ${restored.length}`
    )
  }
  
  // Remove .cc extension if present
  const outputFileName = fileName.endsWith(".cc")
    ? fileName.slice(0, -3)
    : `${fileName}.restored`
  
  return {
    data: restored,
    originalSize,
    compressedSize: data.length,
    multiplier,
    fileName: outputFileName,
  }
}
