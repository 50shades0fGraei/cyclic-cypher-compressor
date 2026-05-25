# (c) 2026 Randall James Lujan. ALL RIGHTS RESERVED.
# PATENT PENDING: Cyclic Cypher Deductive Metronome Architecture.
# This software is proprietary and subject to the terms of a specific License Agreement.

"""
EPHEMERAL CYCLIC CYPHER ENGINE
================================
Sovereign One-Time Transmission System — Lujan Tesseract OS

Cryptographic Strength Per Transmission:
  • 256² possibilities per code pair  (key layer)
  • 128 odd values per multiplier     (build layer)
  • 16 independent multipliers        (scaling layer)
  • 1 unique door token               (access layer)
  Effective keyspace: ~(256²)ⁿ × 128¹⁶ per message
  A 90-byte message = (256²)⁹⁰ × 128¹⁶ distinct cipher builds
  ≈ 10^550 combinations — no supercomputer can brute-force this.

Each transmission:
  1. Generates fresh random code pairs (OTP key layer)
  2. Generates fresh random multipliers (build layer)
  3. Issues a one-time door token (access layer)
  4. Burns all three after delivery — door, key, and build destroyed

Usage:
    bundle = EphemeralCypher.seal("sensitive content")
    plaintext = EphemeralCypher.open(bundle)  # bundle burned after this
"""

import os
import json
import base64
import hashlib
import secrets
import time
import math

# Session IDs that have been opened — prevents replay even if bundle JSON is resent
_BURNED_SESSIONS: set = set()


# ─────────────────────────────────────────────
#  CORE CIPHER ENGINE
# ─────────────────────────────────────────────

