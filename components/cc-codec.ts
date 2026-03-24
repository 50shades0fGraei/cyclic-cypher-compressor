/**
 * CCC2 Cyclic Cypher Codec
 * 
 * Encoding approach:
 * 1. Convert input to binary bit stream
 * 2. Overlay 142857 cyclic pattern (each digit maps to bit positions)
 * 3. Count alignment runs left-to-right (where bits match pattern positions)
 * 4. Store only the run-length counts per multiplier (1-6)
 * 
 * Binary format:
 * - 4 bytes: Magic "CCC2"
 * - 4 bytes: Original file length (big-endian)
 * - 4 bytes: Total bit count
 * - 1 byte: Flags (encoding method in lower 2 bits)
 * - 6 x varint: Run count array lengths for each multiplier stream
 * - N bytes: Run-length encoded alignment counts (zlib compressed)
 */

import pako from "pako"

// Magic bytes for CCC2 format
const MAGIC = new Uint8Array([0x43, 0x43, 0x43, 0x32]) // "CCC2"

// The cyclic number - multiplying by 1-6 rotates digits
const CYCLIC_BASE = [1, 4, 2, 8, 5, 7]

// Get rotation for a given multiplier (1-6)
function getCyclicRotation(multiplier: number): number[] {
  // 142857 × n rotates the sequence
  const rotations: Record<number, number[]> = {
    1: [1, 4, 2, 8, 5, 7],
    2: [2, 8, 5, 7, 1, 4],
    3: [4, 2, 8, 5, 7, 1],
    4: [5, 7, 1, 4, 2, 8],
    5: [7, 1, 4, 2, 8, 5],
    6: [8, 5, 7, 1, 4, 2],
  }
  return rotations[multiplier] || CYCLIC_BASE
}

export interface CompressResult {
  data: Uint8Array
  originalSize: number
  compressedSize: number
  multiplier: number
  alignmentCount: number
  ratio: number
  fileName: string
  encodingMethod: "runs" | "positions"
}

export interface DecompressResult {
  data: Uint8Array
  originalSize: number
  compressedSize: number
  multiplier: number
  fileName: string
}

export function formatBytes(bytes: number): string {
  if (bytes === 0) return "0 B"
  const k = 1024
  const sizes = ["B", "KB", "MB", "GB"]
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return `${parseFloat((bytes / Math.pow(k, i)).toFixed(2))} ${sizes[i]}`
}

/**
 * Convert bytes to bit array
 */
function bytesToBits(data: Uint8Array): number[] {
  const bits: number[] = []
  for (let i = 0; i < data.length; i++) {
    for (let b = 7; b >= 0; b--) {
      bits.push((data[i] >> b) & 1)
    }
  }
  return bits
}

/**
 * Convert bit array back to bytes
 */
function bitsToBytes(bits: number[]): Uint8Array {
  const byteCount = Math.ceil(bits.length / 8)
  const result = new Uint8Array(byteCount)
  for (let i = 0; i < bits.length; i++) {
    if (bits[i]) {
      result[Math.floor(i / 8)] |= (1 << (7 - (i % 8)))
    }
  }
  return result
}

/**
 * Check alignment of bit at position against cyclic pattern
 * Returns the cypher digit (1-8) that aligns, or 0 if no alignment
 */
function checkAlignment(bits: number[], position: number, rotation: number[]): number {
  const patternPos = position % 6
  const expectedDigit = rotation[patternPos]
  
  // The digit represents which bit pattern we expect
  // Alignment means the bit value matches the pattern expectation
  // We use digit mod 2 to determine expected bit (odd=1, even=0)
  const expectedBit = expectedDigit % 2
  const actualBit = bits[position] || 0
  
  if (actualBit === expectedBit) {
    return expectedDigit
  }
  return 0
}

/**
 * Count alignment runs for a given multiplier rotation
 * Returns array of [alignCount, misalignCount, alignCount, ...] 
 */
function countAlignmentRuns(bits: number[], rotation: number[]): { runs: number[], alignments: number } {
  const runs: number[] = []
  let currentRun = 0
  let inAlignment = false
  let totalAlignments = 0
  
  for (let i = 0; i < bits.length; i++) {
    const aligned = checkAlignment(bits, i, rotation) !== 0
    
    if (i === 0) {
      inAlignment = aligned
      currentRun = 1
      if (aligned) totalAlignments++
    } else if (aligned === inAlignment) {
      currentRun++
      if (aligned) totalAlignments++
    } else {
      runs.push(currentRun)
      currentRun = 1
      inAlignment = aligned
      if (aligned) totalAlignments++
    }
  }
  
  if (currentRun > 0) {
    runs.push(currentRun)
  }
  
  return { runs, alignments: totalAlignments }
}

/**
 * Encode runs as variable-length integers
 */
function encodeVarints(runs: number[]): Uint8Array {
  const bytes: number[] = []
  for (const value of runs) {
    let v = value
    while (v >= 0x80) {
      bytes.push((v & 0x7f) | 0x80)
      v >>>= 7
    }
    bytes.push(v)
  }
  return new Uint8Array(bytes)
}

/**
 * Decode variable-length integers
 */
function decodeVarints(data: Uint8Array, count: number): { values: number[], bytesRead: number } {
  const values: number[] = []
  let offset = 0
  
  for (let i = 0; i < count && offset < data.length; i++) {
    let value = 0
    let shift = 0
    let byte: number
    
    do {
      byte = data[offset++]
      value |= (byte & 0x7f) << shift
      shift += 7
    } while (byte >= 0x80 && offset < data.length)
    
    values.push(value)
  }
  
  return { values, bytesRead: offset }
}

