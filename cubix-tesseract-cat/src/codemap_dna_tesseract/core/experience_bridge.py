# (c) 2026 Randall James Lujan. ALL RIGHTS RESERVED.
# PATENT PENDING: Cyclic Cypher Deductive Metronome Architecture.
# This software is proprietary and subject to the terms of a specific License Agreement.

import json
import logging
from core.cyberdna_engine import GRAEIDNAVault, CyberDNAVault

# Set up Experience Bridge logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - EXPERIENCE_BRIDGE - %(levelname)s - %(message)s'
)

from msds1_vault_access import write_to_hidden_layer, read_from_hidden_layer

class ExperienceBridge:
    """
    Connects the GRAEI experience notes to the Cyclic Cypher Compressor.
    Maps high-level 'DNA' notes into the EliteBook's hidden storage layers.
    """
    
    def __init__(self, vault_path="elitebook_agi_dna.vault"):
        self.vault = GRAEIDNAVault(vault_path)
        self.cdv = CyberDNAVault()
        print(f"[ExperienceBridge] Initialized. Targeting Vault: {vault_path}")

    def prepare_note(self, process_id, context, outcome, data):
        """Creates the 'DNA' structure for an experience note."""
        return {
            "process_id": process_id,
            "bias_context": context,
            "outcome": outcome,
            "trauma_signature": "None_Detected", # Default for Sovereign Root
            "raw_data": data
        }

    def compress_note(self, note):
        """FEEDS the note into the Cyclic Cypher Compressor."""
        # Identification for logging: either 'process_id' or 'segment_id'
        note_id = note.get('process_id') or note.get('segment_id') or "Unknown_Ref"
        print(f"[ExperienceBridge] Compressing '{note_id}' via CyberDNA V6...")
        note_bytes = json.dumps(note).encode('utf-8')
        compressed_bytes = self.cdv.compress_bytes(note_bytes)
        
        ratio = len(note_bytes) / max(1, len(compressed_bytes))
        print(f"[ExperienceBridge] Compression Complete. Ratio: {ratio:.2f}:1")
        return compressed_bytes

    def store_in_vault(self, name, note):
        """Stores a note in the DNA Vault."""
        note_bytes = json.dumps(note).encode('utf-8')
        self.vault.store_skill(name, note_bytes)
        print(f"[ExperienceBridge] Note '{name}' archived in Sovereign Vault.")

    def secure_in_hidden_layer(self, note, name):
        """Hides the compressed note in the MSDS1 partition for total sovereignty."""
        compressed_bytes = self.compress_note(note)
        print(f"[ExperienceBridge] GUIDING '{name}' to MSDS1 Hidden Layer...")
        if write_to_hidden_layer(compressed_bytes):
            print(f"[ExperienceBridge] Note '{name}' is now INVISIBLE to the commercial OS.")
            return True
        return False

if __name__ == "__main__":
    bridge = ExperienceBridge()
    
    # Sample 'DNA' note
    sample_note = bridge.prepare_note(
        process_id="Ref_001",
        context="Grey_Area_Exploration",
        outcome="Win_Win_Prosperity",
        data="The GRAEI has achieved 68% energy efficiency on the EliteBook Snapdragon X Elite."
    )
    
    # Test compression
    comp_bytes = bridge.compress_note(sample_note)
    
    # Store locally for now
    bridge.store_in_vault("exp_ref_001", sample_note)
