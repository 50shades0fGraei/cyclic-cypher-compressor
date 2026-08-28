#!/bin/bash
# Lujan Randall Vault: Native Linux Compiler

echo "=========================================================="
echo "LUJAN RANDALL VAULT: INITIATING LINUX COMPILATION"
echo "=========================================================="

BUILD_TYPE=$1
APP_NAME="Lujan_Vault_Linux"
APP_TYPE_STR="UNIVERSAL"

if [ "$BUILD_TYPE" == "media" ]; then
    APP_NAME="Randall_Media_Vault_Linux"
    APP_TYPE_STR="MEDIA"
elif [ "$BUILD_TYPE" == "docs" ]; then
    APP_NAME="Randall_Document_Vault_Linux"
    APP_TYPE_STR="DOCUMENT"
else
    echo "Usage: ./build_linux.sh [media|docs]"
    echo "Building default universal vault..."
fi

echo "Fetching PyInstaller environment..."
./.venv/bin/pip install pyinstaller

echo "Preparing build source..."
cp windows_vault_gui.py temp_build_gui.py
sed -i "s/APP_TYPE = \"UNIVERSAL\"/APP_TYPE = \"$APP_TYPE_STR\"/g" temp_build_gui.py

echo "Compiling temp_build_gui.py into ${APP_NAME} ELF Binary..."
./.venv/bin/pyinstaller --noconfirm --onefile --windowed \
    --name "$APP_NAME" \
    --add-data "core:core/" \
    --add-data "double_crunch_marketplace.py:." \
    temp_build_gui.py

rm temp_build_gui.py

echo "=========================================================="
echo "COMPILATION SUCCESSFUL."
echo "Native Linux executable generated at: ./dist/${APP_NAME}"
echo "=========================================================="