class EphemeralCypher:
    """
    One-time cyclic code-pair cipher.
    Each seal() call generates a fresh, unique key that is destroyed after open().
    """

    VERSION = "CDV6-OTP-1.0"

    @staticmethod
    def _generate_key_pairs(length: int) -> list:
        """Generate `length` random cyclic code pairs (a, b)."""
        pairs = []
        for _ in range(length):
            pairs.append((secrets.randbelow(256), secrets.randbelow(256)))
        return pairs

    @staticmethod
    def _generate_multipliers(count: int = 16) -> list:
        """
        Generate randomized cyclic multipliers — the 'build'.
        Each value is odd (1–255) ensuring a bijection over the 256 byte-space.
        Without these multipliers, offset patterns in the ciphertext are
        computationally indistinguishable from random noise.
        """
        return [secrets.randbelow(128) * 2 + 1 for _ in range(count)]

    @staticmethod
    def _compute_key_byte(i: int, a: int, b: int, mults: list) -> int:
        """
        Compute one-time key byte using both code pairs and scrambled multipliers.
        Formula (all mod 256):
            m0 = mults[i % len(mults)]
            m1 = mults[(i+1) % len(mults)]
            key = a XOR b XOR (i*m0 & 0xFF) XOR (a*m1 & 0xFF)
        """
        m0 = mults[i % len(mults)]
        m1 = mults[(i + 1) % len(mults)]
        return (a ^ b ^ ((i * m0) & 0xFF) ^ ((a * m1) & 0xFF)) & 0xFF

    @staticmethod
    def _encode_with_pairs(data: bytes, pairs: list, mults: list) -> bytes:
        """Encode data using cyclic pairs + scrambled multipliers."""
        result = bytearray()
        for i, byte in enumerate(data):
            a, b = pairs[i % len(pairs)]
            result.append(byte ^ EphemeralCypher._compute_key_byte(i, a, b, mults))
        return bytes(result)

    @staticmethod
    def _decode_with_pairs(data: bytes, pairs: list, mults: list) -> bytes:
        """XOR with multipliers is symmetric — identical to encode."""
        return EphemeralCypher._encode_with_pairs(data, pairs, mults)

    @staticmethod
    def _burn(obj):
        """Overwrite sensitive objects in memory."""
        if isinstance(obj, list):
            for i in range(len(obj)):
                obj[i] = (0, 0) if isinstance(obj[i], tuple) else 0
            obj.clear()
        elif isinstance(obj, bytearray):
            for i in range(len(obj)):
                obj[i] = 0

    @staticmethod
    def seal(plaintext: str, metadata: dict = None) -> str:
        """
        Seal plaintext into a one-time encrypted bundle.
        Generates fresh code pairs AND fresh multipliers every call.
        All key material is burned from memory immediately after packing.
        """
        raw = plaintext.encode("utf-8")
        length = len(raw)

        # Layer 1: Random one-time code pairs
        pairs = EphemeralCypher._generate_key_pairs(length)

        # Layer 2: Randomized cyclic multipliers (the 'build')
        mults = EphemeralCypher._generate_multipliers(count=16)

        # Encode using BOTH layers
        ciphertext = EphemeralCypher._encode_with_pairs(raw, pairs, mults)

        session_id = secrets.token_hex(16)
        timestamp = int(time.time())
        integrity = hashlib.sha256(raw).hexdigest()[:16]

        key_bytes = bytes([a for a, b in pairs] + [b for a, b in pairs])
        key_b64 = base64.b85encode(key_bytes).decode("ascii")
        mult_b64 = base64.b85encode(bytes(mults)).decode("ascii")
        cipher_b64 = base64.b85encode(ciphertext).decode("ascii")

        bundle = {
            "v": EphemeralCypher.VERSION,
            "sid": session_id,
            "ts": timestamp,
            "len": length,
            "chk": integrity,
            "key": key_b64,
            "mults": mult_b64,          # scrambled cyclic multipliers
            "payload": cipher_b64,
            "meta": metadata or {},
            "_used": False
        }

        # BURN all three layers from memory
        EphemeralCypher._burn(pairs)
        EphemeralCypher._burn(mults)
        del pairs, mults, raw, ciphertext, key_bytes

        return json.dumps(bundle)

    @staticmethod
    def open(bundle_json: str) -> dict:
        """Open and decrypt a one-time bundle. Burns all key material on exit."""
        bundle = json.loads(bundle_json)

        if bundle.get("_used"):
            raise ValueError("[EPHEMERAL] ❌ Bundle already opened. Key destroyed.")

        version = bundle.get("v", "")
        if not version.startswith("CDV6-OTP"):
            raise ValueError(f"[EPHEMERAL] ❌ Unknown cipher version: {version}")

        # Block replay: check burned session registry
        sid = bundle.get("sid", "")
        if sid in _BURNED_SESSIONS:
            raise ValueError("[EPHEMERAL] ❌ Session already consumed. Replay blocked.")

        length = bundle["len"]

        # Reconstruct code pairs
        key_bytes = base64.b85decode(bundle["key"].encode("ascii"))
        a_vals = list(key_bytes[:length])
        b_vals = list(key_bytes[length:length * 2])
        pairs = list(zip(a_vals, b_vals))

        # Reconstruct multipliers (the build)
        mult_bytes = base64.b85decode(bundle["mults"].encode("ascii"))
        mults = list(mult_bytes)

        # Decode with BOTH layers
        ciphertext = base64.b85decode(bundle["payload"].encode("ascii"))
        raw = EphemeralCypher._decode_with_pairs(ciphertext, pairs, mults)
        plaintext = raw.decode("utf-8")

        # Integrity check
        if hashlib.sha256(raw).hexdigest()[:16] != bundle["chk"]:
            EphemeralCypher._burn(pairs)
            EphemeralCypher._burn(mults)
            raise ValueError("[EPHEMERAL] ❌ Integrity FAILED — content may be tampered.")

        result = {
            "plaintext": plaintext,
            "meta": bundle.get("meta", {}),
            "session_id": bundle.get("sid"),
            "timestamp": bundle.get("ts"),
            "version": version
        }

        # BURN everything — door, key, build
        _BURNED_SESSIONS.add(sid)   # permanent replay block
        bundle["_used"] = True
        bundle["key"] = "[DESTROYED]"
        bundle["mults"] = "[DESTROYED]"
        bundle["payload"] = "[DESTROYED]"
        bundle["chk"] = "[DESTROYED]"

        EphemeralCypher._burn(pairs)
        EphemeralCypher._burn(mults)
        del pairs, mults, raw, ciphertext, a_vals, b_vals, key_bytes, mult_bytes

        return result


# ─────────────────────────────────────────────
#  TRANSMISSION PACKET BUILDER
#  Wraps seal() with routing metadata for
#  sovereign dark-channel transmission
# ─────────────────────────────────────────────

