"""
Test 14 — Login Again
=========================================
End-to-end scenario:
  1. Login using the email/password from test_12/test_13 (shared_email.json)
  2. Confirm successfully reached Home Page.

Dependencies: shared_email.json from test_12/13
"""

import pytest
import time
import json
import os
import logging
from appium.webdriver.common.appiumby import AppiumBy

logger = logging.getLogger(__name__)

pytestmark = [pytest.mark.login, pytest.mark.regression]

SHARED_FILE = os.path.join(os.path.dirname(__file__), "..", "reports", "shared_email.json")

# The password may have been changed in test_13 (forgot password)
NEW_PASSWORD = "NewSandi123!"


def _load_shared_email():
    """Load email + password from shared_email.json."""
    if os.path.exists(SHARED_FILE):
        with open(SHARED_FILE, "r") as f:
            data = json.load(f)
        return data.get("email"), data.get("password")
    return None, None


class TestLoginAgain:
    """Tests logging in again with the registered/reset email."""

    def test_01_login_with_registered_email(self, driver):
        """Login using the email from test_12/13."""
        logger.info("\n=== LOGIN AGAIN: Login with registered email ===")

        email, original_password = _load_shared_email()
        assert email, "No email in shared_email.json — run test_12 first"

        # Check if we're already logged in (on Home screen)
        welcome = driver.find_elements(AppiumBy.XPATH,
            "//*[contains(@content-desc, 'Welcome,')]")
        home_tab = driver.find_elements(AppiumBy.XPATH,
            "//*[contains(@content-desc, 'Home\nTab 1 of 4')]")
        if welcome or home_tab:
            logger.info("  ✅ Already logged in — skipping login")
            return

        # Should be on Login screen
        login_btn = driver.find_elements(AppiumBy.XPATH,
            "//*[@content-desc='Login']")
        if not login_btn:
            logger.warning("  ⚠ Not on login screen, trying to navigate...")
            for _ in range(3):
                try:
                    driver.press_keycode(4)
                except Exception:
                    pass
                time.sleep(2)

        # Fill login form
        edit_fields = driver.find_elements(AppiumBy.XPATH, "//android.widget.EditText")
        assert len(edit_fields) >= 2, f"Need 2 fields for login, found {len(edit_fields)}"

        # Email
        edit_fields[0].click()
        time.sleep(0.3)
        edit_fields[0].send_keys(email)
        time.sleep(0.5)

        # Try NEW_PASSWORD first (from test_13 forgot password), fallback to original
        edit_fields[1].click()
        time.sleep(0.3)
        edit_fields[1].send_keys(NEW_PASSWORD)
        time.sleep(0.5)

        try:
            driver.hide_keyboard()
        except Exception:
            pass
        time.sleep(1)

        # Tap Login
        login_btn = driver.find_elements(AppiumBy.XPATH,
            "//android.widget.Button[@content-desc='Login']")
        if login_btn:
            login_btn[-1].click()
            time.sleep(5)

        # Check if login succeeded
        welcome = driver.find_elements(AppiumBy.XPATH,
            "//*[contains(@content-desc, 'Welcome,')]")
        home_tab = driver.find_elements(AppiumBy.XPATH,
            "//*[contains(@content-desc, 'Home\nTab 1 of 4')]")

        if not welcome and not home_tab:
            # Try original password
            logger.info("  ⚠ New password failed, trying original password...")
            for _ in range(3):
                try:
                    driver.press_keycode(4)
                except Exception:
                    pass
                time.sleep(1)

            edit_fields = driver.find_elements(AppiumBy.XPATH, "//android.widget.EditText")
            if len(edit_fields) >= 2:
                edit_fields[0].click()
                time.sleep(0.3)
                edit_fields[0].clear()
                edit_fields[0].send_keys(email)
                time.sleep(0.5)
                edit_fields[1].click()
                time.sleep(0.3)
                edit_fields[1].clear()
                edit_fields[1].send_keys(original_password or "Sandi123!")
                time.sleep(0.5)

                try:
                    driver.hide_keyboard()
                except Exception:
                    pass

                login_btn = driver.find_elements(AppiumBy.XPATH,
                    "//android.widget.Button[@content-desc='Login']")
                if login_btn:
                    login_btn[-1].click()
                    time.sleep(5)

        welcome = driver.find_elements(AppiumBy.XPATH,
            "//*[contains(@content-desc, 'Welcome,')]")
        home_tab = driver.find_elements(AppiumBy.XPATH,
            "//*[contains(@content-desc, 'Home\nTab 1 of 4')]")
        
        assert welcome or home_tab, "Login failed with both passwords"
        logger.info(f"  ✅ Logged in as {email} and reached Home screen successfully")
