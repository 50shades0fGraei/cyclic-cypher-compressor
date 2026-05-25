# (c) 2026 Randall James Lujan. ALL RIGHTS RESERVED.
# PATENT PENDING: Cyclic Cypher Deductive Metronome Architecture.
# This software is proprietary and subject to the terms of a specific License Agreement.

"""Spiral pipeline: organizes auto-indexed functions into a spiral structure.

Each function becomes a node in the spiral, addressable and invokable through the pipeline.
Functions are ordered by program, purpose, line number.
"""
import json
from typing import Dict, List, Tuple, Any
from .runtime.auto_indexer import index_repository


class PipelineNode:
    """A function node in the spiral pipeline."""
    def __init__(self, address: str, module_name: str, func_name: str, generation: int = 0, parent=None):
        self.address = address
        self.module_name = module_name
        self.func_name = func_name
        self.generation = generation
        self.parent = parent
        self.children = []
        self.traits = [module_name.split(".")[-1], func_name, address]
        self.path = {
            "address": address,
            "module": module_name,
            "function": func_name,
        }

    def to_dict(self):
        return {
            "address": self.address,
            "generation": self.generation,
            "module": self.module_name,
            "function": self.func_name,
            "traits": self.traits,
            "path": self.path,
        }


class FunctionSpiral:
    """A spiral of function nodes, ordered by address."""
    def __init__(self):
        self.root = None
        self.all_nodes = []
        self.address_map = {}

    def build_from_index(self, index: Dict[str, Tuple[str, str]]):
        """Build spiral from auto-indexed functions."""
        # Sort addresses for consistent ordering
        sorted_addrs = sorted(index.keys())
        if not sorted_addrs:
            return

        # Create root node from first function
        addr = sorted_addrs[0]
        mod, func = index[addr]
        self.root = PipelineNode(addr, mod, func, generation=0)
        self.all_nodes.append(self.root)
        self.address_map[addr] = self.root

        # Build spiral chain
        current = self.root
        for gen, addr in enumerate(sorted_addrs[1:], start=1):
            mod, func = index[addr]
            node = PipelineNode(addr, mod, func, generation=gen, parent=current)
            current.children.append(node)
            self.all_nodes.append(node)
            self.address_map[addr] = node
            current = node

    def get_node(self, address: str) -> PipelineNode:
        """Retrieve a node by address."""
        return self.address_map.get(address)

    def call_address(self, address: str, args=None, kwargs=None):
        """Invoke function at address through the spiral pipeline."""
        node = self.get_node(address)
        if not node:
            raise KeyError(f"address not in spiral: {address}")

        # Import and invoke
        import importlib
        mod = importlib.import_module(node.module_name)
        func = getattr(mod, node.func_name)
        return func(*(args or []), **(kwargs or {}))

    def list_functions(self, program_prefix: str = None) -> List[Dict]:
        """List all functions in the spiral, optionally filtered by program."""
        result = []
        for node in self.all_nodes:
            if program_prefix is None or node.address.startswith(program_prefix):
                result.append(node.to_dict())
        return result

    def to_dict(self):
        """Serialize spiral to dictionary."""
        return {
            "root": self.root.to_dict() if self.root else None,
            "total_nodes": len(self.all_nodes),
            "functions": [n.to_dict() for n in self.all_nodes],
        }


def create_spiral(root_path: str = "src") -> FunctionSpiral:
    """Create a spiral from auto-indexed functions."""
    spiral = FunctionSpiral()
    index = index_repository(root_path)
    spiral.build_from_index(index)
    return spiral


if __name__ == "__main__":
    # Test: create and print spiral
    spiral = create_spiral()
    print(json.dumps(spiral.to_dict(), indent=2))
