"""Spiral pipeline viewer: displays the function spiral with address information."""
import json
from .spiral_pipeline import PipelineNode


def print_spiral_pipeline(spiral):
    """Print the function spiral with addresses and traits."""
    if not spiral.root:
        print("Spiral is empty.")
        return

    def print_node(node: PipelineNode, depth: int = 0):
        indent = "  " * depth
        print(f"{indent}🌀 Generation {node.generation}")
        print(f"{indent}Address: {node.address}")
        print(f"{indent}Module: {node.module_name}")
        print(f"{indent}Function: {node.func_name}")
        print(f"{indent}Traits: {', '.join(node.traits)}")
        for child in node.children:
            print_node(child, depth + 1)

    print_node(spiral.root)


def print_function_library(spiral, program_prefix: str = None):
    """Print all functions in the spiral as a library listing."""
    functions = spiral.list_functions(program_prefix=program_prefix)
    if not functions:
        print("No functions found.")
        return

    print(f"\n📚 Function Library ({len(functions)} functions)")
    print("=" * 80)
    for func in functions:
        print(f"Address: {func['address']}")
        print(f"  Module: {func['module']}")
        print(f"  Function: {func['function']}")
        print(f"  Generation: {func['generation']}")
        print(f"  Traits: {', '.join(func['traits'])}")
        print()


def print_spiral_stats(spiral):
    """Print statistics about the spiral."""
    print(f"\n📊 Spiral Statistics")
    print("=" * 80)
    print(f"Total functions indexed: {len(spiral.all_nodes)}")
    print(f"Root address: {spiral.root.address if spiral.root else 'N/A'}")
    
    # Group by program prefix
    programs = {}
    for node in spiral.all_nodes:
        prog = node.address.split(":")[0]
        if prog not in programs:
            programs[prog] = 0
        programs[prog] += 1
    
    print(f"Programs/modules: {len(programs)}")
    for prog, count in sorted(programs.items()):
        print(f"  {prog}: {count} functions")
    print()
