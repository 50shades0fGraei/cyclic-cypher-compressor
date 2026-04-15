"""File access proxy: mediates all file I/O through the function library.

No direct file access allowed. All file operations require mapped function authorization.
Stores file access rules persistently in ACL.
"""
import json
import os
from pathlib import Path
from typing import Dict, Optional, List, Tuple
import platform
from enum import Enum


class FileOp(Enum):
    """File operation types."""
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    EXECUTE = "execute"
    LIST = "list"


def get_file_acl_path() -> Path:
    """Return path to device-specific file access control list."""
    if platform.system() == "Windows":
        config_dir = Path(os.getenv("APPDATA", os.path.expanduser("~"))) / "CodemapOS" / "files"
    else:
        config_dir = Path.home() / ".codemapOS" / "files"
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir


def load_file_acl() -> Dict[str, Dict[str, str]]:
    """Load file access control list.

    Format:
    {
        "/path/to/file.txt": {
            "read": "X:R:ABC1:5",     # function address for read access
            "write": "X:W:ABC1:6"     # function address for write access
        },
        "/path/to/folder/*": {
            "read": "X:R:ABC1:7",     # wildcard for folder
            "list": "X:L:ABC1:8"
        }
    }
    """
    acl_file = get_file_acl_path() / "file_acl.json"
    if not acl_file.exists():
        return {}
    try:
        with open(acl_file, "r") as f:
            return json.load(f)
    except Exception:
        return {}


def save_file_acl(acl: Dict[str, Dict[str, str]]):
    """Save file ACL to disk."""
    acl_file = get_file_acl_path() / "file_acl.json"
    with open(acl_file, "w") as f:
        json.dump(acl, f, indent=2)
    print(f"✅ File ACL saved ({len(acl)} entries)")


def grant_file_access(file_path: str, operation: FileOp, function_address: str):
    """Grant a function permission to perform an operation on a file."""
    acl = load_file_acl()
    if file_path not in acl:
        acl[file_path] = {}
    acl[file_path][operation.value] = function_address
    save_file_acl(acl)
    print(f"✅ Granted {operation.value} access to {file_path} via {function_address}")


def revoke_file_access(file_path: str, operation: FileOp):
    """Revoke a file operation permission."""
    acl = load_file_acl()
    if file_path in acl and operation.value in acl[file_path]:
        del acl[file_path][operation.value]
        save_file_acl(acl)
        print(f"✅ Revoked {operation.value} access from {file_path}")
    else:
        print(f"⚠️  No access rule found for {file_path}")


def _match_path(pattern: str, file_path: str) -> bool:
    """Match a file path against an ACL pattern (supports * wildcard)."""
    import fnmatch
    return fnmatch.fnmatch(file_path, pattern) or fnmatch.fnmatch(file_path, pattern + "/*")


def get_access_function(file_path: str, operation: FileOp) -> Optional[str]:
    """Get function address that can perform operation on file, if authorized."""
    acl = load_file_acl()
    
    # Check exact match
    if file_path in acl and operation.value in acl[file_path]:
        return acl[file_path][operation.value]
    
    # Check wildcard patterns
    for acl_path, ops in acl.items():
        if _match_path(acl_path, file_path) and operation.value in ops:
            return ops[operation.value]
    
    return None


def list_file_acl() -> List[Tuple[str, str, str]]:
    """List all file access rules as (file_path, operation, function_address)."""
    acl = load_file_acl()
    result = []
    for file_path, ops in sorted(acl.items()):
        for op, addr in ops.items():
            result.append((file_path, op, addr))
    return result


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "list":
            rules = list_file_acl()
            print("File Access Rules:")
            print("=" * 80)
            for path, op, addr in rules:
                print(f"  {path:<40} {op:<10} {addr}")
        elif cmd == "grant" and len(sys.argv) > 4:
            grant_file_access(sys.argv[2], FileOp(sys.argv[3]), sys.argv[4])
        elif cmd == "revoke" and len(sys.argv) > 3:
            revoke_file_access(sys.argv[2], FileOp(sys.argv[3]))
    else:
        print("Usage: file_acl.py [list|grant <path> <op> <address>|revoke <path> <op>]")
        print("Operations:", ", ".join([op.value for op in FileOp]))
