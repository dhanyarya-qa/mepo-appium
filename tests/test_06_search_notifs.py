"""
Test 06 — Search & Notifications (Real Device)
================================================
Verifies the Explore Itinerary (search) and Notification screens
accessed from home screen header icons.

XML Source: reports/real_device/search_01_after_tap.xml
            reports/real_device/notif_01_after_tap.xml
"""

import pytest
import time
import logging
from appium.webdriver.common.appiumby import AppiumBy

logger = logging.getLogger(__name__)

pytestmark = [pytest.mark.search, pytest.mark.regression]


def _go_home(driver):
    """Navigate back to home safely via Bottom Nav tab."""
    for _ in range(5):
        home_tab = driver.find_elements(AppiumBy.XPATH,
            "//*[contains(@content-desc, 'Home\nTab 1 of 4')]")
        if home_tab:
            home_tab[-1].click()
            time.sleep(2)
            return True
        try:
            driver.press_keycode(4)
        except Exception:
            pass
        time.sleep(2)
    return False


# ══════════════════════════════════════════════
# SEARCH / EXPLORE ITINERARY
# ══════════════════════════════════════════════

class TestSearchExplore:
    """Verify the Explore Itinerary (search) screen."""

    def test_navigate_to_search(self, driver):
        """Tapping search icon should open Explore Itinerary page."""
        logger.info("\n=== SEARCH: Navigate ===")
        _go_home(driver)
        time.sleep(1)

        # Use semantic locator for search icon (Explore/Search tab)
        search_icon = driver.find_elements(AppiumBy.XPATH,
            "//*[contains(@content-desc, 'Explore\nTab 2 of 4')] | //*[contains(@content-desc, 'Search\nTab')]")
        if search_icon:
            search_icon[-1].click()
        else:
            # Fallback to coordinate (search icon top-right area)
            driver.tap([(747, 245)], 500)
        time.sleep(3)

        # Verify: page title "Explore Itinerary"
        title = driver.find_elements(AppiumBy.XPATH,
            "//*[@content-desc='Explore Itinerary']")
        assert len(title) > 0, "'Explore Itinerary' title not found"
        logger.info("✅ Explore Itinerary page opened")

    def test_search_bar_exists(self, driver):
        """Search bar 'Search any Itinerary ...' should be visible."""
        logger.info("\n=== SEARCH: Search Bar ===")

        # From XML: Button with content-desc="Search any Itinerary ..."
        search_bar = driver.find_elements(AppiumBy.XPATH,
            "//*[contains(@content-desc, 'Search any Itinerary')]")
        assert len(search_bar) > 0, "Search bar not found"
        assert search_bar[0].get_attribute("clickable") == "true"
        logger.info("✅ Search bar visible & clickable")

    def test_explore_popular_section(self, driver):
        """'Explore Popular Itinerary' section should be visible."""
        logger.info("\n=== SEARCH: Popular Section ===")

        # From XML: content-desc="Explore Popular Itinerary"
        section = driver.find_elements(AppiumBy.XPATH,
            "//*[@content-desc='Explore Popular Itinerary']")
        assert len(section) > 0, "'Explore Popular Itinerary' not found"
        logger.info("✅ 'Explore Popular Itinerary' section visible")

    def test_city_cards_displayed(self, driver):
        """Popular city cards should be displayed (Depok, Tebet, etc.)."""
        logger.info("\n=== SEARCH: City Cards ===")

        # From XML: clickable Views with city names
        cities = driver.find_elements(AppiumBy.XPATH,
            "//*[@content-desc='Depok' or @content-desc='Tebet' "
            "or @content-desc='Sulawesi' or @content-desc='Surabaya' "
            "or @content-desc='Makassar' or @content-desc='Jakarta']")
        assert len(cities) >= 3, f"Expected ≥3 city cards, found {len(cities)}"

        city_names = [c.get_attribute("content-desc") for c in cities]
        logger.info(f"✅ Found {len(cities)} city cards: {city_names}")

    def test_recommended_section(self, driver):
        """'Recommended Itinerary' section should be visible on search page."""
        logger.info("\n=== SEARCH: Recommended Section ===")

        rec = driver.find_elements(AppiumBy.XPATH,
            "//*[@content-desc='Recommended Itinerary']")
        assert len(rec) > 0, "'Recommended Itinerary' not found"
        logger.info("✅ 'Recommended Itinerary' section visible")

    def test_itinerary_cards_on_search(self, driver):
        """Recommended itinerary cards should be displayed."""
        logger.info("\n=== SEARCH: Itinerary Cards ===")

        # From XML: ImageView cards with content-desc like "danip\ntitle\ncity"
        cards = driver.find_elements(AppiumBy.XPATH,
            "//android.widget.ScrollView//android.widget.ImageView[@clickable='true']")
        assert len(cards) >= 1, "No itinerary cards found"
        logger.info(f"✅ Found {len(cards)} itinerary cards")

    def test_back_from_search(self, driver):
        """Going back should return to home."""
        logger.info("\n=== SEARCH: Back ===")

        driver.back()
        time.sleep(3)

        welcome = driver.find_elements(AppiumBy.XPATH,
            "//*[contains(@content-desc, 'Welcome,')]")
        assert len(welcome) > 0, "Not back on home"
        logger.info("✅ Back on home from search")


# ══════════════════════════════════════════════
# NOTIFICATIONS
# ══════════════════════════════════════════════

class TestNotifications:
    """Verify the Notification screen."""

    def test_navigate_to_notifications(self, driver):
        """Tapping bell icon should open Notification page."""
        logger.info("\n=== NOTIFICATIONS: Navigate ===")
        _go_home(driver)
        time.sleep(1)

        # Use semantic locator for notification icon
        notif_icon = driver.find_elements(AppiumBy.XPATH,
            "//*[contains(@content-desc, 'Notification') and @clickable='true']")
        if notif_icon:
            notif_icon[0].click()
        else:
            # Fallback to coordinate (notification bell top-right)
            driver.tap([(863, 245)], 500)
        time.sleep(3)

        # Verify: page title "Notification"
        title = driver.find_elements(AppiumBy.XPATH,
            "//*[@content-desc='Notification']")
        assert len(title) > 0, "'Notification' title not found"
        logger.info("✅ Notification page opened")

    def test_empty_state_message(self, driver):
        """Empty state message should be displayed when no notifications."""
        logger.info("\n=== NOTIFICATIONS: Empty State ===")

        # From XML: content-desc="There is no Available Notification yet"
        empty = driver.find_elements(AppiumBy.XPATH,
            "//*[contains(@content-desc, 'no Available Notification')]")
        assert len(empty) > 0, "Empty state message not found"
        logger.info("✅ Empty state: 'There is no Available Notification yet'")

    def test_back_button_exists(self, driver):
        """Back button should be present."""
        # From XML: Button at [11,95][143,227]
        back_btn = driver.find_elements(AppiumBy.XPATH,
            "//android.widget.Button[@clickable='true']")
        assert len(back_btn) > 0, "Back button not found"
        logger.info("✅ Back button present")

    def test_back_from_notifications(self, driver):
        """Going back should return to home."""
        logger.info("\n=== NOTIFICATIONS: Back ===")

        driver.back()
        time.sleep(3)

        welcome = driver.find_elements(AppiumBy.XPATH,
            "//*[contains(@content-desc, 'Welcome,')]")
        assert len(welcome) > 0, "Not back on home"
        logger.info("✅ Back on home from notifications")
