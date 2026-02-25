
import hashlib
import argparse

def generate_sovereign_variables(secret_key):
    """
    Generates 24 unique and deterministic variables from a secret key.
    This is the core of the Cyclic Cypher Engine, creating the foundation
    for the entire personal cypher.
    """
    # Use SHA-512 for a larger hash output to ensure enough entropy
    # for 24 variables.
    hasher = hashlib.sha512()
    hasher.update(secret_key.encode('utf-8'))
    hex_hash = hasher.hexdigest()

    # SHA-512 produces a 128-character hex string.
    # We will slice this into 24 variables. We need to decide on the length
    # of each variable. Let's use 5 characters per variable for now,
    # which uses 120 characters from the hash.
    variables = []
    variable_length = 5
    for i in range(24):
        start = i * variable_length
        end = start + variable_length
        variable_slice = hex_hash[start:end]
        variables.append(variable_slice)

    return variables

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate the 24 Sovereign Variables from a secret key."
    )
    parser.add_argument(
        "--key",
        type=str,
        required=True,
        help="The secret passphrase to seed the cypher."
    )
    args = parser.parse_args()

    sovereign_variables = generate_sovereign_variables(args.key)

    print("--- Sovereign Cypher Variables ---")
    for i, var in enumerate(sovereign_variables):
        print(f"Var {i+1:02d}: {var}")
    print("----------------------------------")
    print(f"Generated {len(sovereign_variables)} variables from key.")

