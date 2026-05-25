# Cyclic Password Generator

## Concept
A stateless, deterministic password generator powered by the Cyclic Cypher Compressor engine. 

Instead of storing passwords in a vulnerability-prone database (like LastPass), this tool dynamically generates unique, site-specific passwords on the fly using a master secret, the target website name, and the username. Because it relies on the internal 97-character encoding scheme, the output is highly entropic and perfectly reproducible.

## Features
- **Stateless:** Zero storage required. Passwords are never saved.
- **Site-Specific:** The same master password yields different results for `gmail` vs `github`.
- **High Entropy:** Utilizes the full 97-character keyboard alphabet for maximum password strength.

## Usage
Run the generator script and provide your master secret along with the site you want to generate a password for.
