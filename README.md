<div align="center">

# 📱 Mepo Travel — Appium E2E Automation

### Android Mobile App Testing Framework

[![Appium](https://img.shields.io/badge/Appium_2.x-662D8C?style=flat-square&logo=appium&logoColor=white)](https://appium.io/)
[![Python](https://img.shields.io/badge/Python_3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org/)
[![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?style=flat-square&logo=pytest&logoColor=white)](https://pytest.org/)
[![Android](https://img.shields.io/badge/Android_15-3DDC84?style=flat-square&logo=android&logoColor=white)](https://developer.android.com/)

*End-to-end mobile automation for the Mepo Travel Android app on real Xiaomi device — powered by Page Object Model, API-driven preconditions, and rich failure diagnostics.*

</div>

---

## ✨ Key Features

<table>
<tr>
<td width="50%">

### 🎯 Test Scenarios (40+ Tests)
- 🔐 **Login** — Positive & negative (5 negative + 1 positive)
- 🏠 **Home Screen** — Layout, banners, service cards, sections
- 🗺 **Open Trip** — Navigation, detail, Custom Trip, references
- 📋 **Create Itinerary** — Modal, form validation, CRUD
- 👤 **Profile** — Navigation, tabs, filters, itinerary cards
- 🔍 **Search & Notifications** — Icon navigation, page content
- 🚪 **Logout** — Settings → Logout → Login screen

</td>
<td width="50%">

### 🔬 Framework Features
- 🏗️ **Page Object Model (POM)** — Clean separation of concerns
- 🔌 **API-Driven Preconditions** — Seed & reset test data
- 📸 **Auto Screenshots** — Capture on every failure
- 📝 **Rich Logging** — Timestamped logs with emoji markers
- 🔄 **Session Persistence** — `noReset=True` across test suite
- 📊 **Custom Terminal Report** — PASS/FAIL summary table
- 🛡️ **Permission Auto-handling** — Auto-grant & dismiss dialogs

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
│   ├── test_01_login.py             # Login negative + positive scenarios
│   ├── test_02_home_banners.py      # Home layout, banners, service cards
│   ├── test_03_open_trip.py         # Open Trip navigation & detail
│   ├── test_04_create_itinerary.py  # Create Itinerary modal CRUD
│   ├── test_05_profile.py           # Profile page layout & tabs
│   ├── test_06_search_notifs.py     # Search & Notification features
│   ├── test_07_logout.py            # Logout flow (final test)
│   └── test_advanced_features.py    # API-driven Open Trip & Budget
├── utils/
│   ├── __init__.py
│   └── api_helper.py               # REST API client for preconditions
├── reports/
│   ├── logs/                        # Test run logs (auto-generated)
│   └── screenshots/                 # Failure screenshots (auto-captured)
├── apps/                            # Place APK file here
├── scripts/                         # Utility scripts
├── .env.example                     # Environment variable template
├── pytest.ini                       # Pytest configuration & markers
├── requirements.txt                 # Python dependencies
└── README.md
```

---

## 📋 Prerequisites

| Component | Version | Purpose |
|-----------|---------|---------|
| Python | ≥ 3.10 | Test runtime |
| Appium Server | ≥ 2.x | Mobile automation server |
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

# 3. Configure environment
cp .env.example .env
# Edit .env with your device UDID and credentials

# 4. Start Appium Server (separate terminal)
appium --relaxed-security

# 5. Connect device via wireless ADB
adb connect <device-ip>:<port>

# 6. Ensure Mepo app is installed on device
```

---

## ▶️ Running Tests

```bash
# Run full E2E suite (recommended order: login → home → trip → itinerary → profile → logout)
pytest tests/ -v -s

# Individual test files
pytest tests/test_01_login.py -v -s              # Login scenarios
pytest tests/test_02_home_banners.py -v -s        # Home screen features
pytest tests/test_03_open_trip.py -v -s           # Open Trip discovery
pytest tests/test_04_create_itinerary.py -v -s    # Create Itinerary CRUD
pytest tests/test_05_profile.py -v -s             # Profile management
pytest tests/test_06_search_notifs.py -v -s       # Search & Notifications
pytest tests/test_07_logout.py -v -s              # Logout flow

# Run by marker
pytest -m smoke -v -s                             # Smoke tests only
pytest -m login -v -s                             # Login tests only
pytest -m home -v -s                              # Home screen tests only

# Advanced API-driven scenarios
pytest tests/test_advanced_features.py -v -s

# Generate HTML report
pytest tests/ -v -s --html=reports/report.html
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

### Test 05 — Profile 👤

| # | Scenario | Type | Validation |
|---|----------|------|------------|
| 1 | Navigate to profile | ✅ Positive | "My Profile" header |
| 2 | Username displayed | ✅ Layout | "danip" |
| 3 | Handle displayed | ✅ Layout | "danip971" |
| 4 | My Itinerary tab | ✅ Feature | Selected by default |
| 5 | Saved Itinerary tab | ✅ Feature | Tab switch works |
| 6 | Filters (Activity/Shared/Draft) | ✅ Feature | 3 filter buttons |
| 7 | Itinerary cards | ✅ Feature | Finished/Ongoing status |

### Test 06 — Search & Notifications 🔍

| # | Scenario | Type | Validation |
|---|----------|------|------------|
| 1 | Tap search icon | ✅ Positive | Search page loads |
| 2 | Search field present | ✅ Layout | Input field found |
| 3 | Tap notification icon | ✅ Positive | Notification page loads |
| 4 | Notification content | ✅ Layout | Page rendered |

### Test 07 — Logout 🚪

| # | Scenario | Type | Validation |
|---|----------|------|------------|
| 1 | Navigate to profile | ✅ Positive | My Profile header |
| 2 | Open settings | ✅ Positive | Settings page |
| 3 | Find & click logout | ✅ Positive | Logout button tapped |
| 4 | Verify logged out | ✅ Positive | Login screen displayed |

---

## ⚙️ Configuration

### Appium Capabilities (Real Device)

```python
{
    "platformName": "Android",
    "appium:automationName": "UiAutomator2",
    "appium:deviceName": "23124RA7EO",          # Xiaomi device
    "appium:platformVersion": "15",
    "appium:udid": "192.168.1.62:41821",        # Wireless ADB
    "appium:appPackage": "com.mepo",
    "appium:appActivity": "com.mepo.MainActivity",
    "appium:noReset": True,                      # Persist login state
    "appium:autoGrantPermissions": True,
    "appium:autoAcceptAlerts": True,
}
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
| 🖥️ Terminal | Custom summary — PASS/FAIL count per test |
| 📝 Logs | `reports/logs/test_run_YYYYMMDD_HHMMSS.log` |
| 📸 Screenshots | `reports/screenshots/` (auto on failure + key steps) |
| 📄 HTML Report | `pytest --html=reports/report.html` |

---

## 📈 Coverage Summary

```
┌──────────────────────────────────────────────────────┐
│           TEST COVERAGE REPORT                       │
├──────────────────────────────────────────────────────┤
│  Test Files          : 8 files                       │
│  Total Test Methods  : 40+ scenarios                 │
│  Positive Tests      : 28+                           │
│  Negative Tests      : 12+                           │
│  Page Objects        : 7 (+ 1 base)                  │
│                                                      │
│  Features Covered:                                   │
│    ✅ Login (positive + negative)                    │
│    ✅ Home Screen (layout + features)                │
│    ✅ Banner Carousel                                │
│    ✅ Open Trip Discovery                            │
│    ✅ Create Itinerary (CRUD)                        │
│    ✅ Profile Management                             │
│    ✅ Search & Notifications                         │
│    ✅ Logout                                         │
│    ✅ Budget Tracking (API-driven)                   │
├──────────────────────────────────────────────────────┤
│  EXECUTION: Real Device (Xiaomi, Android 15)         │
│  CONNECTION: Wireless ADB                            │
└──────────────────────────────────────────────────────┘
```

---

<div align="center">

**Built with ❤️ by [Dhany Arya Pratama](https://github.com/dhanyarya-qa)**

</div>
