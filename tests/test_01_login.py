"""
Test 01 — Login Flow (Real Device)
====================================
Tests login with positive and negative scenarios on Xiaomi real device.
Locators mapped from actual XML dump of the app.

Flow: Negative tests first (fields cleared between each) → Positive login last.
"""

import pytest
import time
import logging
from appium.webdriver.common.appiumby import AppiumBy

logger = logging.getLogger(__name__)

pytestmark = [pytest.mark.login, pytest.mark.regression]

VALID_EMAIL = "danip1@yopmail.com"
VALID_PASSWORD = "Sandi123!"


def _wait_for_app_ready(driver, timeout=15):
    """Wait for app to be fully loaded — either login or home screen."""
    for _ in range(timeout):
        try:
            # Check login screen
            edits = driver.find_elements(AppiumBy.XPATH, "//android.widget.EditText")
            if len(edits) >= 2:
                return "login"

            # Check home screen (already logged in)
            welcome = driver.find_elements(AppiumBy.XPATH,
                "//*[contains(@content-desc, 'Welcome,')]")
            if welcome:
                return "home"

            # Check Welcome Back header
            wb = driver.find_elements(AppiumBy.XPATH,
                "//*[contains(@content-desc, 'Welcome Back')]")
            if wb:
                return "login"
        except Exception:
            pass
        time.sleep(1)
    return "unknown"


def _navigate_to_login_screen(driver):
    """Ensure we're on the login screen. If logged in, logout first."""
    logger.info("  🔍 Checking current app state...")
    
    state = _wait_for_app_ready(driver, timeout=20)

    # If stuck in some random page, restart app to get back to a known state (home or login)
    if state not in ("login", "home"):
        logger.info("  🔄 App stuck in sub-page. Restarting app to reach a known state...")
        try:
            driver.terminate_app("com.mepo")
            time.sleep(2)
            driver.activate_app("com.mepo")
            time.sleep(10)
            state = _wait_for_app_ready(driver, timeout=15)
        except Exception as e:
            logger.error(f"  ❌ App restart failed: {e}")
            return False
            
    if state == "login":
        logger.info("  ✅ Already on login screen")
        return True
    
    if state == "home":
        logger.info("  🏠 On home screen — need to logout first")
        if _perform_logout(driver):
            return True
        
        # Fallback: force restart with app data clear via terminate + activate
        logger.info("  🔄 Logout UI failed — trying app restart fallback...")
        try:
            driver.terminate_app("com.mepo")
            time.sleep(3)
            driver.activate_app("com.mepo")
            time.sleep(10)
            state = _wait_for_app_ready(driver, timeout=15)
            if state == "login":
                logger.info("  ✅ App restart brought us to login screen")
                return True
        except Exception as e:
            logger.warning(f"  ⚠ App restart fallback failed: {e}")
    
    return False


