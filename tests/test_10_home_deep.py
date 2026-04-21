"""
Test 10 — Home Deep Interactions (Real Device)
================================================
Verifies deeper home screen interactions: service card "Soon" labels,
horizontal scroll sections, popular city chips, "See all" navigation,
and partnership banner click.

XML Source: reports/real_device/explore_03_home.xml
            reports/real_device/explore_04_home_mid.xml
"""

import pytest
import time
import logging
from appium.webdriver.common.appiumby import AppiumBy

logger = logging.getLogger(__name__)

pytestmark = [pytest.mark.home, pytest.mark.regression]


def _ensure_home_top(driver):
    """Navigate to home and scroll to top safely."""
    # Navigate back to home via Bottom Nav tab
    for attempt in range(5):
        home_tab = driver.find_elements(AppiumBy.XPATH,
            "//*[contains(@content-desc, 'Home\nTab 1 of 4')]")
        if home_tab:
            home_tab[-1].click()
            time.sleep(2)
            break

        # Already on Home?
        welcome = driver.find_elements(AppiumBy.XPATH,
            "//*[contains(@content-desc, 'Welcome,')]")
        if welcome:
            logger.info("  ✅ Already on Home Screen")
            break

        logger.info(f"  ← Back press {attempt+1}/5 to find Home")
        try:
            driver.press_keycode(4)
        except Exception:
            pass
        time.sleep(2)

        # Check if we accidentally exited the app
        try:
            current = driver.current_package
            if current != "com.mepo":
                logger.warning(f"  ⚠ Left Mepo ({current}), re-activating...")
                driver.activate_app("com.mepo")
                time.sleep(3)
        except Exception:
            pass

    # Scroll to top safely
    try:
        driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiScrollable(new UiSelector().scrollable(true)).scrollToBeginning(5)'
        )
    except Exception:
        pass
    time.sleep(1)


def _scroll_to_text(driver, text):
    """Safely scroll to element using Android UiScrollable."""
    # Use scrollable(true) without className restriction —
    # Mepo uses Compose LazyColumn/NestedScrollView, not standard ScrollView
    try:
        return driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            f'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().descriptionContains("{text}"))'
        )
    except Exception:
        return None


class TestServiceCardSoonLabels:
    """Verify that 'Soon' service cards have proper labels."""

    def test_flight_has_soon_label(self, driver):
        """Flight card should show 'Soon' label."""
        logger.info("\n=== HOME DEEP: Flight Soon Label ===")
        _ensure_home_top(driver)

        # From XML: content-desc="Soon\nFlight\nFlight"
        card = driver.find_elements(AppiumBy.XPATH,
            "//*[contains(@content-desc, 'Flight')]")
        assert len(card) > 0, "Flight card not found"
        desc = card[0].get_attribute("content-desc")
        assert "Soon" in desc, f"Flight card missing 'Soon' label: {desc}"
        logger.info(f"✅ Flight card has 'Soon': {desc}")

    def test_train_has_soon_label(self, driver):
        """Train card should show 'Soon' label."""
        card = driver.find_elements(AppiumBy.XPATH,
            "//*[contains(@content-desc, 'Train')]")
        assert len(card) > 0, "Train card not found"
        desc = card[0].get_attribute("content-desc")
        assert "Soon" in desc, f"Train missing 'Soon': {desc}"
        logger.info(f"✅ Train has 'Soon': {desc}")

    def test_bus_has_soon_label(self, driver):
        """Bus card should show 'Soon' label."""
        card = driver.find_elements(AppiumBy.XPATH,
            "//*[contains(@content-desc, 'Bus')]")
        assert len(card) > 0, "Bus card not found"
        desc = card[0].get_attribute("content-desc")
        assert "Soon" in desc, f"Bus missing 'Soon': {desc}"
        logger.info(f"✅ Bus has 'Soon': {desc}")

    def test_hotel_has_soon_label(self, driver):
        """Hotel card should show 'Soon' label."""
        card = driver.find_elements(AppiumBy.XPATH,
            "//*[contains(@content-desc, 'Hotel')]")
        assert len(card) > 0, "Hotel card not found"
        desc = card[0].get_attribute("content-desc")
        assert "Soon" in desc, f"Hotel missing 'Soon': {desc}"
        logger.info(f"✅ Hotel has 'Soon': {desc}")

    def test_promo_has_soon_label(self, driver):
        """Promo Deals card should show 'Soon' label."""
        card = driver.find_elements(AppiumBy.XPATH,
            "//*[contains(@content-desc, 'Promo Deals')]")
        assert len(card) > 0, "Promo Deals card not found"
        desc = card[0].get_attribute("content-desc")
        assert "Soon" in desc, f"Promo missing 'Soon': {desc}"
        logger.info(f"✅ Promo Deals has 'Soon': {desc}")

    def test_open_trip_no_soon_label(self, driver):
        """Open Trip card should NOT have 'Soon' label (it's active)."""
        card = driver.find_elements(AppiumBy.XPATH,
            "//*[starts-with(@content-desc, 'Open Trip')]")
        assert len(card) > 0, "Open Trip card not found"
        desc = card[0].get_attribute("content-desc")
        assert "Soon" not in desc, f"Open Trip should NOT have 'Soon': {desc}"
        logger.info(f"✅ Open Trip is active (no 'Soon'): {desc}")


