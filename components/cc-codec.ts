/**
 * CCC2 Cyclic Cypher Codec - SIMPLE VERSION
 * 
 * The 142857 pattern rotates when multiplied by 1-6:
 * x1 = 142857, x2 = 285714, x3 = 428571, x4 = 571428, x5 = 714285, x6 = 857142
 * 
 * Encoding:
 * 1. Convert data to binary
 * 2. Check each bit against cyclic pattern overlay
 * 3. Store: [magic][origLen][multiplier][alignment counts L-R]
 * 
 * That's it. No zlib. Just counts.
 */

// Magic bytes
const MAGIC = new Uint8Array([0x43, 0x43, 0x43, 0x32]) // "CCC2"

// Cyclic rotations for multipliers 1-6
const ROTATIONS: Record<number, number[]> = {
  1: [1, 4, 2, 8, 5, 7],
  2: [2, 8, 5, 7, 1, 4],
  3: [4, 2, 8, 5, 7, 1],
  4: [5, 7, 1, 4, 2, 8],
  5: [7, 1, 4, 2, 8, 5],
  6: [8, 5, 7, 1, 4, 2],
}

export interface CompressResult {
  data: Uint8Array
  originalSize: number
  compressedSize: number
  multiplier: number
  alignmentCount: number
  totalBits: number
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

export function formatBytes(bytes: number): string {
  if (bytes === 0) return "0 B"
  const k = 1024
  const sizes = ["B", "KB", "MB", "GB"]
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return `${parseFloat((bytes / Math.pow(k, i)).toFixed(2))} ${sizes[i]}`
}

// Convert bytes to bits (left to right, MSB first)
function toBits(data: Uint8Array): number[] {
  const bits: number[] = []
  for (const byte of data) {
    for (let i = 7; i >= 0; i--) {
      bits.push((byte >> i) & 1)
    }
  }
  return bits
}

// Convert bits back to bytes
function toBytes(bits: number[]): Uint8Array {
  const bytes = new Uint8Array(Math.ceil(bits.length / 8))
  for (let i = 0; i < bits.length; i++) {
    if (bits[i]) {
      bytes[Math.floor(i / 8)] |= (1 << (7 - (i % 8)))
    }
  }
  return bytes
}

// Check if bit aligns with cyclic pattern at position
// Alignment = bit matches (digit % 2)
function isAligned(bit: number, position: number, rotation: number[]): boolean {
  const digit = rotation[position % 6]
  const expected = digit % 2
  return bit === expected
}

// Count runs: returns [count1, count2, ...] alternating aligned/misaligned
// First value is always an aligned run (can be 0)
function countRuns(bits: number[], rotation: number[]): { runs: number[], alignments: number, startsAligned: boolean } {
  if (bits.length === 0) return { runs: [], alignments: 0, startsAligned: true }
  
  const startsAligned = isAligned(bits[0], 0, rotation)
  const runs: number[] = []
  let alignments = 0
  let currentCount = 0
  let currentlyAligned = startsAligned
  
  for (let i = 0; i < bits.length; i++) {
    const aligned = isAligned(bits[i], i, rotation)
    
    if (aligned === currentlyAligned) {
      currentCount++
      if (aligned) alignments++
    } else {
      runs.push(currentCount)
      currentCount = 1
      currentlyAligned = aligned
      if (aligned) alignments++
    }
  }
  runs.push(currentCount)
  
  return { runs, alignments, startsAligned }
}

// Find best multiplier - most alignments wins
function findBest(bits: number[]): { multiplier: number, runs: number[], alignments: number, startsAligned: boolean } {
  let best = { multiplier: 1, runs: [] as number[], alignments: 0, startsAligned: true }
  
  for (let m = 1; m <= 6; m++) {
    const result = countRuns(bits, ROTATIONS[m])
    if (result.alignments > best.alignments) {
      best = { multiplier: m, ...result }
    }
  }
  
  return best
}

// Encode number as varint (7 bits per byte, high bit = more follows)
function toVarint(n: number): number[] {
  const bytes: number[] = []
  do {
    let byte = n & 0x7f
    n >>>= 7
    if (n > 0) byte |= 0x80
    bytes.push(byte)
  } while (n > 0)
  return bytes
}

// Decode varint from array at offset, returns [value, newOffset]
function fromVarint(data: Uint8Array, offset: number): [number, number] {
  let value = 0
  let shift = 0
  let i = offset
  while (i < data.length) {
    const byte = data[i++]
    value |= (byte & 0x7f) << shift
    if ((byte & 0x80) === 0) break
    shift += 7
  }
  return [value, i]
}

/**
 * Compress to .cc format
 */
export function compressToCC(data: Uint8Array, fileName: string): CompressResult {
  const bits = toBits(data)
  const { multiplier, runs, alignments, startsAligned } = findBest(bits)
  
  // Encode runs as varints
  const runBytes: number[] = []
  for (const run of runs) {
    runBytes.push(...toVarint(run))
  }
  
  // Build output:
  // [MAGIC 4B][origLen 4B][bitCount 4B][multiplier 1B][startsAligned 1B][runCount 4B][runs...]
  const headerSize = 18
  const output = new Uint8Array(headerSize + runBytes.length)
  
  // Magic
  output.set(MAGIC, 0)
  
  // Original byte length
  output[4] = (data.length >> 24) & 0xff
  output[5] = (data.length >> 16) & 0xff
  output[6] = (data.length >> 8) & 0xff
  output[7] = data.length & 0xff
  
  // Bit count
  output[8] = (bits.length >> 24) & 0xff
  output[9] = (bits.length >> 16) & 0xff
  output[10] = (bits.length >> 8) & 0xff
  output[11] = bits.length & 0xff
  
  // Multiplier
  output[12] = multiplier
  
  // Starts aligned flag
  output[13] = startsAligned ? 1 : 0
  
  // Run count
  output[14] = (runs.length >> 24) & 0xff
  output[15] = (runs.length >> 16) & 0xff
  output[16] = (runs.length >> 8) & 0xff
  output[17] = runs.length & 0xff
  
  // Runs as varints
  output.set(runBytes, headerSize)
  
  console.log(`[v0] Compress: ${data.length}B -> ${output.length}B`)
  console.log(`[v0] Multiplier: x${multiplier}, Alignments: ${alignments}/${bits.length} (${(alignments/bits.length*100).toFixed(1)}%)`)
  console.log(`[v0] Runs: ${runs.length}, StartsAligned: ${startsAligned}`)
  
  return {
    data: output,
    originalSize: data.length,
    compressedSize: output.length,
    multiplier,
    alignmentCount: alignments,
    totalBits: bits.length,
    ratio: output.length / data.length,
    fileName: `${fileName}.cc`,
  }
}

/**
 * Check if valid .cc file
 */
export function isCCFile(data: Uint8Array): boolean {
  return data.length >= 18 &&
    data[0] === 0x43 && data[1] === 0x43 && data[2] === 0x43 && data[3] === 0x32
}

/**
 * Decompress from .cc format
 */
export function decompressFromCC(data: Uint8Array, fileName: string): DecompressResult {
  if (!isCCFile(data)) throw new Error("Not a valid .cc file")
  
  // Read header
  const origLen = (data[4] << 24) | (data[5] << 16) | (data[6] << 8) | data[7]
  const bitCount = (data[8] << 24) | (data[9] << 16) | (data[10] << 8) | data[11]
  const multiplier = data[12]
  const startsAligned = data[13] === 1
  const runCount = (data[14] << 24) | (data[15] << 16) | (data[16] << 8) | data[17]
  
  // Read runs
  const runs: number[] = []
  let offset = 18
  for (let i = 0; i < runCount; i++) {
    const [value, newOffset] = fromVarint(data, offset)
    runs.push(value)
    offset = newOffset
  }
  
  // Rebuild bits from runs
  const rotation = ROTATIONS[multiplier]
  const bits: number[] = []
  let aligned = startsAligned
  
  for (const count of runs) {
    for (let i = 0; i < count; i++) {
      const pos = bits.length
      const digit = rotation[pos % 6]
      const expected = digit % 2
      bits.push(aligned ? expected : (expected ^ 1))
    }
    aligned = !aligned
  }
  
  // Convert to bytes
  const result = toBytes(bits.slice(0, bitCount))
  
  // Trim to original length
  const output = result.slice(0, origLen)
  
  console.log(`[v0] Decompress: ${data.length}B -> ${output.length}B`)
  
  const outName = fileName.endsWith(".cc") ? fileName.slice(0, -3) : `${fileName}.restored`
  
  return {
    data: output,
    originalSize: output.length,
    compressedSize: data.length,
    multiplier,
    fileName: outName,
  }
}
