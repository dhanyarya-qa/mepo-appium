# ============================================
# Mepo Appium - Test Runner Script
# ============================================
# Usage:
#   .\run_tests.ps1                                        <- prompt input IP:PORT
#   .\run_tests.ps1 -DeviceIp "192.168.1.62:39845"        <- langsung pakai IP:PORT
#   .\run_tests.ps1 -DeviceIp "192.168.1.62:39845" -TestFile "tests/test_01_login.py"
# ============================================

param(
    [string]$DeviceIp  = "",   # IP:PORT dari Wireless Debugging (contoh: 192.168.1.62:39845)
    [string]$TestFile  = ""    # Opsional: run 1 file saja
)

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  MEPO APPIUM - TEST RUNNER" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# -- Step 1: Set ANDROID_HOME -----------------
$detectedPaths = @(
    "$env:LOCALAPPDATA\Android\Sdk",
    "$env:USERPROFILE\AppData\Local\Android\Sdk"
)
$env:ANDROID_HOME = $null
foreach ($p in $detectedPaths) {
    if (Test-Path "$p\platform-tools\adb.exe") {
        $env:ANDROID_HOME = $p.Trim()
        break
    }
}
if (-not $env:ANDROID_HOME) {
    $env:ANDROID_HOME = "$env:LOCALAPPDATA\Android\Sdk".Trim()
}
$env:ANDROID_SDK_ROOT = $env:ANDROID_HOME
$adbPath = "$env:ANDROID_HOME\platform-tools\adb.exe"

$platformTools = "$env:ANDROID_HOME\platform-tools"
$cleanPath = ($env:PATH -split ";" | Where-Object {
    $_ -notlike "*Lenovo*Android*" -and $_.Trim() -ne $platformTools.Trim()
}) -join ";"
$env:PATH = "$cleanPath;$platformTools"

Write-Host "[OK] ANDROID_HOME = $env:ANDROID_HOME" -ForegroundColor Green

if (-Not (Test-Path $adbPath)) {
    Write-Host "[FAIL] ADB not found at: $adbPath" -ForegroundColor Red
    exit 1
}

# -- Step 2: Input IP:PORT device -------------
if ($DeviceIp -eq "") {
    Write-Host ""
    Write-Host "  Buka HP > Settings > Developer Options > Wireless Debugging" -ForegroundColor Gray
    Write-Host "  Lihat IP address & port yang tampil (contoh: 192.168.1.62:39845)" -ForegroundColor Gray
    Write-Host ""
    $DeviceIp = Read-Host "  Masukkan IP:PORT device"
}

if ($DeviceIp -eq "") {
    Write-Host "[FAIL] IP:PORT tidak boleh kosong." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "[...] Connecting ke $DeviceIp ..." -ForegroundColor Yellow
$connectResult = & $adbPath connect $DeviceIp 2>&1
Write-Host "      $connectResult"
Start-Sleep -Seconds 2

# Verifikasi device terdeteksi
$devices = & $adbPath devices -l
Write-Host $devices

if ($devices -match [regex]::Escape($DeviceIp)) {
    Write-Host "[OK] Device $DeviceIp connected!" -ForegroundColor Green
    $env:ANDROID_UDID = $DeviceIp
} else {
    Write-Host "[WARN] Device $DeviceIp tidak terdeteksi." -ForegroundColor Yellow
    Write-Host "  Pastikan HP dan laptop di WiFi yang sama." -ForegroundColor Yellow
    Write-Host ""
    $continue = Read-Host "Lanjut run test anyway? (y/n)"
    if ($continue -ne "y") { exit 0 }
    $env:ANDROID_UDID = $DeviceIp
}

Write-Host "[OK] ANDROID_UDID = $env:ANDROID_UDID" -ForegroundColor Green

# -- Step 3: Start Appium (fresh + ANDROID_HOME benar) -----
Write-Host ""
Write-Host "[...] Setting up Appium server..." -ForegroundColor Yellow

Get-Process -Name "node" -ErrorAction SilentlyContinue | ForEach-Object {
    try {
        $cmdLine = (Get-CimInstance Win32_Process -Filter "ProcessId=$($_.Id)" -ErrorAction SilentlyContinue).CommandLine
        if ($cmdLine -like "*appium*") {
            Stop-Process -Id $_.Id -Force -ErrorAction SilentlyContinue
            Write-Host "  Stopped old Appium (PID $($_.Id))" -ForegroundColor Gray
        }
    } catch {}
}
Start-Sleep -Seconds 2

$npmPrefix = (& npm config get prefix).Trim()
$appiumCmd = Join-Path $npmPrefix "appium.cmd"
if (-not (Test-Path $appiumCmd)) {
    $appiumCmd = (Get-Command appium -ErrorAction SilentlyContinue).Source
    if (-not $appiumCmd) {
        Write-Host "[FAIL] Appium tidak ditemukan. Install: npm install -g appium" -ForegroundColor Red
        exit 1
    }
}

$sdkPath = $env:ANDROID_HOME.Trim()
$startArgs = "/c set `"ANDROID_HOME=$sdkPath`"&&set `"ANDROID_SDK_ROOT=$sdkPath`"&&`"$appiumCmd`" --relaxed-security"
Start-Process -FilePath "cmd.exe" -ArgumentList $startArgs -WindowStyle Minimized
Write-Host "[...] Waiting 8 seconds for Appium to boot..." -ForegroundColor Yellow
Start-Sleep -Seconds 8

try {
    Invoke-WebRequest -Uri "http://127.0.0.1:4723/status" -UseBasicParsing -TimeoutSec 5 | Out-Null
    Write-Host "[OK] Appium running on :4723" -ForegroundColor Green
} catch {
    Write-Host "[FAIL] Appium gagal start. Jalankan manual: appium --relaxed-security" -ForegroundColor Red
    exit 1
}

# -- Step 4: Run Tests ------------------------
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  RUNNING TESTS ON REAL DEVICE" -ForegroundColor Cyan
Write-Host "  $DeviceIp" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

if ($TestFile -ne "") {
    Write-Host "[RUN] $TestFile" -ForegroundColor Magenta
    python -m pytest $TestFile -v -s
} else {
    $allTests = @(
        "tests/test_01_login.py",
        "tests/test_02_home_banners.py",
        "tests/test_03_open_trip.py",
        "tests/test_04_create_itinerary.py",
        "tests/test_05_profile.py",
        "tests/test_06_search_notifs.py",
        "tests/test_07_logout.py",
        "tests/test_08_login_extras.py",
        "tests/test_09_explore_deep.py",
        "tests/test_10_home_deep.py",
        "tests/test_11_profile_deep.py",
        "tests/test_12_registration.py",
        "tests/test_13_forgot_password.py",
        "tests/test_14_login_again.py"
    )
    $testArgs = $allTests -join " "
    Write-Host "[RUN] All 14 test files (sequential)" -ForegroundColor Magenta
    Invoke-Expression "python -m pytest $testArgs -v -s"
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  TEST RUN COMPLETE" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
