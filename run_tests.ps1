# ============================================
# Mepo Appium — Test Runner Script
# ============================================
# Usage: .\run_tests.ps1
# Or:    .\run_tests.ps1 -TestFile "tests/test_01_login.py"
# ============================================

param(
    [string]$TestFile = ""
)

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  MEPO APPIUM — TEST RUNNER" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# ── Step 1: Set ANDROID_HOME ─────────────────
$env:ANDROID_HOME = "C:\Users\Lenovo\AppData\Local\Android\Sdk"
$env:ANDROID_SDK_ROOT = $env:ANDROID_HOME
$env:PATH += ";$env:ANDROID_HOME\platform-tools"
Write-Host "[OK] ANDROID_HOME = $env:ANDROID_HOME" -ForegroundColor Green

# ── Step 2: Check ADB ────────────────────────
Write-Host ""
Write-Host "[...] Checking ADB devices..." -ForegroundColor Yellow
$adbPath = "$env:ANDROID_HOME\platform-tools\adb.exe"

if (-Not (Test-Path $adbPath)) {
    Write-Host "[FAIL] ADB not found at: $adbPath" -ForegroundColor Red
    exit 1
}

# Try to Connect to IP/Port specifically provided
& $adbPath connect 192.168.1.62:39845 | Out-Null
Start-Sleep -Seconds 2

$devices = & $adbPath devices
Write-Host $devices
if ($devices -match "192.168.1.62") {
    Write-Host "[OK] Device connected!" -ForegroundColor Green
} else {
    Write-Host "[WARN] Device not detected. Make sure:" -ForegroundColor Yellow
    Write-Host "  - HP Xiaomi nyala & layar unlocked" -ForegroundColor Yellow
    Write-Host "  - HP & laptop di WiFi yang sama" -ForegroundColor Yellow
    Write-Host "  - Wireless debugging aktif di HP" -ForegroundColor Yellow
    Write-Host ""
    $continue = Read-Host "Lanjut run test anyway? (y/n)"
    if ($continue -ne "y") { exit 0 }
}

# ── Step 3: Check Appium server ──────────────
Write-Host ""
Write-Host "[...] Checking Appium server..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://127.0.0.1:4723/status" -UseBasicParsing -TimeoutSec 3
    Write-Host "[OK] Appium server is running!" -ForegroundColor Green
} catch {
    Write-Host "[WARN] Appium server not found on :4723. Auto-starting Appium..." -ForegroundColor Yellow
    # Start Appium detached 
    Start-Process -FilePath "cmd.exe" -ArgumentList "/c appium" -WindowStyle Minimized
    Write-Host "[...] Waiting 5 seconds for Appium to boot..." -ForegroundColor Yellow
    Start-Sleep -Seconds 5
    try {
        $response = Invoke-WebRequest -Uri "http://127.0.0.1:4723/status" -UseBasicParsing -TimeoutSec 3
        Write-Host "[OK] Appium server started successfully!" -ForegroundColor Green
    } catch {
        Write-Host "[FAIL] Gagal auto-start Appium. Pastikan Appium terinstall." -ForegroundColor Red
        exit 1
    }
}

# ── Step 4: Run tests ────────────────────────
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  RUNNING TESTS..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

if ($TestFile -ne "") {
    Write-Host "[RUN] python -m pytest $TestFile -v -s" -ForegroundColor Magenta
    python -m pytest $TestFile -v -s
} else {
    Write-Host "[RUN] python -m pytest tests/ -v -s" -ForegroundColor Magenta
    python -m pytest tests/ -v -s
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  TEST RUN COMPLETE" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

Write-Host ""
Write-Host "[...] Membangun Allure Dashboard..." -ForegroundColor Yellow
try {
    allure generate reports/allure-results --clean -o reports/allure-report
    Write-Host "[...] Membuka browser Allure Dashboard..." -ForegroundColor Green
    allure open reports/allure-report
} catch {
    Write-Host "[WARN] Gagal mengeksekusi allure, pastikan paket command line 'allure' telah terinstall di system." -ForegroundColor Red
}
