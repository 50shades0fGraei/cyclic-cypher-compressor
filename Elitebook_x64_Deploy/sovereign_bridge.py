import json
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from librarian_vault_manager import LibrarianVaultManager
from gapci_security_protocol import GapciSecuritySystem, DarkArchive, BalancePointFramework, UniversalDownloadGate

from system_cleaner import organize_sovereign_workspace

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
    Uses Python Standard Library Only.
    """
    
    def _set_headers(self, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        # Handle CORS for browser communication
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers()

    def do_GET(self):
        if self.path == '/omni/alerts':
            # Poll for any new system or security alerts for GRAEI to display
            self._set_headers()
            alerts = list(system_alerts)
            system_alerts.clear() # Reset on read
            self.wfile.write(json.dumps({"alerts": alerts}).encode())
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Path not found"}).encode())

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        payload = json.loads(post_data.decode('utf-8'))

        if self.path == '/librarian/summon':
            # UI Summons a sequence of DNA addresses
            sequence = payload.get('sequence', [])
            print(f"[BRIDGE] UI Summons Sequence: {sequence}")
            result = librarian.summon_sequence(sequence)
            
            self._set_headers()
            self.wfile.write(json.dumps({"status": "SUCCESS", "result": str(result)}).encode())

        elif self.path == '/gapci/assess':
            # UI routes a "downloaded file" to the GAPCI sandbox
            filename = payload.get('filename')
            behavior = payload.get('behavior', []) # Simulated logs from UI interaction
            print(f"[BRIDGE] UI Request: Assess Download '{filename}'")
            status = download_gate.assess_download(filename, behavior)
            
            # If quarantined, add to the GRAEI alert stream
            if status == "QUARANTINED":
                system_alerts.append(f"CRITICAL: Malicious Entity Captured in GAPCI Sandbox - '{filename}'")
            
            self._set_headers()
            self.wfile.write(json.dumps({"status": status}).encode())

        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Unknown API path"}).encode())

def run_bridge(port=8081):
    server_address = ('', port)
    httpd = HTTPServer(server_address, SovereignBridgeHandler)
    print(f"\n==================================================")
    print(f" SOVEREIGN BRIDGE: ONLINE AT PORT {port}")
    print(f" [Linkage: 3D UI <-> Python GRAEI Core]")
    print(f"==================================================\n")
    httpd.serve_forever()

if __name__ == "__main__":
    run_bridge()
