#!/bin/bash
# CyberDNA: Arch Linux LightDM Provisioner
# Sets up a Randall Desktop Environment (Tesseract OS) using LightDM on Arch Linux

echo "--- CyberDNA: Arch Linux Provisioner ---"

# 1. Install prerequisites via Pacman
echo "[PACMAN] Installing required packages (lightdm, xorg, chromium, python)..."
sudo pacman -Syu --needed --noconfirm lightdm xorg-server chromium python

# 2. Prepare Randall OS Directory
INSTALL_DIR="/opt/cubix_os"
echo "[INSTALL] Injecting Cubix OS & Lujan Vault stack to $INSTALL_DIR..."
sudo mkdir -p $INSTALL_DIR
sudo cp -r ./Latitude_Deploy/* $INSTALL_DIR/

# Optional: Copy Python backend tools required by QuickVault terminal logic if needed locally in the deployment
sudo cp lujan_vault.py Lujan_SaaS_API.py $INSTALL_DIR/ 2>/dev/null
sudo cp -r core double_crunch_marketplace.py $INSTALL_DIR/ 2>/dev/null

# 3. Create Launch Wrapper
WRAPPER_SCRIPT="/usr/local/bin/start-cubix-os.sh"
echo "[SCRIPT] Creating launch wrapper at $WRAPPER_SCRIPT..."
cat << 'EOF' | sudo tee $WRAPPER_SCRIPT > /dev/null
#!/bin/bash
# (Optional) Start Python Backend Service here if required:
# cd /opt/cubix_os && python3 Lujan_SaaS_API.py &

# Start the Randall Edge Browser in Kiosk/Fullscreen Mode
exec chromium --start-fullscreen --app=file:///opt/cubix_os/cubix_os.html --allow-file-access-from-files
EOF
sudo chmod +x $WRAPPER_SCRIPT

# 4. Create LightDM Session
SESSION_FILE="/usr/share/xsessions/cubix.desktop"
echo "[LIGHTDM] Creating X11 Session Entry..."
sudo mkdir -p /usr/share/xsessions
cat << EOF | sudo tee $SESSION_FILE > /dev/null
[Desktop Entry]
Name=Cubix OS Randall Environment
Comment=Tesseract Environment Bridge
Exec=$WRAPPER_SCRIPT
Type=Application
EOF

echo ""
echo "[POST-INSTALL] Setting optimal power policies for Linux (Simulating ACPI Scheme_Max)..."
# Setting CPU governor to performance (requires cpupower)
sudo pacman -S --needed --noconfirm cpupower
sudo cpupower frequency-set -g performance >/dev/null 2>&1

echo ""
echo "[SUCCESS] Randall Vault Provisioned for Arch Linux."
echo "You can now log out and select 'Cubix OS Randall Environment' from the LightDM login screen."
