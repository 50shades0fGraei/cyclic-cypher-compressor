"""Process router: intercepts process calls and routes to function addresses.

Replaces traditional process execution with function dispatch via process map.
"""
import subprocess
import sys
from typing import List, Optional, Dict, Any
from .process_mapper import get_function_address, load_process_map
from .runtime.host import call_address


class ProcessRouter:
    """Routes process calls to function addresses instead of executing binaries."""

    def __init__(self):
        self.process_map = load_process_map()
        self.cache = {}

    def resolve_process(self, process_name: str) -> Optional[str]:
        """Resolve process name to function address."""
        base_name = process_name.lower().split(".")[0]
        return self.process_map.get(base_name)

    def execute_process(self, process_name: str, args: List[str] = None, **kwargs) -> Any:
        """Execute a process by routing to its mapped function address.

        Falls back to subprocess if no mapping exists.
        """
        address = self.resolve_process(process_name)

        if address:
            print(f"🔗 Routing process '{process_name}' to function address: {address}")
            try:
                result = call_address(address, args=args or [])
                return result
            except Exception as e:
                print(f"⚠️  Function dispatch failed: {e}. Falling back to subprocess.")
                return self._fallback_execute(process_name, args, **kwargs)
        else:
            # No mapping; fall back to normal subprocess execution
            return self._fallback_execute(process_name, args, **kwargs)

    def _fallback_execute(self, process_name: str, args: List[str] = None, **kwargs):
        """Fallback: execute process normally using subprocess."""
        cmd = [process_name] + (args or [])
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=kwargs.get("timeout", 30))
            return {"returncode": result.returncode, "stdout": result.stdout, "stderr": result.stderr}
        except Exception as e:
            return {"error": str(e)}

    def call_process(self, process_cmd: str, *args) -> Any:
        """High-level call: execute <process_name> with args."""
        parts = process_cmd.split()
        return self.execute_process(parts[0], args=parts[1:] + list(args))


def register_program_functions(library: Dict[str, tuple], program_name: str, max_funcs: int = 5):
    """Auto-register top functions from a program in the library."""
    from .process_mapper import register_process
    count = 0
    for addr, (file_path, func_name) in library.items():
        if program_name.lower() in file_path.lower() and count < max_funcs:
            register_process(f"{program_name}_{func_name}", addr)
            count += 1


if __name__ == "__main__":
    # Simple CLI test
    router = ProcessRouter()
    if len(sys.argv) > 1:
        result = router.call_process(sys.argv[1], *sys.argv[2:])
        print(f"Result: {result}")
    else:
        print("Usage: process_router.py <process_name> [args...]")
        print("Mappings:")
        for proc, addr in router.process_map.items():
            print(f"  {proc} -> {addr}")
