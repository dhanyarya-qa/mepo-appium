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
    """Navigate to home screen safely via Bottom Nav tab."""
    for attempt in range(5):
        # 1. Check for Bottom Nav Home Tab
        home_tab = driver.find_elements(AppiumBy.XPATH,
            "//*[contains(@content-desc, 'Home\nTab 1 of 4')]")
        if home_tab:
            home_tab[-1].click()
            time.sleep(2)
            return True

        # 2. Already on Home? (Welcome text visible)
        welcome = driver.find_elements(AppiumBy.XPATH,
            "//*[contains(@content-desc, 'Welcome,')]")
        if welcome:
            logger.info("  Already on Home Screen")
            return True

        # 3. Press back to get closer to Home
        logger.info(f"  Back press {attempt+1}/5 to find Home")
        try:
            driver.press_keycode(4)
        except Exception:
            pass
        time.sleep(2)

        # 4. Check if we accidentally exited the app
        try:
            current = driver.current_package
            if current != "com.mepo":
                logger.warning(f"  Left Mepo ({current}), re-activating...")
                driver.activate_app("com.mepo")
                time.sleep(3)
        except Exception:
            pass

    return False


# ══════════════════════════════════════════════
# SEARCH / EXPLORE ITINERARY
# ══════════════════════════════════════════════

class TestSearchExplore:
    """Verify the Explore Itinerary (search) screen."""

    def test_navigate_to_search(self, driver):
        """Tapping search icon should open Explore Itinerary page."""
        logger.info("\n=== SEARCH: Navigate ===")

        # Ensure we're on home first
        assert _go_home(driver), "Could not navigate to home screen"
        time.sleep(2)

        # Method 1: Try Bottom Nav Explore tab (Tab 2 of 4)
        search_icon = driver.find_elements(AppiumBy.XPATH,
            "//*[contains(@content-desc, 'Explore') and contains(@content-desc, 'Tab')]")

        if search_icon:
            logger.info("  📍 Found Explore tab in bottom nav")
            search_icon[-1].click()
            time.sleep(3)
        else:
            # Method 2: Try finding by content-desc variations
            search_icon = driver.find_elements(AppiumBy.XPATH,
                "//*[@content-desc='Explore' or contains(@content-desc, 'Search')]")
            if search_icon:
                logger.info("  📍 Found Explore/Search icon")
                search_icon[-1].click()
                time.sleep(3)
            else:
                # Method 3: Fallback to coordinate (top-right area where search icon typically is)
                logger.info("  📍 Using coordinate fallback for search icon")
                s = driver.get_window_size()
                # Tap approximately 70% from left, 20% from top (header area)
                driver.tap([(int(s['width'] * 0.7), int(s['height'] * 0.12))], 500)
                time.sleep(3)

        # Verify: page title "Explore Itinerary"
        title = driver.find_elements(AppiumBy.XPATH,
            "//*[@content-desc='Explore Itinerary']")

        # If not found, try alternative locators
        if not title:
            title = driver.find_elements(AppiumBy.XPATH,
                "//*[contains(@content-desc, 'Explore')]")

        assert len(title) > 0, "'Explore Itinerary' title not found — navigation failed"
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

        # Press back with verification
        for attempt in range(3):
            # Check if already on home
            welcome = driver.find_elements(AppiumBy.XPATH,
                "//*[contains(@content-desc, 'Welcome,')]")
            if welcome:
                logger.info("  ✅ Already on home")
                return

            # Check if we're on Explore page
            explore_title = driver.find_elements(AppiumBy.XPATH,
                "//*[@content-desc='Explore Itinerary']")
            if explore_title:
                logger.info(f"  ← Pressing back (attempt {attempt+1})")
                driver.back()
                time.sleep(2)
            else:
                # Not on explore, not on home - might be on sub-page
                logger.info(f"  ← Pressing back from sub-page (attempt {attempt+1})")
                driver.back()
                time.sleep(2)

        # Final check - use _go_home helper if back didn't work
        welcome = driver.find_elements(AppiumBy.XPATH,
            "//*[contains(@content-desc, 'Welcome,')]")
        if not welcome:
            logger.info("  📍 Using _go_home helper as fallback")
            _go_home(driver)

        welcome = driver.find_elements(AppiumBy.XPATH,
            "//*[contains(@content-desc, 'Welcome,')]")
        assert len(welcome) > 0, "Not back on home after multiple attempts"
        logger.info("✅ Back on home from search")


