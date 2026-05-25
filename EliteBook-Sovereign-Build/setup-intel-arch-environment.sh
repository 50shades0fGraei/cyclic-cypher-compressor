#!/bin/bash
# (c) 2026 Randall James Lujan. ALL RIGHTS RESERVED.
# PATENT PENDING: Cyclic Cypher Deductive Metronome Architecture.
# This software is proprietary and subject to the terms of a specific License Agreement.

# ═══════════════════════════════════════════════════════════════════════
#  CyberDNA: Intel i5 vPro GPU & Video Setup for Arch Linux
#  Target: HP EliteBook (Intel i5 vPro)
#
#  What this does:
#  Installs the necessary Intel graphics drivers, X11, and Chromium 
#  so the command-line Arch build can open the 3D Cubix Environment.
# ═══════════════════════════════════════════════════════════════════════

set -e

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║   CyberDNA: Intel i5 vPro Arch Linux Environment Setup      ║"
echo "╚══════════════════════════════════════════════════════════════╝"

# 1. Update package database
echo "[ STEP 1 ] Updating pacman database..."
sudo pacman -Sy

# 2. Install Intel GPU, Media, and Vulkan drivers
echo "[ STEP 2 ] Installing Intel GPU, Media, and Vulkan drivers..."
# We use --needed to avoid reinstalling if already present
sudo pacman -S --noconfirm --needed mesa vulkan-intel intel-media-driver libva-intel-driver xf86-video-intel

# 3. Install X11 and dependencies for graphical environment
echo "[ STEP 3 ] Installing Xorg, Xinit, and Chromium for Cubix OS..."
sudo pacman -S --noconfirm --needed xorg-server xorg-xinit chromium xterm python alsa-utils

# 4. Create the Cubix OS launcher
echo "[ STEP 4 ] Creating Cubix OS launcher script (launch_cubix.sh)..."
LAUNCHER_PATH="$HOME/launch_cubix.sh"

cat > "$LAUNCHER_PATH" << 'EOF'
#!/bin/bash
# Launch the Sovereign Tesseract Cubix Environment

# Start local python server for the environment
killall python 2>/dev/null || true
killall python3 2>/dev/null || true

# Find the repository directory
if [ -d "$HOME/cyclic-cypher-compressor" ]; then
    cd "$HOME/cyclic-cypher-compressor"
elif [ -d "$(pwd)/cyclic-cypher-compressor" ]; then
    cd "$(pwd)/cyclic-cypher-compressor"
else
    # Fallback to current directory if script is run from within the repo
    cd "$(dirname "$0")"
fi

echo "Starting UI server in $(pwd)..."
python3 -m http.server 8080 >/dev/null 2>&1 &
SERVER_PID=$!

# Configure X11 to launch Chromium in kiosk mode
cat > ~/.xinitrc << 'XINIT'
# Disable screen blanking
xset s off
xset -dpms
xset s noblank

# Launch Cubix OS
exec chromium --kiosk --no-sandbox http://localhost:8080/cubix_os.html
XINIT

# Start X
echo "Launching Graphical Environment..."
startx

# Cleanup server when X exits
kill $SERVER_PID
EOF

chmod +x "$LAUNCHER_PATH"

# 5. Optional: Autostart configuration
echo "[ STEP 5 ] Configuring ~/.bash_profile for optional autostart..."
if ! grep -q "launch_cubix.sh" ~/.bash_profile 2>/dev/null; then
    cat >> ~/.bash_profile << 'EOF'

# Auto-launch Tesseract Cubix OS on tty1
if [ "$(tty)" = "/dev/tty1" ]; then
    ~/launch_cubix.sh
fi
EOF
fi

echo ""
echo "[✓] EliteBook Intel i5 GPU and GUI environment setup complete."
echo "    You can now run:  ~/launch_cubix.sh  from the terminal"
echo "    or just reboot to automatically start the Cubix OS on tty1."
