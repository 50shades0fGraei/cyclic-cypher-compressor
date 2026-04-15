"""File manager wrapper: replaces explorer/file manager with function-mediated access.

All file operations go through the proxy and require authorization.
"""
import os
import json
from pathlib import Path
from typing import List, Dict
from .file_proxy import FileAccessProxy
from .file_acl import grant_file_access, FileOp


class VirtualFileManager:
    """Virtual file manager that mediates all file access through the function library."""

    def __init__(self):
        self.proxy = FileAccessProxy()
        self.current_dir = str(Path.home())

    def cd(self, path: str) -> bool:
        """Change directory if authorized."""
        abs_path = os.path.abspath(path)
        if not os.path.isdir(abs_path):
            print(f"❌ Not a directory: {abs_path}")
            return False
        
        try:
            files = self.proxy.list_directory(abs_path)
            self.current_dir = abs_path
            return True
        except PermissionError as e:
            print(e)
            return False

    def ls(self, path: str = None) -> List[str]:
        """List files in directory if authorized."""
        target = path or self.current_dir
        try:
            return self.proxy.list_directory(target)
        except PermissionError as e:
            print(e)
            return []

    def read(self, file_path: str) -> str:
        """Read file if authorized."""
        abs_path = os.path.abspath(file_path)
        try:
            return self.proxy.read_file(abs_path)
        except Exception as e:
            print(e)
            return ""

    def write(self, file_path: str, content: str) -> bool:
        """Write file if authorized."""
        abs_path = os.path.abspath(file_path)
        try:
            return self.proxy.write_file(abs_path, content)
        except Exception as e:
            print(e)
            return False

    def delete(self, file_path: str) -> bool:
        """Delete file if authorized."""
        abs_path = os.path.abspath(file_path)
        try:
            return self.proxy.delete_file(abs_path)
        except Exception as e:
            print(e)
            return False

    def status(self) -> Dict:
        """Print current status."""
        return {
            "current_dir": self.current_dir,
            "acl_rules": len(self.proxy.acl),
        }


def setup_default_file_access(function_address: str = "X:F:AUTH:0"):
    """Set up default file access rules using a default authorization function."""
    # Grant broad access with single authorization function
    home = str(Path.home())
    
    grant_file_access(f"{home}/*", FileOp.READ, function_address)
    grant_file_access(f"{home}/*", FileOp.WRITE, function_address)
    grant_file_access(f"{home}/*", FileOp.DELETE, function_address)
    grant_file_access(f"{home}/*", FileOp.LIST, function_address)
    grant_file_access(f"{home}/*", FileOp.EXECUTE, function_address)
    
    # Grant system access
    grant_file_access("/tmp/*", FileOp.READ, function_address)
    grant_file_access("/tmp/*", FileOp.WRITE, function_address)
    
    print(f"✅ Default file access initialized with function: {function_address}")


if __name__ == "__main__":
    import sys
    fm = VirtualFileManager()
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "ls":
            path = sys.argv[2] if len(sys.argv) > 2 else None
            files = fm.ls(path)
            for f in files:
                print(f)
        elif cmd == "cd" and len(sys.argv) > 2:
            if fm.cd(sys.argv[2]):
                print(f"📁 {fm.current_dir}")
        elif cmd == "read" and len(sys.argv) > 2:
            content = fm.read(sys.argv[2])
            print(content)
        elif cmd == "write" and len(sys.argv) > 3:
            if fm.write(sys.argv[2], sys.argv[3]):
                print(f"✅ Wrote {sys.argv[2]}")
        elif cmd == "delete" and len(sys.argv) > 2:
            if fm.delete(sys.argv[2]):
                print(f"✅ Deleted {sys.argv[2]}")
        elif cmd == "status":
            import json
            print(json.dumps(fm.status(), indent=2))
    else:
        print("Virtual File Manager")
        print(f"Current dir: {fm.current_dir}")
        print("Usage: file_manager.py [ls|cd|read|write|delete|status] [args...]")
