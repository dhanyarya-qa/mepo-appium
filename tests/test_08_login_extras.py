"""
Test 08 — Login Screen Extras (Real Device)
=============================================
Verifies additional login screen elements: onboarding carousel,
language switcher, Register link, Forgot Password, Terms & Conditions.

XML Source: reports/real_device/explore_01_login.xml
"""

import pytest
import time
import logging
from appium.webdriver.common.appiumby import AppiumBy

logger = logging.getLogger(__name__)

pytestmark = [pytest.mark.login, pytest.mark.regression]


def _ensure_login_screen(driver):
    """Ensure we're on the login screen. If logged in, we skip these tests."""
    # Check if we're already on login
    login_btn = driver.find_elements(AppiumBy.XPATH,
        "//*[@content-desc='Login']")
    welcome_back = driver.find_elements(AppiumBy.XPATH,
        "//*[contains(@content-desc, 'Welcome Back')]")
    edit_text = driver.find_elements(AppiumBy.XPATH,
        "//android.widget.EditText")

    if login_btn or welcome_back or len(edit_text) >= 2:
        return True

    # We're not on login screen — we might be logged in
    # Check for home screen
    welcome = driver.find_elements(AppiumBy.XPATH,
        "//*[contains(@content-desc, 'Welcome,')]")
    if welcome:
        return False  # Logged in, can't test login extras

    return False


class TestLoginScreenOnboarding:
    """Verify onboarding carousel on login screen."""

    def test_onboarding_carousel_image(self, driver):
        """Onboarding carousel should show feature descriptions."""
        logger.info("\n=== LOGIN EXTRAS: Onboarding Carousel ===")

        if not _ensure_login_screen(driver):
            pytest.skip("Not on login screen (user may be logged in)")

        # From XML: ImageView with content-desc containing feature description
        # e.g. "Detailed Activity Creation\nAdd details like location..."
        onboarding = driver.find_elements(AppiumBy.XPATH,
            "//android.widget.ImageView[string-length(@content-desc) > 20]")
        assert len(onboarding) > 0, "No onboarding carousel image found"

        desc = onboarding[0].get_attribute("content-desc")
        logger.info(f"✅ Onboarding carousel visible: {desc[:80]}...")

    def test_onboarding_dot_indicators(self, driver):
        """Onboarding dot indicators should be present."""
        if not _ensure_login_screen(driver):
            pytest.skip("Not on login screen")

        # From XML: 4 small Button elements (carousel dots)
        # at y≈887, no content-desc
        dots = driver.find_elements(AppiumBy.XPATH,
            "//android.widget.Button[not(@content-desc) and @clickable='true']")
        # Filter out the Login button and password toggle
        small_dots = []
        for d in dots:
            bounds = d.get_attribute("bounds") or ""
            # dots are small ~16-22px elements
            if "887" in bounds or "903" in bounds or "906" in bounds:
                small_dots.append(d)

        # Fallback: just count all small buttons (dots are typically > 3)
        if len(small_dots) == 0:
            small_dots = [d for d in dots if d.size.get('width', 100) < 50]

        assert len(small_dots) >= 2, f"Expected ≥2 dot indicators, found {len(small_dots)}"
        logger.info(f"✅ Found {len(small_dots)} onboarding dot indicators")


