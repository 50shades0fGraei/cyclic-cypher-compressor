# (c) 2026 Randall James Lujan. ALL RIGHTS RESERVED.
# PATENT PENDING: Cyclic Cypher Deductive Metronome Architecture.
# This software is proprietary and subject to the terms of a specific License Agreement.

import os
import subprocess

# Create a dummy video file
dummy_video = "test_video.mp4"
with open(dummy_video, "wb") as f:
    f.write(os.urandom(1024 * 1024 * 2)) # 2MB of random data

secret = "my_personal_secret_123"

print("--- Testing Personal Vault Store (Profile: primary) ---")
try:
    subprocess.run(["python3", "-m", "personal_vault_system.personal_vault", "store", dummy_video, "--secret", secret, "--profile", "primary"], check=True)
except subprocess.CalledProcessError as e:
    print(f"Store failed: {e}")

print("\n--- Testing Personal Vault Restore (Profile: primary) ---")
restored_video = "restored_primary.mp4"
try:
    subprocess.run(["python3", "-m", "personal_vault_system.personal_vault", "restore", dummy_video + ".pv6", "--secret", secret, "--profile", "primary", "--output", restored_video], check=True)
except subprocess.CalledProcessError as e:
    print(f"Restore failed: {e}")

print("\n--- Testing Personal Vault Restore (Profile: mismatch) ---")
try:
    # This should fail due to profile mismatch
    subprocess.run(["python3", "-m", "personal_vault_system.personal_vault", "restore", dummy_video + ".pv6", "--secret", secret, "--profile", "wrong_profile", "--output", "failed.mp4"], check=True)
except subprocess.CalledProcessError:
    print("Caught expected profile mismatch failure.")

# Verify primary success
if os.path.exists(restored_video):
    with open(dummy_video, "rb") as f1, open(restored_video, "rb") as f2:
        if f1.read() == f2.read():
            print("\nSUCCESS: Restored video matches original for profile: primary!")
        else:
            print("\nFAILURE: Restored video differs from original!")
else:
    print("\nFAILURE: Restored file not found!")

# Cleanup
# os.remove(dummy_video)
# os.remove(dummy_video + ".pv6")
# os.remove(restored_video)
