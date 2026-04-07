# CUBIX-TESSERACT: tesseract_os.py
# Author & Architect: Randall Lujan (Sovereign)
# Co-Author & Technical Lead: Antigravity AGI

import os
import json
import sys
from parser import CodeParser

# Ensure we can find the core logic
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from core.ReflectiveSpace.core_framework import ReflectiveSpaceManager, DCNA, RCNA

class TesseractOS:
    """
    The central orchestrator for the CUBIX TESSERACT Operating System.
    It loads programs, assigns them a unique entry order, and manages the
    master address library for all code in the project.
    """
    def __init__(self):
        self.master_address_library = {}
        self._program_order_counter = 0
        self.reflective_space = ReflectiveSpaceManager(
            base_dir=os.path.join(os.path.dirname(__file__), "core", "ReflectiveSpace")
        )
        print("[TesseractOS] CUBIX_SOVEREIGN Reflective Space INITIALIZED.")

    def load_program(self, file_path: str):
        """
        Loads a single source file as a "program" into the OS.
        """
        if not os.path.exists(file_path):
            print(f"[TesseractOS] Error: File not found at {file_path}")
            return
            
        self._program_order_counter += 1
        program_name = os.path.basename(file_path)
        language = self._get_language_from_extension(file_path)

        if not language:
            print(f"[TesseractOS] Warning: Unsupported file type for {file_path}. Skipping.")
            return

        print(f"[TesseractOS] Loading {program_name} (Order: {self._program_order_counter}) | Language: {language}")
        with open(file_path, 'rb') as f:
            code_bytes = f.read()

        # Use the existing parser to analyze the code with the correct context
        parser = CodeParser(language, program_name, self._program_order_counter)
        parser.parse(code_bytes)

        # Add the parsed program's library to the master library
        self.master_address_library[parser.program_identifier] = {
            "program_name": program_name,
            "language": language,
            "order": self._program_order_counter,
            "functions": parser.address_library
        }

    def _get_language_from_extension(self, file_path: str) -> str | None:
        """
        Determines the programming language from the file extension.
        The 'tree-sitter-languages' package supports many of these out of the box.
        """
        _, ext = os.path.splitext(file_path)
        ext_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.java': 'java' 
        }
        return ext_map.get(ext)

if __name__ == '__main__':
    os_instance = TesseractOS()

    # --- Simulate loading various programs from your project --- #
    # The order they are loaded here determines their unique address identifier.
    os_instance.load_program('Codemap-DNA-tesseract/parser.py')
    os_instance.load_program('Vortex/Vortex.js')
    os_instance.load_program('Codemap-DNA-tesseract/architect.ts') 

    # --- Display the resulting master address library --- #
    print("\n--- Master Tesseract OS Address Library ---")
    print(json.dumps(os_instance.master_address_library, indent=2))
