
import os
import json
from tree_sitter_languages import get_language, get_parser

# --- Language Configuration ---
# This dictionary maps file extensions to their tree-sitter language and
# the specific query used to find function definitions.
LANGUAGE_CONFIG = {
    ".py": {
        "language": "python",
        "query": """
        (function_definition
          name: (identifier) @function.name)
        """
    },
    ".ts": {
        "language": "typescript",
        "query": """
        (function_declaration
          name: (identifier) @function.name)
        """
    },
    ".go": {
        "language": "go",
        "query": """
        (function_declaration
          name: (identifier) @function.name)
        """
    }
}

def find_code_files(root_dir):
    """
    Recursively finds all code files in a directory that match our
    language configuration.
    """
    code_files = []
    for root, _, files in os.walk(root_dir):
        for file in files:
            if any(file.endswith(ext) for ext in LANGUAGE_CONFIG):
                # Exclude the indexer'''s own code
                if "indexer/main.py" not in os.path.join(root, file):
                    code_files.append(os.path.join(root, file))
    return code_files

def parse_functions_from_file(file_path):
    """
    Parses a single file to extract all function definitions.
    """
    file_extension = os.path.splitext(file_path)[1]
    config = LANGUAGE_CONFIG.get(file_extension)

    if not config:
        return []

    language = get_language(config["language"])
    parser = get_parser(config["language"])

    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()

    tree = parser.parse(bytes(code, "utf8"))
    query = language.query(config["query"])
    captures = query.captures(tree.root_node)

    functions = []
    for node, _ in captures:
        functions.append({
            "name": node.text.decode("utf8"),
            "file": file_path,
            "language": config["language"]
        })
    return functions

def generate_process_index(root_dir, output_file):
    """
    Generates the process index for the entire project.
    """
    print("Starting code scan...")
    all_functions = []
    code_files = find_code_files(root_dir)

    for file in code_files:
        print(f"  - Parsing {file}...")
        functions = parse_functions_from_file(file)
        all_functions.extend(functions)

    print(f"\nFound {len(all_functions)} functions. Assigning addresses...")

    process_index = {}
    # Use a high-precision floating-point number for the address
    address_counter = 0.0001
    for func in all_functions:
        address_str = f"{address_counter:.4f}"
        process_index[address_str] = func
        address_counter += 0.0001

    print(f"Writing process index to {output_file}...")
    with open(output_file, "w") as f:
        json.dump(process_index, f, indent=2)

    print("\nIndexing complete!")

if __name__ == "__main__":
    # We start from the parent directory of this script to scan the whole project
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    index_output_file = os.path.join(project_root, "config/processindex.json")
    generate_process_index(project_root, index_output_file)