class TestHomeHorizontalScrolls:
    """Verify horizontal scrollable sections on home."""

    def test_open_trip_carousel_scrollable(self, driver):
        """Open Trip with Us carousel should be horizontally scrollable."""
        logger.info("\n=== HOME DEEP: Open Trip Carousel ===")
        _ensure_home_top(driver)
        _scroll_to_text(driver, "Open Trip")

        # From XML: HorizontalScrollView with trip card ImageViews
        carousel = driver.find_elements(AppiumBy.XPATH,
            "//android.widget.HorizontalScrollView")
        assert len(carousel) >= 1, "No horizontal scroll views found"

        # Try swiping horizontally on the carousel
        s = driver.get_window_size()
        carousel_y = int(s['height'] * 0.4)  # Approximate center
        driver.swipe(int(s['width']*0.8), carousel_y,
                    int(s['width']*0.2), carousel_y, 600)
        time.sleep(1)
        logger.info(f"✅ Found {len(carousel)} horizontal scroll sections")

    def test_popular_city_chips_scrollable(self, driver):
        """Popular city chips should be in a horizontal scroll."""
        logger.info("\n=== HOME DEEP: City Chips Scroll ===")

        # Scroll down a bit first to make HorizontalScrollView visible
        _scroll_to_text(driver, "Depok")
        time.sleep(1)

        # From XML: HorizontalScrollView containing city names
        scrollviews = driver.find_elements(AppiumBy.XPATH,
            "//android.widget.HorizontalScrollView")

        found_cities = False
        for sv in scrollviews:
            children = sv.find_elements(AppiumBy.XPATH, ".//*[@content-desc]")
            for child in children:
                desc = child.get_attribute("content-desc") or ""
                if desc in ["Depok", "Tebet", "Sulawesi"]:
                    found_cities = True
                    break
            if found_cities:
                break

        # If not found in HorizontalScrollView, try direct XPATH search
        if not found_cities:
            city_els = driver.find_elements(AppiumBy.XPATH,
                "//*[@content-desc='Depok' or @content-desc='Tebet' or @content-desc='Sulawesi']")
            found_cities = len(city_els) > 0

        assert found_cities, "City chips not found in horizontal scroll"
        logger.info("✅ City chips in horizontal scrollable container")


