# LUJAN DEDUCTIVE VAULT: Latitude Quick-Drop Utility
# Drag and drop any file onto this script to secure it in the Vault.

param(
    [Parameter(Mandatory=$true, ValueFromRemainingArguments=$true)]
    [string[]]$Files
)

$VaultRoot = "c:\Users\randall\cyclic-cypher-compressor"
$VaultScript = "$VaultRoot\lujan_vault.py"

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "   LUJAN DEDUCTIVE VAULT: QUICK-DROP" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

foreach ($file in $Files) {
    if (Test-Path $file) {
        $absPath = (Get-Item $file).FullName
        Write-Host "Targeting: $absPath" -ForegroundColor Yellow
        
        # Execute the Deep Storage Store command
        python $VaultScript store $absPath --deep --double
        
        # Trigger Windows Notification Integration
        python "$VaultRoot\Lujan_Windows_Bridge.py" "Deep Storage / Double-Crunch (90%) Applied Successfully."
    }
}

Write-Host "`nVaulting Process Complete." -ForegroundColor Green
Write-Host "Press any key to close..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
