"""
Profile Page Object
===================
Locators and actions for the Mepo Travel app's Profile screen.
Handles viewing, editing, and logout functionality.
"""

import logging
import time
from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class ProfilePage(BasePage):
    """Page Object for the Profile / Account screen."""

    # ══════════════════════════════════════════════
    # LOCATORS
    # ══════════════════════════════════════════════

    # Navigation Tab
    TAB_PROFILE = (AppiumBy.ACCESSIBILITY_ID, "Profile")
    TAB_PROFILE_XPATH = (AppiumBy.XPATH, "//*[contains(@content-desc, 'Profile')]")

    # Profile Header
    PROFILE_NAME = (AppiumBy.XPATH, "//*[contains(@content-desc, 'danip') or contains(@text, 'danip')]")
    PROFILE_EMAIL = (AppiumBy.XPATH, "//*[contains(@content-desc, 'yopmail') or contains(@text, 'yopmail')]")
    PROFILE_AVATAR = (AppiumBy.XPATH, "//*[contains(@content-desc, 'Profile') and contains(@content-desc, 'photo')]")

    # Edit Profile
    BTN_EDIT_PROFILE = (AppiumBy.XPATH,
        "//*[contains(@content-desc, 'Edit') or contains(@text, 'Edit')]"
    )
    INPUT_NAME = (AppiumBy.XPATH, "//android.widget.EditText[1]")
    INPUT_PHONE = (AppiumBy.XPATH, "//android.widget.EditText[2]")
    BTN_SAVE = (AppiumBy.XPATH,
        "//*[contains(@content-desc, 'Save') or contains(@text, 'Save') "
        "or contains(@content-desc, 'Update') or contains(@text, 'Update')]"
    )

    # Logout
    BTN_LOGOUT = (AppiumBy.XPATH,
        "//*[contains(@content-desc, 'Logout') or contains(@text, 'Logout') "
        "or contains(@content-desc, 'Log Out') or contains(@text, 'Log Out') "
        "or contains(@content-desc, 'Sign Out') or contains(@text, 'Sign Out')]"
    )
    BTN_CONFIRM_LOGOUT = (AppiumBy.XPATH,
        "//*[contains(@content-desc, 'Yes') or contains(@text, 'Yes') "
        "or contains(@content-desc, 'OK') or contains(@text, 'OK') "
        "or contains(@content-desc, 'Confirm') or contains(@text, 'Confirm')]"
    )

    # Settings / Info sections
    SECTION_SETTINGS = (AppiumBy.XPATH,
        "//*[contains(@content-desc, 'Settings') or contains(@text, 'Settings')]"
    )
    SECTION_ABOUT = (AppiumBy.XPATH,
        "//*[contains(@content-desc, 'About') or contains(@text, 'About')]"
    )
    SECTION_PRIVACY = (AppiumBy.XPATH,
        "//*[contains(@content-desc, 'Privacy') or contains(@text, 'Privacy')]"
    )
    SECTION_HELP = (AppiumBy.XPATH,
        "//*[contains(@content-desc, 'Help') or contains(@text, 'Help')]"
    )

    # ══════════════════════════════════════════════
    # ACTIONS
    # ══════════════════════════════════════════════

    def navigate_to_profile(self):
        """Navigate to Profile tab."""
        for loc in [self.TAB_PROFILE, self.TAB_PROFILE_XPATH]:
            if self.is_element_present(loc, timeout=5):
                self.driver.find_element(*loc).click()
                time.sleep(3)
                logger.info("👤 Navigated to Profile tab")
                return True
        return False

    def is_profile_displayed(self) -> bool:
        """Check if profile page is displayed."""
        return (
            self.is_element_present(self.PROFILE_NAME, timeout=5)
            or self.is_element_present(self.PROFILE_EMAIL, timeout=3)
            or self.is_element_present(self.BTN_LOGOUT, timeout=3)
        )

    def wait_for_profile_loaded(self, timeout=10):
        """Wait for profile page to load."""
        time.sleep(2)
        # Take screenshot for debugging
        self._capture_screenshot("profile_loaded")
        
        # Try multiple indicators
        indicators = [
            self.PROFILE_NAME, self.PROFILE_EMAIL, self.BTN_LOGOUT,
            self.BTN_EDIT_PROFILE, self.SECTION_SETTINGS,
        ]
        for ind in indicators:
            if self.is_element_present(ind, timeout=timeout):
                logger.info(f"✅ Profile page loaded — detected: {ind}")
                return True
        logger.warning("⚠ Profile page could not be confirmed")
        return False

    def get_profile_name(self) -> str:
        """Get displayed profile name."""
        if self.is_element_present(self.PROFILE_NAME, timeout=5):
            el = self.driver.find_element(*self.PROFILE_NAME)
            return el.text or el.get_attribute("content-desc") or ""
        return ""

    def get_profile_email(self) -> str:
        """Get displayed profile email."""
        if self.is_element_present(self.PROFILE_EMAIL, timeout=5):
            el = self.driver.find_element(*self.PROFILE_EMAIL)
            return el.text or el.get_attribute("content-desc") or ""
        return ""

    def tap_edit_profile(self):
        """Tap Edit Profile button."""
        if self.is_element_present(self.BTN_EDIT_PROFILE, timeout=5):
            self.driver.find_element(*self.BTN_EDIT_PROFILE).click()
            time.sleep(2)
            logger.info("✏️ Edit Profile tapped")
            return True
        logger.warning("⚠ Edit Profile button not found")
        return False

    def edit_name(self, new_name: str):
        """Edit the profile name field."""
        if self.is_element_present(self.INPUT_NAME, timeout=5):
            el = self.driver.find_element(*self.INPUT_NAME)
            el.click()
            time.sleep(0.3)
            el.clear()
            el.send_keys(new_name)
            self.hide_keyboard()
            logger.info(f"📝 Name edited to: {new_name}")

    def edit_phone(self, new_phone: str):
        """Edit the phone number field."""
        if self.is_element_present(self.INPUT_PHONE, timeout=5):
            el = self.driver.find_element(*self.INPUT_PHONE)
            el.click()
            time.sleep(0.3)
            el.clear()
            el.send_keys(new_phone)
            self.hide_keyboard()
            logger.info(f"📱 Phone edited to: {new_phone}")

    def tap_save(self):
        """Tap save button."""
        if self.is_element_present(self.BTN_SAVE, timeout=5):
            self.driver.find_element(*self.BTN_SAVE).click()
            time.sleep(2)
            logger.info("💾 Save tapped")
            return True
        return False

    def tap_logout(self):
        """Tap the logout button."""
        # Scroll to find logout
        for _ in range(5):
            if self.is_element_present(self.BTN_LOGOUT, timeout=3):
                self.driver.find_element(*self.BTN_LOGOUT).click()
                time.sleep(2)
                logger.info("🚪 Logout tapped")
                return True
            self._swipe_up()
            time.sleep(1)
        logger.warning("⚠ Logout button not found")
        return False

    def confirm_logout(self):
        """Confirm logout in the dialog."""
        if self.is_element_present(self.BTN_CONFIRM_LOGOUT, timeout=5):
            self.driver.find_element(*self.BTN_CONFIRM_LOGOUT).click()
            time.sleep(3)
            logger.info("✅ Logout confirmed")
            return True
        # If no dialog, already logged out
        logger.info("ℹ No logout confirmation dialog")
        return True

    def perform_logout(self):
        """Full logout flow: navigate to profile, tap logout, confirm."""
        self.navigate_to_profile()
        time.sleep(2)
        self.tap_logout()
        self.confirm_logout()
        logger.info("🔐 Logout complete")
