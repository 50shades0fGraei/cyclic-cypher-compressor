"""Data binding: maps logical data IDs to function addresses and metadata.

Bindings are stored per-device under the library config directory.
"""
import json
import platform
from pathlib import Path
from typing import Dict, Optional

try:
    from .system_indexer import get_library_path
except Exception:
    from codemap_dna_tesseract.system_indexer import get_library_path


def _bindings_path() -> Path:
    return get_library_path() / "data_bindings.json"


def load_bindings() -> Dict[str, Dict]:
    p = _bindings_path()
    if not p.exists():
        return {}
    try:
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_bindings(bindings: Dict[str, Dict]):
    p = _bindings_path()
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(bindings, f, indent=2)
    return p


def bind_data(data_id: str, function_address: str, description: str = "") -> None:
    bindings = load_bindings()
    bindings[data_id] = {"address": function_address, "description": description}
    save_bindings(bindings)


def unbind_data(data_id: str) -> None:
    bindings = load_bindings()
    if data_id in bindings:
        del bindings[data_id]
        save_bindings(bindings)


def get_binding(data_id: str) -> Optional[Dict]:
    bindings = load_bindings()
    return bindings.get(data_id)


if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 3 and sys.argv[1] == "bind":
        bind_data(sys.argv[2], sys.argv[3], "")
        print("bound")
    elif len(sys.argv) >= 2 and sys.argv[1] == "list":
        print(json.dumps(load_bindings(), indent=2))
    else:
        print("Usage: data_binding.py bind <data_id> <function_address> | list | unbind <data_id>")
