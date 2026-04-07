"""Process address mapper: maps process names/commands to function addresses.

Allows replacing traditional process execution with function dispatch.
Stores device-specific process routing rules persistently.
"""
import json
import os
from pathlib import Path
from typing import Dict, Optional, List, Tuple
import platform


def get_process_rules_path() -> Path:
    """Return path to device-specific process routing rules."""
    if platform.system() == "Windows":
        config_dir = Path(os.getenv("APPDATA", os.path.expanduser("~"))) / "CodemapOS" / "processes"
    else:
        config_dir = Path.home() / ".codemapOS" / "processes"
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir


def load_process_map() -> Dict[str, str]:
    """Load process -> function address mappings.

    Format:
    {
        "notepad": "X:E:ABC1:5",           # map cmd to function address
        "explorer": "P:O:DEF2:10",
        "python": "X:R:GHI3:15",
    }
    """
    rules_file = get_process_rules_path() / "process_map.json"
    if not rules_file.exists():
        return {}
    try:
        with open(rules_file, "r") as f:
            return json.load(f)
    except Exception:
        return {}


def save_process_map(process_map: Dict[str, str]):
    """Save process routing map to disk."""
    rules_file = get_process_rules_path() / "process_map.json"
    with open(rules_file, "w") as f:
        json.dump(process_map, f, indent=2)
    print(f"✅ Process map saved ({len(process_map)} mappings)")


def register_process(process_name: str, function_address: str):
    """Register a process to be routed to a function address."""
    process_map = load_process_map()
    process_map[process_name.lower()] = function_address
    save_process_map(process_map)
    print(f"✅ Registered: {process_name} -> {function_address}")


def unregister_process(process_name: str):
    """Unregister a process from routing."""
    process_map = load_process_map()
    if process_name.lower() in process_map:
        del process_map[process_name.lower()]
        save_process_map(process_map)
        print(f"✅ Unregistered: {process_name}")
    else:
        print(f"⚠️  Process not found: {process_name}")


def get_function_address(process_name: str) -> Optional[str]:
    """Get function address for a process name, if mapped."""
    process_map = load_process_map()
    return process_map.get(process_name.lower())


def list_process_mappings() -> List[Tuple[str, str]]:
    """List all process -> function mappings."""
    return sorted(load_process_map().items())


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "list":
            mappings = list_process_mappings()
            print("Process Mappings:")
            print("=" * 60)
            for proc, addr in mappings:
                print(f"  {proc:<20} -> {addr}")
        elif cmd == "register" and len(sys.argv) > 3:
            register_process(sys.argv[2], sys.argv[3])
        elif cmd == "unregister" and len(sys.argv) > 2:
            unregister_process(sys.argv[2])
    else:
        print("Usage: process_mapper.py [list|register <name> <address>|unregister <name>]")
