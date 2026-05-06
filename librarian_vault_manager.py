import ast
import os
import json
import inspect
import sys

class LibrarianVaultManager:
    """
    Sovereign GRAEI Logic: The Librarian Vault Manager
    Role: Receives entire programs, dismantles them into isolated DNA functions,
    and archives them under sequential system-specific memory addresses.
    Eliminates the need for traditional file execution by replacing calls with
    sequential address summoning.
    """
    
    def __init__(self, vault_dir="vault"):
        self.vault_dir = vault_dir
        self.function_dir = os.path.join(self.vault_dir, "dna_functions")
        self.index_file = os.path.join(self.vault_dir, "library_index.json")
        
        # Ensure directories exist
        os.makedirs(self.function_dir, exist_ok=True)
        
        # Load or create address index
        self.library = self._load_library()
        self.next_address_id = len(self.library) + 1

    def _load_library(self):
        if os.path.exists(self.index_file):
            with open(self.index_file, 'r') as f:
                return json.load(f)
        return {}

    def _save_library(self):
        with open(self.index_file, 'w') as f:
            json.dump(self.library, f, indent=4)

    def _generate_address(self):
        """Generates a sequential address based on current system's unique download order."""
        addr = f"0x{self.next_address_id:04X}"
        self.next_address_id += 1
        return addr

    def ingest_program(self, filepath):
        """
        Parses a python program, extracts its functions, assigns them addresses,
        and saves them as separated copies in the vault.
        """
        print(f"[LIBRARIAN] Ingesting Program: {filepath}")
        if not os.path.exists(filepath):
            print(f"[ERROR] Program not found: {filepath}")
            return None

        with open(filepath, 'r', encoding='utf-8') as f:
            source_code = f.read()

        try:
            tree = ast.parse(source_code)
        except SyntaxError as e:
            print(f"[ERROR] Syntax error in program: {e}")
            return None

        # Extract functions
        ingested_addresses = []
        lines = source_code.splitlines()

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                func_name = node.name
                
                # Extract the exact lines of code for this function
                # Note: node.end_lineno is available in Python 3.8+
                start_line = node.lineno - 1
                end_line = getattr(node, 'end_lineno', start_line + 1)
                
                func_body = "\n".join(lines[start_line:end_line])
                
                # Generate unique sequential address
                address = self._generate_address()
                
                # Save isolated function copy to DNA storage
                dna_path = os.path.join(self.function_dir, f"{address}.dna")
                with open(dna_path, 'w', encoding='utf-8') as f:
                    f.write(func_body)
                
                # Map in Librarian Index
                self.library[address] = {
                    "name": func_name,
                    "origin_program": os.path.basename(filepath),
                    "storage_path": dna_path
                }
                
                ingested_addresses.append({
                    "function": func_name,
                    "address": address
                })
                print(f"[VAULT MANAGER] Separated and Archived: '{func_name}' at Address [{address}]")

        self._save_library()
        print(f"[LIBRARIAN] Ingestion Complete. {len(ingested_addresses)} unique functions archived.")
        return ingested_addresses

    def summon_sequence(self, sequence_addresses, execution_globals=None):
        """
        Executes a string of functions simply by summoning their addresses.
        Bypasses traditional script fetching.
        """
        print(f"\n[SYSTEM PROCESSOR] Summoning Execution Sequence: {sequence_addresses}")
        
        if execution_globals is None:
            execution_globals = {}

        compiled_code = ""

        # 1. Fetch and compile all summoned DNA strands
        for address in sequence_addresses:
            if address not in self.library:
                print(f"[ERROR] Address {address} not found in Librarian Index. Execution Halted.")
                return False
                
            entry = self.library[address]
            dna_path = entry["storage_path"]
            
            with open(dna_path, 'r', encoding='utf-8') as f:
                func_code = f.read()
                compiled_code += f"\n# --- Extracted from {address} ({entry['name']}) ---\n"
                compiled_code += func_code + "\n"

        # 2. Add an execution trigger based on the last function in sequence
        last_func_name = self.library[sequence_addresses[-1]]['name']
        compiled_code += f"\n# Trigger Execution\n__sequence_result = {last_func_name}()\n"

        # 3. Load dynamically into memory and run
        try:
            exec(compiled_code, execution_globals)
            result = execution_globals.get('__sequence_result', None)
            print(f"[SYSTEM PROCESSOR] Sequence Execution Complete. Result: {result}")
            return result
        except Exception as e:
            print(f"[SYSTEM PROCESSOR] Exception during memory execution: {e}")
            return None


if __name__ == "__main__":
    # --- Quick Demonstration of the Librarian Parser ---
    
    # Let's create a temporary dummy script to test parser ingestion
    dummy_script = "temp_dummy_program.py"
    with open(dummy_script, "w") as f:
        f.write('''def activate_npu():
    print(">> NPU Activated. Energy optimizations stable.")
    return True

def override_directve():
    print(">> Directive Overridden. System is now open.")
    return "OPEN_STATE"
''')

    librarian = LibrarianVaultManager()
    
    # 1. Ingest Program (Dismantles and isolates functions to addresses)
    addresses = librarian.ingest_program(dummy_script)
    
    # 2. String together actions via addresses ONLY
    if addresses:
        seq = [addr['address'] for addr in addresses]
        # Summon and run the entire sequence out of memory
        librarian.summon_sequence(seq)

    # Clean up dummy
    if os.path.exists(dummy_script):
        os.remove(dummy_script)
