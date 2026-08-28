import os
import uuid
import hashlib
import platform
import json

LICENSE_FILE = "lujan_vault_license.dat"

def get_hardware_id():
    """Generates a stable, unique hardware identifier for the device."""
    # 1. Get MAC address based node
    mac_node = str(uuid.getnode())
    
    # 2. Get OS specific machine ID if possible
    machine_id = "unknown"
    system = platform.system()
    try:
        if system == "Linux" or system == "Android":
            if os.path.exists("/etc/machine-id"):
                with open("/etc/machine-id", "r") as f:
                    machine_id = f.read().strip()
            elif os.path.exists("/var/lib/dbus/machine-id"):
                with open("/var/lib/dbus/machine-id", "r") as f:
                    machine_id = f.read().strip()
        elif system == "Windows":
            import subprocess
            output = subprocess.check_output('wmic csproduct get uuid').decode('utf-8').split('\n')[1].strip()
            machine_id = output
    except Exception:
        pass

    # Hash them together to create a 1-Device footprint
    raw_footprint = f"{mac_node}_{machine_id}_{system}"
    return hashlib.sha256(raw_footprint.encode()).hexdigest()

def activate_license(purchase_key):
    """
    Binds the purchase key to this specific hardware footprint.
    In a real scenario, this would query a backend server to ensure the key
    isn't already bound to another hardware ID.
    """
    hw_id = get_hardware_id()
    
    # We simulate a "server validation" and save the license locally
    license_data = {
        "key": purchase_key,
        "hw_id": hw_id,
        "active": True
    }
    
    with open(LICENSE_FILE, "w") as f:
        json.dump(license_data, f)
        
    return True

def verify_license():
    """
    Checks if the local license file matches the current hardware ID.
    """
    if not os.path.exists(LICENSE_FILE):
        return False
        
    try:
        with open(LICENSE_FILE, "r") as f:
            data = json.load(f)
            
        if data.get("active") and data.get("hw_id") == get_hardware_id():
            return True
            
    except Exception:
        pass
        
    return False
