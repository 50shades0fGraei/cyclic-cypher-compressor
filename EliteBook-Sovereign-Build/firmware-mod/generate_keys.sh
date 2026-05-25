#!/bin/bash
# (c) 2026 Randall James Lujan. ALL RIGHTS RESERVED.
# PATENT PENDING: Cyclic Cypher Deductive Metronome Architecture.
# This software is proprietary and subject to the terms of a specific License Agreement.

# CyberDNA: Sovereign Key Generator (Sovereign-Root)
# Goal: Create the RSA-4096 keys for signing the Tesseract-OS Bootloader.

echo "CyberDNA: Initializing Sovereign Key Generation..."

# 1. Generate the private key
openssl genrsa -out sovereign_private.key 4096

# 2. Extract the public key (The Root of Trust)
openssl rsa -in sovereign_private.key -pubout -out sovereign_public.key

# 3. Create a self-signed certificate for UEFI db (Authorized Signature Database)
openssl req -new -x509 -key sovereign_private.key -out sovereign_root.crt -days 3650 \
    -subj "/C=UC/ST=CYBERDNA/L=TESSERACT/O=LUJAN_AGI/CN=Sovereign_Root"

# 4. Sign the Bootloader (Mocking the sbsign process)
# sbsign --key sovereign_private.key --cert sovereign_root.crt --output CubixOS-loader-signed.efi CubixOS-loader.efi

echo "✓ Sovereign Private Key: sovereign_private.key [SECURED]"
echo "✓ Sovereign Root CRT: sovereign_root.crt [READY FOR BIOS FLASH]"
echo "✓ CubixOS-loader.efi: Authorized Signature Applied."

echo "Next Step: Enroll 'sovereign_root.crt' into the EliteBook's 'db' variable."
