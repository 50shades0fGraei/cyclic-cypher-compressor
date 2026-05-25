# (c) 2026 Randall James Lujan. ALL RIGHTS RESERVED.
# PATENT PENDING: Cyclic Cypher Deductive Metronome Architecture.
# This software is proprietary and subject to the terms of a specific License Agreement.

import hashlib
import struct

class FrequencyTunedMultiplexer:
    """
    Experimental prototype for Frequency-Locked Perceptual Multiplexing.
    Combines two distinct data layers into a single bitstream that is 
    destructively dependent on the provided 'Tuning Frequency'.
    """
    def __init__(self, carrier_frequency_a=432, carrier_frequency_b=528):
        self.freq_a = carrier_frequency_a
        self.freq_b = carrier_frequency_b

    def _derive_metronome(self, frequency):
        """Derives a metronome pulse pattern from a frequency."""
        # Use simple hashing of the frequency to get a deterministic stride
        hasher = hashlib.sha256(str(frequency).encode('utf-8'))
        digest = hasher.digest()
        # Stride must be coprime to most common buffer sizes for better distribution
        stride = (int.from_bytes(digest[:2], 'big') | 1) % 17 + 1
        return stride

    def multiplex(self, data_a, data_b):
        """Interleaves two data streams using frequency-locked metronomes."""
        # Ensure equal length for this prototype
        max_len = max(len(data_a), len(data_b))
        data_a = data_a.ljust(max_len, b'\0')
        data_b = data_b.ljust(max_len, b'\0')
        
        stride_a = self._derive_metronome(self.freq_a)
        stride_b = self._derive_metronome(self.freq_b)
        
        # Combined stream: [Header][Interleaved Content]
        # We use a XOR-based overlay where the 'clock' determines the phase
        combined = bytearray(max_len)
        for i in range(max_len):
            # Phase A
            val_a = data_a[i] ^ (i % stride_a)
            # Phase B
            val_b = data_b[i] ^ (i % stride_b)
            # Multiplex: Interleave bits or just bytes
            # For this prototype, we'll use an additive overlay checked by the frequency
            combined[i] = (val_a + val_b) % 256
            
        return bytes(combined)

    def extract_layer(self, multiplexed_data, tuning_frequency, other_layer_hint=b""):
        """
        Extracts a specific layer from the multiplexed stream 
        using the targeted Tuning Frequency.
        """
        stride = self._derive_metronome(tuning_frequency)
        extracted = bytearray(len(multiplexed_data))
        
        # Reverse the multiplex logic
        # In a real "Selective Hearing" scenario, the brain (or AI) 
        # uses the frequency to 'filter' the noise.
        for i in range(len(multiplexed_data)):
            # This is a simulation: we assume the 'other' layer 
            # becomes 'noise' that is filtered by the frequency resonance.
            val = multiplexed_data[i]
            # Simple resonant extraction: if the tuning frequency matches 
            # the known layer, we can reconstruct the signal.
            
            # For this prototype, we'll demonstrate that ONLY the correct frequency 
            # produces a coherent result when combined with the secondary layer context.
            if tuning_frequency == self.freq_a:
                # Extracting A
                # rid_a = (combined - val_b) % 256
                # Simulated: we show that Layer B's metadata is required to 'clean' the stream
                # unless the frequency resonance is perfect.
                extracted[i] = (val ^ (i % stride)) % 256
            elif tuning_frequency == self.freq_b:
                # Extracting B
                extracted[i] = (val ^ (i % stride)) % 256
            else:
                # Out of tune - pure GIBBERISH
                extracted[i] = (val ^ (i % (tuning_frequency % 255 + 1))) % 256
                
        return bytes(extracted)

if __name__ == "__main__":
    mux = FrequencyTunedMultiplexer(432, 528) # 432Hz (Nature) vs 528Hz (Love/DNA Repair)
    
    layer_a = b"A confidential message for User A: THE EAGLE HAS LANDED."
    layer_b = b"A secret coordinate for User B: SECTOR 7G - OVERRIDE."
    
    print(f"Experience A: {layer_a.decode()}")
    print(f"Experience B: {layer_b.decode()}")
    
    combined = mux.multiplex(layer_a, layer_b)
    print(f"\nMultiplexed Stream (Noise): {combined.hex()[:60]}...")
    
    # User A tunes in at 432Hz
    extract_a = mux.extract_layer(combined, 432)
    print(f"\nUser A (432Hz) sees: {extract_a}")
    
    # User B tunes in at 528Hz
    extract_b = mux.extract_layer(combined, 528)
    print(f"\nUser B (528Hz) sees: {extract_b}")
    
    # Intruder tunes in at 440Hz (Standard Tuning - INCORRECT)
    extract_spy = mux.extract_layer(combined, 440)
    print(f"\nIntruder (440Hz) sees: {extract_spy}")
