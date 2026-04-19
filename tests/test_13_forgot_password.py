"""
Test 13 — Forgot Password Flow
==============================
Verifies the forgot password screen accessibility and OTP send validation.
"""

import pytest
import logging
import time
from appium.webdriver.common.appiumby import AppiumBy

logger = logging.getLogger(__name__)

pytestmark = [pytest.mark.login, pytest.mark.regression]


def _ensure_forgot_screen(driver):
    # If on login screen, tap forgot password
    forgot_link = driver.find_elements(AppiumBy.XPATH, "//*[@content-desc='Forgot Password?']")
    if forgot_link and forgot_link[-1].get_attribute("clickable") == "true":
        forgot_link[-1].click()
        time.sleep(2)
        return True
        
    # Check if already on forgot password screen
    send_otp = driver.find_elements(AppiumBy.XPATH, "//*[@content-desc='Send otp']")
    if send_otp:
        return True
        
    return False


class TestForgotPassword:

    def test_navigate_to_forgot_password(self, driver):
        logger.info("\n=== FORGOT PASSWORD: Navigate ===")
        assert _ensure_forgot_screen(driver), "Failed to reach Forgot Password screen"
        logger.info("✅ Reached Forgot Password screen")

    def test_forgot_form_elements(self, driver):
        if not _ensure_forgot_screen(driver):
            pytest.skip("Not on forgot password screen")

        title = driver.find_elements(AppiumBy.XPATH, "//*[@content-desc='Forgot Password?']")
        assert len(title) > 0, "Title not found"
        
        email = driver.find_elements(AppiumBy.XPATH, "//android.widget.EditText[@hint='Input your email']")
        assert len(email) > 0, "Email field not found"

        logger.info("✅ Forgot Password form elements found")

    def test_send_otp_button_disabled(self, driver):
        if not _ensure_forgot_screen(driver):
            pytest.skip("Not on forgot password screen")

        btn = driver.find_element(AppiumBy.XPATH, "//android.widget.Button[@content-desc='Send otp']")
        assert btn.get_attribute("enabled") == "false", "Send OTP button should be disabled when empty"
        logger.info("✅ Send OTP button correctly disabled")
        
    def test_back_to_login(self, driver):
        if not _ensure_forgot_screen(driver):
            pytest.skip("Not on forgot password screen")

        # The back button is an ImageView without content-desc at the top left
        back_btn = driver.find_elements(AppiumBy.XPATH, "//android.widget.ImageView[@clickable='true']")
        if back_btn:
            back_btn[0].click()
        else:
            driver.back()
            
        time.sleep(2)
        login_btn = driver.find_elements(AppiumBy.XPATH, "//android.widget.Button[@content-desc='Login']")
        assert len(login_btn) > 0, "Failed to navigate back to login"
        logger.info("✅ Successfully navigated back to Login screen")
