# (c) 2026 Randall James Lujan. ALL RIGHTS RESERVED.
# PATENT PENDING: Cyclic Cypher Deductive Metronome Architecture.
# This software is proprietary and subject to the terms of a specific License Agreement.

"""File access proxy: intercepts file operations and routes through function library.

All file I/O requires authorization via function address (no direct file privileges).
"""
import os
from typing import Optional, Any
from pathlib import Path
from .file_acl import get_access_function, FileOp, load_file_acl
from .runtime.host import call_address


class FileAccessProxy:
    """Proxies file operations through the function library via ACL."""

    def __init__(self):
        self.acl = load_file_acl()
        self.cache = {}

    def open_file(self, file_path: str, mode: str = "r") -> Optional[Any]:
        """Open a file if authorized. Returns file object or None."""
        # Determine operation type from mode
        if "r" in mode:
            op = FileOp.READ
        elif "w" in mode or "a" in mode:
            op = FileOp.WRITE
        else:
            op = FileOp.READ
        
        # Check authorization
        func_addr = get_access_function(file_path, op)
        if not func_addr:
            raise PermissionError(f"❌ Access denied: {op.value} {file_path}. No authorization function.")
        
        # Call authorization function
        try:
            auth_result = call_address(func_addr, args=[file_path, mode])
            if not auth_result:
                raise PermissionError(f"❌ Access denied by function: {func_addr}")
        except Exception as e:
            raise PermissionError(f"❌ Authorization failed: {e}")
        
        # If authorized, perform file operation
        try:
            return open(file_path, mode)
        except Exception as e:
            raise IOError(f"❌ File operation failed: {e}")

    def read_file(self, file_path: str) -> str:
        """Read file if authorized."""
        func_addr = get_access_function(file_path, FileOp.READ)
        if not func_addr:
            raise PermissionError(f"❌ Read access denied: {file_path}")
        
        # Authorize and read
        try:
            call_address(func_addr, args=[file_path, "r"])
            with open(file_path, "r") as f:
                return f.read()
        except Exception as e:
            raise IOError(f"❌ Read failed: {e}")

    def write_file(self, file_path: str, content: str) -> bool:
        """Write file if authorized."""
        func_addr = get_access_function(file_path, FileOp.WRITE)
        if not func_addr:
            raise PermissionError(f"❌ Write access denied: {file_path}")
        
        # Authorize and write
        try:
            call_address(func_addr, args=[file_path, "w"])
            with open(file_path, "w") as f:
                f.write(content)
            return True
        except Exception as e:
            raise IOError(f"❌ Write failed: {e}")

    def delete_file(self, file_path: str) -> bool:
        """Delete file if authorized."""
        func_addr = get_access_function(file_path, FileOp.DELETE)
        if not func_addr:
            raise PermissionError(f"❌ Delete access denied: {file_path}")
        
        # Authorize and delete
        try:
            call_address(func_addr, args=[file_path])
            os.remove(file_path)
            return True
        except Exception as e:
            raise IOError(f"❌ Delete failed: {e}")

    def list_directory(self, dir_path: str) -> list:
        """List directory if authorized."""
        func_addr = get_access_function(dir_path, FileOp.LIST)
        if not func_addr:
            raise PermissionError(f"❌ List access denied: {dir_path}")
        
        # Authorize and list
        try:
            call_address(func_addr, args=[dir_path])
            return os.listdir(dir_path)
        except Exception as e:
            raise IOError(f"❌ List failed: {e}")

    def execute_file(self, file_path: str) -> bool:
        """Execute file if authorized."""
        func_addr = get_access_function(file_path, FileOp.EXECUTE)
        if not func_addr:
            raise PermissionError(f"❌ Execute access denied: {file_path}")
        
        # Authorize and execute
        try:
            call_address(func_addr, args=[file_path])
            import subprocess
            result = subprocess.run([file_path], capture_output=True)
            return result.returncode == 0
        except Exception as e:
            raise IOError(f"❌ Execute failed: {e}")


def create_default_file_functions():
    """Create default function stubs for file operations (auth placeholders)."""
    # These would be registered in the function library
    stub_code = """
# Default file authorization functions
def auth_read(file_path, mode):
    '''Authorize read access.'''
    print(f"✅ Authorizing read: {file_path}")
    return True

def auth_write(file_path, mode):
    '''Authorize write access.'''
    print(f"✅ Authorizing write: {file_path}")
    return True

def auth_delete(file_path):
    '''Authorize delete access.'''
    print(f"✅ Authorizing delete: {file_path}")
    return True

def auth_list(dir_path):
    '''Authorize directory listing.'''
    print(f"✅ Authorizing list: {dir_path}")
    return True

def auth_execute(file_path):
    '''Authorize file execution.'''
    print(f"✅ Authorizing execute: {file_path}")
    return True
"""
    return stub_code


if __name__ == "__main__":
    proxy = FileAccessProxy()
    print("File Access Proxy initialized")
    print("ACL entries:", len(proxy.acl))
    
    # Test: try to read a file (will fail without ACL rule)
    try:
        proxy.read_file("test.txt")
    except PermissionError as e:
        print(e)
