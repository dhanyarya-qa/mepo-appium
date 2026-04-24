<div align="center">

# 📱 Mepo Travel — Appium E2E Automation

### Android Mobile App Testing Framework

[![Appium](https://img.shields.io/badge/Appium_3.x-662D8C?style=flat-square&logo=appium&logoColor=white)](https://appium.io/)
[![Python](https://img.shields.io/badge/Python_3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org/)
[![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?style=flat-square&logo=pytest&logoColor=white)](https://pytest.org/)
[![Android](https://img.shields.io/badge/Android_15-3DDC84?style=flat-square&logo=android&logoColor=white)](https://developer.android.com/)

*Production-ready E2E mobile automation for the Mepo Travel Android app on a real Xiaomi device — featuring 100+ test cases across 14 test files, sequential pipeline execution, automated OTP verification via mail.tm API, smart WebDriverWait performance optimization, and rich failure diagnostics with video recording.*
</div>

---

## ✨ Key Features

<table>
<tr>
<td width="50%">

### 🎯 Test Scenarios (115+ Tests)
- 🔐 **Login** — 5 negative + 1 positive + extras validation
- 🏠 **Home Screen** — Layout, banners, service cards, deep interactions
- 🗺 **Open Trip** — Navigation, detail, Custom Trip, booking checkout
- 📋 **Create Itinerary** — Modal, form validation, full CRUD + cleanup
- 👤 **Profile** — Navigation, tabs, filters, deep card interactions
- 🔍 **Search & Notifications** — Semantic icon navigation
- 🚪 **Logout & Re-login** — Full cycle with session restoration
- 📝 **Registration** — Automated with mail.tm OTP + login verify
- 🔑 **Forgot Password** — Screen validation & form elements
- 🔄 **Login Again** — Verifying persistent login across sessions

</td>
<td width="50%">

### 🔬 Framework Features
- 🏗️ **Page Object Model (POM)** — Clean separation of concerns
- ⚡ **Smart WebDriverWait** — Dynamic waits instead of fixed sleeps
- 🔌 **API-Driven Preconditions** — Seed & reset test data
- 📸 **Auto Screenshots** — Capture on every failure
- 🎬 **Video Recording** — Automatic screen recording per test
- 📝 **Rich Logging** — Timestamped logs with emoji markers
- 🔄 **Session Persistence** — Single driver session across all tests
- 📊 **Spreadsheet Export** — CSV report for Google Sheets import
- 📧 **mail.tm OTP Integration** — Automated email OTP extraction
- 🛡️ **Smart Navigation** — Bottom Nav semantic locators
- ♻️ **Auto Retry** — 3x rerun on failure via `pytest-rerunfailures`

</td>
</tr>
</table>

---

## 🏗️ Architecture

```
mepo-appium/
├── config/
│   ├── __init__.py
│   └── settings.py                  # Appium caps, API endpoints, test data
├── pages/
│   ├── __init__.py
│   ├── base_page.py                 # Common interactions (wait, tap, scroll)
│   ├── splash_page.py               # Splash & welcome screens
│   ├── login_page.py                # Authentication flow
│   ├── home_page.py                 # Home/Dashboard navigation hub
│   ├── open_trip_page.py            # Open Trip discovery & detail
│   ├── create_itinerary_page.py     # Create Itinerary form & modal
│   ├── profile_page.py              # Profile view, edit, logout
│   └── budget_page.py               # Budget/Expense tracking
├── tests/
│   ├── __init__.py
│   ├── conftest.py                  # Fixtures, driver lifecycle, reporting
│   ├── test_01_login.py             # Login negative + positive (6 tests)
│   ├── test_02_home_banners.py      # Home layout & banners (10 tests)
│   ├── test_03_open_trip.py         # Open Trip navigation (6 tests)
│   ├── test_04_create_itinerary.py  # Create Itinerary full CRUD (11 tests)
│   ├── test_05_profile.py           # Profile page layout & tabs (10 tests)
│   ├── test_06_search_notifs.py     # Search & Notification flow (8 tests)
│   ├── test_07_logout.py            # Logout flow (5 tests)
│   ├── test_08_login_extras.py      # Login screen extras + re-login (9 tests)
│   ├── test_09_explore_deep.py      # Explore page deep interactions (6 tests)
│   ├── test_10_home_deep.py         # Home deep scroll & carousels (13 tests)
│   ├── test_11_profile_deep.py      # Profile deep interactions (10 tests)
│   ├── test_12_registration.py      # Registration + OTP + login verify (7 tests)
│   ├── test_13_forgot_password.py   # Forgot Password validation (4 tests)
│   └── test_14_login_again.py       # Login again using shared email (1 test)
├── utils/
│   ├── __init__.py
│   ├── api_helper.py               # REST API client for preconditions
│   └── wait_helpers.py             # ⚡ Smart WebDriverWait utilities
├── reports/
│   ├── logs/                        # Test run logs (auto-generated)
│   ├── screenshots/                 # Failure screenshots (auto-captured)
│   └── videos/                      # Failure screen recordings (auto-saved)
├── apps/                            # Place APK file here
├── scripts/                         # Utility & exploration scripts
├── pytest.ini                       # Pytest config, markers & rerun rules
├── requirements.txt                 # Python dependencies
└── README.md
```

---

## 📋 Prerequisites

| Component | Version | Purpose |
|-----------|---------|---------|
| Python | ≥ 3.10 | Test runtime |
| Appium Server | ≥ 3.x | Mobile automation server |
| Android SDK | API 33+ | Android platform tools |
| Java JDK | ≥ 11 | Required by UiAutomator2 |
| Node.js | ≥ 18 | Appium server runtime |
| Real Device | Xiaomi (Android 15) | Test target device |

---

## 🚀 Quick Start

```bash
# 1. Clone repository
git clone https://github.com/dhanyarya-qa/mepo-appium.git
cd mepo-appium

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Start Appium Server (Terminal 1 — keep running)
appium --relaxed-security

# 4. Connect device via wireless ADB (Terminal 2)
adb connect <device-ip>:<port>

# 5. Verify device is connected
adb devices

# 6. Ensure Mepo app is installed on device
```

---

## ▶️ Running Tests

### Sequential Full Suite (Recommended)

```bash
python -m pytest tests/test_01_login.py tests/test_02_home_banners.py tests/test_03_open_trip.py tests/test_04_create_itinerary.py tests/test_05_profile.py tests/test_06_search_notifs.py tests/test_07_logout.py tests/test_08_login_extras.py tests/test_09_explore_deep.py tests/test_10_home_deep.py tests/test_11_profile_deep.py tests/test_12_registration.py tests/test_13_forgot_password.py tests/test_14_login_again.py -v -s
```

### Individual Test Files

```bash
python -m pytest tests/test_01_login.py -v -s              # Login scenarios
python -m pytest tests/test_02_home_banners.py -v -s        # Home screen features
python -m pytest tests/test_03_open_trip.py -v -s           # Open Trip discovery
python -m pytest tests/test_04_create_itinerary.py -v -s    # Create Itinerary CRUD
python -m pytest tests/test_05_profile.py -v -s             # Profile management
python -m pytest tests/test_06_search_notifs.py -v -s       # Search & Notifications
python -m pytest tests/test_07_logout.py -v -s              # Logout flow
python -m pytest tests/test_08_login_extras.py -v -s        # Login extras + re-login
python -m pytest tests/test_09_explore_deep.py -v -s        # Explore deep interactions
python -m pytest tests/test_10_home_deep.py -v -s           # Home deep interactions
python -m pytest tests/test_11_profile_deep.py -v -s        # Profile deep interactions
python -m pytest tests/test_12_registration.py -v -s        # Registration + OTP
python -m pytest tests/test_13_forgot_password.py -v -s     # Forgot Password
python -m pytest tests/test_14_login_again.py -v -s         # Login again with shared email
```

### Run by Marker

```bash
pytest -m smoke -v -s             # Smoke tests only
pytest -m login -v -s             # Login tests only
pytest -m home -v -s              # Home screen tests only
pytest -m regression -v -s        # All regression tests
pytest -m cleanup -v -s           # Cleanup/data management tests
```

### Generate Reports

```bash
# HTML report
pytest tests/ -v -s --html=reports/report.html

# CSV spreadsheet report (auto-generated on every run)
# → reports/Test_Results_Spreadsheet_YYYYMMDD_HHMMSS.csv
```

---

## ⚡ Performance Optimization

All test files use **smart WebDriverWait** instead of fixed `time.sleep()` calls, reducing total execution time by ~40%.

| Technique | Before | After | Impact |
|-----------|--------|-------|--------|
| `implicit_wait` | 10s | 5s | Faster negative assertions |
| Login wait | `sleep(10)` | `WebDriverWait(12)` | Usually resolves in 3-5s |
| Navigation wait | `sleep(5)` | `sleep(3)` | Saves 2s per transition |
| Settings/Profile tap | `sleep(5)` | `sleep(3)` | Saves 2s per page |
| Scroll gaps | `sleep(1)` | `sleep(0.5)` | Saves 0.5s per scroll |
| **Total fixed sleep** | **~12 min** | **~7 min** | **-40%** |

### Smart Wait Helpers (`utils/wait_helpers.py`)

```python
from utils.wait_helpers import wait_for, wait_find, wait_and_click, wait_for_any

# Wait until element appears (max 5s, but returns as soon as found)
element = wait_for(driver, "//*[@content-desc='Welcome,']", timeout=5)

# Wait and click in one call
wait_and_click(driver, "//android.widget.Button[@content-desc='Login']")

# Wait for any of multiple possible screens
idx, els = wait_for_any(driver, [
    "//android.widget.EditText",           # Login screen
    "//*[contains(@content-desc, 'Welcome,')]",  # Home screen
], timeout=10)
```

---

## 🧪 Test Scenarios

### Test 01 — Login Flow 🔐

| # | Scenario | Type |
|---|----------|------|
| 1 | Empty email → rejected | ❌ Negative |
| 2 | Empty password → rejected | ❌ Negative |
| 3 | Wrong email → rejected | ❌ Negative |
| 4 | Wrong password → rejected | ❌ Negative |
| 5 | Invalid email format → rejected | ❌ Negative |
| 6 | Valid credentials → Welcome screen | ✅ Positive |

### Test 02 — Home Screen 🏠 (10 tests)

Welcome greeting, subtitle, header icons, banner carousel (swipe + dots), 6 service cards, Create Itinerary CTA, popular city chips, Open Trip section, Recommended Itinerary, Partnership banner.

### Test 03 — Open Trip 🗺 (6 tests)

Navigate via card, trip cards listing, trip detail, Custom Trip section, itinerary references, return to home.

### Test 04 — Create Itinerary 📋 (11 tests)

Modal open, form fields, save disabled by default, empty submit blocked, title-only blocked, fill & save, cancel dismisses, full E2E with 5 activities, verify draft in profile.

### Test 05 — Profile 👤 (10 tests)

Navigate via Bottom Nav, username/handle display, My Itinerary tab, Saved tab, filters (Activity/Shared/Draft), itinerary cards.

### Test 06 — Search & Notifications 🔍 (8 tests)

Navigate to Explore, search bar, popular section, city cards, recommended section, itinerary cards, notifications page, empty state.

### Test 07 — Logout 🚪 (5 tests)

Navigate to profile, open settings, find & tap logout, confirm dialog, verify login screen.

### Test 08 — Login Extras 🔐 (9 tests)

Onboarding carousel, dot indicators, Register link, Forgot Password link, Terms link, language switcher, email/password hints, login button state, session restoration.

### Test 09 — Explore Deep 🔎 (6 tests)

City card tap (Depok), clickable verification, search input, recommended cards, card detail, return home.

### Test 10 — Home Deep 🏠 (13 tests)

Service card "Soon" labels (5), Open Trip active, carousel scroll, popular city chips, See All navigation, partnership banner, recommended itinerary cards.

### Test 11 — Profile Deep 👤 (10 tests)

Itinerary card detail, filter chip interactions (Shared/Draft/Activity), Saved Itinerary tab, settings navigation.

### Test 12 — Registration 📝 (7 tests)

| # | Step | Description |
|---|------|-------------|
| 1 | Create email | Generate unique email via **mail.tm** REST API |
| 2 | Navigate | Login → tap "Register" link |
| 3 | Fill form | Email + Display Name + Username + Password + Confirm |
| 4 | Fetch OTP | Poll mail.tm inbox → extract 4-6 digit OTP → enter in app |
| 5 | Back to login | Return to Login screen |
| 6 | **Login verify** | Login with newly registered account → confirm Welcome screen |
| 7 | **Logout** | Logout from new account → back to Login screen |

> ✨ **Email is 100% unique every run** using timestamp + random suffix: `autoqa{timestamp}_{random}@domain`

### Test 13 — Forgot Password 🔑 (4 tests)

Navigate to forgot page, form elements, send OTP disabled, return to login.

### Test 14 — Login Again 🔄 (1 test)

Login using shared email from Test 12/13 and confirm Home screen.

---

## ⚙️ Configuration

### Appium Capabilities (Real Device)

```python
{
    "platformName": "Android",
    "appium:automationName": "UiAutomator2",
    "appium:deviceName": "23124RA7EO",          # Xiaomi device
    "appium:platformVersion": "15",
    "appium:udid": "192.168.1.62:39289",        # Wireless ADB
    "appium:appPackage": "com.mepo",
    "appium:appActivity": "com.mepo.MainActivity",
    "appium:noReset": True,
    "appium:autoGrantPermissions": True,
    "appium:autoAcceptAlerts": True,
}
```

### Test Data

```python
VALID_EMAIL    = "danip1@yopmail.com"
VALID_PASSWORD = "Sandi123!"
```

---

## 📊 Reporting

| Report Type | Location |
|-------------|----------|
| 🖥️ Terminal | Custom PASS/FAIL summary table |
| 📝 Logs | `reports/logs/test_run_YYYYMMDD_HHMMSS.log` |
| 📸 Screenshots | `reports/screenshots/FAIL_*.png` (auto on failure) |
| 🎬 Videos | `reports/videos/FAIL_*.mp4` (auto screen recording) |
| 📄 HTML Report | `pytest --html=reports/report.html` |
| 📊 CSV Spreadsheet | `reports/Test_Results_Spreadsheet_*.csv` (auto-generated) |

---

## 📈 Coverage Summary

```
┌──────────────────────────────────────────────────────────┐
│              TEST COVERAGE REPORT                        │
├──────────────────────────────────────────────────────────┤
│  Test Files          : 14 files                          │
│  Total Test Cases    : 100+ scenarios                    │
│  Positive Tests      : 85+                               │
│  Negative Tests      : 15+                               │
│  Page Objects        : 7 (+ 1 base)                      │
│                                                          │
│  Features Covered:                                       │
│    ✅ Login (positive + 5 negative scenarios)            │
│    ✅ Home Screen (layout + features + deep)             │
│    ✅ Banner Carousel (swipe + indicators)               │
│    ✅ Open Trip Discovery & Detail                       │
│    ✅ Create Itinerary (full CRUD + 5 activities)        │
│    ✅ Profile Management (tabs, filters, deep)           │
│    ✅ Search & Notifications                             │
│    ✅ Logout & Session Restoration                       │
│    ✅ Login Extras Validation                            │
│    ✅ Explore Deep Interactions                          │
│    ✅ Home Deep Scroll & Carousels                       │
│    ✅ Registration + mail.tm OTP + Login Verify          │
│    ✅ Forgot Password Flow                               │
│    ✅ Login Again (Persistent Login)                     │
├──────────────────────────────────────────────────────────┤
│  EXECUTION : Real Device (Xiaomi Redmi Note 13, API 35) │
│  CONNECTION: Wireless ADB                                │
│  FRAMEWORK : Appium 3.x + UiAutomator2 + Pytest         │
│  PERFORMANCE: ~40% faster with WebDriverWait             │
└──────────────────────────────────────────────────────────┘
```

---

## 🛡️ Stability Features

| Feature | Implementation |
|---------|----------------|
| **Smart Navigation** | Bottom Nav semantic locators instead of hardcoded coordinates |
| **Safe Scrolling** | `UiScrollable(scrollable(true))` — no blind swipe gestures |
| **Smart Waits** | `WebDriverWait` dynamic waits via `utils/wait_helpers.py` |
| **Auto Retry** | 3x rerun on failure via `pytest-rerunfailures` |
| **Session Persistence** | Single Appium session across all 115+ tests |
| **State Recovery** | Automated re-login after logout tests (test_08) |
| **Driver Keep-Alive** | Active polling during OTP wait to prevent idle timeout |
| **Unique Emails** | Timestamp-based email generation for registration tests |
| **Safe Back Navigation** | Conditional `press_keycode(4)` — stops when target screen found |

---

<div align="center">

**Built with ❤️ by [Dhany Arya Pratama](https://github.com/dhanyarya-qa)**

</div>
#   m e p o - a p p i u m  
 