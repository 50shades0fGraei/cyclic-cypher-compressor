# CyberDNA: Latitude Side-by-Side Provisioner (Diskpart Version)
# Creates a Native VHD for Cubix OS files using diskpart for compatibility.

$vhdPath = "C:\Sovereign_Vault.vhd"
$sourceDir = "c:\Users\randall\cyclic-cypher-compressor\Latitude_Deploy"
$tempScript = "$env:TEMP\vhd_script.txt"

Write-Host "--- CyberDNA: Latitude Side-by-Side Provisioner ---" -ForegroundColor Cyan

# 1. Create and Mount VHD using Diskpart
if (-not (Test-Path $vhdPath)) {
    Write-Host "[VHD] Creating 20GB Sovereign Vault at $vhdPath..."
    $script = @"
create vdisk file="$vhdPath" maximum=20480 type=expandable
attach vdisk
create partition primary
format fs=ntfs label="CubixOS_Vault" quick
assign letter=S
"@
    $script | Out-File -FilePath $tempScript -Encoding ASCII
    diskpart /s $tempScript
} else {
    Write-Host "[VHD] Vault already exists. Mounting..."
    $script = @"
select vdisk file="$vhdPath"
attach vdisk
assign letter=S
"@
    $script | Out-File -FilePath $tempScript -Encoding ASCII
    diskpart /s $tempScript
}

# 2. Inject Latitude Deployment Stack
if (Test-Path "S:\") {
    Write-Host "[INSTALL] Injecting Cubix OS & Lujan Vault stack to S:\..."
    Copy-Item -Path "$sourceDir\*" -Destination "S:\" -Recurse -Force
    
    # 3. Create the Sovereign Boot Shortcut
    Write-Host "[SHORTCUT] Creating desktop bridge..."
    $WshShell = New-Object -ComObject WScript.Shell
    $Shortcut = $WshShell.CreateShortcut("$([Environment]::GetFolderPath('Desktop'))\Boot Cubix OS.lnk")
    
    # Target Edge or Chrome
    $browserPath = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    if (-not (Test-Path $browserPath)) { $browserPath = "msedge.exe" }
    
    $Shortcut.TargetPath = $browserPath
    $Shortcut.Arguments = "--app=file:///S:/cubix_os.html --start-fullscreen"
    $Shortcut.Description = "Launch Cubix OS Sovereign Environment"
    $Shortcut.Save()
    
    Write-Host "`n[POWER] Enforcing ACPI P-State Lock (Max Power Savings)..." -ForegroundColor Cyan
    powercfg /setactive scheme_max
    powercfg /setacvalueindex SCHEME_MAX SUB_PROCESSOR PROCTHROTTLEMAX 50
    powercfg /setdcvalueindex SCHEME_MAX SUB_PROCESSOR PROCTHROTTLEMAX 50
    powercfg /setactive scheme_max
    
    Write-Host "`n[SUCCESS] Sovereign Vault Provisioned Successfully." -ForegroundColor Green
    Write-Host "You now have a 'Boot Cubix OS' shortcut on your desktop."
    Write-Host "The Vault is currently mounted as Drive S:\"
} else {
    Write-Host "[ERROR] Failed to mount VHD to Drive S:. Please check Administrator privileges." -ForegroundColor Red
}

if (Test-Path $tempScript) { Remove-Item $tempScript }
