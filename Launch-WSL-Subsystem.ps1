# (c) 2026 Randall James Lujan. ALL RIGHTS RESERVED.
# PATENT PENDING: Cyclic Cypher Deductive Metronome Architecture.
# This software is proprietary and subject to the terms of a specific License Agreement.

# Launch Tesseract OS Build in WSL (Windows Subsystem for Linux)
# This will simulate the bare-metal Linux environment hosted natively via Windows Subsystem.

Write-Host "=========================================================" -ForegroundColor Cyan
Write-Host "   INITIALIZING SOVEREIGN BUILD IN WSL SUBSYSTEM         " -ForegroundColor Cyan
Write-Host "=========================================================" -ForegroundColor Cyan
Write-Host "Target: EliteBook x64 Deployment Environment Tests"

$DeployDir = "c:\Users\randall\cyclic-cypher-compressor\Elitebook_x64_Deploy"
$WslDir = "/mnt/c/Users/randall/cyclic-cypher-compressor/Elitebook_x64_Deploy"

# 1. Kill any existing instances on 8080/8081 via WSL
Write-Host "[1/3] Terminating any existing test bridges..."
wsl -e bash -c "kill `$(lsof -t -i:8080) 2>/dev/null; kill `$(lsof -t -i:8081) 2>/dev/null; exit 0"

# 2. Launch the components inside WSL using bash
Write-Host "[2/3] Booting Sovereign Bridge and HTTP Server in Linux Subsystem..."

# Start Sovereign Bridge (Python backend api for UI)
Start-Process wsl.exe -ArgumentList "-e", "bash", "-c", "cd '$WslDir' && python3 sovereign_bridge.py" -WindowStyle Minimized

# Start Python HTTP Server
Start-Process wsl.exe -ArgumentList "-e", "bash", "-c", "cd '$WslDir' && python3 -m http.server 8080" -WindowStyle Minimized

Start-Sleep -Seconds 3

# 3. Open the UI in edge/default browser on the host
Write-Host "[3/3] Opening Tesseract Cubix OS Interface in default browser..." -ForegroundColor Green
Start-Process "http://localhost:8080/cubix_os.html"

Write-Host "`n[✓] Subsystem successfully initialized. You can now test the EliteBook deployment."
Write-Host "    (Close the minimized WSL windows when you are done testing)" -ForegroundColor Yellow
