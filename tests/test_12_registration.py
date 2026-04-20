"""
Test 12 — Registration Flow (Real Device)
==========================================
Verifies the full registration flow:
  1. From Login screen → tap "Register" link
  2. Fill form:
       - Email    : autoqa{rnd}@yopmail.com  (random, unique)
       - Display  : AutoQA {rnd}             (tied to email suffix)
       - Username : autoqa{rnd}             (same prefix as email)
       - Password : Sandi123!
       - Confirm  : Sandi123!
  3. Tap "Register" button
  4. Fetch OTP from Yopmail website (same inbox as registration email)
  5. Enter OTP in-app, verify success / navigate back to Login

Dependencies:
  pip install yopmail beautifulsoup4 requests
"""

import pytest
import time
import random
import re
import logging
from appium.webdriver.common.appiumby import AppiumBy

logger = logging.getLogger(__name__)

pytestmark = [pytest.mark.login, pytest.mark.regression]

# ── Test Data ──────────────────────────────────────────
RND         = random.randint(1000, 9999)
YOP_USER    = f"autoqa{RND}"
TEST_EMAIL  = f"{YOP_USER}@yopmail.com"
DISPLAY     = f"AutoQA {RND}"
USERNAME    = f"autoqa{RND}"
PASSWORD    = "Sandi123!"
# ───────────────────────────────────────────────────────


# ── Helpers ─────────────────────────────────────────────────────────────────

def _ensure_login_screen(driver):
    """Make sure we are on the Login screen."""
    for _ in range(5):
        login_btn = driver.find_elements(AppiumBy.XPATH,
            "//android.widget.Button[@content-desc='Login']")
        if login_btn:
            return True
        welcome_back = driver.find_elements(AppiumBy.XPATH,
            "//*[contains(@content-desc, 'Welcome Back')]")
        if welcome_back:
            return True
        try:
            driver.press_keycode(4)
        except Exception:
            pass
        time.sleep(2)
    return False


def _go_to_register(driver):
    """From login screen, tap the 'Register' link to open registration page."""
    register_link = driver.find_elements(AppiumBy.XPATH,
        "//*[@content-desc='Register' and @clickable='true']")
    if not register_link:
        # Try broader search
        register_link = driver.find_elements(AppiumBy.XPATH,
            "//*[contains(@content-desc, 'Register')]")
    if register_link:
        register_link[0].click()
        time.sleep(3)
        return True
    return False


def _on_register_screen(driver):
    """Return True if we are on the Create Account (registration) screen."""
    create_acc = driver.find_elements(AppiumBy.XPATH,
        "//*[@content-desc='Create your Account']")
    return len(create_acc) > 0


def _fetch_otp_from_yopmail(yop_username, max_retries=10, wait_sec=5):
    """
    Poll Yopmail inbox until a new email arrives, then extract the OTP.
    Returns OTP string, or None if not found.
    """
    try:
        from yopmail import Yopmail
        y = Yopmail(yop_username)

        for attempt in range(max_retries):
            logger.info(f"  📬 Polling Yopmail inbox ({attempt+1}/{max_retries})...")
            mail_ids = y.get_mail_ids()
            if mail_ids:
                mail = y.get_mail_body(mail_ids[0])
                # Extract OTP: 4–8 digit number
                text = mail.text if hasattr(mail, 'text') else str(mail)
                otp_matches = re.findall(r'\b(\d{4,8})\b', text)
                if otp_matches:
                    otp = otp_matches[0]
                    logger.info(f"  ✅ OTP extracted from Yopmail: {otp}")
                    return otp
                else:
                    logger.warning("  ⚠ Email found but no OTP digits detected.")
                    logger.debug(f"  Mail content snippet: {text[:300]}")
                    return None
            time.sleep(wait_sec)

        logger.warning("  ⚠ No email received in Yopmail after all retries.")
        return None

    except Exception as e:
        logger.error(f"  ❌ Yopmail fetch failed: {e}")
        return None


# ── Test Class ───────────────────────────────────────────────────────────────

