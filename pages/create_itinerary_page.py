"""
Create Itinerary Page Object
=============================
Locators and actions for the Create Itinerary feature.
"""

import logging
import time
from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class CreateItineraryPage(BasePage):
    """Page Object for Create Itinerary flow."""

    # ══════════════════════════════════════════════
    # LOCATORS
    # ══════════════════════════════════════════════

    # Entry point
    BTN_CREATE_ITINERARY = (AppiumBy.XPATH,
        "//*[contains(@content-desc, 'Create New Itinerary') or contains(@text, 'Create New Itinerary')]"
    )
    BTN_CREATE_ALT = (AppiumBy.XPATH,
        "//*[contains(@content-desc, 'create') and contains(@content-desc, 'itinerary')]"
    )

    # Itinerary Tab (bottom nav)
    TAB_ITINERARY = (AppiumBy.ACCESSIBILITY_ID, "Itinerary")
    TAB_ITINERARY_XPATH = (AppiumBy.XPATH, "//*[contains(@content-desc, 'Itinerary')]")

    # Form fields
    INPUT_TRIP_NAME = (AppiumBy.XPATH, "//android.widget.EditText[1]")
    INPUT_DESTINATION = (AppiumBy.XPATH, "//android.widget.EditText[2]")
    INPUT_START_DATE = (AppiumBy.XPATH,
        "//*[contains(@content-desc, 'Start') or contains(@text, 'Start')]"
    )
    INPUT_END_DATE = (AppiumBy.XPATH,
        "//*[contains(@content-desc, 'End') or contains(@text, 'End')]"
    )

    # Buttons
    BTN_SUBMIT = (AppiumBy.XPATH,
        "//*[contains(@content-desc, 'Create') or contains(@text, 'Create') "
        "or contains(@content-desc, 'Save') or contains(@text, 'Save') "
        "or contains(@content-desc, 'Submit') or contains(@text, 'Submit')]"
    )
    BTN_CANCEL = (AppiumBy.XPATH,
        "//*[contains(@content-desc, 'Cancel') or contains(@text, 'Cancel')]"
    )
    BTN_DELETE = (AppiumBy.XPATH,
        "//*[contains(@content-desc, 'Delete') or contains(@text, 'Delete')]"
    )

    # Error / Validation messages
    ERROR_MSG = (AppiumBy.XPATH,
        "//*[contains(@content-desc, 'required') or contains(@text, 'required') "
        "or contains(@content-desc, 'invalid') or contains(@text, 'invalid') "
        "or contains(@content-desc, 'error') or contains(@text, 'error') "
        "or contains(@content-desc, 'fill') or contains(@text, 'fill')]"
    )

    # Itinerary list items
    ITINERARY_LIST_ITEM = (AppiumBy.XPATH,
        "//*[contains(@content-desc, 'itinerary') or contains(@content-desc, 'trip')]"
    )

    # ══════════════════════════════════════════════
    # ACTIONS
    # ══════════════════════════════════════════════

    def navigate_to_itinerary_tab(self):
        """Navigate to Itinerary tab."""
        for loc in [self.TAB_ITINERARY, self.TAB_ITINERARY_XPATH]:
            if self.is_element_present(loc, timeout=5):
                self.driver.find_element(*loc).click()
                time.sleep(3)
                logger.info("📋 Navigated to Itinerary tab")
                return True
        return False

    def tap_create_new_itinerary(self):
        """Tap Create New Itinerary button from home screen."""
        # First scroll down to find it
        for _ in range(3):
            for loc in [self.BTN_CREATE_ITINERARY, self.BTN_CREATE_ALT]:
                if self.is_element_present(loc, timeout=3):
                    self.driver.find_element(*loc).click()
                    time.sleep(3)
                    logger.info("➕ Create New Itinerary tapped")
                    return True
            self._swipe_up()
            time.sleep(1)
        logger.warning("⚠ Create New Itinerary button not found")
        return False

    def fill_trip_name(self, name: str):
        """Fill in trip name."""
        if self.is_element_present(self.INPUT_TRIP_NAME, timeout=5):
            el = self.driver.find_element(*self.INPUT_TRIP_NAME)
            el.click()
            time.sleep(0.3)
            el.clear()
            el.send_keys(name)
            self.hide_keyboard()
            logger.info(f"✏️ Trip name: {name}")

    def fill_destination(self, destination: str):
        """Fill in destination."""
        if self.is_element_present(self.INPUT_DESTINATION, timeout=5):
            el = self.driver.find_element(*self.INPUT_DESTINATION)
            el.click()
            time.sleep(0.3)
            el.clear()
            el.send_keys(destination)
            self.hide_keyboard()
            logger.info(f"📍 Destination: {destination}")

    def tap_start_date(self):
        """Tap start date field."""
        if self.is_element_present(self.INPUT_START_DATE, timeout=5):
            self.driver.find_element(*self.INPUT_START_DATE).click()
            time.sleep(2)
            logger.info("📅 Start date picker opened")

    def tap_end_date(self):
        """Tap end date field."""
        if self.is_element_present(self.INPUT_END_DATE, timeout=5):
            self.driver.find_element(*self.INPUT_END_DATE).click()
            time.sleep(2)
            logger.info("📅 End date picker opened")

    def tap_submit(self):
        """Tap the submit/create button."""
        if self.is_element_present(self.BTN_SUBMIT, timeout=5):
            self.driver.find_element(*self.BTN_SUBMIT).click()
            time.sleep(3)
            logger.info("✅ Submit button tapped")
            return True
        return False

    def is_error_displayed(self) -> bool:
        """Check if validation error is shown."""
        return self.is_element_present(self.ERROR_MSG, timeout=3)

    def get_error_message(self) -> str:
        """Get validation error text."""
        if self.is_element_present(self.ERROR_MSG, timeout=3):
            el = self.driver.find_element(*self.ERROR_MSG)
            return el.text or el.get_attribute("content-desc") or ""
        return ""
