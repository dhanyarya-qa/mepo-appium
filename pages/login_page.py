"""
Login Page Object
=================
Locators and actions for the Mepo Travel app's Login / Sign-In screen.
Handles email/password input, login submission, and validation.

Based on actual UI screenshot:
- Header: "Welcome Back!"
- Email field: "Input your email"
- Password field: "Input your password"
- Button: "Login"
- Links: "Register", "Forgot Password?"
"""

import logging
import time
from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class LoginPage(BasePage):
    """Page Object for the Login / Sign-In screen."""

    # ══════════════════════════════════════════════
    # LOCATORS — Based on actual app UI
    # ══════════════════════════════════════════════

    # ── Page Header ──────────────────────────────
    HEADER_WELCOME = (AppiumBy.XPATH, "//*[contains(@text, 'Welcome Back')]")
    HEADER_WELCOME_DESC = (AppiumBy.XPATH, "//*[contains(@content-desc, 'Welcome Back')]")

    # ── Email Field ──────────────────────────────
    INPUT_EMAIL = (AppiumBy.XPATH, "//*[contains(@text, 'Input your email')]")
    INPUT_EMAIL_DESC = (AppiumBy.XPATH, "//*[contains(@content-desc, 'Input your email')]")
    INPUT_EMAIL_EDIT = (AppiumBy.XPATH, "//android.widget.EditText[1]")

    # ── Password Field ───────────────────────────
    INPUT_PASSWORD = (AppiumBy.XPATH, "//*[contains(@text, 'Input your password')]")
    INPUT_PASSWORD_DESC = (AppiumBy.XPATH, "//*[contains(@content-desc, 'Input your password')]")
    INPUT_PASSWORD_EDIT = (AppiumBy.XPATH, "//android.widget.EditText[2]")

    # ── Login Button ─────────────────────────────
    BTN_LOGIN = (AppiumBy.XPATH, "//*[@text='Login']")
    BTN_LOGIN_DESC = (AppiumBy.ACCESSIBILITY_ID, "Login")
    BTN_LOGIN_CONTAINS = (AppiumBy.XPATH, "//*[contains(@content-desc, 'Login')]")

    # ── Register Link ────────────────────────────
    LINK_REGISTER = (AppiumBy.XPATH, "//*[@text='Register']")
    LINK_REGISTER_DESC = (AppiumBy.ACCESSIBILITY_ID, "Register")

    # ── Forgot Password ─────────────────────────
    LINK_FORGOT = (AppiumBy.XPATH, "//*[contains(@text, 'Forgot Password')]")
    LINK_FORGOT_DESC = (AppiumBy.XPATH, "//*[contains(@content-desc, 'Forgot Password')]")

    # ── Show/Hide Password Toggle ────────────────
    BTN_TOGGLE_PASSWORD = (AppiumBy.XPATH,
        "//android.widget.EditText[2]/following-sibling::*[1]"
    )

    # ── Error Messages ───────────────────────────
    ERROR_MESSAGE = (AppiumBy.XPATH,
        "//*[contains(@text, 'wrong') or contains(@text, 'invalid') "
        "or contains(@text, 'Error') or contains(@text, 'failed') "
        "or contains(@text, 'salah') or contains(@text, 'gagal')]"
    )

    # ══════════════════════════════════════════════
    # ACTIONS
    # ══════════════════════════════════════════════

    def wait_for_login_page_loaded(self, timeout: int = 15):
        """Wait until the login page is fully rendered."""
        logger.info("🔐 Waiting for login page to load...")

        indicators = [
            self.HEADER_WELCOME, self.HEADER_WELCOME_DESC,
            self.INPUT_EMAIL, self.INPUT_EMAIL_DESC, self.INPUT_EMAIL_EDIT,
        ]

        for ind in indicators:
            if self.is_element_present(ind, timeout=timeout):
                logger.info(f"✅ Login page loaded — detected: {ind}")
                return True

        logger.warning("⚠ Login page could not be confirmed as loaded")
        return False

    def enter_email(self, email: str):
        """Enter email address into the email field."""
        email_fields = [
            self.INPUT_EMAIL, self.INPUT_EMAIL_DESC, self.INPUT_EMAIL_EDIT,
        ]

        for field in email_fields:
            try:
                if self.is_element_present(field, timeout=5):
                    element = self.driver.find_element(*field)
                    element.click()
                    time.sleep(0.3)
                    element.clear()
                    element.send_keys(email)
                    logger.info(f"📧 Email entered: {email} (via {field})")
                    # Hide keyboard
                    try:
                        self.driver.hide_keyboard()
                    except Exception:
                        pass
                    return
            except Exception as e:
                logger.debug(f"  Email field {field} failed: {e}")
                continue

        raise Exception("❌ Could not find email input field")

    def enter_password(self, password: str):
        """Enter password into the password field."""
        password_fields = [
            self.INPUT_PASSWORD, self.INPUT_PASSWORD_DESC, self.INPUT_PASSWORD_EDIT,
        ]

        for field in password_fields:
            try:
                if self.is_element_present(field, timeout=5):
                    element = self.driver.find_element(*field)
                    element.click()
                    time.sleep(0.3)
                    element.clear()
                    element.send_keys(password)
                    logger.info(f"🔑 Password entered (via {field})")
                    # Hide keyboard
                    try:
                        self.driver.hide_keyboard()
                    except Exception:
                        pass
                    return
            except Exception as e:
                logger.debug(f"  Password field {field} failed: {e}")
                continue

        raise Exception("❌ Could not find password input field")

    def tap_login_button(self):
        """Tap the Login button to submit."""
        login_buttons = [
            self.BTN_LOGIN, self.BTN_LOGIN_DESC, self.BTN_LOGIN_CONTAINS,
        ]

        for btn in login_buttons:
            try:
                if self.is_element_present(btn, timeout=5):
                    element = self.driver.find_element(*btn)
                    element.click()
                    logger.info(f"🔓 Login button tapped (via {btn})")
                    return
            except Exception as e:
                logger.debug(f"  Login button {btn} failed: {e}")
                continue

        raise Exception("❌ Could not find Login button")

    def login(self, email: str, password: str):
        """Complete login flow: enter email, password, tap login."""
        logger.info(f"🔐 Performing login with email: {email}")
        self.enter_email(email)
        self.enter_password(password)
        self.tap_login_button()
        logger.info("✅ Login form submitted")

    def wait_for_login_success(self, timeout: int = 30) -> bool:
        """
        Wait for login to complete — detect home screen elements.
        """
        logger.info("⏳ Waiting for login to complete...")
        time.sleep(3)  # Wait for API response

        # Check for home screen indicators
        home_indicators = [
            (AppiumBy.XPATH, "//*[contains(@content-desc, 'Home')]"),
            (AppiumBy.XPATH, "//*[contains(@text, 'Home')]"),
            (AppiumBy.XPATH, "//*[contains(@content-desc, 'Open Trip')]"),
            (AppiumBy.XPATH, "//*[contains(@text, 'Open Trip')]"),
            (AppiumBy.XPATH, "//*[contains(@content-desc, 'Itinerary')]"),
            (AppiumBy.XPATH, "//*[contains(@text, 'Itinerary')]"),
            (AppiumBy.XPATH, "//*[contains(@content-desc, 'Profile')]"),
        ]

        for indicator in home_indicators:
            if self.is_element_present(indicator, timeout=timeout):
                logger.info(f"✅ Login successful — home detected: {indicator}")
                return True

        # Check if still on login page (login failed)
        if self.is_error_displayed():
            logger.error("❌ Login failed — error message on screen")
            return False

        logger.warning("⚠ Login result unclear")
        return False

    def is_error_displayed(self) -> bool:
        """Check if any error message is displayed."""
        return self.is_element_present(self.ERROR_MESSAGE, timeout=3)

    def get_error_message(self) -> str:
        """Get the error message text if displayed."""
        if self.is_element_present(self.ERROR_MESSAGE, timeout=3):
            try:
                el = self.driver.find_element(*self.ERROR_MESSAGE)
                return el.text or el.get_attribute("content-desc") or ""
            except Exception:
                return ""
        return ""

    def is_login_page_displayed(self) -> bool:
        """Check if the login page is currently displayed."""
        indicators = [
            self.HEADER_WELCOME, self.HEADER_WELCOME_DESC,
            self.INPUT_EMAIL, self.INPUT_EMAIL_DESC, self.INPUT_EMAIL_EDIT,
        ]
        return any(self.is_element_present(f, timeout=3) for f in indicators)

    def tap_forgot_password(self):
        """Tap the 'Forgot Password?' link."""
        links = [self.LINK_FORGOT, self.LINK_FORGOT_DESC]
        for link in links:
            if self.is_element_present(link, timeout=3):
                self.driver.find_element(*link).click()
                logger.info("🔗 Forgot Password tapped")
                return

    def tap_register_link(self):
        """Tap the 'Register' link."""
        links = [self.LINK_REGISTER, self.LINK_REGISTER_DESC]
        for link in links:
            if self.is_element_present(link, timeout=3):
                self.driver.find_element(*link).click()
                logger.info("📝 Register link tapped")
                return