/**
 * Find the best multiplier (1-6) that maximizes alignments
 */
function findBestMultiplier(bits: number[]): { multiplier: number, runs: number[], alignments: number } {
  let bestMultiplier = 1
  let bestAlignments = 0
  let bestRuns: number[] = []
  
  for (let m = 1; m <= 6; m++) {
    const rotation = getCyclicRotation(m)
    const { runs, alignments } = countAlignmentRuns(bits, rotation)
    
    if (alignments > bestAlignments) {
      bestAlignments = alignments
      bestMultiplier = m
      bestRuns = runs
    }
  }
  
  return { multiplier: bestMultiplier, runs: bestRuns, alignments: bestAlignments }
}

/**
 * Compress data to CCC2 format using cyclic alignment counting
 */
export function compressToCC(data: Uint8Array, fileName: string): CompressResult {
  const originalSize = data.length
  
  // Convert to bits
  const bits = bytesToBits(data)
  const bitCount = bits.length
  
  // Find best multiplier
  const { multiplier, runs, alignments } = findBestMultiplier(bits)
  
  // Encode runs as varints
  const encodedRuns = encodeVarints(runs)
  
  // Also store the starting state (aligned or not)
  const rotation = getCyclicRotation(multiplier)
  const startsAligned = bits.length > 0 && checkAlignment(bits, 0, rotation) !== 0
  
  // Compress the encoded runs
  const compressed = pako.deflate(encodedRuns, { level: 9 })
  
  // Build header
  // Magic (4) + OrigLen (4) + BitCount (4) + Multiplier (1) + Flags (1) + RunCount (4) = 18 bytes
  const headerSize = 18
  const header = new Uint8Array(headerSize)
  
  // Magic
  header.set(MAGIC, 0)
  
  // Original length (big-endian)
  header[4] = (originalSize >> 24) & 0xff
  header[5] = (originalSize >> 16) & 0xff
  header[6] = (originalSize >> 8) & 0xff
  header[7] = originalSize & 0xff
  
  // Bit count (big-endian)
  header[8] = (bitCount >> 24) & 0xff
  header[9] = (bitCount >> 16) & 0xff
  header[10] = (bitCount >> 8) & 0xff
  header[11] = bitCount & 0xff
  
  // Multiplier (1-6)
  header[12] = multiplier
  
  // Flags: bit 0 = starts aligned
  header[13] = startsAligned ? 1 : 0
  
  // Run count (big-endian)
  const runCount = runs.length
  header[14] = (runCount >> 24) & 0xff
  header[15] = (runCount >> 16) & 0xff
  header[16] = (runCount >> 8) & 0xff
  header[17] = runCount & 0xff
  
  // Combine header and compressed data
  const result = new Uint8Array(headerSize + compressed.length)
  result.set(header, 0)
  result.set(compressed, headerSize)
  
  const compressedSize = result.length
  const ratio = compressedSize / originalSize
  
  console.log(`[v0] Compress: ${originalSize}B -> ${compressedSize}B, multiplier=${multiplier}, alignments=${alignments}/${bitCount} (${(alignments/bitCount*100).toFixed(1)}%), runs=${runs.length}`)
  
  return {
    data: result,
    originalSize,
    compressedSize,
    multiplier,
    alignmentCount: alignments,
    ratio,
    fileName: `${fileName}.cc`,
    encodingMethod: "runs",
  }
}

/**
 * Check if data is a valid CCC2 file
 */
export function isCCFile(data: Uint8Array): boolean {
  if (data.length < 18) return false
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
  
  // Read header
  const originalSize = (data[4] << 24) | (data[5] << 16) | (data[6] << 8) | data[7]
  const bitCount = (data[8] << 24) | (data[9] << 16) | (data[10] << 8) | data[11]
  const multiplier = data[12]
  const startsAligned = (data[13] & 1) === 1
  const runCount = (data[14] << 24) | (data[15] << 16) | (data[16] << 8) | data[17]
  
  // Decompress runs
  const compressedPayload = data.slice(18)
  const decompressedRuns = pako.inflate(compressedPayload)
  
  // Decode varints
  const { values: runs } = decodeVarints(decompressedRuns, runCount)
  
  // Rebuild bits from runs
  const rotation = getCyclicRotation(multiplier)
  const bits: number[] = []
  let isAligned = startsAligned
  
  for (const runLength of runs) {
    for (let i = 0; i < runLength; i++) {
      const pos = bits.length
      const patternPos = pos % 6
      const expectedDigit = rotation[patternPos]
      const expectedBit = expectedDigit % 2
      
      if (isAligned) {
        // Aligned: bit matches expected
        bits.push(expectedBit)
      } else {
        // Misaligned: bit is opposite of expected
        bits.push(expectedBit ^ 1)
      }
    }
    isAligned = !isAligned
  }
  
  // Convert bits back to bytes
  const restored = bitsToBytes(bits.slice(0, bitCount))
  
  // Verify length
  if (restored.length !== originalSize) {
    console.log(`[v0] Warning: Size mismatch - expected ${originalSize}, got ${restored.length}`)
  }
  
  // Remove .cc extension
  const outputFileName = fileName.endsWith(".cc")
    ? fileName.slice(0, -3)
    : `${fileName}.restored`
  
  console.log(`[v0] Decompress: ${data.length}B -> ${restored.length}B, multiplier=${multiplier}`)
  
  return {
    data: restored,
    originalSize: restored.length,
    compressedSize: data.length,
    multiplier,
    fileName: outputFileName,
  }
}
