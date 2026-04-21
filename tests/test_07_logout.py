"""
Test 07 — Logout (Real Device)
================================
Verifies the logout flow: navigate to profile settings, logout,
and confirm return to login screen.

XML Source: reports/real_device/profile_02_after_tap.xml
            reports/real_device/explore_01_login.xml
"""

import pytest
import time
import logging
from appium.webdriver.common.appiumby import AppiumBy
from utils.wait_helpers import wait_find, wait_for_any, FAST, NORMAL, SLOW

logger = logging.getLogger(__name__)

pytestmark = [pytest.mark.logout, pytest.mark.regression]


def _go_home(driver):
    """Navigate to home screen safely via Bottom Nav tab."""
    for attempt in range(5):
        # 1. Check for Bottom Nav Home Tab
        home_tab = driver.find_elements(AppiumBy.XPATH,
            "//*[contains(@content-desc, 'Home\nTab 1 of 4')]")
        if home_tab:
            home_tab[-1].click()
            time.sleep(2)
            return True

        # 2. Already on Home? (Welcome text visible)
        welcome = driver.find_elements(AppiumBy.XPATH,
            "//*[contains(@content-desc, 'Welcome,')]")
        if welcome:
            logger.info("  Already on Home Screen")
            return True

        # 3. Press back to get closer to Home
        logger.info(f"  Back press {attempt+1}/5 to find Home")
        try:
            driver.press_keycode(4)
        except Exception:
            pass
        time.sleep(2)

        # 4. Check if we accidentally exited the app
        try:
            current = driver.current_package
            if current != "com.mepo":
                logger.warning(f"  Left Mepo ({current}), re-activating...")
                driver.activate_app("com.mepo")
                time.sleep(3)
        except Exception:
            pass

    return False


class TestLogout:
    """Full logout flow."""

    def test_navigate_to_profile(self, driver):
        """Navigate to profile from home."""
        logger.info("\n=== LOGOUT: Navigate to Profile ===")

        assert _go_home(driver), "Cannot reach home screen"
        time.sleep(1)

        # Use Bottom Nav Profile Tab (semantic locator, not coordinates)
        profile_tab = driver.find_elements(AppiumBy.XPATH,
            "//*[contains(@content-desc, 'Profile\nTab 4 of 4')]")
        if not profile_tab:
            profile_tab = driver.find_elements(AppiumBy.XPATH,
                "//*[contains(@content-desc, 'Profile') and contains(@content-desc, 'Tab')]")

        if profile_tab:
            profile_tab[-1].click()
            time.sleep(3)
        else:
            # Fallback: tap profile icon (top-right)
            driver.tap([(978, 245)], 500)
            time.sleep(3)

        title = driver.find_elements(AppiumBy.XPATH,
            "//*[@content-desc='My Profile']")
        assert len(title) > 0, "Profile page not opened"
        logger.info("✅ On profile page")

    def test_open_settings(self, driver):
        """Tap settings button on profile page."""
        logger.info("\n=== LOGOUT: Open Settings ===")

        # From XML: settings button is the last Button at [948,95][1080,227]
        buttons = driver.find_elements(AppiumBy.XPATH,
            "//android.widget.Button[@clickable='true']")
        assert len(buttons) >= 2, "Settings button not found"

        # Settings is the last button in the header
        buttons[-1].click()
        time.sleep(1.5)
        logger.info("✅ Settings page opened")

    def test_find_logout(self, driver):
        """Find and tap logout button in settings."""
        logger.info("\n=== LOGOUT: Find & Tap Logout ===")

        s = driver.get_window_size()

        # Scroll through settings to find Logout
        for attempt in range(5):
            logout_elements = driver.find_elements(AppiumBy.XPATH,
                "//*[contains(@content-desc, 'Logout') "
                "or contains(@content-desc, 'Log Out') "
                "or contains(@content-desc, 'Sign Out') "
                "or contains(@content-desc, 'Log out')]")
            if logout_elements:
                logout_elements[0].click()
                time.sleep(1.5)
                logger.info("✅ Logout button tapped")
                break

            # Scroll down to find it
            driver.swipe(s['width']//2, int(s['height']*0.75),
                        s['width']//2, int(s['height']*0.25), 800)
            time.sleep(0.5)

    def test_confirm_logout(self, driver):
        """Confirm logout in dialog if present."""
        logger.info("\n=== LOGOUT: Confirm ===")

        # Look for confirmation dialog
        confirm_buttons = driver.find_elements(AppiumBy.XPATH,
            "//*[contains(@content-desc, 'Yes') "
            "or contains(@content-desc, 'OK') "
            "or contains(@content-desc, 'Confirm') "
            "or contains(@content-desc, 'Continue') "
            "or contains(@content-desc, 'continue') "
            "or contains(@content-desc, 'Logout') "
            "or contains(@content-desc, 'Log Out')]")

        if confirm_buttons:
            confirm_buttons[0].click()
            time.sleep(2)
            logger.info("✅ Logout confirmed")
        else:
            logger.info("ℹ No confirmation dialog (direct logout)")

    def test_verify_logged_out(self, driver):
        """Should be on login screen after logout."""
        logger.info("\n=== LOGOUT: Verify Logged Out ===")

        time.sleep(2)

        # Check for login screen indicators
        # From XML: content-desc="Welcome Back!", EditText elements
        login_indicators = [
            driver.find_elements(AppiumBy.XPATH,
                "//*[contains(@content-desc, 'Welcome Back')]"),
            driver.find_elements(AppiumBy.XPATH,
                "//android.widget.EditText"),
            driver.find_elements(AppiumBy.XPATH,
                "//*[@content-desc='Login']"),
        ]

        found = any(len(ind) > 0 for ind in login_indicators)
        assert found, "Login screen not detected — logout may have failed"

        driver.save_screenshot("reports/screenshots/logout_success.png")
        logger.info("✅ LOGOUT SUCCESSFUL — Login screen displayed!")
