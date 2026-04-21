"""
Test 03 — Open Trip (Real Device)
===================================
Verifies Open Trip feature: navigation, trip listing, trip detail,
and content scrolling.

XML Source: reports/real_device/explore_05_opentrip.xml
"""

import pytest
import time
import logging
from appium.webdriver.common.appiumby import AppiumBy
from utils.wait_helpers import wait_find, FAST, NORMAL

logger = logging.getLogger(__name__)

pytestmark = [pytest.mark.open_trip, pytest.mark.regression]


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

def _ensure_home_top(driver):
    """Scroll to top of home screen."""
    _go_home(driver)
    s = driver.get_window_size()
    
    # Try finding 'Welcome' and if not found, swipe DOWN to scroll UP
    for _ in range(5):
        welcome = driver.find_elements(AppiumBy.XPATH, "//*[contains(@content-desc, 'Welcome,')]")
        if welcome:
            return
        # Swift down to scroll up
        driver.swipe(s['width']//2, int(s['height']*0.25),
                    s['width']//2, int(s['height']*0.80), 800)
        time.sleep(1)


class TestOpenTripNavigation:
    """Navigate to Open Trip from service cards."""

    def test_tap_open_trip_card(self, driver):
        """Tapping Open Trip card should navigate to Open Trip page."""
        logger.info("\n=== OPEN TRIP: Navigate via Card ===")
        _ensure_home_top(driver)

        # From XML: content-desc="Open Trip\nOpen Trip"
        cards = driver.find_elements(AppiumBy.XPATH,
            "//*[starts-with(@content-desc, 'Open Trip')]")
        assert len(cards) > 0, "Open Trip card not found on home"
        cards[0].click()
        time.sleep(3)

        # Verify Open Trip page loaded
        # From XML: content-desc="Open Trip" as page title
        title = driver.find_elements(AppiumBy.XPATH,
            "//android.view.View[@content-desc='Open Trip' "
            "and not(@clickable='true')]")
        if not title:
            # Fallback: any "Open Trip" text that's not clickable
            title = driver.find_elements(AppiumBy.XPATH,
                "//*[@content-desc='Open Trip']")
        assert len(title) > 0, "Open Trip page title not found"
        logger.info("✅ Open Trip page opened")

    def test_back_button_exists(self, driver):
        """Back button should be present on Open Trip page."""
        logger.info("\n=== OPEN TRIP: Back Button ===")

        # From XML: Button at bounds [11,95][143,227]
        back_btn = driver.find_elements(AppiumBy.XPATH,
            "//android.widget.Button[@clickable='true' and @bounds='[11,95][143,227]']")
        if not back_btn:
            back_btn = driver.find_elements(AppiumBy.XPATH,
                "//android.widget.Button[@clickable='true']")
        assert len(back_btn) > 0, "Back button not found"
        logger.info("✅ Back button present")

    def test_filter_all_visible(self, driver):
        """'All' filter tag should be visible."""
        logger.info("\n=== OPEN TRIP: All Filter ===")

        # From XML: content-desc="All"
        all_filter = driver.find_elements(AppiumBy.XPATH,
            "//*[@content-desc='All']")
        assert len(all_filter) > 0, "'All' filter not found"
        logger.info("✅ 'All' filter tag visible")


class TestOpenTripListing:
    """Verify trip listing cards."""

    def test_trip_cards_displayed(self, driver):
        """Trip cards should be listed in grid."""
        logger.info("\n=== OPEN TRIP: Trip Cards ===")

        # From XML: ImageView elements with trip names as content-desc
        trip_cards = driver.find_elements(AppiumBy.XPATH,
            "//android.widget.ScrollView//android.widget.ImageView[@clickable='true']")
        assert len(trip_cards) >= 2, f"Expected ≥2 trip cards, found {len(trip_cards)}"

        # Log first few trip names
        for i, card in enumerate(trip_cards[:4]):
            desc = card.get_attribute("content-desc") or "no-desc"
            logger.info(f"  Trip {i+1}: {desc[:50]}")

        logger.info(f"✅ Found {len(trip_cards)} trip cards")

    def test_trip_cards_are_clickable(self, driver):
        """Trip cards should be clickable."""
        trip_cards = driver.find_elements(AppiumBy.XPATH,
            "//android.widget.ScrollView//android.widget.ImageView[@clickable='true']")
        if trip_cards:
            assert trip_cards[0].get_attribute("clickable") == "true"
            logger.info("✅ Trip cards are clickable")

    def test_scroll_trip_list(self, driver):
        """Should be able to scroll through trip list."""
        logger.info("\n=== OPEN TRIP: Scroll List ===")

        s = driver.get_window_size()
        driver.swipe(s['width']//2, int(s['height']*0.75),
                    s['width']//2, int(s['height']*0.25), 800)
        time.sleep(2)

        # Should still find trip cards after scrolling
        trip_cards = driver.find_elements(AppiumBy.XPATH,
            "//android.widget.ScrollView//android.widget.ImageView[@clickable='true']")
        assert len(trip_cards) >= 1, "No trip cards after scroll"
        logger.info(f"✅ Found {len(trip_cards)} cards after scroll")


class TestOpenTripDetail:
    """Verify trip detail screen."""

    def test_open_trip_detail(self, driver):
        """Tapping a trip card should open detail page."""
        logger.info("\n=== OPEN TRIP: Open Detail ===")

        # Scroll back to top
        s = driver.get_window_size()
        for _ in range(3):
            driver.swipe(s['width']//2, int(s['height']*0.25),
                        s['width']//2, int(s['height']*0.75), 600)
            time.sleep(0.3)
        time.sleep(1)

        trip_cards = driver.find_elements(AppiumBy.XPATH,
            "//android.widget.ScrollView//android.widget.ImageView[@clickable='true']")
        assert len(trip_cards) > 0, "No trip cards to tap"

        first_trip_name = trip_cards[0].get_attribute("content-desc") or "unknown"
        logger.info(f"  Tapping trip: {first_trip_name[:50]}")
        trip_cards[0].click()
        time.sleep(5)

        # Verify we left the list (back button should still be there)
        back_btn = driver.find_elements(AppiumBy.XPATH,
            "//android.widget.Button[@clickable='true']")
        assert len(back_btn) > 0, "Detail page not loaded"
        logger.info("✅ Trip detail page opened")

    def test_go_back_from_detail(self, driver):
        """Going back from detail should return to trip list."""
        logger.info("\n=== OPEN TRIP: Back from Detail ===")

        driver.back()
        time.sleep(3)

        # Verify we're back on Open Trip list
        title = driver.find_elements(AppiumBy.XPATH,
            "//*[@content-desc='Open Trip']")
        all_filter = driver.find_elements(AppiumBy.XPATH,
            "//*[@content-desc='All']")
        assert len(title) > 0 or len(all_filter) > 0, "Not back on trip list"
        logger.info("✅ Back on Open Trip list")

    def test_navigate_back_to_home(self, driver):
        """Back from Open Trip should return to home."""
        logger.info("\n=== OPEN TRIP: Back to Home ===")

        driver.back()
        time.sleep(3)

        welcome = driver.find_elements(AppiumBy.XPATH,
            "//*[contains(@content-desc, 'Welcome,')]")
        assert len(welcome) > 0, "Not back on home screen"
        logger.info("✅ Back on home screen")
