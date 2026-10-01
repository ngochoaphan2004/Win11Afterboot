# ============================================================
#  Win11 After Boot - Build Script
#  Compiles Python source into standalone executable (.exe)
# ============================================================

[CmdletBinding()]
param(
    [switch]$NoPrompt,
    [switch]$RunNow
)

$ErrorActionPreference = "Stop"

# Ensure working directory is the script directory
Set-Location -Path $PSScriptRoot

Write-Host ""
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "   🚀 Win11 After Boot v1.1.0 - Build Script " -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

# [1/5] Check Python environment (.venv prioritized, then PATH, then default install dirs)
Write-Host "[1/5] Checking Python environment..." -ForegroundColor Yellow
$PYTHON = $null

if (Test-Path "$PSScriptRoot\.venv\Scripts\python.exe") {
    $PYTHON = "$PSScriptRoot\.venv\Scripts\python.exe"
}

if (-not $PYTHON) {
    try {
        $ver = & python --version 2>&1
        if ($LASTEXITCODE -eq 0) { $PYTHON = "python" }
    } catch {}
}

if (-not $PYTHON) {
    $candidates = @(
        "$env:LOCALAPPDATA\Programs\Python\Python313\python.exe",
        "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe",
        "$env:LOCALAPPDATA\Programs\Python\Python311\python.exe",
        "$env:LOCALAPPDATA\Programs\Python\Python310\python.exe",
        "C:\Python313\python.exe",
        "C:\Python312\python.exe"
    )
    foreach ($c in $candidates) {
        if (Test-Path $c) { $PYTHON = $c; break }
    }
}

if (-not $PYTHON) {
    Write-Host "[-] Python not found! Please install Python or set up .venv first." -ForegroundColor Red
    exit 1
}

$pythonVersion = & $PYTHON --version 2>&1
Write-Host "[+] Using: $pythonVersion ($PYTHON)" -ForegroundColor Green

# [2/5] Check & install dependencies
Write-Host ""
Write-Host "[2/5] Installing dependencies from requirements.txt..." -ForegroundColor Yellow
& $PYTHON -m pip install -r requirements.txt --quiet
if ($LASTEXITCODE -ne 0) {
    Write-Host "[-] Failed to install requirements!" -ForegroundColor Red
    exit 1
}
Write-Host "[+] Dependencies are up to date." -ForegroundColor Green

# [3/5] Check PyInstaller
Write-Host ""
Write-Host "[3/5] Checking PyInstaller..." -ForegroundColor Yellow
$hasPyinstaller = & $PYTHON -c "import PyInstaller; print('OK')" 2>$null
if ($hasPyinstaller -ne "OK") {
    Write-Host "[*] Installing PyInstaller..." -ForegroundColor Yellow
    & $PYTHON -m pip install pyinstaller --quiet
}
Write-Host "[+] PyInstaller is ready." -ForegroundColor Green

# [4/5] Clean previous builds
Write-Host ""
Write-Host "[4/5] Cleaning previous build artifacts..." -ForegroundColor Yellow
if (Test-Path "dist") { 
    try { Remove-Item -Recurse -Force "dist" -ErrorAction SilentlyContinue } catch {}
}
if (Test-Path "build") { 
    try { Remove-Item -Recurse -Force "build" -ErrorAction SilentlyContinue } catch {}
}
Write-Host "[+] Cleaned dist/ and build/ folders." -ForegroundColor Green

# [5/5] Build executable
Write-Host ""
Write-Host "[5/5] Building standalone executable (this may take 1-2 minutes)..." -ForegroundColor Yellow
Write-Host ""

$specFile = Join-Path $PSScriptRoot "Win11AfterBoot.spec"
if (-not (Test-Path $specFile)) {
    Write-Host "[-] Spec file not found: $specFile" -ForegroundColor Red
    exit 1
}

& $PYTHON -m PyInstaller $specFile --clean --noconfirm

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "[-] Build failed!" -ForegroundColor Red
    exit 1
}

# Success result
Write-Host ""
Write-Host "=============================================" -ForegroundColor Green
Write-Host "   BUILD SUCCESSFUL!                         " -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Green
Write-Host ""

$exePath = Join-Path $PSScriptRoot "dist\Win11AfterBoot.exe"
if (Test-Path $exePath) {
    $size = (Get-Item $exePath).Length / 1MB
    Write-Host "Output File: $exePath" -ForegroundColor Cyan
    Write-Host "File Size:   $([math]::Round($size, 1)) MB" -ForegroundColor Cyan
    Write-Host ""

    if ($RunNow) {
        Start-Process $exePath
    } elseif (-not $NoPrompt) {
        $run = Read-Host "Launch Win11AfterBoot now? (y/N)"
        if ($run -eq "y" -or $run -eq "Y") {
            Start-Process $exePath
        }
    }
} else {
    Write-Host "[-] Output executable not found in dist folder!" -ForegroundColor Yellow
}

if (-not $NoPrompt) {
    Write-Host ""
    Write-Host "Press Enter to exit..."
    Read-Host | Out-Null
}
