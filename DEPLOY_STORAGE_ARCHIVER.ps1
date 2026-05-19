# SOVEREIGN STORAGE ARCHIVER: DEPLOYMENT SCRIPT
# This script packages the QuickVault and its monetization bridge for deployment.

$projectName = "StorageArchiveDrop"
$distDir = "c:\Users\randall\cyclic-cypher-compressor\dist_archiver"

Write-Host "--- Initializing Sovereign Archive Deployment ---" -ForegroundColor Cyan

# 1. Prepare Distribution Directory
if (Test-Path $distDir) {
    Remove-Item -Path $distDir -Recurse -Force
}
New-Item -ItemType Directory -Path $distDir

# 2. Package Web Frontend (QuickVault)
Write-Host "Packaging QuickVault Frontend..." -ForegroundColor Yellow
Copy-Item -Path "c:\Users\randall\cyclic-cypher-compressor\QuickVault\*" -Destination $distDir -Recurse -Force

# 3. Package Sovereign Backend (Lujan Vault & API)
Write-Host "Packaging Sovereign API Backend..." -ForegroundColor Yellow
$backendFiles = @(
    "lujan_vault.py",
    "Lujan_SaaS_API.py",
    "c_drive_archiver.py",
    "integrity_enforcer_core.py",
    "requirements.txt"
)

foreach ($file in $backendFiles) {
    if (Test-Path "c:\Users\randall\cyclic-cypher-compressor\$file") {
        Copy-Item -Path "c:\Users\randall\cyclic-cypher-compressor\$file" -Destination $distDir -Force
    }
}

# 4. Create Azure Deployment Package
Write-Host "Preparing Azure ARM Template..." -ForegroundColor Yellow
Copy-Item -Path "c:\Users\randall\cyclic-cypher-compressor\dark_encryptor_standalone\azure-deployment.json" -Destination "$distDir\azure-deployment.json"

# 5. Generate Execution Script
$launchScript = @"
@echo off
echo ========================================================
echo   SOVEREIGN STORAGE ARCHIVER: STARTING REVENUE NODE
echo   Partner: meta2graei@gmail.com
echo ========================================================
echo.
echo 1. Starting Local Sovereign API (Port 8080)...
start /B python Lujan_SaaS_API.py
echo.
echo 2. Your Archive Drop is now active at: http://localhost:8080
echo.
echo 3. To make it PUBLIC on the market, run this in a new terminal:
echo    cloudflared.exe tunnel --url http://localhost:8080
echo.
echo Node Status: ACTIVE
echo Revenue Mode: ENABLED
pause
"@

$launchScript | Out-File -FilePath "$distDir\Launch_Archive_Node.bat" -Encoding ASCII

Write-Host "--- Deployment Package Ready at $distDir ---" -ForegroundColor Green
Write-Host "To go live:" -ForegroundColor White
Write-Host "1. Upload $distDir to your partner server."
Write-Host "2. Run 'Launch_Archive_Node.bat'."
Write-Host "3. Share the URL with users to begin generating revenue."