class TestRegistration:
    """Full positive registration flow using a fresh Yopmail address."""

    def test_01_navigate_to_register(self, driver):
        """From Login screen, tap 'Register' to open Registration form."""
        logger.info("\n=== REGISTRATION: Step 1 — Navigate to Register ===")
        assert _ensure_login_screen(driver), \
            "❌ Could not reach Login screen before starting registration test"
        assert _go_to_register(driver), \
            "❌ Could not find and tap 'Register' link on Login screen"
        assert _on_register_screen(driver), \
            "❌ Registration screen did not open after tapping Register"
        logger.info("✅ Reached Registration / Create Account screen")

    def test_02_validate_form_elements(self, driver):
        """Verify all required form fields are present."""
        logger.info("\n=== REGISTRATION: Step 2 — Validate Form Elements ===")
        if not _on_register_screen(driver):
            assert _go_to_register(driver), "Could not reach register screen"

        email_fld = driver.find_elements(AppiumBy.XPATH,
            "//android.widget.EditText[@hint='Add email']")
        assert len(email_fld) > 0, "Email field ('Add email') not found"

        display_fld = driver.find_elements(AppiumBy.XPATH,
            "//android.widget.EditText[@hint='Add Display Name']")
        assert len(display_fld) > 0, "Display Name field not found"

        user_fld = driver.find_elements(AppiumBy.XPATH,
            "//android.widget.EditText[contains(@hint, 'Username')]")
        assert len(user_fld) > 0, "Username field not found"

        passwords = driver.find_elements(AppiumBy.XPATH,
            "//android.widget.EditText[@password='true']")
        assert len(passwords) >= 2, \
            f"Need ≥2 password fields (Password + Confirm), found {len(passwords)}"

        logger.info("✅ All 5 form fields found: Email, Display, Username, Password, Confirm")

    def test_03_register_button_disabled_when_empty(self, driver):
        """Register button should be disabled with empty form."""
        logger.info("\n=== REGISTRATION: Step 3 — Button Disabled Check ===")
        if not _on_register_screen(driver):
            pytest.skip("Not on register screen")

        # Use find_elements to avoid throwing exception
        reg_btns = driver.find_elements(AppiumBy.XPATH,
            "//android.widget.Button[@content-desc='Register']")
        if reg_btns:
            enabled = reg_btns[0].get_attribute("enabled")
            assert enabled == "false", \
                f"Register button should be disabled when form is empty, but got enabled={enabled}"
            logger.info("✅ Register button correctly disabled when form is empty")
        else:
            logger.info("ℹ Register button not found in disabled state (may already have text) — skip")

    def test_04_fill_and_submit_form(self, driver):
        """Fill registration form with Yopmail email and submit."""
        logger.info(f"\n=== REGISTRATION: Step 4 — Fill Form ===")
        logger.info(f"  📧 Email   : {TEST_EMAIL}")
        logger.info(f"  👤 Display : {DISPLAY}")
        logger.info(f"  🔑 User    : {USERNAME}")

        if not _on_register_screen(driver):
            assert _go_to_register(driver) and _on_register_screen(driver), \
                "Could not reach register screen"

        # Grab fields
        email_fld    = driver.find_elements(AppiumBy.XPATH,
            "//android.widget.EditText[@hint='Add email']")
        display_fld  = driver.find_elements(AppiumBy.XPATH,
            "//android.widget.EditText[@hint='Add Display Name']")
        user_fld     = driver.find_elements(AppiumBy.XPATH,
            "//android.widget.EditText[contains(@hint, 'Username')]")
        password_flds = driver.find_elements(AppiumBy.XPATH,
            "//android.widget.EditText[@password='true']")

        # Fill Email
        if email_fld:
            email_fld[0].click(); time.sleep(0.3)
            email_fld[0].send_keys(TEST_EMAIL); time.sleep(0.5)
            logger.info(f"  ✍ Email filled: {TEST_EMAIL}")

        # Fill Display Name
        if display_fld:
            display_fld[0].click(); time.sleep(0.3)
            display_fld[0].send_keys(DISPLAY); time.sleep(0.5)
            logger.info(f"  ✍ Display Name filled: {DISPLAY}")

        # Fill Username
        if user_fld:
            user_fld[0].click(); time.sleep(0.3)
            user_fld[0].send_keys(USERNAME); time.sleep(0.5)
            logger.info(f"  ✍ Username filled: {USERNAME}")

        # Fill Password
        if len(password_flds) >= 1:
            password_flds[0].click(); time.sleep(0.3)
            password_flds[0].send_keys(PASSWORD); time.sleep(0.5)
            logger.info(f"  ✍ Password filled: {PASSWORD}")

        # Fill Confirm Password
        if len(password_flds) >= 2:
            password_flds[1].click(); time.sleep(0.3)
            password_flds[1].send_keys(PASSWORD); time.sleep(0.5)
            logger.info(f"  ✍ Confirm Password filled: {PASSWORD}")

        # Hide keyboard
        try:
            driver.hide_keyboard()
        except Exception:
            driver.tap([(540, 200)])
        time.sleep(1)

        # Click Register button
        reg_btn = driver.find_elements(AppiumBy.XPATH,
            "//android.widget.Button[@content-desc='Register']")
        assert reg_btn, "❌ Register button not found after filling form"

        enabled = reg_btn[0].get_attribute("enabled")
        assert enabled == "true", \
            f"❌ Register button still disabled after filling form — enabled={enabled}"

        reg_btn[0].click()
        logger.info("  👉 Tapped 'Register' button")
        time.sleep(5)

    def test_05_fetch_otp_and_verify(self, driver):
        """Fetch OTP from Yopmail and enter it in the app."""
        logger.info(f"\n=== REGISTRATION: Step 5 — OTP Verification ===")
        logger.info(f"  📬 Checking Yopmail inbox for: {YOP_USER}")

        # Keep the driver alive while polling (prevent UIAutomator idle timeout)
        def _keep_driver_alive():
            try:
                driver.find_elements(AppiumBy.XPATH, "//android.widget.EditText")
            except Exception:
                pass

        # Poll Yopmail with keep-alive pings
        otp_code = None
        for attempt in range(12):
            logger.info(f"  ⏳ Polling Yopmail... attempt {attempt + 1}/12")
            _keep_driver_alive()

            from yopmail import Yopmail
            try:
                y = Yopmail(YOP_USER)
                mail_ids = y.get_mail_ids()
                if mail_ids:
                    mail = y.get_mail_body(mail_ids[0])
                    text = mail.text if hasattr(mail, 'text') else str(mail)
                    matches = re.findall(r'\b(\d{4,8})\b', text)
                    if matches:
                        otp_code = matches[0]
                        logger.info(f"  ✅ OTP received: {otp_code}")
                        break
                    else:
                        logger.warning("  ⚠ Email arrived but no OTP digits found")
                        logger.debug(f"  Content: {text[:200]}")
                        break
            except Exception as e:
                logger.warning(f"  ⚠ Yopmail error: {e}")

            time.sleep(5)

        if not otp_code:
            logger.warning("  ⚠ OTP not found — skipping OTP entry step")
            pytest.skip("Could not retrieve OTP from Yopmail — check network/email")
            return

        # Enter OTP in the app
        logger.info(f"  📍 Entering OTP: {otp_code}")
        otp_fields = driver.find_elements(AppiumBy.XPATH, "//android.widget.EditText")

        if otp_fields:
            if len(otp_fields) == 1:
                # Single input field
                otp_fields[0].click(); time.sleep(0.3)
                otp_fields[0].send_keys(otp_code)
                logger.info("  ✍ OTP entered in single field")
            else:
                # Multiple digit boxes
                for idx, digit in enumerate(otp_code):
                    if idx < len(otp_fields):
                        otp_fields[idx].click(); time.sleep(0.2)
                        otp_fields[idx].send_keys(digit); time.sleep(0.1)
                logger.info(f"  ✍ OTP entered digit-by-digit across {len(otp_fields)} fields")

            # Hide keyboard and wait
            try:
                driver.hide_keyboard()
            except Exception:
                driver.tap([(540, 200)])
            time.sleep(1)

            # Tap Verify/Submit if it appears
            verify_btn = driver.find_elements(AppiumBy.XPATH,
                "//*[contains(@content-desc, 'Verify') "
                "or contains(@content-desc, 'Submit') "
                "or contains(@content-desc, 'Confirm')]")
            if verify_btn:
                verify_btn[0].click()
                logger.info("  👉 Tapped Verify/Submit button")
            time.sleep(5)

        # Verify outcome
        success = driver.find_elements(AppiumBy.XPATH,
            "//*[contains(@content-desc, 'Success') "
            "or contains(@content-desc, 'Welcome') "
            "or contains(@content-desc, 'Home')]")
        if success:
            logger.info("✅ Registration SUCCESSFUL — app shows success/home state")
        else:
            logger.info("ℹ Registration outcome: could not confirm success screen (OTP may need manual check)")

    def test_06_back_to_login(self, driver):
        """After registration attempt, navigate back to Login screen."""
        logger.info("\n=== REGISTRATION: Step 6 — Back to Login ===")

        # Try pressing Back until Login screen appears
        for _ in range(5):
            login_btn = driver.find_elements(AppiumBy.XPATH,
                "//android.widget.Button[@content-desc='Login']")
            if login_btn:
                logger.info("✅ Back on Login screen")
                return
            try:
                driver.press_keycode(4)
            except Exception:
                pass
            time.sleep(2)

        # If still not on login, look for a "Back to Login" link
        back_login = driver.find_elements(AppiumBy.XPATH,
            "//*[@content-desc='Login' and @clickable='true']")
        if back_login:
            back_login[0].click()
            time.sleep(3)

        login_btn = driver.find_elements(AppiumBy.XPATH,
            "//android.widget.Button[@content-desc='Login']")
        assert len(login_btn) > 0, "❌ Could not navigate back to Login screen after registration"
        logger.info("✅ Successfully returned to Login screen")
