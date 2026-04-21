"""
Test 13 — Forgot Password Flow (Real Device)
=============================================
Full positive forgot password flow using the SAME email
registered in test_12:

  1. Read email + token from shared_email.json (saved by test_12)
  2. From Login screen → tap "Forgot Password?"
  3. Input the registered email → Send OTP
  4. Poll mail.tm inbox for OTP email
  5. Extract OTP digits → enter in app
  6. Set new password → verify back to login

Dependencies:
  pip install requests
"""

import pytest
import time
import re
import json
import os
import logging
import requests as http_requests
from appium.webdriver.common.appiumby import AppiumBy

logger = logging.getLogger(__name__)

pytestmark = [pytest.mark.login, pytest.mark.regression]


# ═══════════════════════════════════════════════════════════════
# Shared state from test_12
# ═══════════════════════════════════════════════════════════════

MAILTM_BASE = "https://api.mail.tm"
SHARED_FILE = os.path.join(os.path.dirname(__file__), "..", "reports", "shared_email.json")
NEW_PASSWORD = "NewSandi123!"

# Module-level storage
_stored = {
    "email": None,
    "token": None,
    "password": None,
    "mailtm_pass": None,
}


def _load_shared_email():
    """Load email + token from shared_email.json (saved by test_12)."""
    if os.path.exists(SHARED_FILE):
        with open(SHARED_FILE, "r") as f:
            data = json.load(f)
        _stored["email"] = data.get("email")
        _stored["token"] = data.get("token")
        _stored["password"] = data.get("password")
        _stored["mailtm_pass"] = data.get("mailtm_pass")
        logger.info(f"  📧 Loaded email from test_12: {_stored['email']}")
        return True
    else:
        logger.error(f"  ❌ shared_email.json not found — run test_12 first!")
        return False


def _refresh_mailtm_token():
    """Re-login to mail.tm to get a fresh token (old one may have expired)."""
    email = _stored["email"]
    mailtm_pass = _stored["mailtm_pass"]
    if not email or not mailtm_pass:
        return False
    try:
        r = http_requests.post(f"{MAILTM_BASE}/token", json={
            "address": email,
            "password": mailtm_pass
        }, timeout=15)
        if r.status_code == 200:
            _stored["token"] = r.json()["token"]
            logger.info("  🔑 Refreshed mail.tm JWT token")
            return True
        else:
            logger.error(f"  ❌ Token refresh failed: {r.status_code}")
            return False
    except Exception as e:
        logger.error(f"  ❌ Token refresh error: {e}")
        return False


def _poll_otp_from_mailtm(token, max_retries=20, wait_sec=5):
    """
    Poll mail.tm inbox until a NEW email arrives, then extract OTP digits.
    Returns OTP string, or None if not found.
    """
    headers = {"Authorization": f"Bearer {token}"}

    for attempt in range(max_retries):
        logger.info(f"  📬 Polling inbox... ({attempt + 1}/{max_retries})")
        try:
            r = http_requests.get(f"{MAILTM_BASE}/messages", headers=headers, timeout=15)
            if r.status_code == 200:
                messages = r.json().get("hydra:member", [])
                if messages:
                    msg_id = messages[0]["id"]
                    logger.info(f"  ✉️ Email arrived! Subject: {messages[0].get('subject', 'N/A')}")

                    # Read full message
                    r2 = http_requests.get(f"{MAILTM_BASE}/messages/{msg_id}", headers=headers, timeout=15)
                    if r2.status_code == 200:
                        body = r2.json()
                        text = body.get("text", "") or body.get("html", [""])[0] if isinstance(body.get("html"), list) else body.get("html", "")
                        if not text:
                            text = str(body)

                        logger.info(f"  📄 Email body snippet: {text[:200]}")

                        # Extract OTP: 4–6 digit number
                        otp_matches = re.findall(r'\b(\d{4,6})\b', text)
                        if otp_matches:
                            otp = otp_matches[0]
                            logger.info(f"  ✅ OTP extracted: {otp}")
                            return otp
                        else:
                            logger.warning("  ⚠ Email body has no 4-6 digit OTP pattern")
                            return None
        except Exception as e:
            logger.warning(f"  ⚠ Poll error: {e}")

        time.sleep(wait_sec)

    logger.error(f"  ❌ No email after {max_retries} retries")
    return None


def _clear_inbox(token):
    """Delete all existing messages so we only see the forgot password OTP."""
    headers = {"Authorization": f"Bearer {token}"}
    try:
        r = http_requests.get(f"{MAILTM_BASE}/messages", headers=headers, timeout=10)
        if r.status_code == 200:
            for msg in r.json().get("hydra:member", []):
                http_requests.delete(f"{MAILTM_BASE}/messages/{msg['id']}",
                                   headers=headers, timeout=10)
            logger.info("  🗑 Cleared old messages from inbox")
    except Exception as e:
        logger.warning(f"  ⚠ Could not clear inbox: {e}")


# ═══════════════════════════════════════════════════════════════
# Tests
# ═══════════════════════════════════════════════════════════════