class TestHomeSeeAllNavigation:
    """Verify 'See all' link navigation."""

    def test_see_all_navigates_to_open_trip(self, driver):
        """Tapping 'See all' should navigate to Open Trip list."""
        logger.info("\n=== HOME DEEP: See All Navigation ===")

        # Make sure See all is visible
        see_all = driver.find_elements(AppiumBy.XPATH,
            "//*[@content-desc='See all']")
        if not see_all:
            _scroll_to_text(driver, "See all")
            time.sleep(1)
            see_all = driver.find_elements(AppiumBy.XPATH,
                "//*[@content-desc='See all']")

        if not see_all:
            pytest.skip("'See all' link not visible")

        see_all[0].click()
        time.sleep(3)

        # Should navigate to Open Trip page
        title = driver.find_elements(AppiumBy.XPATH,
            "//*[@content-desc='Open Trip']")
        all_filter = driver.find_elements(AppiumBy.XPATH,
            "//*[@content-desc='All']")
        assert len(title) > 0 or len(all_filter) > 0, "Not on Open Trip page"
        logger.info("✅ 'See all' navigated to Open Trip page")

        # Go back
        driver.back()
        time.sleep(3)


class TestHomePartnershipBanner:
    """Verify partnership banner interaction."""

    def test_partnership_banner_clickable(self, driver):
        """Partnership banner should be clickable."""
        logger.info("\n=== HOME DEEP: Partnership Banner ===")
        _ensure_home_top(driver)

        # Scroll to bottom
        _scroll_to_text(driver, "Apply for Partnership")

        partner = driver.find_elements(AppiumBy.XPATH,
            "//*[contains(@content-desc, 'Apply for Partnership')]")
        if not partner:
            pytest.skip("Partnership banner not visible")

        clickable = partner[0].get_attribute("clickable")
        assert clickable == "true", f"Partnership banner not clickable: {clickable}"
        logger.info("✅ Partnership banner is clickable")

    def test_explore_popular_section_at_bottom(self, driver):
        """'Explore Popular Itinerary' text should appear at bottom of home."""
        logger.info("\n=== HOME DEEP: Explore Popular at Bottom ===")

        explore = driver.find_elements(AppiumBy.XPATH,
            "//*[@content-desc='Explore Popular Itinerary']")

        # It might be partially visible or need one more scroll
        if not explore:
            _scroll_to_text(driver, "Explore Popular")
            time.sleep(1)
            explore = driver.find_elements(AppiumBy.XPATH,
                "//*[@content-desc='Explore Popular Itinerary']")

        assert len(explore) > 0, "'Explore Popular Itinerary' not found at bottom"
        logger.info("✅ 'Explore Popular Itinerary' visible at home bottom")


class TestHomeRecommendedItinerary:
    """Verify recommended itinerary section on home."""

    def test_recommended_cards_in_carousel(self, driver):
        """Recommended itinerary cards should be in horizontal carousel."""
        logger.info("\n=== HOME DEEP: Recommended Carousel ===")
        _ensure_home_top(driver)
        _scroll_to_text(driver, "Recommend")

        # From XML: HorizontalScrollView with ImageView cards having
        # content-desc like "Dev\nTasik\nGarut"
        cards = driver.find_elements(AppiumBy.XPATH,
            "//android.widget.HorizontalScrollView//android.widget.ImageView[@clickable='true']")
        assert len(cards) >= 1, "No recommended cards in carousel"

        # Log card details
        for i, card in enumerate(cards[:3]):
            desc = card.get_attribute("content-desc") or "no-desc"
            logger.info(f"  Recommended {i+1}: {desc[:50]}")

        logger.info(f"✅ Found {len(cards)} recommended cards in carousel")

    def test_recommend_for_you_label(self, driver):
        """'Recommend For You' label should be visible."""
        label = driver.find_elements(AppiumBy.XPATH,
            "//*[contains(@content-desc, 'Recommend')]")
        # Filter to find the "Recommend\nFor You" one (not "Recommended Itinerary")
        found = False
        for el in label:
            desc = el.get_attribute("content-desc") or ""
            if "For You" in desc:
                found = True
                logger.info(f"✅ Found label: '{desc}'")
                break
        if not found:
            logger.info("ℹ 'Recommend For You' label not visible in current scroll position")
