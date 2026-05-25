#!/bin/bash
# (c) 2026 Randall James Lujan. ALL RIGHTS RESERVED.
# PATENT PENDING: Cyclic Cypher Deductive Metronome Architecture.
# This software is proprietary and subject to the terms of a specific License Agreement.

# ═══════════════════════════════════════════════════════════════════════════
#  LUJAN TESSERACT OS — Sovereign Boot Launcher
#  Author: Randall Lujan | AGE-I Sovereign Stack
#  Run: ./launch_cubix.sh
#  No internet. No Chromium flags. No manual setup.
# ═══════════════════════════════════════════════════════════════════════════

set -e

# ── 1. Find repo root ────────────────────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
DEPLOY_DIR="$SCRIPT_DIR"
HTML_FILE="$DEPLOY_DIR/cubix_os.html"
BRIDGE_PY="$DEPLOY_DIR/sovereign_bridge.py"
ELECTRON_DIR="$REPO_ROOT/Cyberdna-tesseract-os"

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║   LUJAN TESSERACT OS — Sovereign Boot                       ║"
echo "║   Randall Lujan | AGE-I Art-Gen Emotion-Intel               ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "  Deploy dir : $DEPLOY_DIR"
echo "  HTML       : $HTML_FILE"
echo ""

# ── 2. Verify the UI file exists ─────────────────────────────────────────────
if [ ! -f "$HTML_FILE" ]; then
    echo "[ERROR] cubix_os.html not found at $HTML_FILE"
    echo "        Run: git pull origin main  — then try again."
    exit 1
fi

# ── 3. Kill any stale processes ──────────────────────────────────────────────
pkill -f sovereign_bridge.py 2>/dev/null || true
pkill -f "http.server"       2>/dev/null || true
pkill chromium               2>/dev/null || true
pkill electron               2>/dev/null || true

# ── 4. Start sovereign_bridge.py in background ───────────────────────────────
if [ -f "$BRIDGE_PY" ]; then
    echo "[BRIDGE] Starting sovereign_bridge.py..."
    python3 "$BRIDGE_PY" > /tmp/sovereign_bridge.log 2>&1 &
    BRIDGE_PID=$!
    sleep 1
    echo "[BRIDGE] PID $BRIDGE_PID — logs at /tmp/sovereign_bridge.log"
else
    echo "[BRIDGE] sovereign_bridge.py not found — skipping (UI will still load)"
fi

# ── 5. Detect display server ─────────────────────────────────────────────────
if [ -n "$WAYLAND_DISPLAY" ]; then
    OZONE="wayland"
elif [ -n "$DISPLAY" ]; then
    OZONE="x11"
else
    OZONE="x11"   # bare tty — startx will set $DISPLAY
fi
echo "[DISPLAY] Ozone platform: $OZONE"

# ── 6. Launch strategy: Electron → Chromium → Firefox ────────────────────────
launch_electron() {
    echo "[LAUNCH] Using Electron (self-contained, no flags needed)..."
    cd "$ELECTRON_DIR"
    # Install deps if node_modules missing
    if [ ! -d "node_modules" ]; then
        echo "[INSTALL] Running npm install..."
        npm install --prefer-offline 2>&1 | tail -5
    fi
    exec npx electron . --no-sandbox
}

launch_chromium() {
    local BIN="$1"
    echo "[LAUNCH] Using $BIN..."
    # Write a clean xinitrc if we're not already in X
    if [ -z "$DISPLAY" ]; then
        cat > ~/.xinitrc << XINIT
xset s off
xset -dpms
xset s noblank
exec $BIN \
    --ozone-platform=$OZONE \
    --no-sandbox \
    --kiosk \
    --disable-infobars \
    --noerrdialogs \
    --disable-session-crashed-bubble \
    "file://$HTML_FILE"
XINIT
        startx
    else
        exec "$BIN" \
            --ozone-platform="$OZONE" \
            --no-sandbox \
            --kiosk \
            "file://$HTML_FILE"
    fi
}

# Try Electron first (cleanest), then Chromium variants, then Firefox
if [ -d "$ELECTRON_DIR/node_modules" ] || command -v npx &>/dev/null; then
    if [ -f "$ELECTRON_DIR/package.json" ]; then
        launch_electron
    fi
fi

if command -v chromium &>/dev/null; then
    launch_chromium chromium
elif command -v chromium-browser &>/dev/null; then
    launch_chromium chromium-browser
elif command -v google-chrome &>/dev/null; then
    launch_chromium google-chrome
elif command -v firefox &>/dev/null; then
    echo "[LAUNCH] Using Firefox..."
    [ -z "$DISPLAY" ] && { echo "exec firefox --kiosk file://$HTML_FILE" > ~/.xinitrc && startx; } \
                      || exec firefox --kiosk "file://$HTML_FILE"
else
    echo "[ERROR] No browser or Electron found. Install one:"
    echo "        sudo pacman -S electron  OR  sudo pacman -S chromium"
    exit 1
fi
