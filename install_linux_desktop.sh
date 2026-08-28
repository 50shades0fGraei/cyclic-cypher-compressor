#!/bin/bash
echo "Installing Double Crunch Vault to modern Linux desktop environment (LightDM compatible)..."

# Ensure directories exist
mkdir -p ~/.local/bin
mkdir -p ~/.local/share/applications
mkdir -p ~/.local/share/icons/hicolor/scalable/apps

# Copy the generated binary from dist folder if it exists
if [ -f "./dist/Randall_Media_Vault_Linux" ]; then
    echo "Copying application binary to ~/.local/bin/randall-media-vault ..."
    cp ./dist/Randall_Media_Vault_Linux ~/.local/bin/randall-media-vault
    chmod +x ~/.local/bin/randall-media-vault
else
    echo "ERROR: ./dist/Randall_Media_Vault_Linux not found! Build failed or was not run."
    exit 1
fi

# Copy icon
if [ -f "./cubix_icon.svg" ]; then
    echo "Copying icon to user hicolor directory..."
    cp ./cubix_icon.svg ~/.local/share/icons/hicolor/scalable/apps/
else
    echo "WARNING: cubix_icon.svg not found."
fi

# Copy desktop entry
if [ -f "./double-crunch.desktop" ]; then
    echo "Installing desktop entry launcher..."
    cp ./double-crunch.desktop ~/.local/share/applications/
else
    echo "WARNING: double-crunch.desktop not found."
fi

# Update desktop database
echo "Refreshing desktop database index..."
if command -v update-desktop-database > /dev/null; then
    update-desktop-database ~/.local/share/applications || true
fi

echo "Installation complete! You can now launch 'Double Crunch Vault' from your application menu."