class TestLoginScreenLinks:
    """Verify Register, Forgot Password, and Terms links."""

    def test_register_link_visible(self, driver):
        """'Register' link should be visible and clickable."""
        logger.info("\n=== LOGIN EXTRAS: Register Link ===")

        if not _ensure_login_screen(driver):
            pytest.skip("Not on login screen")

        # From XML: content-desc="Register", clickable="true"
        register = driver.find_elements(AppiumBy.XPATH,
            "//*[@content-desc='Register']")
        assert len(register) > 0, "'Register' link not found"
        assert register[0].get_attribute("clickable") == "true"
        logger.info("✅ 'Register' link visible & clickable")

    def test_dont_have_account_text(self, driver):
        """'Don't have account yet?' text should be visible."""
        if not _ensure_login_screen(driver):
            pytest.skip("Not on login screen")

        text = driver.find_elements(AppiumBy.XPATH,
            "//*[contains(@content-desc, 'have account')]")
        assert len(text) > 0, "'Don't have account?' text not found"
        logger.info("✅ 'Don't have account yet?' text visible")

    def test_forgot_password_link(self, driver):
        """'Forgot Password?' link should be visible and clickable."""
        logger.info("\n=== LOGIN EXTRAS: Forgot Password ===")

        if not _ensure_login_screen(driver):
            pytest.skip("Not on login screen")

        # From XML: content-desc="Forgot Password?", clickable="true"
        forgot = driver.find_elements(AppiumBy.XPATH,
            "//*[@content-desc='Forgot Password?']")
        assert len(forgot) > 0, "'Forgot Password?' link not found"
        assert forgot[0].get_attribute("clickable") == "true"
        logger.info("✅ 'Forgot Password?' link visible & clickable")

    def test_terms_and_conditions_link(self, driver):
        """Terms & Conditions link should be visible."""
        logger.info("\n=== LOGIN EXTRAS: Terms & Conditions ===")

        if not _ensure_login_screen(driver):
            pytest.skip("Not on login screen")

        # From XML: content-desc=" Terms & Conditions"
        terms = driver.find_elements(AppiumBy.XPATH,
            "//*[contains(@content-desc, 'Terms')]")
        assert len(terms) > 0, "'Terms & Conditions' link not found"
        logger.info("✅ 'Terms & Conditions' link visible")

    def test_terms_disclaimer_text(self, driver):
        """Terms disclaimer text should be visible."""
        if not _ensure_login_screen(driver):
            pytest.skip("Not on login screen")

        # From XML: "By login the app, you agree with our"
        disclaimer = driver.find_elements(AppiumBy.XPATH,
            "//*[contains(@content-desc, 'By login the app')]")
        assert len(disclaimer) > 0, "Terms disclaimer text not found"
        logger.info("✅ Terms disclaimer text visible")


class TestLoginScreenLanguage:
    """Verify language switcher."""

    def test_language_switcher_visible(self, driver):
        """Language switcher (EN) should be visible."""
        logger.info("\n=== LOGIN EXTRAS: Language Switcher ===")

        if not _ensure_login_screen(driver):
            pytest.skip("Not on login screen")

        # From XML: ImageView with content-desc="EN", clickable="true"
        lang = driver.find_elements(AppiumBy.XPATH,
            "//*[@content-desc='EN']")
        assert len(lang) > 0, "Language switcher 'EN' not found"
        assert lang[0].get_attribute("clickable") == "true"
        logger.info("✅ Language switcher 'EN' visible & clickable")

    def test_email_field_hint(self, driver):
        """Email field should have correct hint text."""
        if not _ensure_login_screen(driver):
            pytest.skip("Not on login screen")

        # From XML: EditText with hint="Input your email"
        email = driver.find_elements(AppiumBy.XPATH,
            "//android.widget.EditText[@hint='Input your email']")
        if not email:
            email = driver.find_elements(AppiumBy.XPATH,
                "//android.widget.EditText[1]")
        assert len(email) > 0, "Email field not found"
        hint = email[0].get_attribute("hint") or ""
        assert "email" in hint.lower(), f"Email hint wrong: {hint}"
        logger.info(f"✅ Email field hint: '{hint}'")

    def test_password_field_hint(self, driver):
        """Password field should have correct hint and be masked."""
        if not _ensure_login_screen(driver):
            pytest.skip("Not on login screen")

        # From XML: EditText with hint="Input your password", password="true"
        pwd = driver.find_elements(AppiumBy.XPATH,
            "//android.widget.EditText[@password='true']")
        assert len(pwd) > 0, "Password field not found"
        hint = pwd[0].get_attribute("hint") or ""
        assert "password" in hint.lower(), f"Password hint wrong: {hint}"
        logger.info(f"✅ Password field hint: '{hint}', masked=true")

    def test_login_button_disabled_when_empty(self, driver):
        """Login button should be disabled when fields are empty."""
        if not _ensure_login_screen(driver):
            pytest.skip("Not on login screen")

        # From XML: Button content-desc="Login", enabled="false" by default
        login_btn = driver.find_elements(AppiumBy.XPATH,
            "//*[@content-desc='Login']")
        assert len(login_btn) > 0, "Login button not found"

        enabled = login_btn[0].get_attribute("enabled")
        assert enabled == "false", f"Login button should be disabled, got enabled={enabled}"
        logger.info("✅ Login button disabled when fields empty")
