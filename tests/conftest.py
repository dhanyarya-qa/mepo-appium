"""
Pytest Configuration & Fixtures
================================
Shared fixtures for Appium driver lifecycle, page object injection,
and test reporting for Mepo Travel E2E testing on real device.
"""

import os
import sys
import io
import logging
import time
import pytest
import base64
import csv
from datetime import datetime

from appium import webdriver as appium_webdriver
from appium.options.android import UiAutomator2Options

from config.settings import AppiumConfig, LoginCredentials

# ──────────────────────────────────────────────────
# Force UTF-8 stdout on Windows to support Unicode
# ──────────────────────────────────────────────────
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# ──────────────────────────────────────────────────
# Logging Setup
# ──────────────────────────────────────────────────

LOG_DIR = os.path.join(os.path.dirname(__file__), "..", "reports", "logs")
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
    datefmt="%H:%M:%S",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(
            os.path.join(LOG_DIR, f"test_run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
            encoding="utf-8",
        ),
    ],
)

logger = logging.getLogger("conftest")


# ──────────────────────────────────────────────────
# Report Directory Setup
# ──────────────────────────────────────────────────

SCREENSHOT_DIR = os.path.join(os.path.dirname(__file__), "..", "reports", "screenshots")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

VIDEO_DIR = os.path.join(os.path.dirname(__file__), "..", "reports", "videos")
os.makedirs(VIDEO_DIR, exist_ok=True)


# ──────────────────────────────────────────────────
# Fixtures — Appium Driver (Session-Scoped)
# ──────────────────────────────────────────────────

@pytest.fixture(scope="session")
def driver():
    """
    Session-scoped Appium driver targeting real device via wireless ADB.
    Creates a single driver instance shared across ALL tests.
    """
    logger.info("=" * 60)
    logger.info("[INIT] INITIALIZING APPIUM DRIVER — REAL DEVICE")
    logger.info("=" * 60)

    caps = AppiumConfig.DESIRED_CAPS.copy()
    options = UiAutomator2Options()
    for key, value in caps.items():
        options.set_capability(key, value)

    _driver = None
    try:
        _driver = appium_webdriver.Remote(
            command_executor=AppiumConfig.SERVER_URL,
            options=options,
        )
        _driver.implicitly_wait(10)
        logger.info(f"[OK] Appium driver started — session: {_driver.session_id}")
        logger.info(f"     Device: {caps.get('appium:deviceName')}")
        logger.info(f"     UDID: {caps.get('appium:udid')}")
        logger.info(f"     App: {caps.get('appium:appPackage')}")

        # Wait for app to fully load
        time.sleep(5)

        yield _driver

    except Exception as e:
        logger.error(f"[FAIL] Failed to start Appium driver: {e}")
        pytest.exit(f"Cannot connect to Appium/device: {e}", returncode=1)

    finally:
        if _driver:
            logger.info("[STOP] Quitting Appium driver...")
            _driver.quit()
            logger.info("[OK] Appium driver terminated")


@pytest.fixture(autouse=True)
def video_recording(request, driver):
    """
    Starts screen recording before a test and stops it after.
    If the test fails, saves the video payload.
    """
    try:
        driver.start_recording_screen(videoSize="720x1280", timeLimit=1800, bitRate=2000000)
    except Exception as e:
        logger.warning(f"Failed to start recording: {e}")

    yield

    try:
        payload = driver.stop_recording_screen()
        # Ensure rep_call exists and check if failed
        if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            video_name = f"FAIL_{request.node.name}_{timestamp}.mp4"
            video_path = os.path.join(VIDEO_DIR, video_name)
            with open(video_path, "wb") as f:
                f.write(base64.b64decode(payload))
            logger.info(f"[VIDEO] Failure video saved: {video_path}")
    except Exception as e:
        logger.warning(f"Failed to process video recording: {e}")


# ──────────────────────────────────────────────────
# Fixtures — Page Objects
# ──────────────────────────────────────────────────

@pytest.fixture
def login_page(driver):
    from pages.login_page import LoginPage
    return LoginPage(driver)


@pytest.fixture
def home_page(driver):
    from pages.home_page import HomePage
    return HomePage(driver)


@pytest.fixture
def open_trip_page(driver):
    from pages.open_trip_page import OpenTripPage
    return OpenTripPage(driver)


@pytest.fixture
def profile_page(driver):
    from pages.profile_page import ProfilePage
    return ProfilePage(driver)


@pytest.fixture
def create_itinerary_page(driver):
    from pages.create_itinerary_page import CreateItineraryPage
    return CreateItineraryPage(driver)


@pytest.fixture
def budget_page(driver):
    from pages.budget_page import BudgetPage
    return BudgetPage(driver)


@pytest.fixture
def splash_page(driver):
    from pages.splash_page import SplashPage
    return SplashPage(driver)


@pytest.fixture(scope="session")
def appium_driver(driver):
    """Alias for the session-scoped driver fixture (used by advanced tests)."""
    return driver


@pytest.fixture(scope="session")
def api_helper():
    """Session-scoped API helper for backend pre-conditions."""
    from utils.api_helper import MepoAPIHelper
    helper = MepoAPIHelper()
    yield helper
    helper.close()


