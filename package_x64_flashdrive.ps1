# (c) 2026 Randall James Lujan. ALL RIGHTS RESERVED.
# PATENT PENDING: Cyclic Cypher Deductive Metronome Architecture.
# This software is proprietary and subject to the terms of a specific License Agreement.

$deployDir = "c:\Users\randall\cyclic-cypher-compressor\Elitebook_x64_Deploy"

Write-Host "Packaging Cubix UI and Antigravity Matrix for x64 EliteBook to $deployDir..."

# Arrays of files and folders
$files = @(
    "cubix_os.html", "cubix_os.css", "cubix_environment_core.js", 
    "cubix_logo_wallpaper.png", "cubix_logo_placeholder.txt",
    "tesseract_ui_demo.html", "tesseract_ui_demo.css", "tesseract_ui_demo.js",
    "agi_communication_matrix.py", "agi_deployment.py", "experience_bridge.py", 
    "gapci_security_protocol.py", "randall_bridge.py", "system_cleaner.py", 
    "system_polish.py", "msds1_vault_access.py", "librarian_vault_manager.py"
)

$folders = @(
    "graei_dna", "ReflectiveSpace", "core", "QuickVault", "cubix-tesseract-cat", "lib"
)

foreach ($f in $files) {
    if (Test-Path "c:\Users\randall\cyclic-cypher-compressor\$f") {
        Copy-Item -Path "c:\Users\randall\cyclic-cypher-compressor\$f" -Destination "$deployDir" -Force
    }
}

foreach ($d in $folders) {
    if (Test-Path "c:\Users\randall\cyclic-cypher-compressor\$d") {
        Copy-Item -Path "c:\Users\randall\cyclic-cypher-compressor\$d" -Destination "$deployDir\$d" -Recurse -Force
    }
}

Write-Host "✅ Files copied successfully."
