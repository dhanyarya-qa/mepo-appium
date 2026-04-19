"""
Open Trip Page Object
=====================
Locators and actions for the Open Trip discovery feature.
Handles trip listing, banners, Custom Your Trip, and itinerary references.
"""

import logging
import time
from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class OpenTripPage(BasePage):
    """Page Object for the Open Trip feature."""

    # ══════════════════════════════════════════════
    # LOCATORS
    # ══════════════════════════════════════════════

    # Navigation
    TAB_OPEN_TRIP = (AppiumBy.ACCESSIBILITY_ID, "Open Trip")
    TAB_OPEN_TRIP_XPATH = (AppiumBy.XPATH, "//*[contains(@content-desc, 'Open Trip')]")

    # Page header
    HEADER = (AppiumBy.XPATH,
        "//*[contains(@content-desc, 'Open Trip') or contains(@text, 'Open Trip')]"
    )

    # Trip listing cards
    TRIP_CARDS = (AppiumBy.XPATH,
        "//*[contains(@content-desc, 'Trip') or contains(@content-desc, 'Pulau')]"
    )

    # Banners / carousel
    BANNER_IMAGES = (AppiumBy.XPATH, "//android.widget.ImageView")

    # Custom Your Trip
    BTN_CUSTOM_TRIP = (AppiumBy.XPATH,
        "//*[contains(@content-desc, 'Custom') or contains(@text, 'Custom')]"
    )

    # Itinerary references section
    SECTION_ITINERARY_REF = (AppiumBy.XPATH,
        "//*[contains(@content-desc, 'itinerary') or contains(@text, 'itinerary')]"
    )

    # See All button
    BTN_SEE_ALL = (AppiumBy.XPATH,
        "//*[contains(@content-desc, 'See all') or contains(@text, 'See all') "
        "or contains(@content-desc, 'See All') or contains(@text, 'See All')]"
    )

    # ══════════════════════════════════════════════
    # ACTIONS
    # ══════════════════════════════════════════════

    def navigate_to_open_trip(self):
        """Navigate to Open Trip via tab."""
        for loc in [self.TAB_OPEN_TRIP, self.TAB_OPEN_TRIP_XPATH]:
            if self.is_element_present(loc, timeout=5):
                self.driver.find_element(*loc).click()
                time.sleep(3)
                logger.info("🧭 Navigated to Open Trip")
                return True
        return False

    def is_open_trip_displayed(self) -> bool:
        """Check if Open Trip page is displayed."""
        return self.driver.current_package == "com.mepo"

    def wait_for_page_loaded(self, timeout=10):
        """Wait for Open Trip page to load."""
        time.sleep(3)
        self._capture_screenshot("open_trip_loaded")
        return self.driver.current_package == "com.mepo"

    def get_all_banners(self):
        """Get all visible banner/image elements."""
        try:
            return self.driver.find_elements(*self.BANNER_IMAGES)
        except Exception:
            return []

    def click_banner_at_index(self, index: int) -> bool:
        """Click a specific banner by index."""
        banners = self.get_all_banners()
        if index < len(banners):
            try:
                banners[index].click()
                time.sleep(3)
                logger.info(f"🖼️ Banner #{index} clicked")
                return True
            except Exception as e:
                logger.warning(f"⚠ Banner #{index} click failed: {e}")
        return False

    def click_all_banners_and_return(self):
        """Click all banners, check if they redirect, and return to app."""
        banners = self.get_all_banners()
        results = []

        for i, banner in enumerate(banners):
            try:
                banner.click()
                time.sleep(3)

                current_pkg = self.driver.current_package
                is_external = current_pkg != "com.mepo"

                if is_external:
                    logger.info(f"🌐 Banner #{i} → external ({current_pkg})")
                    self.driver.activate_app("com.mepo")
                    time.sleep(3)
                else:
                    logger.info(f"📱 Banner #{i} → in-app navigation")
                    self.driver.back()
                    time.sleep(2)

                results.append({
                    "index": i,
                    "external": is_external,
                    "status": "ok"
                })
            except Exception as e:
                logger.warning(f"⚠ Banner #{i} error: {e}")
                results.append({
                    "index": i,
                    "external": False,
                    "status": f"error: {e}"
                })

        return results

    def scroll_to_custom_trip(self) -> bool:
        """Scroll down to find Custom Your Trip section."""
        for _ in range(8):
            if self.is_element_present(self.BTN_CUSTOM_TRIP, timeout=2):
                logger.info("🎯 Found 'Custom Your Trip'")
                return True
            self._swipe_up()
            time.sleep(1)
        logger.warning("⚠ Custom Your Trip not found after scrolling")
        return False

    def click_custom_trip(self) -> bool:
        """Click Custom Your Trip button."""
        if self.is_element_present(self.BTN_CUSTOM_TRIP, timeout=5):
            self.driver.find_element(*self.BTN_CUSTOM_TRIP).click()
            time.sleep(3)
            logger.info("✅ Custom Your Trip clicked")
            return True
        return False

    def scroll_to_itinerary_references(self) -> bool:
        """Scroll to itinerary reference section at bottom."""
        for _ in range(10):
            if self.is_element_present(self.SECTION_ITINERARY_REF, timeout=2):
                logger.info("📋 Found itinerary references section")
                return True
            self._swipe_up()
            time.sleep(1)
        return False

    def return_to_app_if_external(self):
        """Check if we're outside the app and return if so."""
        if self.driver.current_package != "com.mepo":
            logger.info(f"🔄 Returning to app from: {self.driver.current_package}")
            self.driver.activate_app("com.mepo")
            time.sleep(3)
            return True
        return False
