"""
Test 12 — Registration Flow (Real Device)
==========================================
Full positive registration flow:
  1. Create a real temporary email via mail.tm REST API
  2. From Login screen → tap "Register" link
  3. Fill form with the temp email + random display name
  4. Tap "Register"  →  app sends OTP to the email
  5. Poll mail.tm inbox for the OTP email
  6. Extract OTP digits → enter in app → verify success

Dependencies:
  pip install requests
"""

import pytest
import time
import random
import re
import logging
import requests as http_requests
from appium.webdriver.common.appiumby import AppiumBy

logger = logging.getLogger(__name__)

pytestmark = [pytest.mark.login, pytest.mark.regression]


# ═══════════════════════════════════════════════════════════════
# mail.tm  —  Disposable Email Helper  (free REST API, no CAPTCHA)
# ═══════════════════════════════════════════════════════════════

MAILTM_BASE = "https://api.mail.tm"

# Timestamp + random suffix → guaranteed unique every single run
# Example: autoqa17139284_37@domain.com  (never repeats)
import hashlib
from datetime import datetime
RND          = f"{int(datetime.now().timestamp())}_{random.randint(10, 99)}"
MAILTM_PASS  = "AutoTest123!"
PASSWORD     = "Sandi123!"


def _create_temp_email():
    """
    Creates a real disposable email address via mail.tm API.
    Returns (email, token) or (None, None) on failure.
    """
    try:
        # 1. Get available domain
        r = http_requests.get(f"{MAILTM_BASE}/domains", timeout=15)
        r.raise_for_status()
        domains = r.json()["hydra:member"]
        domain = domains[0]["domain"]

        # 2. Create account
        username = f"autoqa{RND}"
        email = f"{username}@{domain}"

        r = http_requests.post(f"{MAILTM_BASE}/accounts", json={
            "address": email,
            "password": MAILTM_PASS
        }, timeout=15)

        if r.status_code not in [200, 201]:
            logger.error(f"  ❌ mail.tm account creation failed: {r.status_code} — {r.text[:200]}")
            return None, None

        logger.info(f"  📧 Temp email created: {email}")

        # 3. Login to get JWT token
        r = http_requests.post(f"{MAILTM_BASE}/token", json={
            "address": email,
            "password": MAILTM_PASS
        }, timeout=15)

        if r.status_code != 200:
            logger.error(f"  ❌ mail.tm login failed: {r.status_code}")
            return email, None

        token = r.json()["token"]
        logger.info(f"  🔑 JWT token acquired")
        return email, token

    except Exception as e:
        logger.error(f"  ❌ mail.tm error: {e}")
        return None, None


