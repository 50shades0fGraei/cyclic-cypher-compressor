# Codemap-DNA-tesseract/jin.py

import argparse
import json
from tesseract_os import TesseractOS
import os

class Jin:
    """
    The CLI and execution engine for Tesseract OS. The Jin.
    It summons functions to operate on a central data store,
    embodying the principle of one-way data traffic.
    """
    def __init__(self):
        self.os_instance = TesseractOS()
        
        # --- Dynamic Program Loading ---
        print("[Jin] Scanning for compatible program files...")
        compatible_extensions = ('.py', '.js', '.ts')
        excluded_dirs = {'node_modules', '.git', '.idx', '__pycache__'}
        
        for root, dirs, files in os.walk('.'):
            # Prune the search by modifying the directory list in-place
            dirs[:] = [d for d in dirs if d not in excluded_dirs]
            
            for file in files:
                if file.endswith(compatible_extensions):
                    # We need to ignore the jin script itself to avoid a loop
                    if os.path.basename(file) == 'jin.py':
                        continue
                    file_path = os.path.join(root, file)
                    # Normalize path for consistency
                    file_path = os.path.normpath(file_path)
                    print(f"[Jin] Loading program: {file_path}")
                    self.os_instance.load_program(file_path)
        # --- End Dynamic Loading ---

        self.action_directory_path = 'Codemap-DNA-tesseract/action_directory.json'
        self.shared_data_store_path = 'Codemap-DNA-tesseract/shared_data_store.json'
        
        try:
            with open(self.action_directory_path, 'r') as f:
                self.actions = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            print(f"[Jin] Error: Action directory not found or corrupted.")
            self.actions = []

    def _get_program_details(self, address: str):
        program_identifier = address.split('f')[0]
        return self.os_instance.master_address_library.get(program_identifier)

    def _find_function_by_address(self, address: str):
        program_details = self._get_program_details(address)
        if program_details:
            return program_details['functions'].get(address)
        return None

    def _summon_and_execute_python(self, function_details: dict, data_store: dict, params: list):
        dependencies = "\n".join(function_details.get('dependencies', []))
        function_code = function_details.get('text', '')
        function_name = function_code.split('def ')[1].split('(')[0].strip()

        param_strings = ['data_store'] + [repr(p) for p in params]
        function_call = f"{function_name}({', '.join(param_strings)})"

        cyclone_code = f"{dependencies}\n\n{function_code}\n\n{function_call}"
        
        print("    -> Constructing Cyclone for Sovereign Invocation...")
        execution_namespace = {'data_store': data_store, 'print': print} # Provide data store and print
        
        try:
            print(f"    -> SUMMONING: '{function_name}' with params {params}")
            exec(cyclone_code, execution_namespace)
            print(f"    -> SUCCESS: Invocation complete.")
        except Exception as e:
            print(f"    -> INVOCATION FAILED: {e}")

    def execute_action(self, action_id: str):
        action_to_run = next((action for action in self.actions if action['id'] == action_id), None)
        if not action_to_run:
            print(f"Error: Action '{action_id}' not found.")
            return

        print(f"--- Executing Action: {action_id} ---")
        try:
            with open(self.shared_data_store_path, 'r') as f:
                in_memory_data_store = json.load(f)
            print(f"[Data Store] READ complete.")
        except (FileNotFoundError, json.JSONDecodeError):
            print(f"[Data Store] Error: Could not read data store. Aborting.")
            return

        sequence = action_to_run.get('sequence', [])
        for i, step in enumerate(sequence):
            address = step['address']
            params = step.get('params', [])
            print(f"  Step {i+1}: Processing address '{address}'")
            
            function_details = self._find_function_by_address(address)
            program_details = self._get_program_details(address)
            
            if function_details and program_details:
                if program_details['language'] == 'python':
                    self._summon_and_execute_python(function_details, in_memory_data_store, params)
                else:
                    print(f"    -> (Skipping non-Python function for now)")
            else:
                print(f"    -> Error: Function for address '{address}' not found!")

        try:
            with open(self.shared_data_store_path, 'w') as f:
                json.dump(in_memory_data_store, f, indent=2)
            print(f"[Data Store] WRITE complete.")
        except IOError as e:
            print(f"[Data Store] Error: Could not write to data store: {e}")

        print("--- Action Complete ---")

if __name__ == '__main__':
    cli_parser = argparse.ArgumentParser(prog='jin', description="Tesseract OS Jin Summoner CLI")
    subparsers = cli_parser.add_subparsers(dest='command', help='Available commands')
    run_parser = subparsers.add_parser('run', help='Execute a predefined action by its ID')
    run_parser.add_argument('action_id', type=str, help='The ID of the action to execute')
    args = cli_parser.parse_args()
    
    if args.command == 'run':
        jin_instance = Jin()
        jin_instance.execute_action(args.action_id)
    else:
        cli_parser.print_help()
