# (c) 2026 Randall James Lujan. ALL RIGHTS RESERVED.
# PATENT PENDING: Cyclic Cypher Deductive Metronome Architecture.
# This software is proprietary and subject to the terms of a specific License Agreement.

$deployDir = "c:\Users\randall\cyclic-cypher-compressor\Latitude_Deploy"

Write-Host "Packaging Cubix OS and Lujan Vault for Latitude to $deployDir..."

# Create deploy directory if it doesn't exist
if (-not (Test-Path $deployDir)) {
    New-Item -ItemType Directory -Force -Path $deployDir | Out-Null
}

# Arrays of files and folders
$files = @(
    "cubix_os.html", "cubix_os.css", "cubix_environment_core.js", 
    "cubix_logo_wallpaper.png", "cubix_logo_placeholder.txt",
    "Lujan_Latitude_Hub.html", "Lujan_Latitude_QuickVault.ps1",
    "lujan_vault.py", "Lujan_Windows_Bridge.py", "Lujan_SaaS_API.py",
    "LUJAN_VAULT_MVP.html", "COMMERCIAL_LANDING_PAGE.html",
    "lujan_wallpaper.png", "system_cleaner.py", "system_polish.py",
    "agent_dna_builder.html", "function_library_mapper.py", "vault_app.py", "Dockerfile.vaultUI", "docker-compose.vault.yml"
)

$folders = @(
    "QuickVault", "core", "lib", "cloud_landing_page", "templates", "static"
)

foreach ($f in $files) {
    if (Test-Path "c:\Users\randall\cyclic-cypher-compressor\$f") {
        Copy-Item -Path "c:\Users\randall\cyclic-cypher-compressor\$f" -Destination "$deployDir" -Force
    } else {
        Write-Warning "File not found: $f"
    }
}

foreach ($d in $folders) {
    if (Test-Path "c:\Users\randall\cyclic-cypher-compressor\$d") {
        Copy-Item -Path "c:\Users\randall\cyclic-cypher-compressor\$d" -Destination "$deployDir\$d" -Recurse -Force
    } else {
        Write-Warning "Folder not found: $d"
    }
}

Write-Host "✅ Latitude Deployment Packaged Successfully."
