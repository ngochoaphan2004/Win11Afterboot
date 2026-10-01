<#
.SYNOPSIS
    Win11 After Boot - Quick One-Line Installer
.DESCRIPTION
    Downloads and launches the latest version of Win11 After Boot.
.EXAMPLE
    & ([scriptblock]::Create((irm "https://raw.githubusercontent.com/<YOUR_USERNAME>/Win11Afterboot/main/install.ps1")))
#>

[CmdletBinding()]
param(
    [string]$Repo = "phann/Win11Afterboot"
)

$ErrorActionPreference = "Stop"
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

$targetDir = "$env:LOCALAPPDATA\Win11AfterBoot"
$exePath = "$targetDir\Win11AfterBoot.exe"
$releaseUrl = "https://github.com/$Repo/releases/latest/download/Win11AfterBoot.exe"

Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "       Win11 After Boot Installer        " -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

if (-not (Test-Path $targetDir)) {
    New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
}

Write-Host "[*] Downloading Win11 After Boot from $Repo..." -ForegroundColor Yellow

try {
    Invoke-WebRequest -Uri $releaseUrl -OutFile $exePath -UseBasicParsing
    Write-Host "[+] Download completed successfully!" -ForegroundColor Green
    Write-Host "[*] Launching Win11 After Boot..." -ForegroundColor Cyan
    Start-Process -FilePath $exePath
} catch {
    Write-Host "[-] Failed to download release from: $releaseUrl" -ForegroundColor Red
    Write-Host "    Make sure the repository release exists or clone and run from source:" -ForegroundColor Yellow
    Write-Host "    git clone https://github.com/$Repo.git" -ForegroundColor Gray
    Write-Host "    pip install -r requirements.txt; python main.py" -ForegroundColor Gray
}