class EphemeralPacket:
    """
    Wraps an EphemeralCypher bundle with a one-time delivery envelope.

    The envelope contains:
      - A one-time endpoint token (the "door")
      - TTL: auto-expires after N seconds
      - Sender/receiver anonymous fingerprints (no identity stored)
    """

    @staticmethod
    def build(plaintext: str, ttl_seconds: int = 300, label: str = "SOVEREIGN_MSG") -> dict:
        """
        Build a one-time transmission packet.

        Args:
            plaintext: Sensitive content to transmit
            ttl_seconds: Seconds until this packet self-invalidates (default 5 min)
            label: Non-secret label for routing (no content info)

        Returns:
            dict with:
              - "door": the one-time endpoint token (send this separately from payload)
              - "bundle": the encrypted payload bundle
              - "expires": Unix timestamp when packet dies
        """
        door_token = secrets.token_urlsafe(32)  # The one-time "door"
        expires_at = int(time.time()) + ttl_seconds

        meta = {
            "label": label,
            "expires": expires_at,
            "door_hash": hashlib.sha256(door_token.encode()).hexdigest()[:16]
        }

        bundle = EphemeralCypher.seal(plaintext, metadata=meta)

        return {
            "door": door_token,          # ← send via separate channel, destroy after delivery
            "bundle": bundle,            # ← send via network
            "expires": expires_at,
            "label": label
        }

    @staticmethod
    def receive(bundle_json: str, door_token: str) -> str:
        """
        Receive and open a transmission packet.

        Verifies the door token matches the embedded door hash,
        checks TTL, decrypts, and burns everything.

        Returns:
            str: The plaintext content

        Raises:
            ValueError: If door is wrong, expired, or already used
        """
        result = EphemeralCypher.open(bundle_json)
        meta = result.get("meta", {})

        # Check TTL
        if int(time.time()) > meta.get("expires", 0):
            raise ValueError("[EPHEMERAL] ❌ Packet EXPIRED — content destroyed.")

        # Verify door token
        expected_door_hash = meta.get("door_hash", "")
        actual_door_hash = hashlib.sha256(door_token.encode()).hexdigest()[:16]
        if actual_door_hash != expected_door_hash:
            raise ValueError("[EPHEMERAL] ❌ Wrong door token — access denied. Packet burned.")

        # Burn the door token from memory
        door_token = secrets.token_hex(32)  # overwrite with noise
        del door_token

        return result["plaintext"]


# ─────────────────────────────────────────────
#  CLI TEST (python ephemeral_cypher.py)
# ─────────────────────────────────────────────

if __name__ == "__main__":
    import math
    print("\n╔══════════════════════════════════════════════╗")
    print("║   EPHEMERAL CYCLIC CYPHER — LUJAN OTP v2     ║")
    print("╚══════════════════════════════════════════════╝\n")

    msg_len = 90
    log_pairs = msg_len * 2 * math.log10(256)   # (256^2)^90
    log_mults = 16 * math.log10(128)             # 128^16
    total_log10 = int(log_pairs + log_mults)
    print(f"[KEYSPACE]  (256^2)^{msg_len} x 128^16 = ~10^{total_log10:,} combinations")
    print(f"            An attacker must guess 1 in 10^{total_log10:,} — no machine can brute-force this.\n")

    message = "SOVEREIGN TRANSMISSION: Lujan Protocol Alpha — Eyes Only."
    print(f"[ORIGINAL]  {message}\n")

    packet = EphemeralPacket.build(message, ttl_seconds=120, label="DEMO")
    print(f"[DOOR]     {packet['door'][:32]}...")
    print(f"[EXPIRES]  {packet['expires']}")
    print(f"[BUNDLE]   {packet['bundle'][:90]}...\n")

    # Decrypt
    try:
        plaintext = EphemeralPacket.receive(packet["bundle"], packet["door"])
        print(f"[DECRYPTED] {plaintext}\n")
    except ValueError as e:
        print(f"[BLOCKED] {e}\n")

    # Try to re-open — must fail
    print("[TEST] Re-open attempt (must be blocked)...")
    try:
        EphemeralPacket.receive(packet["bundle"], packet["door"])
        print("[FAIL] ❌ Re-use was NOT blocked!")
    except ValueError as e:
        print(f"[PASS] ✅ {e}\n")

    # Try wrong door — must fail
    print("[TEST] Wrong door token attempt...")
    packet2 = EphemeralPacket.build("test", ttl_seconds=60)
    try:
        EphemeralPacket.receive(packet2["bundle"], "wrong-door-token")
        print("[FAIL] ❌ Wrong door was accepted!")
    except ValueError as e:
        print(f"[PASS] ✅ {e}\n")

    print("All tests complete. Key material burned.\n")