class TestForgotPassword:

    def test_01_load_email_from_test_12(self, driver):
        """Load the email registered in test_12 from shared file."""
        logger.info("\n=== FORGOT PASSWORD: Load Email from test_12 ===")
        assert _load_shared_email(), "shared_email.json not found — run test_12 first"
        assert _stored["email"], "Email is empty in shared file"
        logger.info(f"  ✅ Using email: {_stored['email']}")

        # Refresh token in case old one expired
        _refresh_mailtm_token()

        # Clear old inbox messages so we only get the forgot password OTP
        if _stored["token"]:
            _clear_inbox(_stored["token"])

    def test_02_navigate_to_forgot_password(self, driver):
        """From Login screen, tap 'Forgot Password?' link."""
        logger.info("\n=== FORGOT PASSWORD: Navigate ===")

        forgot_link = driver.find_elements(AppiumBy.XPATH,
            "//*[@content-desc='Forgot Password?']")
        assert forgot_link, "Forgot Password link not found on login screen"
        forgot_link[-1].click()
        time.sleep(3)

        # Verify on forgot password screen
        send_otp = driver.find_elements(AppiumBy.XPATH,
            "//*[@content-desc='Send otp']")
        email_field = driver.find_elements(AppiumBy.XPATH, "//android.widget.EditText")
        assert send_otp or email_field, "Not on Forgot Password screen"
        logger.info("  ✅ On Forgot Password screen")

    def test_03_input_email_and_send_otp(self, driver):
        """Input the registered email and tap Send OTP."""
        logger.info("\n=== FORGOT PASSWORD: Input Email & Send OTP ===")

        email = _stored["email"]
        assert email, "No email loaded"

        # Input email
        email_field = driver.find_elements(AppiumBy.XPATH, "//android.widget.EditText")
        assert email_field, "Email input field not found"
        email_field[0].click()
        time.sleep(0.3)
        email_field[0].send_keys(email)
        time.sleep(0.5)

        try:
            driver.hide_keyboard()
        except Exception:
            pass
        time.sleep(1)

        # Tap Send OTP
        send_btn = driver.find_elements(AppiumBy.XPATH,
            "//*[@content-desc='Send otp']")
        assert send_btn, "Send OTP button not found"
        send_btn[-1].click()
        time.sleep(3)
        logger.info(f"  ✅ Sent forgot password OTP to {email}")

    def test_04_fetch_otp_and_enter(self, driver):
        """Poll mail.tm for forgot password OTP and enter it in the app."""
        logger.info("\n=== FORGOT PASSWORD: Fetch & Enter OTP ===")

        token = _stored["token"]
        assert token, "No JWT token — cannot poll mail.tm"

        # Poll for OTP email (keep driver alive)
        otp = None
        for i in range(20):
            otp = _poll_otp_from_mailtm(token, max_retries=1, wait_sec=0)
            if otp:
                break
            # Keep Appium session alive
            try:
                driver.find_elements(AppiumBy.XPATH, "//android.widget.EditText")
            except Exception:
                pass
            time.sleep(5)

        assert otp, "Failed to get forgot password OTP from mail.tm"

        # Enter OTP digits
        otp_fields = driver.find_elements(AppiumBy.XPATH, "//android.widget.EditText")
        if otp_fields:
            for idx, digit in enumerate(otp):
                if idx < len(otp_fields):
                    otp_fields[idx].click()
                    time.sleep(0.2)
                    otp_fields[idx].send_keys(digit)
                    time.sleep(0.1)
            logger.info(f"  ✅ OTP {otp} entered")
        time.sleep(3)

    def test_05_reset_password(self, driver):
        """Enter new password on the reset form."""
        logger.info("\n=== FORGOT PASSWORD: Reset Password ===")

        # Look for password fields (new password + confirm)
        password_fields = driver.find_elements(AppiumBy.XPATH, "//android.widget.EditText")

        if len(password_fields) >= 2:
            # New password
            password_fields[0].click()
            time.sleep(0.3)
            password_fields[0].send_keys(NEW_PASSWORD)
            time.sleep(0.5)

            # Confirm password
            password_fields[1].click()
            time.sleep(0.3)
            password_fields[1].send_keys(NEW_PASSWORD)
            time.sleep(0.5)

            try:
                driver.hide_keyboard()
            except Exception:
                pass
            time.sleep(1)

            # Submit
            submit_btn = driver.find_elements(AppiumBy.XPATH,
                "//android.widget.Button[@clickable='true']")
            for btn in submit_btn:
                desc = btn.get_attribute("content-desc") or ""
                if any(word in desc.lower() for word in ["reset", "confirm", "submit", "save", "change"]):
                    btn.click()
                    time.sleep(3)
                    logger.info("  ✅ Password reset submitted")
                    break
            else:
                if submit_btn:
                    submit_btn[-1].click()
                    time.sleep(3)
                    logger.info("  ✅ Password reset submitted (fallback)")
        elif len(password_fields) == 1:
            logger.info("  ℹ Only 1 field — may be a single password entry")
            password_fields[0].click()
            time.sleep(0.3)
            password_fields[0].send_keys(NEW_PASSWORD)
            time.sleep(1)
        else:
            logger.info("  ℹ No password fields — app may auto-redirect after OTP")

    def test_06_verify_back_to_login(self, driver):
        """Verify we end up on login screen after password reset."""
        logger.info("\n=== FORGOT PASSWORD: Verify Login Screen ===")

        for _ in range(5):
            login_btn = driver.find_elements(AppiumBy.XPATH,
                "//*[@content-desc='Login']")
            welcome_back = driver.find_elements(AppiumBy.XPATH,
                "//*[contains(@content-desc, 'Welcome Back')]")
            edit_fields = driver.find_elements(AppiumBy.XPATH,
                "//android.widget.EditText")

            if login_btn or welcome_back or len(edit_fields) >= 2:
                logger.info("  ✅ On login screen — Forgot Password flow complete!")
                break
            try:
                driver.press_keycode(4)
            except Exception:
                pass
            time.sleep(2)

        login_indicators = driver.find_elements(AppiumBy.XPATH,
            "//*[@content-desc='Login'] | //*[contains(@content-desc, 'Welcome Back')]")
        assert login_indicators, "Not back on login screen after password reset"
        logger.info("  ✅ FORGOT PASSWORD FLOW COMPLETE!")
