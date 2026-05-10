#!/bin/bash
# LUJAN TESSERACT: Sovereign Launcher
# This script starts the desktop environment from the Arch TTY.

cd "$(dirname "$0")"

# 1. Check for dependencies
if ! command -v startx &> /dev/null; then
    echo "Error: Xorg (startx) not installed. Run: sudo pacman -S xorg-xinit"
    exit 1
fi

# 2. Setup the X session to launch Electron via Openbox
cat > ~/.xinitrc << 'EOF'
# Fix for the "Magic Cookie" xauth hex error
xset s off
xset -dpms
xset q

# Launch a tiny window manager to manage the Electron window
openbox &
sleep 1

# Launch the Tesseract
cd ~/cyclic-cypher-compressor
exec ./node_modules/.bin/electron . --no-sandbox
EOF

# 3. Fire it up
startx
