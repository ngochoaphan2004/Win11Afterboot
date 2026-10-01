<#
.SYNOPSIS
    Win11 After Boot - Quick One-Line Installer
.DESCRIPTION
    Downloads, creates shortcut, and launches Win11 After Boot.
.EXAMPLE
    & ([scriptblock]::Create((irm "https://raw.githubusercontent.com/ngochoaphan2004/Win11Afterboot/main/install.ps1")))
#>

[CmdletBinding()]
param(
    [string]$Repo = "ngochoaphan2004/Win11Afterboot"
)

$ErrorActionPreference = "Stop"
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

$targetDir = "$env:LOCALAPPDATA\Win11AfterBoot"
$exePath = "$targetDir\Win11AfterBoot.exe"
$releaseUrl = "https://github.com/$Repo/releases/latest/download/Win11AfterBoot.exe"

Write-Host ""
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "   🚀 Win11 After Boot v1.1.0 Installer      " -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

if (-not (Test-Path $targetDir)) {
    New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
}

Write-Host "[*] Downloading latest Win11 After Boot from $Repo..." -ForegroundColor Yellow

try {
    Invoke-WebRequest -Uri $releaseUrl -OutFile $exePath -UseBasicParsing
    Write-Host "[+] Download completed successfully!" -ForegroundColor Green

    # Create Desktop shortcut for convenient access
    try {
        $wshShell = New-Object -ComObject WScript.Shell
        $shortcut = $wshShell.CreateShortcut("$env:USERPROFILE\Desktop\Win11 After Boot.lnk")
        $shortcut.TargetPath = $exePath
        $shortcut.WorkingDirectory = $targetDir
        $shortcut.Description = "Win11 After Boot - Post-installation Setup Utility"
        $shortcut.Save()
        Write-Host "[+] Desktop shortcut created." -ForegroundColor Green
    } catch {}

    Write-Host "[*] Launching Win11 After Boot..." -ForegroundColor Cyan
    Start-Process -FilePath $exePath
} catch {
    Write-Host "[-] Failed to download release from: $releaseUrl" -ForegroundColor Red
    Write-Host "    Make sure the repository release exists on GitHub: https://github.com/$Repo/releases" -ForegroundColor Yellow
}
