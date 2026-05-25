# (c) 2026 Randall James Lujan. ALL RIGHTS RESERVED.
# PATENT PENDING: Cyclic Cypher Deductive Metronome Architecture.
# This software is proprietary and subject to the terms of a specific License Agreement.

"""Virtual data store: retrieves data by executing bound functions on demand.

Data is computed on-demand by calling the function address bound to a data id.
Supports optional caching.
"""
from typing import Any, Optional
from functools import lru_cache

try:
    from .data_binding import get_binding
    from .runtime.host import call_address
except Exception:
    from codemap_dna_tesseract.data_binding import get_binding
    from codemap_dna_tesseract.runtime.host import call_address


def get_data(data_id: str, args: Optional[list] = None, kwargs: Optional[dict] = None, use_cache: bool = True) -> Any:
    binding = get_binding(data_id)
    if not binding:
        raise KeyError(f"No binding for data id: {data_id}")
    address = binding.get("address")
    if not address:
        raise KeyError(f"Binding for {data_id} has no address")

    if use_cache:
        return _cached_call(address, args or [], kwargs or {})
    return call_address(address, args=args or [], kwargs=kwargs or {})


@lru_cache(maxsize=256)
def _cached_call(address: str, args_tuple, kwargs_dict):
    # lru_cache requires hashable args; convert to tuple/str
    # Note: args_tuple expected to be tuple-serializable; we accept simple use-case here.
    try:
        # Convert kwargs string to avoid unhashable dict
        return call_address(address, args=list(args_tuple), kwargs=kwargs_dict)
    except Exception as e:
        raise


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "get":
        print(get_data(sys.argv[2]))
    else:
        print("Usage: virtual_data_store.py get <data_id>")
