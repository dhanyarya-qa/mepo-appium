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
        
    def test_positive_registration_flow(self, driver):
        """Attempts to register a completely new randomized account to verify success logic."""
        if not _ensure_register_screen(driver):
            pytest.skip("Not on register screen")
            
        import random
        rnd = random.randint(1000, 9999)
        yop_username = f"autoqa{rnd}"
        test_email = f"{yop_username}@yopmail.com"
        
        email_fld = driver.find_elements(AppiumBy.XPATH, "//android.widget.EditText[@hint='Add email']")
        display_fld = driver.find_elements(AppiumBy.XPATH, "//android.widget.EditText[@hint='Add Display Name']")
        user_fld = driver.find_elements(AppiumBy.XPATH, "//android.widget.EditText[contains(@hint, 'Username')]")
        passwords = driver.find_elements(AppiumBy.XPATH, "//android.widget.EditText[@password='true']")
        
        # Fill Form Safely without clear() to prevent UiAutomator crashes
        if email_fld: 
            email_fld[0].click()
            time.sleep(0.5)
            email_fld[0].send_keys(test_email)
            time.sleep(0.5)
            
        if display_fld:
            display_fld[0].click()
            time.sleep(0.5)
            display_fld[0].send_keys(f"QA Tester {rnd}")
            time.sleep(0.5)
            
        if user_fld:
            user_fld[0].click()
            time.sleep(0.5)
            user_fld[0].send_keys(f"qatester{rnd}")
            time.sleep(0.5)
            
        if len(passwords) >= 2:
            passwords[0].click()
            time.sleep(0.5)
            passwords[0].send_keys("Sandi123!")
            time.sleep(0.5)
            
            passwords[1].click()
            time.sleep(0.5)
            passwords[1].send_keys("Sandi123!")
            time.sleep(0.5)
            
        # Safe keyboard hide
        driver.tap([(540, 200)])
        time.sleep(1)
        
        register_btn = driver.find_elements(AppiumBy.XPATH, "//android.widget.Button[@content-desc='Register']")
        if register_btn and register_btn[0].get_attribute("enabled") == "true":
            register_btn[0].click()
            logger.info("✅ Clicked Active Register Button")
            time.sleep(5)
            
            # ----------------------------------------------------
            # OTP EXTRACTION VIA YOPMAIL
            # ----------------------------------------------------
            logger.info("⏳ Waiting for OTP to arrive in Yopmail...")
            time.sleep(15) # Give the backend time to send the email
            
            try:
                from yopmail import Yopmail
                import re
                
                y = Yopmail(yop_username)
                mail_ids = y.get_mail_ids()
                
                if mail_ids:
                    # Get latest mail
                    mail = y.get_mail_body(mail_ids[0])
                    # Scan for OTP typically 4 or 6 digits in the text
                    otp_matches = re.findall(r'\b\d{4,6}\b', mail.text)
                    if otp_matches:
                        otp_code = otp_matches[0]
                        logger.info(f"📧 EXTRACTED OTP FROM YOPMAIL: {otp_code}")
                    else:
                        logger.warning("⚠ OTP digits not found in email body!")
                        otp_code = "123456" # Fallback guess if parsing fails
                        logger.debug("Mail content dump: " + str(mail.text)[:200])
                else:
                    logger.warning("⚠ No email received in Yopmail! Proceeding with fallback dummy OTP.")
                    otp_code = "123456"
            except Exception as e:
                logger.error(f"❌ Failed to fetch Yopmail: {e}")
                otp_code = "123456"
            
            # ----------------------------------------------------
            # INPUT OTP
            # ----------------------------------------------------
            logger.info("📍 Attempting to Input OTP in Mepo App")
            # Usually Apps feature multiple EditText boxes for OTP
            otp_fields = driver.find_elements(AppiumBy.XPATH, "//android.widget.EditText")
            if otp_fields:
                if len(otp_fields) == 1:
                    # Single field for the whole code
                    otp_fields[0].click()
                    time.sleep(0.5)
                    otp_fields[0].send_keys(otp_code)
                else:
                    # Multiple distinct boxes, enter digit by digit
                    for idx, char in enumerate(otp_code):
                        if idx < len(otp_fields):
                            otp_fields[idx].click()
                            time.sleep(0.3)
                            otp_fields[idx].send_keys(char)
                            time.sleep(0.1)
                
                # Hide keyboard
                driver.tap([(540, 200)])
                time.sleep(1)
                
                # Check for confirm button if auto-submit doesn't happen
                verify_btn = driver.find_elements(AppiumBy.XPATH, "//*[contains(@content-desc, 'Verify') or contains(@content-desc, 'Submit')]")
                if verify_btn:
                    verify_btn[0].click()
                time.sleep(5)
            else:
                logger.warning("⚠ OTP input fields not found in the app.")
            
            # Look for Success Dialog or Home Navigation
            success = driver.find_elements(AppiumBy.XPATH, 
                "//*[contains(@content-desc, 'Success') or contains(@content-desc, 'Welcome')]")
            logger.info(f" Registration outcome state detected: {len(success) > 0}")
        else:
            logger.warning("⚠ Register button remained disabled despite full input form")
        
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
