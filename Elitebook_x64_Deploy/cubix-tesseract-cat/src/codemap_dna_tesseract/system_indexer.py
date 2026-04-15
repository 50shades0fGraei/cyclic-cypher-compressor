"""System-wide indexer: scans computer's programs and builds device-specific function library.

Discovers Python/JavaScript files from Program Files, AppData, and user directories.
Generates addressable function library stored in user's config directory.
"""
import os
import json
import ast
import hashlib
from pathlib import Path
from typing import Dict, List, Tuple, Set
import platform


def get_library_path() -> Path:
    """Return path to device-specific function library cache."""
    if platform.system() == "Windows":
        config_dir = Path(os.getenv("APPDATA", os.path.expanduser("~"))) / "CodemapOS" / "library"
    else:
        config_dir = Path.home() / ".codemapOS" / "library"
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir


def get_common_program_paths() -> List[Path]:
    """Return list of common paths to scan for programs."""
    paths = []
    if platform.system() == "Windows":
        paths.extend([
            Path("C:/Program Files"),
            Path("C:/Program Files (x86)"),
            Path(os.path.expanduser("~/AppData/Roaming")),
            Path(os.path.expanduser("~/AppData/Local")),
        ])
    else:
        paths.extend([
            Path("/usr/local/bin"),
            Path("/opt"),
            Path.home() / ".local" / "bin",
        ])
    return [p for p in paths if p.exists()]


def discover_functions_from_file(file_path: str, max_functions: int = 50) -> List[Tuple[str, int]]:
    """Parse Python/JS file and extract functions. Returns (func_name, line_number)."""
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except Exception:
        return []

    funcs = []

    # Python AST parsing
    if file_path.endswith(".py"):
        try:
            tree = ast.parse(content, filename=file_path)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    funcs.append((node.name, node.lineno))
        except Exception:
            pass

    # Basic JavaScript regex parsing (simple heuristic)
    elif file_path.endswith((".js", ".ts")):
        import re
        # Match function declarations and arrow functions
        pattern = r"(?:function\s+(\w+)|const\s+(\w+)\s*=|let\s+(\w+)\s*=|var\s+(\w+)\s*=)"
        for match in re.finditer(pattern, content):
            name = next((g for g in match.groups() if g), None)
            if name:
                line_no = content[:match.start()].count("\n") + 1
                funcs.append((name, line_no))

    return funcs[:max_functions]


def scan_directory(base_path: Path, max_files: int = 500, exclude_dirs: Set[str] = None) -> Dict[str, List[Tuple[str, int]]]:
    """Recursively scan directory for Python/JS files and extract functions."""
    if exclude_dirs is None:
        exclude_dirs = {"__pycache__", ".git", "node_modules", ".venv", "venv", ".pytest_cache", "build", "dist"}

    file_functions = {}
    file_count = 0

    try:
        for root, dirs, files in os.walk(base_path):
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            for file in files:
                if file_count >= max_files:
                    return file_functions
                if file.endswith((".py", ".js", ".ts")):
                    file_path = os.path.join(root, file)
                    try:
                        funcs = discover_functions_from_file(file_path)
                        if funcs:
                            file_functions[file_path] = funcs
                            file_count += 1
                    except Exception:
                        pass
    except Exception:
        pass

    return file_functions


def build_system_library(scan_paths: List[Path] = None, max_total: int = 1000) -> Dict[str, Tuple[str, str]]:
    """Scan system paths and build function library. Returns address -> (file_path, func_name)."""
    if scan_paths is None:
        scan_paths = get_common_program_paths()

    library = {}
    total_funcs = 0
    file_func_map = {}

    for scan_path in scan_paths:
        if total_funcs >= max_total:
            break
        print(f"Scanning {scan_path}...")
        discovered = scan_directory(scan_path, max_files=200)
        file_func_map.update(discovered)
        total_funcs += sum(len(funcs) for funcs in discovered.values())

    # Generate addresses (program:purpose:filehash:func_index)
    func_idx = 0
    for file_path, funcs in sorted(file_func_map.items()):
        prog = Path(file_path).parent.name[:1].upper() or "X"
        file_hash = hashlib.md5(file_path.encode()).hexdigest()[:4].upper()

        for func_name, line_no in funcs:
            purpose = func_name[0].upper() if func_name else "X"
            address = f"{prog}:{purpose}:{file_hash}:{func_idx}"
            library[address] = (file_path, func_name)
            func_idx += 1

    return library


def save_library(library: Dict[str, Tuple[str, str]]):
    """Save device-specific library to disk."""
    lib_path = get_library_path() / "system_library.json"
    data = {
        "device": platform.node(),
        "platform": platform.system(),
        "total_functions": len(library),
        "library": {addr: {"file": fp, "function": fn} for addr, (fp, fn) in library.items()},
    }
    with open(lib_path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Saved library to {lib_path} ({len(library)} functions)")
    return lib_path


def load_library() -> Dict[str, Tuple[str, str]]:
    """Load device-specific library from disk."""
    lib_path = get_library_path() / "system_library.json"
    if not lib_path.exists():
        return {}
    try:
        with open(lib_path, "r") as f:
            data = json.load(f)
        return {addr: (info["file"], info["function"]) for addr, info in data.get("library", {}).items()}
    except Exception:
        return {}


if __name__ == "__main__":
    # Install/index system
    print("🔍 Scanning system for programs...")
    lib = build_system_library()
    save_library(lib)
    print(f"✅ System library created: {len(lib)} functions indexed")