def _perform_logout(driver):
    """Navigate Home → Profile → Settings → Logout. Returns True if reached login screen."""
    try:
        s = driver.get_window_size()
        
        # Scroll to top first
        for _ in range(3):
            driver.swipe(s['width']//2, int(s['height']*0.25),
                       s['width']//2, int(s['height']*0.75), 800)
            time.sleep(0.5)
        
        # --- Try to tap profile icon via content-desc locators first ---
        profile_opened = False
        profile_locators = [
            "//*[contains(@content-desc, 'Profile') and @clickable='true']",
            "//*[contains(@content-desc, 'profile') and @clickable='true']",
            "//*[contains(@content-desc, 'Profil') and @clickable='true']",
            "//android.view.View[contains(@content-desc, 'danip')]",
        ]
        for loc in profile_locators:
            els = driver.find_elements(AppiumBy.XPATH, loc)
            if els:
                els[0].click()
                time.sleep(3)
                # Verify we reached profile
                title = driver.find_elements(AppiumBy.XPATH, "//*[@content-desc='My Profile']")
                if title:
                    profile_opened = True
                    break
        
        # Fallback: tap top-right area (profile icon) using relative coordinates
        if not profile_opened:
            logger.info("  📍 Using coordinate-based profile tap fallback...")
            x_right = int(s['width'] * 0.9)
            y_top = int(s['height'] * 0.1)
            driver.tap([(x_right, y_top)], 500)
            time.sleep(3)
            title = driver.find_elements(AppiumBy.XPATH, "//*[@content-desc='My Profile']")
            profile_opened = len(title) > 0
        
        if not profile_opened:
            logger.warning("  ⚠ Could not open Profile page")
            return False
        
        logger.info("  📋 Profile opened — looking for Settings...")
        
        # Tap settings button (gear icon) — try content-desc first, then last button
        settings_opened = False
        settings_locators = [
            "//*[contains(@content-desc, 'Settings') or contains(@content-desc, 'Pengaturan')]",
            "//*[contains(@content-desc, 'setting')]",
        ]
        for loc in settings_locators:
            els = driver.find_elements(AppiumBy.XPATH, loc)
            if els:
                els[0].click()
                time.sleep(3)
                settings_opened = True
                break
        
        if not settings_opened:
            # Fallback: tap last clickable button in header area
            buttons = driver.find_elements(AppiumBy.XPATH,
                "//android.widget.Button[@clickable='true']")
            if len(buttons) >= 2:
                buttons[-1].click()
                time.sleep(3)
                settings_opened = True
        
        # Find and click logout
        for _ in range(5):
            logout = driver.find_elements(AppiumBy.XPATH,
                "//*[contains(@content-desc, 'Logout') "
                "or contains(@content-desc, 'Log out') "
                "or contains(@content-desc, 'Sign out')]")
            if logout:
                logout[0].click()
                time.sleep(2)
                # Confirm if dialog appears
                confirm = driver.find_elements(AppiumBy.XPATH,
                    "//*[contains(@content-desc, 'Yes') "
                    "or contains(@content-desc, 'OK') "
                    "or contains(@content-desc, 'Confirm')]")
                if confirm:
                    confirm[0].click()
                    time.sleep(5)
                else:
                    # Try tapping the Logout button itself if it acts as confirm
                    logout2 = driver.find_elements(AppiumBy.XPATH,
                        "//*[contains(@content-desc, 'Logout')]")
                    if logout2:
                        logout2[0].click()
                        time.sleep(5)
                break
            driver.swipe(s['width']//2, int(s['height']*0.75),
                       s['width']//2, int(s['height']*0.25), 800)
            time.sleep(1)
        
        # Wait for login screen
        time.sleep(5)
        state = _wait_for_app_ready(driver, timeout=20)
        if state == "login":
            logger.info("  ✅ Logged out → login screen ready")
            return True
            
    except Exception as e:
        logger.warning(f"  ⚠ Logout attempt failed: {e}")
    
    return False


def _clear_and_type(element, text):
    """Safely click a field and type text."""
    element.click()
    time.sleep(0.5)
    try:
        element.clear()
    except Exception:
        pass  # some frameworks don't play well with clear(), fallback to just send_keys
    time.sleep(0.5)
    if text != "":
        element.send_keys(text)
    else:
        # If text is empty, send empty string to force trigger change event
        element.send_keys("")
    time.sleep(0.5)


def _do_login(driver, email, password):
    """Perform login with given credentials."""
    edits = driver.find_elements(AppiumBy.XPATH, "//android.widget.EditText")
    if len(edits) < 2:
        logger.error("  ❌ Cannot find 2 EditText fields on login screen")
        return False

    # Clear and fill email
    _clear_and_type(edits[0], email)

    # Clear and fill password
    _clear_and_type(edits[1], password)

    # Safe keyboard hide
    driver.tap([(540, 200)])
    time.sleep(0.5)

    # Tap Login button
    for loc in [
        (AppiumBy.ACCESSIBILITY_ID, "Login"),
        (AppiumBy.XPATH, "//*[@content-desc='Login']"),
        (AppiumBy.XPATH, "//*[contains(@content-desc, 'Login')]"),
    ]:
        try:
            btn = driver.find_element(*loc)
            btn.click()
            logger.info("  🔓 Login button tapped")
            time.sleep(5)
            return True
        except Exception:
            continue

    logger.warning("  ⚠ Login button not found")
    return False


def _is_on_home(driver):
    """Check if we reached home screen."""
    welcome = driver.find_elements(AppiumBy.XPATH,
        "//*[contains(@content-desc, 'Welcome,')]")
    return len(welcome) > 0


def _is_on_login(driver):
    """Check if still on login screen."""
    for _ in range(5):
        edits = driver.find_elements(AppiumBy.XPATH, "//android.widget.EditText")
        if len(edits) >= 2:
            return True
        time.sleep(1)
    return False


def _reset_to_login(driver):
    """Reset app back to login screen for next negative test."""
    if _is_on_login(driver):
        return True

    # If somehow landed on home, restart
    try:
        driver.terminate_app("com.mepo")
        time.sleep(2)
        driver.activate_app("com.mepo")
        time.sleep(10)
        return _wait_for_app_ready(driver, timeout=10) == "login"
    except Exception:
        return False


class TestLoginNegative:
    """Negative login scenarios — app should reject invalid credentials."""

    def test_login_empty_email(self, driver):
        """Login with empty email should fail."""
        logger.info("\n=== NEGATIVE: Empty email ===")

        assert _navigate_to_login_screen(driver), "Cannot get to login screen"
        _do_login(driver, "", VALID_PASSWORD)
        assert not _is_on_home(driver), "Should NOT reach home with empty email"
        logger.info("✅ PASS: Empty email correctly rejected")

    def test_login_empty_password(self, driver):
        """Login with empty password should fail."""
        logger.info("\n=== NEGATIVE: Empty password ===")

        _reset_to_login(driver)
        edits = driver.find_elements(AppiumBy.XPATH, "//android.widget.EditText")
        if len(edits) >= 2:
            _clear_and_type(edits[0], VALID_EMAIL)
            _clear_and_type(edits[1], "")
            # Safe keyboard hide
            driver.tap([(540, 200)])

            for loc in [
                (AppiumBy.ACCESSIBILITY_ID, "Login"),
                (AppiumBy.XPATH, "//*[contains(@content-desc, 'Login')]"),
            ]:
                try:
                    driver.find_element(*loc).click()
                    break
                except Exception:
                    continue
            time.sleep(5)

        assert not _is_on_home(driver), "Should NOT reach home with empty password"
        logger.info("✅ PASS: Empty password correctly rejected")

    def test_login_wrong_email(self, driver):
        """Login with unregistered email should fail."""
        logger.info("\n=== NEGATIVE: Wrong email ===")

        _reset_to_login(driver)
        _do_login(driver, "wronguser@yopmail.com", VALID_PASSWORD)
        assert not _is_on_home(driver), "Should NOT reach home with wrong email"
        logger.info("✅ PASS: Wrong email correctly rejected")

    def test_login_wrong_password(self, driver):
        """Login with wrong password should fail."""
        logger.info("\n=== NEGATIVE: Wrong password ===")

        _reset_to_login(driver)
        _do_login(driver, VALID_EMAIL, "WrongPass999!")
        assert not _is_on_home(driver), "Should NOT reach home with wrong password"
        logger.info("✅ PASS: Wrong password correctly rejected")

    def test_login_invalid_email_format(self, driver):
        """Login with invalid email format should fail."""
        logger.info("\n=== NEGATIVE: Invalid email format ===")

        _reset_to_login(driver)
        _do_login(driver, "not-an-email", VALID_PASSWORD)
        assert not _is_on_home(driver), "Should NOT reach home with invalid email"
        logger.info("✅ PASS: Invalid email format correctly rejected")


class TestLoginPositive:
    """Positive login — must succeed to enable all subsequent tests."""

    def test_login_success(self, driver):
        """Login with valid credentials → home screen with Welcome greeting."""
        logger.info("\n" + "=" * 50)
        logger.info("POSITIVE: Login with valid credentials")
        logger.info("=" * 50)

        # Ensure on login screen
        if not _is_on_login(driver):
            _reset_to_login(driver)
            time.sleep(2)

        edits = driver.find_elements(AppiumBy.XPATH, "//android.widget.EditText")
        if len(edits) < 2:
            # Last resort: restart app
            driver.terminate_app("com.mepo")
            time.sleep(2)
            driver.activate_app("com.mepo")
            time.sleep(10)
            edits = driver.find_elements(AppiumBy.XPATH, "//android.widget.EditText")

        assert len(edits) >= 2, f"Expected 2 EditText fields, found {len(edits)}"

        # Enter email
        _clear_and_type(edits[0], VALID_EMAIL)
        logger.info(f"📧 Email: {VALID_EMAIL}")

        # Enter password
        _clear_and_type(edits[1], VALID_PASSWORD)
        logger.info("🔑 Password entered")

        # Safe keyboard hide
        driver.tap([(540, 200)])

        # Tap Login
        for loc in [
            (AppiumBy.ACCESSIBILITY_ID, "Login"),
            (AppiumBy.XPATH, "//*[@content-desc='Login']"),
            (AppiumBy.XPATH, "//*[contains(@content-desc, 'Login')]"),
        ]:
            try:
                driver.find_element(*loc).click()
                logger.info("🔓 Login button tapped")
                break
            except Exception:
                continue

        # Wait for home screen
        time.sleep(10)

        # Verify — "Welcome, danip" should be visible
        welcome = driver.find_elements(AppiumBy.XPATH,
            "//*[contains(@content-desc, 'Welcome,')]")
        assert len(welcome) > 0, "Home screen not reached — login failed"

        driver.save_screenshot("reports/screenshots/login_success.png")
        logger.info("✅ LOGIN SUCCESSFUL — Welcome screen displayed!")