# ──────────────────────────────────────────────────
# Fixtures — Helpers
# ──────────────────────────────────────────────────

@pytest.fixture
def ensure_app_foreground(driver):
    """Ensure Mepo app is in the foreground."""
    if driver.current_package != "com.mepo":
        driver.activate_app("com.mepo")
        time.sleep(3)


@pytest.fixture
def go_home(driver):
    """Navigate back to home screen within the app."""
    from pages.home_page import HomePage
    home = HomePage(driver)

    # If not in app, activate it
    if driver.current_package != "com.mepo":
        driver.activate_app("com.mepo")
        time.sleep(3)

    # Try tapping Home tab
    if not home.is_home_displayed():
        try:
            home.tap(home.TAB_HOME, timeout=5)
            time.sleep(2)
        except Exception:
            driver.back()
            time.sleep(1)

    return home


# ──────────────────────────────────────────────────
# Hooks — Reporting & Screenshots
# ──────────────────────────────────────────────────

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Capture screenshot on test failure and attach to report."""
    outcome = yield
    report = outcome.get_result()
    
    # Store the report on the item so fixtures can access it (e.g. rep_setup, rep_call, rep_teardown)
    setattr(item, "rep_" + report.when, report)

    if report.when == "call" and report.failed:
        _driver = item.funcargs.get("driver")
        if _driver:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_name = f"FAIL_{item.name}_{timestamp}.png"
            screenshot_path = os.path.join(SCREENSHOT_DIR, screenshot_name)
            try:
                _driver.save_screenshot(screenshot_path)
                logger.info(f"[SCREENSHOT] Failure screenshot saved: {screenshot_path}")
            except Exception as e:
                logger.warning(f"[WARN] Could not save failure screenshot: {e}")


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """Custom terminal summary showing final PASS/FAIL report."""
    _safe_print("")
    _safe_print("=" * 70)
    _safe_print("  MEPO TRAVEL E2E TEST — FINAL REPORT")
    _safe_print("=" * 70)

    passed = terminalreporter.stats.get("passed", [])
    failed = terminalreporter.stats.get("failed", [])
    errors = terminalreporter.stats.get("error", [])
    skipped = terminalreporter.stats.get("skipped", [])

    total = len(passed) + len(failed) + len(errors) + len(skipped)

    if passed:
        _safe_print(f"\n  [PASS] PASSED ({len(passed)}):")
        for test in passed:
            _safe_print(f"     +-- {test.nodeid}")

    if failed:
        _safe_print(f"\n  [FAIL] FAILED ({len(failed)}):")
        for test in failed:
            _safe_print(f"     +-- {test.nodeid}")
            if test.longrepr:
                lines = str(test.longrepr).strip().split("\n")
                if lines:
                    _safe_print(f"     |   +-- {lines[-1].strip()}")

    if errors:
        _safe_print(f"\n  [ERROR] ERRORS ({len(errors)}):")
        for test in errors:
            _safe_print(f"     +-- {test.nodeid}")

    if skipped:
        _safe_print(f"\n  [SKIP] SKIPPED ({len(skipped)}):")
        for test in skipped:
            _safe_print(f"     +-- {test.nodeid}")

    _safe_print(f"\n  {'-' * 50}")
    _safe_print(
        f"  Total: {total}  |  PASS: {len(passed)}  |  "
        f"FAIL: {len(failed)}  |  ERROR: {len(errors)}  |  SKIP: {len(skipped)}"
    )
    _safe_print(f"  {'-' * 50}")

    if not failed and not errors:
        _safe_print("\n  >>> ALL TESTS PASSED <<<")
    else:
        _safe_print("\n  >>> SOME TESTS FAILED <<<")

    _safe_print("=" * 70)
    _safe_print("")

    # ── Custom Code for Spreadsheet Dump ──
    spreadsheet_path = os.path.join(LOG_DIR, "..", f"Test_Results_Spreadsheet_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
    try:
        with open(spreadsheet_path, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Test Name", "Status", "Duration (s)", "Error Details"])
            
            for k, v in terminalreporter.stats.items():
                if k in ['passed', 'failed', 'error', 'skipped']:
                    for test in v:
                        name = test.nodeid.split("::")[-1] if "::" in test.nodeid else test.nodeid
                        status = k.upper()
                        duration = getattr(test, 'duration', 0.0)
                        error = ""
                        if hasattr(test, 'longrepr') and test.longrepr:
                            lines = str(test.longrepr).strip().split('\n')
                            error = lines[-1].strip() if lines else ""
                        writer.writerow([name, status, f"{duration:.2f}", error])
        _safe_print(f"  [SPREADSHEET] Laporan Google Sheets-ready tersimpan di: \n  => {os.path.abspath(spreadsheet_path)}")
        _safe_print("=" * 70)
    except Exception as e:
        _safe_print(f"  [WARN] Failed to write Spreadsheet report: {e}")


def _safe_print(text: str):
    """Print text safely, handling encoding errors on Windows."""
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode("ascii", errors="replace").decode("ascii"))
