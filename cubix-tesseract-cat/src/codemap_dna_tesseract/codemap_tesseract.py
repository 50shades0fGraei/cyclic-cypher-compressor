# codemap_tesseract.py

import random
from .codemap_constants import TRAITS, PLANES, DUALITY

# --- New: Executable Actions ---
# Here, we map specific traits to actual, callable Python functions. This is the
# core of turning the symbolic representation into an executable one.

def execute_integrity_check():
    """Simulates an integrity check action."""
    print("EXECUTING: Integrity Check")

def execute_adaptation_routine():
    """Simulates an adaptation action."""
    print("EXECUTING: Adaptation Routine")

def execute_recursion_step():
    """Simulates a recursion action."""
    print("EXECUTING: Recursion Step")

# This dictionary acts as a registry, mapping a trait's name to its
# corresponding executable function. This is far more efficient than searching
# the filesystem for a script to run.
EXECUTABLE_TRAITS = {
    "Integrity": execute_integrity_check,
    "Adaptation": execute_adaptation_routine,
    "Recursion": execute_recursion_step,
}
# --- End of New Section ---


class CodemapTesseract:
    def __init__(self, generation=0, parent=None):
        self.generation = generation
        self.parent = parent
        self.traits = self.lock_traits()
        self.path = self.compile_path()
        self.output = self.manifest_entity()
        self.child = None

    def lock_traits(self):
        # Randomly select 4 traits for this tesseract
        return random.sample(TRAITS, 4)

    def compile_path(self):
        # Build a symbolic execution path from traits and planes
        return {
            "planes": random.sample(PLANES, 4),
            "duality": random.choice(DUALITY),
            "traits": self.traits
        }

    def manifest_entity(self):
        # Create a symbolic print of this tesseract's identity
        return {
            "type": "Codemap Entity",
            "generation": self.generation,
            "traits": self.traits,
            "path": self.path
        }

    # --- New: invoke Method ---
    def invoke(self):
        """
        This is the heart of "Codemap Invocation."
        Instead of searching for and interpreting a script, it directly executes
        the action associated with this tesseract's traits via a dictionary lookup.
        This is designed to be significantly faster and more efficient.
        """
        print(f"\n--- Invoking Tesseract (Generation: {self.generation}) ---")
        print(f"Traits: {self.traits}")
        for trait in self.traits:
            # Direct dictionary lookup and function call
            action = EXECUTABLE_TRAITS.get(trait)
            if action:
                action()
            else:
                # This trait doesn't have a direct action in this demo,
                # but it could in a more complex system.
                print(f"INFO: Trait '{trait}' has no executable action.")
    # --- End of New Section ---

    def build_next_tesseract(self):
        # Recursive expansion
        self.child = CodemapTesseract(generation=self.generation + 1, parent=self)
        return self.child
