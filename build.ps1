# ============================================================
#  Win11 After Boot - Build Script
#  Chạy script này để build ra file .exe standalone
# ============================================================

Write-Host ""
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "  Win11 After Boot - Build Script" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

# Tìm Python (kiểm tra PATH trước, rồi tìm ở vị trí cài mặc định)
Write-Host "[1/5] Kiểm tra Python..." -ForegroundColor Yellow
$PYTHON = $null
$PYINSTALLER = $null

try {
    $ver = & python --version 2>&1
    if ($LASTEXITCODE -eq 0) { $PYTHON = "python" }
} catch {}

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
    Write-Host "❌ Không tìm thấy Python! Cài Python trước khi build." -ForegroundColor Red
    exit 1
}

$pythonVersion = & $PYTHON --version 2>&1
$pythonDir = Split-Path $PYTHON
$PYINSTALLER = Join-Path $pythonDir "Scripts\pyinstaller.exe"
Write-Host "✅ $pythonVersion (path: $PYTHON)" -ForegroundColor Green

# Kiểm tra pip
Write-Host ""
Write-Host "[2/5] Cài đặt dependencies..." -ForegroundColor Yellow
& $PYTHON -m pip install -r requirements.txt --quiet
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Lỗi khi cài dependencies!" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Dependencies đã cài xong" -ForegroundColor Green

# Kiểm tra PyInstaller
Write-Host ""
Write-Host "[3/5] Kiểm tra PyInstaller..." -ForegroundColor Yellow
if (-not (Test-Path $PYINSTALLER)) {
    Write-Host "Cài đặt PyInstaller..." -ForegroundColor Yellow
    & $PYTHON -m pip install pyinstaller --quiet
}
Write-Host "✅ PyInstaller sẵn sàng" -ForegroundColor Green

# Xóa build cũ
Write-Host ""
Write-Host "[4/5] Dọn dẹp build cũ..." -ForegroundColor Yellow
if (Test-Path "dist") { Remove-Item -Recurse -Force "dist" }
if (Test-Path "build") { Remove-Item -Recurse -Force "build" }
Write-Host "✅ Đã dọn dẹp" -ForegroundColor Green

# Build
Write-Host ""
Write-Host "[5/5] Đang build .exe (có thể mất 1-3 phút)..." -ForegroundColor Yellow
Write-Host ""

& $PYINSTALLER Win11AfterBoot.spec --clean --noconfirm

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "❌ Build thất bại!" -ForegroundColor Red
    exit 1
}

# Kết quả
Write-Host ""
Write-Host "=============================================" -ForegroundColor Green
Write-Host "  ✅ BUILD THÀNH CÔNG!" -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Green
Write-Host ""

$exePath = "dist\Win11AfterBoot.exe"
if (Test-Path $exePath) {
    $size = (Get-Item $exePath).Length / 1MB
    Write-Host "📦 File output: $exePath" -ForegroundColor Cyan
    Write-Host "📏 Kích thước:  $([math]::Round($size, 1)) MB" -ForegroundColor Cyan
    Write-Host ""
    
    # Hỏi có muốn chạy thử không
    $runNow = Read-Host "Chạy thử ngay bây giờ? (y/N)"
    if ($runNow -eq "y" -or $runNow -eq "Y") {
        Start-Process $exePath
    }
} else {
    Write-Host "⚠️  Không tìm thấy file output!" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Nhấn Enter để thoát..."
Read-Host