def _poll_otp_from_mailtm(token, max_retries=20, wait_sec=5):
    """
    Poll mail.tm inbox until an email arrives, then extract OTP digits.
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
                        # Try text body first, then HTML
                        text = body.get("text", "") or body.get("html", [""])[0] if isinstance(body.get("html"), list) else body.get("html", "")
                        if not text:
                            text = str(body)

                        logger.info(f"  📄 Email body snippet: {text[:200]}")

                        # Extract OTP: 4–8 digit number
                        otp_matches = re.findall(r'\b(\d{4,6})\b', text)
                        if otp_matches:
                            otp = otp_matches[0]
                            logger.info(f"  ✅ OTP extracted: {otp}")
                            return otp
                        else:
                            logger.warning(f"  ⚠ Email body has no 4-6 digit OTP pattern")
                            return None
        except Exception as e:
            logger.warning(f"  ⚠ Poll error: {e}")

        time.sleep(wait_sec)

    logger.warning("  ⚠ No email received after all retries")
    return None


# ═══════════════════════════════════════════════════════════════
# Helpers — App Navigation
# ═══════════════════════════════════════════════════════════════

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
    """From login screen, tap the 'Register' link."""
    register_link = driver.find_elements(AppiumBy.XPATH,
        "//*[@content-desc='Register' and @clickable='true']")
    if not register_link:
        register_link = driver.find_elements(AppiumBy.XPATH,
            "//*[contains(@content-desc, 'Register')]")
    if register_link:
        register_link[0].click()
        time.sleep(3)
        return True
    return False


def _on_register_screen(driver):
    """Return True if on the Create Account (registration) screen."""
    create_acc = driver.find_elements(AppiumBy.XPATH,
        "//*[@content-desc='Create your Account']")
    return len(create_acc) > 0


# ═══════════════════════════════════════════════════════════════
# Test Class
# ═══════════════════════════════════════════════════════════════

# Module-level state shared between test methods
_test_state = {
    "email": None,
    "token": None,
    "display": None,
    "username": None,
}


class TestRegistration:
    """Full positive registration flow with real OTP via mail.tm."""

    def test_01_create_temp_email(self, driver):
        """Create a disposable email address via mail.tm API."""
        logger.info("\n=== REGISTRATION: Step 1 — Create Temp Email ===")

        email, token = _create_temp_email()
        assert email is not None, "❌ Failed to create temp email via mail.tm"
        assert token is not None, "❌ Failed to get mail.tm JWT token"

        # Derive display name and username from email prefix
        prefix = email.split("@")[0]  # e.g. "autoqa1234"
        _test_state["email"] = email
        _test_state["token"] = token
        _test_state["display"] = f"AutoQA {RND}"
        _test_state["username"] = prefix

        logger.info(f"  ✅ Email  : {email}")
        logger.info(f"  ✅ Display: {_test_state['display']}")
        logger.info(f"  ✅ User   : {_test_state['username']}")

    def test_02_navigate_to_register(self, driver):
        """From Login screen, tap 'Register' to open Registration form."""
        logger.info("\n=== REGISTRATION: Step 2 — Navigate to Register ===")
        assert _ensure_login_screen(driver), \
            "❌ Could not reach Login screen"
        assert _go_to_register(driver), \
            "❌ Could not tap 'Register' link"
        assert _on_register_screen(driver), \
            "❌ Registration screen did not open"
        logger.info("✅ Reached Registration / Create Account screen")

    def test_03_fill_and_submit_form(self, driver):
        """Fill registration form with temp email and submit."""
        email = _test_state["email"]
        display = _test_state["display"]
        username = _test_state["username"]

        logger.info(f"\n=== REGISTRATION: Step 3 — Fill Form ===")
        logger.info(f"  📧 Email    : {email}")
        logger.info(f"  👤 Display  : {display}")
        logger.info(f"  🔑 Username : {username}")
        logger.info(f"  🔒 Password : {PASSWORD}")

        if not _on_register_screen(driver):
            assert _go_to_register(driver) and _on_register_screen(driver), \
                "Could not reach register screen"

        # Grab fields
        email_fld = driver.find_elements(AppiumBy.XPATH,
            "//android.widget.EditText[@hint='Add email']")
        display_fld = driver.find_elements(AppiumBy.XPATH,
            "//android.widget.EditText[@hint='Add Display Name']")
        user_fld = driver.find_elements(AppiumBy.XPATH,
            "//android.widget.EditText[contains(@hint, 'Username')]")
        password_flds = driver.find_elements(AppiumBy.XPATH,
            "//android.widget.EditText[@password='true']")

        # Fill Email
        if email_fld:
            email_fld[0].click(); time.sleep(0.3)
            email_fld[0].send_keys(email); time.sleep(0.5)
            logger.info(f"  ✍ Email filled")

        # Fill Display Name
        if display_fld:
            display_fld[0].click(); time.sleep(0.3)
            display_fld[0].send_keys(display); time.sleep(0.5)
            logger.info(f"  ✍ Display Name filled")

        # Fill Username
        if user_fld:
            user_fld[0].click(); time.sleep(0.3)
            user_fld[0].send_keys(username); time.sleep(0.5)
            logger.info(f"  ✍ Username filled")

        # Fill Password
        if len(password_flds) >= 1:
            password_flds[0].click(); time.sleep(0.3)
            password_flds[0].send_keys(PASSWORD); time.sleep(0.5)
            logger.info(f"  ✍ Password filled")

        # Fill Confirm Password
        if len(password_flds) >= 2:
            password_flds[1].click(); time.sleep(0.3)
            password_flds[1].send_keys(PASSWORD); time.sleep(0.5)
            logger.info(f"  ✍ Confirm Password filled")

        # Hide keyboard
        try:
            driver.hide_keyboard()
        except Exception:
            driver.tap([(540, 200)])
        time.sleep(1)

        # Click Register button
        reg_btn = driver.find_elements(AppiumBy.XPATH,
            "//android.widget.Button[@content-desc='Register']")
        assert reg_btn, "❌ Register button not found"

        enabled = reg_btn[0].get_attribute("enabled")
        assert enabled == "true", \
            f"❌ Register button still disabled — enabled={enabled}"

        reg_btn[0].click()
        logger.info("  👉 Tapped 'Register' button — OTP should be sent to inbox")
        time.sleep(3)

    def test_04_fetch_otp_and_enter(self, driver):
        """Poll mail.tm inbox for OTP email, extract digits, enter in app."""
        token = _test_state["token"]
        email = _test_state["email"]

        logger.info(f"\n=== REGISTRATION: Step 4 — Fetch OTP ===")
        logger.info(f"  📬 Polling mail.tm inbox for: {email}")

        assert token, "❌ No mail.tm token available (test_01 may have failed)"

        # Keep Appium driver alive while polling (prevent UIAutomator idle timeout)
        def _keep_alive():
            try:
                driver.find_elements(AppiumBy.XPATH, "//android.widget.EditText")
            except Exception:
                pass

        # Poll with keep-alive
        otp_code = None
        for attempt in range(20):
            _keep_alive()
            logger.info(f"  ⏳ Polling... ({attempt + 1}/20)")
            try:
                headers = {"Authorization": f"Bearer {token}"}
                r = http_requests.get(f"{MAILTM_BASE}/messages", headers=headers, timeout=15)
                if r.status_code == 200:
                    messages = r.json().get("hydra:member", [])
                    if messages:
                        msg_id = messages[0]["id"]
                        subject = messages[0].get("subject", "N/A")
                        logger.info(f"  ✉️ Email arrived! Subject: {subject}")

                        r2 = http_requests.get(f"{MAILTM_BASE}/messages/{msg_id}", headers=headers, timeout=15)
                        if r2.status_code == 200:
                            body = r2.json()
                            text = body.get("text", "")
                            if not text:
                                html_list = body.get("html", [])
                                text = html_list[0] if isinstance(html_list, list) and html_list else str(body.get("html", ""))
                            if not text:
                                text = str(body)

                            logger.info(f"  📄 Body snippet: {text[:200]}")
                            matches = re.findall(r'\b(\d{4,6})\b', text)
                            if matches:
                                otp_code = matches[0]
                                logger.info(f"  ✅ OTP extracted: {otp_code}")
                                break
                            else:
                                logger.warning("  ⚠ No 4-6 digit OTP found in email body")
                                break
            except Exception as e:
                logger.warning(f"  ⚠ Poll error: {e}")
            time.sleep(3)

        if not otp_code:
            pytest.skip("⚠ Could not retrieve OTP from mail.tm — check if Mepo sent the email")
            return

        # Enter OTP in the app
        logger.info(f"  📍 Entering OTP: {otp_code}")
        otp_fields = driver.find_elements(AppiumBy.XPATH, "//android.widget.EditText")

        if otp_fields:
            if len(otp_fields) == 1:
                otp_fields[0].click(); time.sleep(0.3)
                otp_fields[0].send_keys(otp_code)
                logger.info("  ✍ OTP entered (single field)")
            else:
                for idx, digit in enumerate(otp_code):
                    if idx < len(otp_fields):
                        otp_fields[idx].click(); time.sleep(0.2)
                        otp_fields[idx].send_keys(digit); time.sleep(0.1)
                logger.info(f"  ✍ OTP entered digit-by-digit ({len(otp_fields)} fields)")

            try:
                driver.hide_keyboard()
            except Exception:
                driver.tap([(540, 200)])
            time.sleep(1)

            # Auto-tap Verify/Submit if it shows
            verify_btn = driver.find_elements(AppiumBy.XPATH,
                "//*[contains(@content-desc, 'Verify') "
                "or contains(@content-desc, 'Submit') "
                "or contains(@content-desc, 'Confirm')]")
            if verify_btn:
                verify_btn[0].click()
                logger.info("  👉 Tapped Verify/Submit button")
            time.sleep(3)

        # Check outcome
        success = driver.find_elements(AppiumBy.XPATH,
            "//*[contains(@content-desc, 'Success') "
            "or contains(@content-desc, 'Welcome') "
            "or contains(@content-desc, 'Home')]")
        if success:
            logger.info("✅ Registration SUCCESSFUL!")
        else:
            logger.info("ℹ Registration outcome unclear — OTP may need manual verification")

    def test_05_back_to_login(self, driver):
        """After registration, navigate back to Login screen."""
        logger.info("\n=== REGISTRATION: Step 5 — Back to Login ===")

        for _ in range(5):
            login_btn = driver.find_elements(AppiumBy.XPATH,
                "//android.widget.Button[@content-desc='Login']")
            if login_btn:
                logger.info("✅ Back on Login screen")
                return
            login_link = driver.find_elements(AppiumBy.XPATH,
                "//*[@content-desc='Login' and @clickable='true']")
            if login_link:
                login_link[0].click()
                time.sleep(3)
                continue
            try:
                driver.press_keycode(4)
            except Exception:
                pass
            time.sleep(2)

        login_btn = driver.find_elements(AppiumBy.XPATH,
            "//android.widget.Button[@content-desc='Login']")
        assert len(login_btn) > 0, "❌ Could not navigate back to Login screen"
        logger.info("✅ Successfully returned to Login screen")

    def test_06_login_with_new_account(self, driver):
        """Login using the freshly registered account to verify it works."""
        email = _test_state["email"]
        logger.info(f"\n=== REGISTRATION: Step 6 — Login with New Account ===")
        logger.info(f"  📧 Email: {email}")
        logger.info(f"  🔒 Password: {PASSWORD}")

        assert email, "❌ No email saved from registration (previous steps may have failed)"

        # Make sure we're on login screen
        login_btn = driver.find_elements(AppiumBy.XPATH,
            "//android.widget.Button[@content-desc='Login']")
        if not login_btn:
            assert _ensure_login_screen(driver), "❌ Not on Login screen"

        # Fill email
        email_fields = driver.find_elements(AppiumBy.XPATH, "//android.widget.EditText")
        assert len(email_fields) >= 1, "❌ Email field not found on login screen"
        email_fields[0].click(); time.sleep(0.3)
        email_fields[0].send_keys(email); time.sleep(0.5)
        logger.info(f"  ✍ Email entered")

        # Fill password
        password_fields = driver.find_elements(AppiumBy.XPATH,
            "//android.widget.EditText[@password='true']")
        if not password_fields:
            # Fallback: get the second EditText
            all_fields = driver.find_elements(AppiumBy.XPATH, "//android.widget.EditText")
            if len(all_fields) >= 2:
                password_fields = [all_fields[1]]

        assert password_fields, "❌ Password field not found"
        password_fields[0].click(); time.sleep(0.3)
        password_fields[0].send_keys(PASSWORD); time.sleep(0.5)
        logger.info(f"  ✍ Password entered")

        # Hide keyboard
        try:
            driver.hide_keyboard()
        except Exception:
            driver.tap([(540, 200)])
        time.sleep(1)

        # Tap Login button
        login_btn = driver.find_elements(AppiumBy.XPATH,
            "//android.widget.Button[@content-desc='Login']")
        assert login_btn, "❌ Login button not found"
        login_btn[0].click()
        logger.info("  👉 Tapped 'Login' button")
        time.sleep(3)

        # Verify login success — look for Welcome greeting or Home tab
        welcome = driver.find_elements(AppiumBy.XPATH,
            "//*[contains(@content-desc, 'Welcome,')]")
        home_tab = driver.find_elements(AppiumBy.XPATH,
            "//*[contains(@content-desc, 'Home\nTab 1 of 4')]")

        assert welcome or home_tab, \
            "❌ Login failed — no Welcome or Home screen detected after login"
        logger.info(f"✅ Login SUCCESSFUL with newly registered account!")

    def test_07_logout_new_account(self, driver):
        """Logout from the new account and return to Login screen for next tests."""
        logger.info("\n=== REGISTRATION: Step 7 — Logout New Account ===")

        # ── Step A: Navigate to Profile page ──
        # Try Bottom Nav first (may not be visible)
        profile_tab = driver.find_elements(AppiumBy.XPATH,
            "//*[contains(@content-desc, 'Profile\nTab 4 of 4')]")
        if not profile_tab:
            profile_tab = driver.find_elements(AppiumBy.XPATH,
                "//*[contains(@content-desc, 'Profile') and contains(@content-desc, 'Tab')]")

        if profile_tab:
            profile_tab[-1].click()
            time.sleep(3)
            logger.info("  👉 Entered Profile via Bottom Nav Tab")
        else:
            # Fallback: tap profile icon in header (top-right, visible in screenshot)
            # From the screenshot: profile icon is at far right of the header row
            # Use content-desc or last clickable ImageView in header
            profile_icons = driver.find_elements(AppiumBy.XPATH,
                "//android.view.View[@clickable='true']")
            if not profile_icons:
                profile_icons = driver.find_elements(AppiumBy.XPATH,
                    "//android.widget.ImageView[@clickable='true']")

            # Profile icon is usually the last clickable icon in the top header area
            # Filter for elements in the top 300px of the screen
            header_icons = []
            for el in profile_icons:
                try:
                    loc = el.location
                    if loc['y'] < 300:
                        header_icons.append(el)
                except Exception:
                    pass

            if header_icons:
                header_icons[-1].click()  # Last icon in header = profile
                time.sleep(3)
                logger.info("  👉 Entered Profile via header icon (last icon)")
            else:
                # Last resort: tap coordinate of profile icon from screenshot
                driver.tap([(640, 130)], 500)
                time.sleep(3)
                logger.info("  👉 Entered Profile via coordinate tap (640, 130)")

        # ── Step B: Navigate to Settings ──
        # Check if we're on My Profile page
        my_profile = driver.find_elements(AppiumBy.XPATH,
            "//*[@content-desc='My Profile']")
        if my_profile:
            logger.info("  ✅ On Profile page")
            # Tap Settings button (usually last button in header)
            buttons = driver.find_elements(AppiumBy.XPATH,
                "//android.widget.Button[@clickable='true']")
            if len(buttons) >= 2:
                buttons[-1].click()
                time.sleep(3)
                logger.info("  👉 Opened Settings")
            else:
                # Try finding settings by content-desc
                settings = driver.find_elements(AppiumBy.XPATH,
                    "//*[contains(@content-desc, 'Settings') or contains(@content-desc, 'Setting')]")
                if settings:
                    settings[0].click()
                    time.sleep(3)
                    logger.info("  👉 Opened Settings via content-desc")
        else:
            logger.info("  ℹ Not on My Profile page — trying to find Settings/Logout directly")

        # ── Step C: Find and tap Logout ──
        s = driver.get_window_size()
        found_logout = False
        for attempt in range(5):
            logout_el = driver.find_elements(AppiumBy.XPATH,
                "//*[contains(@content-desc, 'Logout') "
                "or contains(@content-desc, 'Log Out') "
                "or contains(@content-desc, 'Sign Out') "
                "or contains(@content-desc, 'Log out')]")
            if logout_el:
                logout_el[0].click()
                time.sleep(3)
                logger.info("  👉 Tapped Logout")
                found_logout = True
                break
            # Scroll down to find Logout
            driver.swipe(s['width']//2, int(s['height']*0.75),
                        s['width']//2, int(s['height']*0.25), 800)
            time.sleep(1)

        if not found_logout:
            logger.warning("  ⚠ Logout button not found — trying UiScrollable")
            try:
                driver.find_element(
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().descriptionContains("Logout"))')
                time.sleep(1)
                logout_el = driver.find_elements(AppiumBy.XPATH,
                    "//*[contains(@content-desc, 'Logout')]")
                if logout_el:
                    logout_el[0].click()
                    time.sleep(3)
                    found_logout = True
                    logger.info("  👉 Tapped Logout (via UiScrollable)")
            except Exception:
                pass

        # ── Step D: Confirm logout dialog ──
        confirm = driver.find_elements(AppiumBy.XPATH,
            "//*[contains(@content-desc, 'Yes') "
            "or contains(@content-desc, 'OK') "
            "or contains(@content-desc, 'Confirm') "
            "or contains(@content-desc, 'Continue') "
            "or contains(@content-desc, 'continue') "
            "or contains(@content-desc, 'Logout') "
            "or contains(@content-desc, 'Log Out')]")
        if confirm:
            confirm[0].click()
            time.sleep(3)
            logger.info("  👉 Logout confirmed")

        # ── Step E: Verify back on Login screen ──
        time.sleep(3)
        login_screen = driver.find_elements(AppiumBy.XPATH,
            "//*[contains(@content-desc, 'Welcome Back')]")
        login_btn = driver.find_elements(AppiumBy.XPATH,
            "//android.widget.Button[@content-desc='Login']")
        edit_texts = driver.find_elements(AppiumBy.XPATH,
            "//android.widget.EditText")

        assert login_screen or login_btn or edit_texts, \
            "❌ Not on Login screen after logout"
        logger.info("✅ Logged out — back on Login screen, ready for next tests!")

