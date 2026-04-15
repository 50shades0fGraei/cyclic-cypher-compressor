# Codemap-DNA-tesseract/parser.py

from tree_sitter import Language, Parser
from tree_sitter_languages import get_language, get_parser
import json

class CodeParser:
    """
    Parses source code into an AST to identify "code sequences" (functions)
    and their specific dependencies (imports), creating a precise address library.
    """

    def __init__(self, language_name: str, program_name: str, program_order: int):
        """
        Initializes the parser with a specific language and program context.
        """
        self.language = get_language(language_name)
        self.parser = get_parser(language_name)
        self.program_name = program_name
        self.program_order = program_order
        self.address_library = {}
        self._function_counter = 0
        self.program_identifier = self._get_program_identifier()
        # This will map the imported name (e.g., 'os', 'datetime') to the full import statement.
        self.import_map = {}

    def _get_program_identifier(self):
        """
        Generates a unique identifier for the program based on its name and order.
        """
        return f"{self.program_name[0].lower()}{self.program_order}"

    def _extract_imports(self, node):
        """
        First pass: Traverse the AST to find all import statements and map the
        imported names to their original statement text.
        """
        if node.type == 'import_statement':
            # Handles cases like `import os` or `import sys as system`
            for child in node.children:
                if child.type == 'dotted_name':
                    name = child.text.decode('utf8')
                    self.import_map[name] = node.text.decode('utf8')
                elif child.type == 'aliased_import': # import sys as system
                    alias = child.child_by_field_name('alias').text.decode('utf8')
                    self.import_map[alias] = node.text.decode('utf8')

        elif node.type == 'import_from_statement':
            # Handles `from datetime import datetime`
            module_name = node.child_by_field_name('module_name').text.decode('utf8')
            for child in node.children:
                if child.type == 'dotted_name' and child.parent.type != 'import_from_statement':
                     name = child.text.decode('utf8')
                     self.import_map[name] = node.text.decode('utf8')
                elif child.type == 'aliased_import': # from datetime import datetime as dt
                    alias = child.child_by_field_name('alias').text.decode('utf8')
                    self.import_map[alias] = node.text.decode('utf8')

        for child in node.children:
            self._extract_imports(child)

    def _find_dependencies_in_function(self, function_node):
        """
        For a given function node, traverse its body to find identifiers that
        match our map of imported names.
        """
        dependencies = set()
        
        def find_identifiers(sub_node):
            if sub_node.type == 'identifier':
                identifier = sub_node.text.decode('utf8')
                if identifier in self.import_map:
                    dependencies.add(self.import_map[identifier])
            
            for child in sub_node.children:
                find_identifiers(child)

        find_identifiers(function_node)
        return list(dependencies)

    def process_functions(self, node):
        """
        Second pass: Traverse the AST to find functions, analyze their specific
        dependencies, and build the address library.
        """
        if node.type == 'function_definition':
            self._function_counter += 1
            function_number = str(self._function_counter).zfill(4)
            address = f"{self.program_identifier}f{function_number}"

            # Find the specific imports used by this function
            dependencies = self._find_dependencies_in_function(node)

            self.address_library[address] = {
                "text": node.text.decode('utf8'),
                "start_point": node.start_point,
                "end_point": node.end_point,
                "type": "function",
                "dependencies": dependencies # Now specific to this function!
            }

        for child in node.children:
            self.process_functions(child)
            
    def parse(self, code_bytes: bytes):
        """
        Parses the code, extracts imports, and then processes functions.
        """
        tree = self.parser.parse(code_bytes)
        root_node = tree.root_node
        
        # 1. First pass to build the import map
        self._extract_imports(root_node)
        
        # 2. Second pass to process functions and their dependencies
        self.process_functions(root_node)


if __name__ == '__main__':
    # Example Usage:
    python_parser = CodeParser('python', 'MyAwesomeApp', 7)

    sample_code = b"""
import os
import sys
from datetime import datetime, date

def get_os_info():
    # This function only uses 'os'
    return f"OS: {os.name}"

def get_time():
    # This function only uses 'datetime'
    now = datetime.now()
    return now.strftime("%H:%M:%S")

def get_python_version():
    # This function only uses 'sys'
    return f"Python version: {sys.version}"
"""

    # Parse the code to build the full address library
    python_parser.parse(sample_code)

    print(f"Generated Address Library for {python_parser.program_name}:")
    print(json.dumps(python_parser.address_library, indent=2))
