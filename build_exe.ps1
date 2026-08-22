# Lujan Sovereign Vault: Executable Compiler

Write-Host "=========================================================="
Write-Host "LUJAN SOVEREIGN VAULT: INITIATING STANDALONE COMPILATION"
Write-Host "=========================================================="

# Ensure PyInstaller is installed
pip install pyinstaller

# Compile the GUI script with hidden console and standalone logic
# We add core/ as a data dependency so it hooks into the engine correctly
Write-Host "Compiling windows_vault_gui.py into Lujan_Vault.exe..."
pyinstaller --noconfirm --onefile --windowed `
    --name "Lujan_Vault" `
    --add-data "core;core/" `
    --add-data "double_crunch_marketplace.py;." `
    windows_vault_gui.py

Write-Host "=========================================================="
Write-Host "COMPILATION SUCCESSFUL."
Write-Host "Artifact generated at: ./dist/Lujan_Vault.exe"
Write-Host "You can now distribute this standalone file on the $80 portal."
Write-Host "=========================================================="
