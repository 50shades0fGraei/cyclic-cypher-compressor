# Launch Cubix OS as a standalone desktop application using MS Edge / Chrome App Mode
Write-Host "Initializing Sovereign Bridge & HTTP Server..." -ForegroundColor Cyan

# Start the background Python servers
Start-Process python -ArgumentList "-m http.server 8000" -WindowStyle Hidden
Start-Process python -ArgumentList "sovereign_bridge.py" -WindowStyle Hidden

Start-Sleep -Seconds 2

Write-Host "Launching Cubix OS UI without standard browser interface..." -ForegroundColor Green

# Launch the browser in App Mode (Borderless, no tabs, no address bar)
try {
    # Attempt Chrome first
    Start-Process "chrome.exe" -ArgumentList "--app=http://localhost:8000/cubix_os.html" -ErrorAction Stop
} catch {
    # Fallback to Edge if Chrome is not in PATH
    Start-Process "msedge.exe" -ArgumentList "--app=http://localhost:8000/cubix_os.html"
}

Write-Host "Done! You can now use the Cubix UI side by side with your IDE." -ForegroundColor Yellow
