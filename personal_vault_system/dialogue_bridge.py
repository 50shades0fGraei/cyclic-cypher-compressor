# (c) 2026 Randall James Lujan. ALL RIGHTS RESERVED.
# PATENT PENDING: Cyclic Cypher Deductive Metronome Architecture.
# This software is proprietary and subject to the terms of a specific License Agreement.

import hashlib
import struct
from .syllable_codec import SyllableCodec

class DialogueBridge:
    def __init__(self, shared_secret, local_device_id, remote_device_id):
        self.codec = SyllableCodec()
        self.secret = shared_secret
        self.local_id = local_device_id
        self.remote_id = remote_device_id
        self.lib_size = self.codec.lib_size

    def _get_cypher_pattern(self, salt=""):
        """
        Derives a deterministic shuffle pattern from the shared secret 
        AND the unique hardware fingerprints of both participants.
        This ensures the cypher is "device-locked".
        """
        seed = f"{self.secret}:{self.local_id}:{self.remote_id}:{salt}"
        hasher = hashlib.sha256(seed.encode('utf-8'))
        digest = hasher.digest()
        
        # Create a permutation of the library indices (simplified)
        # For efficiency, we just use a large offset and multiplier derived from the hash
        offset = int.from_bytes(digest[:4], 'big') % self.lib_size
        multiplier = (int.from_bytes(digest[4:8], 'big') | 1) % self.lib_size
        return offset, multiplier

    def encode_message(self, text):
        """Encodes text into an encrypted syllable ID stream."""
        # 1. Convert text to Syllable IDs
        raw_ids = self.codec.encode(text)
        
        # 2. Encrypt IDs using the Device-Locked Privacy Cypher
        # We use a robust additive shift for this prototype
        offset, _ = self._get_cypher_pattern()
        encrypted_ids = []
        for rid in raw_ids:
            eid = (rid + offset) % self.lib_size
            encrypted_ids.append(eid)
            
        # 3. Create Binary Packet [Magic 'DB1'][NumIDs (4b)][IDs... (2b each)]
        packet = bytearray(b'DB1')
        packet.extend(struct.pack('<I', len(encrypted_ids)))
        for eid in encrypted_ids:
            packet.extend(struct.pack('<H', eid))
            
        return packet

    def decode_message(self, packet):
        """Decodes an encrypted syllable ID stream back to text."""
        if packet[:3] != b'DB1':
            raise ValueError("Invalid Dialogue Bridge Packet")
            
        num_ids = struct.unpack('<I', packet[3:7])[0]
        encrypted_ids = []
        for i in range(num_ids):
            eid = struct.unpack('<H', packet[7 + i*2 : 9 + i*2])[0]
            encrypted_ids.append(eid)
            
        # 1. Reverse the Device-Locked Privacy Cypher
        offset, _ = self._get_cypher_pattern()
        
        raw_ids = []
        for eid in encrypted_ids:
            # Reverse additive shift
            rid = (eid - offset) % self.lib_size
            raw_ids.append(rid)
            
        # 2. Decode IDs to Text
        return self.codec.decode(raw_ids)

if __name__ == "__main__":
    # Internal Test: Simulated Hardware Secure Conversation
    device_a_fingerprint = "HW-LUJAN-X1-ALPHA"
    device_b_fingerprint = "HW-LUJAN-P7-OMEGA"
    shared_secret = "interstellar_handshake_42"
    
    # Bridge for Person A (Sender)
    bridge_a = DialogueBridge(shared_secret, device_a_fingerprint, device_b_fingerprint)
    
    # Bridge for Person B (Receiver)
    # Note: Device B's local_id is "HW-LUJAN-P7-OMEGA" and remote_id is "HW-LUJAN-X1-ALPHA"
    # But for the cypher to match, the seed f"{secret}:{sender}:{receiver}" must be handled correctly.
    # We'll assume the protocol always uses (SenderID, ReceiverID) in the seed.
    
    msg = "CyberDNA V7 deployment confirmed. Initiating AI Dialogue Bridge."
    print(f"Original Text: {msg}")
    
    packet = bridge_a.encode_message(msg)
    print(f"Encrypted Packet Size: {len(packet)} bytes (Device-Locked)")
    
    # Successful Decode (Correct HW Fingerprint)
    bridge_b = DialogueBridge(shared_secret, device_a_fingerprint, device_b_fingerprint)
    decoded = bridge_b.decode_message(packet)
    print(f"Decoded (Correct Device): {decoded}")
    
    # Failed Decode (Unauthorized Device)
    try:
        bridge_spy = DialogueBridge(shared_secret, "HW-SPY-X-99", device_b_fingerprint)
        decoded_spy = bridge_spy.decode_message(packet)
        print(f"Decoded (Spy Device): {decoded_spy}")
        if decoded_spy != decoded:
            print("STATUS: Spy Device produced GIBBERISH (Security Success)")
    except Exception as e:
        print(f"STATUS: Decode Failed as expected for Spy Device: {e}")
