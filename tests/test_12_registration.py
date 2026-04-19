"""
Test 12 — Registration Flow
===========================
Verifies the registration screen accessibility and form validation.
"""

import pytest
import logging
from appium.webdriver.common.appiumby import AppiumBy

logger = logging.getLogger(__name__)

pytestmark = [pytest.mark.login, pytest.mark.regression]


def _ensure_register_screen(driver):
    # If on login screen, tap register
    register_link = driver.find_elements(AppiumBy.XPATH, "//*[@content-desc='Register']")
    if register_link and register_link[0].get_attribute("clickable") == "true":
        register_link[0].click()
        return True
        
    # Check if already on register screen
    create_acc = driver.find_elements(AppiumBy.XPATH, "//*[@content-desc='Create your Account']")
    if create_acc:
        return True
        
    return False


class TestRegistration:

    def test_navigate_to_register(self, driver):
        logger.info("\n=== REGISTRATION: Navigate ===")
        assert _ensure_register_screen(driver), "Failed to reach Registration screen"
        logger.info("✅ Reached Registration screen")

    def test_registration_form_elements(self, driver):
        if not _ensure_register_screen(driver):
            pytest.skip("Not on register screen")

        email = driver.find_elements(AppiumBy.XPATH, "//android.widget.EditText[@hint='Add email']")
        assert len(email) > 0, "Email field not found"
        
        display_name = driver.find_elements(AppiumBy.XPATH, "//android.widget.EditText[@hint='Add Display Name']")
        assert len(display_name) > 0, "Display name field not found"
        
        username = driver.find_elements(AppiumBy.XPATH, "//android.widget.EditText[contains(@hint, 'Username')]")
        assert len(username) > 0, "Username field not found"

        passwords = driver.find_elements(AppiumBy.XPATH, "//android.widget.EditText[@password='true']")
        assert len(passwords) >= 2, "Password / Confirm fields missing"

        logger.info("✅ All registration form elements found")

    def test_register_button_disabled(self, driver):
        if not _ensure_register_screen(driver):
            pytest.skip("Not on register screen")

        register_btn = driver.find_element(AppiumBy.XPATH, "//android.widget.Button[@content-desc='Register']")
        assert register_btn.get_attribute("enabled") == "false", "Register button should be disabled when empty"
        logger.info("✅ Register button correctly disabled")
        
    def test_back_to_login(self, driver):
        if not _ensure_register_screen(driver):
            pytest.skip("Not on register screen")

        back_login = driver.find_elements(AppiumBy.XPATH, "//*[@content-desc='Login' and @clickable='true']")
        if back_login:
            back_login[0].click()
        else:
            driver.back()
            
        login_btn = driver.find_elements(AppiumBy.XPATH, "//android.widget.Button[@content-desc='Login']")
        assert len(login_btn) > 0, "Failed to navigate back to login"
        logger.info("✅ Successfully navigated back to Login screen")
