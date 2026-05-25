# (c) 2026 Randall James Lujan. ALL RIGHTS RESERVED.
# PATENT PENDING: Cyclic Cypher Deductive Metronome Architecture.
# This software is proprietary and subject to the terms of a specific License Agreement.

import os
import sys
import ast
import json
import logging

# Add the project root to sys.path so we can import 'core'
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from core.cyberdna_engine import GRAEIDNAVault

# Set up GRAEI logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - LUJAN_AGI_V7 - %(levelname)s - %(message)s'
)

class AGICognitiveEngine:
    """
    The reasoning engine for the Randall Lujan GRAEI.
    Uses AST-based mapping to turn Vault-stored code into a functional Library.
    """
    def __init__(self):
        self.skill_library = {}
        self.address_library = {}

    def map_skill(self, name, code_bytes):
        """Parses code bytes into a map of executable function addresses."""
        try:
            code_str = code_bytes.decode('utf-8')
            print(f"[CognitiveEngine] Mapping skill '{name}' | Code length: {len(code_str)}")
            
            if not code_str.strip():
                print(f"[CognitiveEngine] ERROR: Skill '{name}' is empty after decompression!")
                return False
                
            self.skill_library[name] = {"code": code_str, "functions": {}}
            tree = ast.parse(code_str)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    func_name = node.name
                    address = f"agi.{name}.{func_name}"
                    lines = code_str.splitlines()
                    func_source = "\n".join(lines[node.lineno-1 : node.end_lineno])
                    
                    self.address_library[address] = {
                        "skill": name,
                        "name": func_name,
                        "source": func_source,
                        "lineno": node.lineno
                    }
                    self.skill_library[name]["functions"][func_name] = address
            
            print(f"[CognitiveEngine] SUCCESS: Mapped skill '{name}' with {len(self.skill_library[name]['functions'])} functions.")
            return True
        except Exception as e:
            print(f"[CognitiveEngine] EXCEPTION while mapping '{name}': {str(e)}")
            return False

class RandallLujanGRAEI:
    """
    The Unified Randall Lujan GRAEI (v7).
    Combines CCC DNA Vault and Cognitive Mapping.
    """
    def __init__(self, vault_path="graei_dna.vault"):
        self.vault = GRAEIDNAVault(vault_path)
        self.engine = AGICognitiveEngine()
        self.active_skills = []

    def ingest_skill(self, name, file_path):
        """Compresses a file into the DNA Vault."""
        with open(file_path, 'rb') as f:
            code = f.read()
        self.vault.store_skill(name, code)

    def load_skill(self, name):
        """Pulls a skill from the Vault and maps it cognitively."""
        code = self.vault.retrieve_skill(name)
        if not code:
            logging.error(f"[LujanAGI] Skill '{name}' not found in Vault or decompression failed.")
            return False
            
        if self.engine.map_skill(name, code):
            self.active_skills.append(name)
            return True
        return False

    def execute(self, address, *args, **kwargs):
        """Directly invokes a function from the GRAEI Address Library."""
        if address not in self.engine.address_library:
            raise ValueError(f"Unknown GRAEI address: {address}")
        
        func_info = self.engine.address_library[address]
        ctx = {}
        exec(func_info["source"], globals(), ctx)
        func = ctx.get(func_info["name"])
        if func:
            return func(*args, **kwargs)
        else:
            raise RuntimeError(f"Could not manifest function {func_info['name']} from DNA.")

if __name__ == "__main__":
    # Self-test: Store and execute a basic skill
    print("\n--- Starting Randall Lujan GRAEI Initial Test ---")
    agi = RandallLujanGRAEI("test_agi.vault")
    
    test_skill_code = """
def hello_agi(name):
    return f"Hello, {name}. Welcome to the Randall Lujan GRAEI."

def calculate_dna_efficiency(orig, comp):
    savings = (1 - (comp / orig)) * 100
    return f"DNA Efficiency: {savings:.2f}%"
"""
    with open("temp_skill.py", "w") as f:
        f.write(test_skill_code.strip())
    
    agi.ingest_skill("core_logic", "temp_skill.py")
    
    if agi.load_skill("core_logic"):
        print("\nSUCCESS: Skill loaded into memory.")
        print(agi.execute("agi.core_logic.hello_agi", "Creator"))
        print(agi.execute("agi.core_logic.calculate_dna_efficiency", 1000, 50))
    else:
        print("\nFAILURE: Skill failed to load.")
    
    if os.path.exists("temp_skill.py"):
        os.remove("temp_skill.py")