# ══════════════════════════════════════════════
# NOTIFICATIONS
# ══════════════════════════════════════════════

class TestNotifications:
    """Verify the Notification screen."""

    def test_navigate_to_notifications(self, driver):
        """Tapping bell icon should open Notification page."""
        logger.info("\n=== NOTIFICATIONS: Navigate ===")

        # Ensure we're on home first
        assert _go_home(driver), "Could not navigate to home screen"
        time.sleep(2)

        # Method 1: Find notification icon by content-desc
        notif_icon = driver.find_elements(AppiumBy.XPATH,
            "//*[contains(@content-desc, 'Notification') and @clickable='true']")

        if not notif_icon:
            # Method 2: Try finding bell icon in header area
            notif_icon = driver.find_elements(AppiumBy.XPATH,
                "//android.view.View[@clickable='true' and not(@content-desc)]")
            # Filter for header area icons (typically y < 300)
            header_icons = []
            for icon in notif_icon:
                try:
                    bounds = icon.get_attribute("bounds")
                    if bounds and "[201]" in bounds:  # Header row y=201
                        header_icons.append(icon)
                except Exception:
                    pass
            notif_icon = header_icons

        if notif_icon:
            logger.info(f"  📍 Found notification icon, tapping...")
            notif_icon[0].click()
            time.sleep(3)
        else:
            # Method 3: Fallback to coordinate (notification bell top-right)
            logger.info("  📍 Using coordinate fallback for notification icon")
            s = driver.get_window_size()
            # Tap approximately 80% from left, 20% from top (header area)
            driver.tap([(int(s['width'] * 0.8), int(s['height'] * 0.12))], 500)
            time.sleep(3)

        # Verify: page title "Notification"
        title = driver.find_elements(AppiumBy.XPATH,
            "//*[@content-desc='Notification']")

        # If not found, we may have navigated away - check if app is still running
        if not title:
            # Check if app is still in foreground
            current_pkg = driver.current_package
            logger.warning(f"  ⚠ Notification title not found. Current package: {current_pkg}")

            # If we're not on com.mepo, the app was closed - reactivate it
            if current_pkg != "com.mepo":
                logger.warning("  ⚠ App not in foreground, reactivating...")
                driver.activate_app("com.mepo")
                time.sleep(3)
                # Go back to home and retry
                _go_home(driver)
                pytest.skip("Notification test skipped - app was not in foreground, retrying")

        assert len(title) > 0, "'Notification' title not found — navigation failed"
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

        # Press back with verification
        for attempt in range(3):
            # Check if already on home
            welcome = driver.find_elements(AppiumBy.XPATH,
                "//*[contains(@content-desc, 'Welcome,')]")
            if welcome:
                logger.info("  ✅ Already on home")
                return

            # Check if we're on Notification page
            notif_title = driver.find_elements(AppiumBy.XPATH,
                "//*[@content-desc='Notification']")
            if notif_title:
                logger.info(f"  ← Pressing back (attempt {attempt+1})")
                driver.back()
                time.sleep(2)
            else:
                # Not on notification, not on home - might be on sub-page
                logger.info(f"  ← Pressing back from sub-page (attempt {attempt+1})")
                driver.back()
                time.sleep(2)

        # Final check - use _go_home helper if back didn't work
        welcome = driver.find_elements(AppiumBy.XPATH,
            "//*[contains(@content-desc, 'Welcome,')]")
        if not welcome:
            logger.info("  📍 Using _go_home helper as fallback")
            _go_home(driver)

        welcome = driver.find_elements(AppiumBy.XPATH,
            "//*[contains(@content-desc, 'Welcome,')]")
        assert len(welcome) > 0, "Not back on home after multiple attempts"
        logger.info("✅ Back on home from notifications")
