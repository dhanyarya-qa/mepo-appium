"""
Home Page Object
================
Locators and actions for the Mepo Travel app's main Home screen.
Acts as the navigation hub to all major features.

Based on actual UI: "Welcome, danip", Open Trip, Flight, Train, Hotel, etc.
"""

import logging
from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class HomePage(BasePage):
    """Page Object for the Mepo Travel Home / Dashboard screen."""

    # ──────────────────────────────────────────────
    # Locators — from actual app screenshot
    # ──────────────────────────────────────────────

    # Greeting / Header
    GREETING_TEXT = (AppiumBy.XPATH, "//*[contains(@text, 'Welcome,')]")
    GREETING_DESC = (AppiumBy.XPATH, "//*[contains(@content-desc, 'Welcome,')]")
    WHERE_TO_GO = (AppiumBy.XPATH, "//*[contains(@text, 'Where do you want to go')]")

    # Navigation Tabs / Menu Items
    TAB_HOME = (AppiumBy.ACCESSIBILITY_ID, "Home")
    TAB_OPEN_TRIP = (AppiumBy.ACCESSIBILITY_ID, "Open Trip")
    TAB_ITINERARY = (AppiumBy.ACCESSIBILITY_ID, "Itinerary")
    TAB_PROFILE = (AppiumBy.ACCESSIBILITY_ID, "Profile")

    # Service Menu Cards
    CARD_OPEN_TRIP = (AppiumBy.XPATH, "//*[@text='Open Trip']")
    CARD_FLIGHT = (AppiumBy.XPATH, "//*[@text='Flight']")
    CARD_TRAIN = (AppiumBy.XPATH, "//*[@text='Train']")
    CARD_BUS = (AppiumBy.XPATH, "//*[@text='Bus']")
    CARD_HOTEL = (AppiumBy.XPATH, "//*[@text='Hotel']")
    CARD_PROMO = (AppiumBy.XPATH, "//*[@text='Promo Deals']")
    BTN_SHOW_ALL = (AppiumBy.XPATH, "//*[contains(@text, 'Show All')]")

    # Create Itinerary CTA
    BTN_CREATE_ITINERARY = (AppiumBy.XPATH,
        "//*[contains(@text, 'Create New Itinerary')]"
    )
    BTN_CREATE_ITINERARY_DESC = (AppiumBy.XPATH,
        "//*[contains(@content-desc, 'Create New Itinerary')]"
    )

    # ──────────────────────────────────────────────
    # Actions
    # ──────────────────────────────────────────────

    def wait_for_home_loaded(self, timeout: int = 15):
        """Wait until the home screen is fully loaded."""
        self.dismiss_all_dialogs()
        indicators = [
            self.GREETING_TEXT, self.GREETING_DESC,
            self.CARD_OPEN_TRIP, self.TAB_OPEN_TRIP,
        ]
        for ind in indicators:
            if self.is_element_present(ind, timeout=timeout):
                logger.info(f"🏠 Home screen loaded — detected: {ind}")
                return True
        logger.warning("⚠ Home screen could not be confirmed")
        return False

    def navigate_to_open_trip(self):
        """Tap on the Open Trip tab or card."""
        if self.is_element_present(self.TAB_OPEN_TRIP, timeout=3):
            self.tap(self.TAB_OPEN_TRIP)
        elif self.is_element_present(self.CARD_OPEN_TRIP, timeout=3):
            self.tap(self.CARD_OPEN_TRIP)
        logger.info("🧭 Navigating to Open Trip")

    def navigate_to_itinerary(self):
        """Tap on the Itinerary tab."""
        self.tap(self.TAB_ITINERARY)
        logger.info("📋 Navigating to Itinerary tab")

    def navigate_to_profile(self):
        """Tap on the Profile tab."""
        self.tap(self.TAB_PROFILE)
        logger.info("👤 Navigating to Profile tab")

    def is_home_displayed(self) -> bool:
        """Check if the home screen is currently displayed."""
        return (
            self.is_element_present(self.GREETING_TEXT, timeout=5)
            or self.is_element_present(self.GREETING_DESC, timeout=3)
            or self.is_element_present(self.CARD_OPEN_TRIP, timeout=3)
        )

    def get_greeting_text(self) -> str:
        """Return the greeting text shown on the home screen."""
        for loc in [self.GREETING_TEXT, self.GREETING_DESC]:
            if self.is_element_present(loc, timeout=3):
                try:
                    el = self.driver.find_element(*loc)
                    return el.text or el.get_attribute("content-desc") or ""
                except Exception:
                    continue
        return ""
