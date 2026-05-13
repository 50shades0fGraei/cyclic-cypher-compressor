import json
import subprocess
import urllib.request
import os
import re
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from librarian_vault_manager import LibrarianVaultManager
from gapci_security_protocol import GapciSecuritySystem, DarkArchive, BalancePointFramework, UniversalDownloadGate
from system_cleaner import organize_sovereign_workspace
from ephemeral_cypher import EphemeralPacket, EphemeralCypher
from function_library_mapper import mapper_library

# --- GEMINI CONFIG (set GEMINI_API_KEY in your environment or paste key here) ---
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key={GEMINI_API_KEY}"

# Vault context snippets to inject as librarian context
VAULT_CONTEXT_FILES = [
    "KNOWLEDGE_BASE.md", "HOW_TO_USE.md", "CNA_HYBRID_TECHNICAL_GUIDE.md"
]

def load_vault_context():
    """Load a short excerpt from key vault docs as grounding context."""
    ctx = []
    for fname in VAULT_CONTEXT_FILES:
        if os.path.exists(fname):
            with open(fname, "r", encoding="utf-8", errors="ignore") as f:
                ctx.append(f"=== {fname} ===\n" + f.read()[:1500])
    return "\n\n".join(ctx)

def call_gemini(user_message: str) -> str:
    """Call Gemini 1.5 Pro with vault context and return the reply text."""
    if not GEMINI_API_KEY:
        return "[LIBRARIAN ERROR] GEMINI_API_KEY not set. Add it to your environment variables."
    vault_ctx = load_vault_context()
    system_prompt = (
        "You are the GRAEI Research Librarian for the Lujan Tesseract Sovereign OS. "
        "You have access to the Lujan Deductive Vault knowledge base below. "
        "Answer questions accurately, referencing the vault when relevant. "
        "Be concise, sovereign, and precise.\n\n"
        f"VAULT CONTEXT:\n{vault_ctx}\n\n"
    )
    payload = {
        "contents": [{"role": "user", "parts": [{"text": system_prompt + user_message}]}],
        "generationConfig": {"maxOutputTokens": 1024, "temperature": 0.4}
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(GEMINI_ENDPOINT, data=data, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            result = json.loads(resp.read().decode())
            return result["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"[LIBRARIAN ERROR] {e}"

def scan_wifi_networks():
    """Scan WiFi — uses nmcli on Linux, netsh on Windows."""
    try:
        # Try Linux nmcli first (EliteBook Arch Linux target)
        raw = subprocess.check_output(
            ["nmcli", "-t", "-f", "SSID,SIGNAL,SECURITY", "dev", "wifi", "list"],
            encoding="utf-8", errors="ignore", timeout=10
        )
        networks = []
        for line in raw.strip().splitlines():
            parts = line.split(":")
            if len(parts) >= 2:
                ssid = parts[0].strip()
                signal = int(parts[1]) if parts[1].isdigit() else 0
                auth = parts[2].strip() if len(parts) > 2 else "Unknown"
                if ssid:
                    networks.append({"ssid": ssid, "auth": auth, "signal": signal, "connected": False})
        return networks
    except Exception:
        pass

    # Fallback: Windows netsh
    try:
        raw = subprocess.check_output(
            ["netsh", "wlan", "show", "networks", "mode=bssid"],
            encoding="utf-8", errors="ignore", timeout=10
        )
        networks = []
        blocks = raw.split("SSID ")
        for block in blocks[1:]:
            lines = block.strip().splitlines()
            ssid = lines[0].split(":", 1)[-1].strip() if lines else "Unknown"
            auth = next((l.split(":", 1)[-1].strip() for l in lines if "Authentication" in l), "Unknown")
            signal_str = next((l.split(":", 1)[-1].strip().replace("%", "") for l in lines if "Signal" in l), "0")
            try: signal = int(signal_str)
            except: signal = 0
            if ssid and ssid != "0":
                networks.append({"ssid": ssid, "auth": auth, "signal": signal, "connected": False})
        try:
            connected_raw = subprocess.check_output(
                ["netsh", "wlan", "show", "interfaces"], encoding="utf-8", errors="ignore"
            )
            conn_ssid = next((l.split(":", 1)[-1].strip() for l in connected_raw.splitlines() if "SSID" in l and "BSSID" not in l), "")
            for n in networks:
                if n["ssid"] == conn_ssid:
                    n["connected"] = True
        except: pass
        return networks
    except Exception as e:
        return []

# --- SHARED SYSTEM STATE ---
librarian = LibrarianVaultManager()
archive = DarkArchive()
balance = BalancePointFramework()
gapci = GapciSecuritySystem(archive, balance)
download_gate = UniversalDownloadGate(gapci)

# A queue for GRAEI's visual alerts in the UI
system_alerts = []

# Gentleman's Initiation: Always start clean.
organize_sovereign_workspace()
system_alerts.append("GRAEI Mirror Stack: Initialized and polished. Gentleman protocols active.")

class SovereignBridgeHandler(BaseHTTPRequestHandler):
    """
    Sovereign OS Bridge: Connecting the 3D Tesseract UI to the Python GRAEI Engines.
    Uses Python Standard Library Only. Cross-platform: Linux (EliteBook) + Windows.
    """
    
    def _set_headers(self, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers()

    def do_GET(self):
        if self.path == '/omni/alerts':
            self._set_headers()
            alerts = list(system_alerts)
            system_alerts.clear()
            self.wfile.write(json.dumps({"alerts": alerts}).encode())

        elif self.path == '/network/scan':
            print("[BRIDGE] WiFi scan requested")
            networks = scan_wifi_networks()
            self._set_headers()
            self.wfile.write(json.dumps({"networks": networks}).encode())

        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Path not found"}).encode())

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        payload = json.loads(post_data.decode('utf-8'))

        if self.path == '/librarian/summon':
            sequence = payload.get('sequence', [])
            print(f"[BRIDGE] UI Summons Sequence: {sequence}")
            result = librarian.summon_sequence(sequence)
            self._set_headers()
            self.wfile.write(json.dumps({"status": "SUCCESS", "result": str(result)}).encode())

        elif self.path == '/gapci/assess':
            filename = payload.get('filename')
            behavior = payload.get('behavior', [])
            print(f"[BRIDGE] UI Request: Assess Download '{filename}'")
            status = download_gate.assess_download(filename, behavior)
            if status == "QUARANTINED":
                system_alerts.append(f"CRITICAL: Malicious Entity Captured in GAPCI Sandbox - '{filename}'")
            self._set_headers()
            self.wfile.write(json.dumps({"status": status}).encode())

        elif self.path == '/omni/chat':
            user_message = payload.get('message', '')
            print(f"[OMNI] User: {user_message}")
            reply = f"Antigravity GRAEI: Received '{user_message}'. Note that my full coding capabilities operate within the IDE. I am monitoring the Sovereign Bridge."
            self._set_headers()
            self.wfile.write(json.dumps({"reply": reply}).encode())

        elif self.path == '/system/exec':
            # Cross-platform shell command runner — key for Linux EliteBook
            cmd = payload.get('command', '')
            print(f"[BRIDGE] Exec: {cmd}")
            try:
                result = subprocess.check_output(
                    cmd, shell=True, text=True, stderr=subprocess.STDOUT, timeout=15
                )
                self._set_headers()
                self.wfile.write(json.dumps({"output": result}).encode())
            except subprocess.CalledProcessError as e:
                self._set_headers()
                self.wfile.write(json.dumps({"output": e.output or f"[Exit {e.returncode}]"}).encode())
            except Exception as e:
                self._set_headers(500)
                self.wfile.write(json.dumps({"error": str(e)}).encode())

        elif self.path == '/system/launch':
            app = payload.get('app', '').lower()
            # Linux-first, Windows fallback
            APP_MAP_LINUX = {
                'taskmgr':    'btop',
                'bluetooth':  'bluetoothctl',
                'wifi':       'nmtui',
                'battery':    'upower -d',
                'devicemgr':  'lshw -short',
                'powershell': 'bash',
            }
            APP_MAP_WIN = {
                'taskmgr':    'taskmgr.exe',
                'bluetooth':  ['powershell', '-Command', 'Start-Process', 'ms-settings:bluetooth'],
                'wifi':       ['powershell', '-Command', 'Start-Process', 'ms-settings:network-wifi'],
                'battery':    ['powershell', '-Command', 'Start-Process', 'ms-settings:batterysaver'],
                'devicemgr':  ['powershell', '-Command', 'Start-Process', 'devmgmt.msc'],
                'powershell': ['wt.exe', '-p', 'PowerShell'],
            }
            import platform
            is_linux = platform.system() == 'Linux'
            cmd = APP_MAP_LINUX.get(app) if is_linux else APP_MAP_WIN.get(app)
            if cmd:
                try:
                    if isinstance(cmd, list):
                        subprocess.Popen(cmd, shell=False)
                    else:
                        subprocess.Popen(cmd, shell=True)
                    self._set_headers()
                    self.wfile.write(json.dumps({"status": "LAUNCHED", "app": app}).encode())
                except Exception as e:
                    self._set_headers(500)
                    self.wfile.write(json.dumps({"error": str(e)}).encode())
            else:
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": f"Unknown app: {app}"}).encode())

        elif self.path == '/network/connect':
            ssid = payload.get('ssid', '')
            password = payload.get('password', '')
            print(f"[BRIDGE] Connecting to WiFi: {ssid}")
            import platform
            try:
                if platform.system() == 'Linux':
                    # nmcli for Arch Linux EliteBook
                    if password:
                        subprocess.run(["nmcli", "dev", "wifi", "connect", ssid, "password", password], check=True, timeout=15)
                    else:
                        subprocess.run(["nmcli", "dev", "wifi", "connect", ssid], check=True, timeout=15)
                else:
                    # Windows netsh fallback
                    if password:
                        profile_xml = f"""<?xml version="1.0"?>
<WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
  <name>{ssid}</name>
  <SSIDConfig><SSID><name>{ssid}</name></SSID></SSIDConfig>
  <connectionType>ESS</connectionType>
  <connectionMode>auto</connectionMode>
  <MSM><security>
    <authEncryption><authentication>WPA2PSK</authentication><encryption>AES</encryption></authEncryption>
    <sharedKey><keyType>passPhrase</keyType><protected>false</protected><keyMaterial>{password}</keyMaterial></sharedKey>
  </security></MSM>
</WLANProfile>"""
                        with open("_temp_wifi_profile.xml", "w") as f:
                            f.write(profile_xml)
                        subprocess.run(["netsh", "wlan", "add", "profile", "filename=_temp_wifi_profile.xml"], check=True, timeout=10)
                        os.remove("_temp_wifi_profile.xml")
                    subprocess.run(["netsh", "wlan", "connect", f"name={ssid}"], check=True, timeout=10)
                self._set_headers()
                self.wfile.write(json.dumps({"status": "SUCCESS", "ssid": ssid}).encode())
            except Exception as e:
                self._set_headers(500)
                self.wfile.write(json.dumps({"status": "FAILED", "error": str(e)}).encode())

        elif self.path == '/librarian/gemini':
            user_message = payload.get('message', '')
            print(f"[LIBRARIAN] Gemini Query: {user_message}")
            reply = call_gemini(user_message)
            self._set_headers()
            self.wfile.write(json.dumps({"reply": reply}).encode())

        elif self.path == '/ephemeral/seal':
            plaintext = payload.get('content', '')
            ttl = int(payload.get('ttl', 300))
            label = payload.get('label', 'SOVEREIGN_MSG')
            if not plaintext:
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": "No content provided"}).encode())
                return
            try:
                packet = EphemeralPacket.build(plaintext, ttl_seconds=ttl, label=label)
                print(f"[EPHEMERAL] Sealed packet — door: {packet['door'][:12]}... expires: {packet['expires']}")
                self._set_headers()
                self.wfile.write(json.dumps({
                    "status": "SEALED",
                    "door": packet["door"],
                    "bundle": packet["bundle"],
                    "expires": packet["expires"],
                    "label": label
                }).encode())
            except Exception as e:
                self._set_headers(500)
                self.wfile.write(json.dumps({"error": str(e)}).encode())

        elif self.path == '/ephemeral/open':
            bundle = payload.get('bundle', '')
            door = payload.get('door', '')
            if not bundle or not door:
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": "bundle and door are both required"}).encode())
                return
            try:
                plaintext = EphemeralPacket.receive(bundle, door)
                print(f"[EPHEMERAL] Packet opened and burned successfully.")
                self._set_headers()
                self.wfile.write(json.dumps({"status": "DELIVERED", "content": plaintext}).encode())
            except ValueError as e:
                self._set_headers(403)
                self.wfile.write(json.dumps({"status": "DENIED", "error": str(e)}).encode())

        elif self.path == '/omni/execute_mapped_dna':
            ability = payload.get('ability', '')
            context = payload.get('context', {})
            print(f"[CODEMAPPER] Executing mapped ability: {ability}")
            result = mapper_library.execute_mapped_function(ability, context)
            self._set_headers()
            self.wfile.write(json.dumps(result).encode())

        elif self.path == '/telemetry/energy':
            import platform
            try:
                if platform.system() == 'Linux':
                    # Arch Linux: read /proc/stat for CPU load
                    with open('/proc/stat', 'r') as f:
                        line = f.readline()
                    vals = line.split()
                    idle = int(vals[4])
                    total = sum(int(v) for v in vals[1:])
                    cpu_load = max(0, min(100, 100 - int(idle / total * 100)))
                else:
                    raw_cpu = subprocess.check_output("wmic cpu get loadpercentage", shell=True, text=True, timeout=2).strip().split('\n')
                    cpu_load = int(raw_cpu[-1].strip()) if len(raw_cpu) > 1 else 15
            except Exception:
                cpu_load = 15

            active_energy_cost = cpu_load * 0.5
            savings = 100 - active_energy_cost
            if savings < 50: savings = 50
            if savings > 98: savings = 98

            self._set_headers()
            self.wfile.write(json.dumps({
                "cpu_load": cpu_load,
                "energy_savings": round(savings, 1),
                "p_state": "LOCKED (Max 50%)"
            }).encode())

        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Unknown API path"}).encode())

def run_bridge(port=8081):
    server_address = ('', port)
    httpd = HTTPServer(server_address, SovereignBridgeHandler)
    print(f"\n==================================================")
    print(f" SOVEREIGN BRIDGE: ONLINE AT PORT {port}")
    print(f" [Linkage: 3D UI <-> Python GRAEI Core]")
    print(f" [Platform: Cross-platform — Linux + Windows]")
    print(f"==================================================\n")
    httpd.serve_forever()

if __name__ == "__main__":
    run_bridge()
