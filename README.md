<div align="center">

# 📱 Mepo Travel — Appium E2E Automation

### Android Mobile App Testing Framework

[![Appium](https://img.shields.io/badge/Appium_3.x-662D8C?style=flat-square&logo=appium&logoColor=white)](https://appium.io/)
[![Python](https://img.shields.io/badge/Python_3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org/)
[![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?style=flat-square&logo=pytest&logoColor=white)](https://pytest.org/)
[![Android](https://img.shields.io/badge/Android_15-3DDC84?style=flat-square&logo=android&logoColor=white)](https://developer.android.com/)

*Production-ready E2E mobile automation for the Mepo Travel Android app on a real Xiaomi device — featuring 109+ test cases across 15 test files, sequential pipeline execution, automated OTP verification via Yopmail, and rich failure diagnostics with video recording.*

</div>

---

## ✨ Key Features

<table>
<tr>
<td width="50%">

### 🎯 Test Scenarios (109+ Tests)
- 🔐 **Login** — 5 negative + 1 positive + extras validation
- 🏠 **Home Screen** — Layout, banners, service cards, deep interactions
- 🗺 **Open Trip** — Navigation, detail, Custom Trip, booking checkout
- 📋 **Create Itinerary** — Modal, form validation, full CRUD + cleanup
- 👤 **Profile** — Navigation, tabs, filters, deep card interactions
- 🔍 **Search & Notifications** — Semantic icon navigation
- 🚪 **Logout & Re-login** — Full cycle with session restoration
- 📝 **Registration** — Automated with Yopmail OTP extraction
- 🔑 **Forgot Password** — Screen validation & form elements
- 💳 **Booking Checkout** — End-to-end trip booking flow

</td>
<td width="50%">

### 🔬 Framework Features
- 🏗️ **Page Object Model (POM)** — Clean separation of concerns
- 🔌 **API-Driven Preconditions** — Seed & reset test data
- 📸 **Auto Screenshots** — Capture on every failure
- 🎬 **Video Recording** — Automatic screen recording per test
- 📝 **Rich Logging** — Timestamped logs with emoji markers
- 🔄 **Session Persistence** — Single driver session across all tests
- 📊 **Spreadsheet Export** — CSV report for Google Sheets import
- 📧 **Yopmail OTP Integration** — Automated email OTP extraction
- 🛡️ **Smart Navigation** — Bottom Nav semantic locators (no hardcoded coords)
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
│   ├── test_04b_manage_itinerary.py # Cleanup auto-test itineraries (2 tests)
│   ├── test_05_profile.py          # Profile page layout & tabs (10 tests)
│   ├── test_06_search_notifs.py     # Search & Notification flow (8 tests)
│   ├── test_07_logout.py            # Logout flow (5 tests)
│   ├── test_08_login_extras.py      # Login screen extras + re-login (9 tests)
│   ├── test_09_explore_deep.py      # Explore page deep interactions (6 tests)
│   ├── test_10_home_deep.py         # Home deep scroll & carousels (13 tests)
│   ├── test_11_profile_deep.py      # Profile deep interactions (10 tests)
│   ├── test_12_registration.py      # Registration + Yopmail OTP (6 tests)
│   ├── test_13_forgot_password.py   # Forgot Password validation (4 tests)
│   ├── test_14_booking_checkout.py  # Open Trip booking checkout (1 test)
│   └── test_advanced_features.py    # API-driven Open Trip & Budget
├── utils/
│   ├── __init__.py
│   └── api_helper.py               # REST API client for preconditions
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
| `yopmail` | ≥ 1.9 | OTP extraction for registration tests |

---

## 🚀 Quick Start

```bash
# 1. Clone repository
git clone https://github.com/dhanyarya-qa/mepo-appium.git
cd mepo-appium

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Start Appium Server (separate terminal)
appium --relaxed-security

# 4. Connect device via wireless ADB
adb connect <device-ip>:<port>

# 5. Verify device is connected
adb devices

# 6. Ensure Mepo app is installed on device
```

---

## ▶️ Running Tests

### Sequential Full Suite (Recommended)

```bash
# Run all 15 test files in proper order (login → features → logout → re-login → deep tests)
python -m pytest tests/test_01_login.py tests/test_02_home_banners.py tests/test_03_open_trip.py tests/test_04_create_itinerary.py tests/test_04b_manage_itinerary.py tests/test_05_profile.py tests/test_06_search_notifs.py tests/test_07_logout.py tests/test_08_login_extras.py tests/test_09_explore_deep.py tests/test_10_home_deep.py tests/test_11_profile_deep.py tests/test_12_registration.py tests/test_13_forgot_password.py tests/test_14_booking_checkout.py -v -s
```

### Individual Test Files

```bash
python -m pytest tests/test_01_login.py -v -s              # Login scenarios
python -m pytest tests/test_02_home_banners.py -v -s        # Home screen features
python -m pytest tests/test_03_open_trip.py -v -s           # Open Trip discovery
python -m pytest tests/test_04_create_itinerary.py -v -s    # Create Itinerary CRUD
python -m pytest tests/test_04b_manage_itinerary.py -v -s   # Cleanup test itineraries
python -m pytest tests/test_05_profile.py -v -s             # Profile management
python -m pytest tests/test_06_search_notifs.py -v -s       # Search & Notifications
python -m pytest tests/test_07_logout.py -v -s              # Logout flow
python -m pytest tests/test_08_login_extras.py -v -s        # Login extras + re-login
python -m pytest tests/test_09_explore_deep.py -v -s        # Explore deep interactions
python -m pytest tests/test_10_home_deep.py -v -s           # Home deep interactions
python -m pytest tests/test_11_profile_deep.py -v -s        # Profile deep interactions
python -m pytest tests/test_12_registration.py -v -s        # Registration + OTP
python -m pytest tests/test_13_forgot_password.py -v -s     # Forgot Password
python -m pytest tests/test_14_booking_checkout.py -v -s    # Booking checkout
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

## 🧪 Test Scenarios

### Test 01 — Login Flow 🔐

| # | Scenario | Type | Validation |
|---|----------|------|------------|
| 1 | Empty email | ❌ Negative | Should NOT reach home |
| 2 | Empty password | ❌ Negative | Should NOT reach home |
| 3 | Wrong email | ❌ Negative | Should NOT reach home |
| 4 | Wrong password | ❌ Negative | Should NOT reach home |
| 5 | Invalid email format | ❌ Negative | Should NOT reach home |
| 6 | Valid credentials | ✅ Positive | Welcome greeting displayed |

### Test 02 — Home Screen 🏠

| # | Scenario | Type | Validation |
|---|----------|------|------------|
| 1 | Welcome greeting | ✅ Layout | "Welcome, danip" visible |
| 2 | Where to go text | ✅ Layout | Subtitle text displayed |
| 3 | Header icons | ✅ Layout | 3 icons (search/notif/profile) |
| 4 | Banner carousel | ✅ Feature | 5-6 dot indicators + swipe |
| 5 | Service cards (×6) | ✅ Feature | Open Trip, Flight, Train, Bus, Hotel, Promo |
| 6 | Create Itinerary CTA | ✅ Feature | Button + intro text visible |
| 7 | Popular cities (×3) | ✅ Feature | Depok, Tebet, Sulawesi |
| 8 | Open Trip with Us | ✅ Section | Section + See all link |
| 9 | Recommended Itinerary | ✅ Section | Section visible |
| 10 | Partnership link | ✅ Section | Apply for Partnership visible |

### Test 03 — Open Trip 🗺

| # | Scenario | Type | Validation |
|---|----------|------|------------|
| 1 | Navigate via service card | ✅ Positive | Open Trip page loads |
| 2 | Trip cards visible | ✅ Positive | Cards with images found |
| 3 | View trip detail | ✅ Positive | Detail page + scroll |
| 4 | Custom Your Trip | ✅ Positive | Section found + clickable |
| 5 | Itinerary references | ✅ Positive | Reference cards visible |
| 6 | Return to home | ✅ Navigation | Welcome greeting confirmed |

### Test 04 — Create Itinerary 📋

| # | Scenario | Type | Validation |
|---|----------|------|------------|
| 1 | Modal opens | ✅ Positive | "Create Itinerary" header |
| 2 | Title field present | ✅ Layout | Hint: "Create title of itinerary" |
| 3 | Destination field | ✅ Layout | Hint: "Destination" |
| 4 | Cancel + Save buttons | ✅ Layout | Both buttons present |
| 5 | Save disabled by default | ❌ Negative | `enabled=false` when empty |
| 6 | Empty submit blocked | ❌ Negative | Save stays disabled |
| 7 | Title-only blocked | ❌ Negative | Save stays disabled |
| 8 | Fill & save | ✅ Positive | Complete form → submit |
| 9 | Cancel dismisses modal | ✅ Positive | Modal closes on cancel |
| 10 | Full E2E creation | ✅ Positive | Create with 5 activities + save draft |
| 11 | Verify draft in profile | ✅ Positive | Draft exists in Profile tab |

### Test 04b — Manage Itinerary 🗑️

| # | Scenario | Type | Validation |
|---|----------|------|------------|
| 1 | Navigate to profile | ✅ Navigation | Bottom Nav Profile Tab |
| 2 | Clean auto-test items | ✅ Cleanup | Delete `[Auto-Test]` itineraries |

### Test 05 — Profile 👤

| # | Scenario | Type | Validation |
|---|----------|------|------------|
| 1 | Navigate to profile | ✅ Positive | Bottom Nav → "My Profile" |
| 2 | Username displayed | ✅ Layout | "danip" visible |
| 3 | Handle displayed | ✅ Layout | "danip971" visible |
| 4 | My Itinerary tab | ✅ Feature | Selected by default |
| 5 | Saved Itinerary tab | ✅ Feature | Tab switch works |
| 6 | Filters (Activity/Shared/Draft) | ✅ Feature | 3 filter buttons |
| 7 | Itinerary cards | ✅ Feature | Finished/Ongoing status |

### Test 06 — Search & Notifications 🔍

| # | Scenario | Type | Validation |
|---|----------|------|------------|
| 1 | Navigate to search | ✅ Positive | Explore Itinerary page |
| 2 | Search bar present | ✅ Layout | "Search any Itinerary..." |
| 3 | Popular section | ✅ Feature | Explore Popular Itinerary |
| 4 | City cards | ✅ Feature | ≥3 city cards displayed |
| 5 | Recommended section | ✅ Feature | Recommended Itinerary visible |
| 6 | Itinerary cards | ✅ Feature | Clickable cards found |
| 7 | Navigate to notifications | ✅ Positive | Notification page loads |
| 8 | Empty state message | ✅ Layout | "No Available Notification" |

### Test 07 — Logout 🚪

| # | Scenario | Type | Validation |
|---|----------|------|------------|
| 1 | Navigate to profile | ✅ Navigation | My Profile header |
| 2 | Open settings | ✅ Positive | Settings page |
| 3 | Find & click logout | ✅ Positive | Logout button tapped |
| 4 | Confirm logout dialog | ✅ Positive | Continue/Yes tapped |
| 5 | Verify logged out | ✅ Positive | Login screen displayed |

### Test 08 — Login Extras & Re-login 🔐

| # | Scenario | Type | Validation |
|---|----------|------|------------|
| 1 | Login button exists | ✅ Layout | Button present and enabled |
| 2 | Register link | ✅ Layout | "Register" link clickable |
| 3 | Forgot Password link | ✅ Layout | Link navigates correctly |
| 4 | Password visibility toggle | ✅ Feature | Toggle works |
| 5 | Email field attributes | ✅ Layout | Hint text verified |
| 6-9 | Automated re-login | ✅ Positive | Restores session for subsequent tests |

### Test 09 — Explore Deep 🔎

| # | Scenario | Type | Validation |
|---|----------|------|------------|
| 1-6 | Deep Explore interactions | ✅ Feature | Search, filter, card taps |

### Test 10 — Home Deep 🏠

| # | Scenario | Type | Validation |
|---|----------|------|------------|
| 1-5 | Service card "Soon" labels | ✅ Feature | Flight/Train/Bus/Hotel/Promo |
| 6 | Open Trip active (no Soon) | ✅ Feature | Active card verified |
| 7 | Open Trip carousel scroll | ✅ Feature | HorizontalScrollView swipe |
| 8 | Popular city chips | ✅ Feature | UiScrollable + city chips |
| 9 | See All navigation | ✅ Navigation | Opens Open Trip list |
| 10 | Partnership banner | ✅ Feature | Clickable banner check |
| 11-13 | Recommended itinerary | ✅ Feature | Carousel cards verified |

### Test 11 — Profile Deep 👤

| # | Scenario | Type | Validation |
|---|----------|------|------------|
| 1-3 | Itinerary card detail | ✅ Feature | Tap → detail → back |
| 4-6 | Filter chip interactions | ✅ Feature | Shared/Draft/Activity |
| 7-9 | Saved Itinerary tab | ✅ Feature | Tab switch + content |
| 10 | Settings navigation | ✅ Navigation | Settings page accessible |

### Test 12 — Registration 📝

| # | Scenario | Type | Validation |
|---|----------|------|------------|
| 1 | Navigate to Register | ✅ Navigation | Login → Register screen |
| 2 | Form elements present | ✅ Layout | Email, Display, Username, Password, Confirm |
| 3 | Button disabled when empty | ❌ Negative | Register button disabled |
| 4 | Fill form & submit | ✅ Positive | Random Yopmail email, submit form |
| 5 | OTP from Yopmail | ✅ Positive | Auto-extract OTP + enter in app |
| 6 | Back to login | ✅ Navigation | Return to login screen |

### Test 13 — Forgot Password 🔑

| # | Scenario | Type | Validation |
|---|----------|------|------------|
| 1 | Navigate to forgot page | ✅ Navigation | From login screen |
| 2 | Form elements | ✅ Layout | Title + email field |
| 3 | Send OTP disabled | ❌ Negative | Button disabled when empty |
| 4 | Back to login | ✅ Navigation | Return to login screen |

### Test 14 — Booking Checkout 💳

| # | Scenario | Type | Validation |
|---|----------|------|------------|
| 1 | Trip → Book → Checkout | ✅ E2E | Full booking flow to invoice page |

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
    "appium:noReset": True,                      # Persist login state
    "appium:autoGrantPermissions": True,
    "appium:autoAcceptAlerts": True,
}
```

### Test Data

```python
VALID_EMAIL    = "danip1@yopmail.com"
VALID_PASSWORD = "Sandi123!"
```

### Permission Dialog Handling

```python
# Auto-handled via Appium capabilities
"appium:autoGrantPermissions": True,
"appium:autoAcceptAlerts": True,
```

Fallback: `BasePage.dismiss_permission_dialog()` catches any remaining dialogs.

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
│  Test Files          : 15 files (+1 advanced)            │
│  Total Test Cases    : 109+ scenarios                    │
│  Positive Tests      : 80+                               │
│  Negative Tests      : 15+                               │
│  Page Objects        : 7 (+ 1 base)                      │
│                                                          │
│  Features Covered:                                       │
│    ✅ Login (positive + 5 negative scenarios)            │
│    ✅ Home Screen (layout + features + deep)             │
│    ✅ Banner Carousel (swipe + indicators)               │
│    ✅ Open Trip Discovery & Detail                       │
│    ✅ Create Itinerary (full CRUD + 5 activities)        │
│    ✅ Itinerary Cleanup (auto-delete test data)          │
│    ✅ Profile Management (tabs, filters, deep)           │
│    ✅ Search & Notifications                             │
│    ✅ Logout & Session Restoration                       │
│    ✅ Login Extras Validation                            │
│    ✅ Explore Deep Interactions                          │
│    ✅ Home Deep Scroll & Carousels                       │
│    ✅ Registration + Yopmail OTP                         │
│    ✅ Forgot Password Flow                               │
│    ✅ Booking Checkout (E2E)                             │
│    ✅ Budget Tracking (API-driven)                       │
├──────────────────────────────────────────────────────────┤
│  EXECUTION : Real Device (Xiaomi Redmi Note 13, API 35) │
│  CONNECTION: Wireless ADB                                │
│  FRAMEWORK : Appium 3.x + UiAutomator2 + Pytest         │
└──────────────────────────────────────────────────────────┘
```

---

## 🛡️ Stability Features

| Feature | Implementation |
|---------|----------------|
| **Smart Navigation** | Bottom Nav semantic locators instead of hardcoded coordinates |
| **Safe Scrolling** | `UiScrollable(scrollable(true))` — no blind swipe gestures |
| **Auto Retry** | 3x rerun on failure via `pytest-rerunfailures` |
| **Session Persistence** | Single Appium session across all 109+ tests |
| **State Recovery** | Automated re-login after logout tests (test_08) |
| **Driver Keep-Alive** | Active polling during Yopmail OTP wait to prevent idle timeout |
| **Safe Back Navigation** | Conditional `press_keycode(4)` — stops when target screen found |

---

<div align="center">

**Built with ❤️ by [Dhany Arya Pratama](https://github.com/dhanyarya-qa)**

</div>
