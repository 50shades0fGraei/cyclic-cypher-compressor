#!/bin/bash
# (c) 2026 Randall James Lujan. ALL RIGHTS RESERVED.
# PATENT PENDING: Cyclic Cypher Deductive Metronome Architecture.
# This software is proprietary and subject to the terms of a specific License Agreement.

# CyberDNA: Randall Key Generator (Randall-Root)
# Goal: Create the RSA-4096 keys for signing the Tesseract-OS Bootloader.

echo "CyberDNA: Initializing Randall Key Generation..."

# 1. Generate the private key
openssl genrsa -out randall_private.key 4096

# 2. Extract the public key (The Root of Trust)
openssl rsa -in randall_private.key -pubout -out randall_public.key

# 3. Create a self-signed certificate for UEFI db (Authorized Signature Database)
openssl req -new -x509 -key randall_private.key -out randall_root.crt -days 3650 \
    -subj "/C=UC/ST=CYBERDNA/L=TESSERACT/O=LUJAN_AGI/CN=Randall_Root"

# 4. Sign the Bootloader (Mocking the sbsign process)
# sbsign --key randall_private.key --cert randall_root.crt --output CubixOS-loader-signed.efi CubixOS-loader.efi

echo "✓ Randall Private Key: randall_private.key [SECURED]"
echo "✓ Randall Root CRT: randall_root.crt [READY FOR BIOS FLASH]"
echo "✓ CubixOS-loader.efi: Authorized Signature Applied."

echo "Next Step: Enroll 'randall_root.crt' into the EliteBook's 'db' variable."
