"""
Test 02 — Home Screen & Banners (Real Device)
===============================================
Verifies the home screen layout, banner carousel, service cards,
and scrollable sections using locators from actual XML dump.

XML Source: reports/real_device/explore_03_home.xml
            reports/real_device/explore_04_home_mid.xml
"""

import pytest
import time
import logging
from appium.webdriver.common.appiumby import AppiumBy

logger = logging.getLogger(__name__)

pytestmark = [pytest.mark.home, pytest.mark.regression]


# ──────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────

def _ensure_home(driver):
    """Ensure we're on the home screen (scroll to top)."""
    # Check for Welcome greeting
    welcome = driver.find_elements(AppiumBy.XPATH,
        "//*[contains(@content-desc, 'Welcome,')]")
    if not welcome:
        # Maybe scrolled, try scrolling up
        s = driver.get_window_size()
        for _ in range(5):
            driver.swipe(s['width']//2, int(s['height']*0.25),
                        s['width']//2, int(s['height']*0.75), 600)
            time.sleep(0.5)
            welcome = driver.find_elements(AppiumBy.XPATH,
                "//*[contains(@content-desc, 'Welcome,')]")
            if welcome:
                break
    time.sleep(1)
    return len(welcome) > 0


def _swipe_up(driver):
    """Scroll content up (swipe from bottom to top)."""
    s = driver.get_window_size()
    driver.swipe(s['width']//2, int(s['height']*0.75),
                s['width']//2, int(s['height']*0.25), 800)
    time.sleep(1.5)


# ══════════════════════════════════════════════
# TEST CLASS: Home Layout
# ══════════════════════════════════════════════

class TestHomeLayout:
    """Verify core home screen layout elements."""

    def test_welcome_greeting_visible(self, driver):
        """Welcome greeting with username should be visible."""
        logger.info("\n=== HOME: Welcome Greeting ===")
        _ensure_home(driver)

        welcome = driver.find_elements(AppiumBy.XPATH,
            "//*[contains(@content-desc, 'Welcome,')]")
        assert len(welcome) > 0, "Welcome greeting not found"

        text = welcome[0].get_attribute("content-desc")
        assert "danip" in text.lower(), f"Username not in greeting: {text}"
        logger.info(f"✅ Greeting found: {text}")

    def test_subtitle_visible(self, driver):
        """'Where do you want to go?' subtitle should be visible."""
        logger.info("\n=== HOME: Subtitle ===")
        _ensure_home(driver)

        subtitle = driver.find_elements(AppiumBy.XPATH,
            "//*[contains(@content-desc, 'Where do you want to go')]")
        assert len(subtitle) > 0, "Subtitle not found"
        logger.info("✅ Subtitle visible: 'Where do you want to go?'")

    def test_header_icons_present(self, driver):
        """Three clickable icons (search, notif, profile) at top-right."""
        logger.info("\n=== HOME: Header Icons ===")
        _ensure_home(driver)

        # From XML: 3 clickable android.view.View elements after the subtitle
        # bounds: [690,201][805,289], [805,201][921,289], [921,201][1036,289]
        clickable_views = driver.find_elements(AppiumBy.XPATH,
            "//android.widget.ScrollView/android.view.View[@clickable='true' and not(@content-desc)]")

        # At minimum we should find the 3 header icons
        icon_count = 0
        for v in clickable_views:
            try:
                bounds = v.get_attribute("bounds")
                if bounds and "201" in bounds:  # y=201 is header row
                    icon_count += 1
            except Exception:
                continue

        assert icon_count >= 3, f"Expected 3 header icons, found {icon_count}"
        logger.info(f"✅ Found {icon_count} header icons (search, notif, profile)")


# ══════════════════════════════════════════════
# TEST CLASS: Banner Carousel
# ══════════════════════════════════════════════

class TestBannerCarousel:
    """Verify the banner/slider carousel on home screen."""

    def test_banner_carousel_exists(self, driver):
        """Banner carousel (scrollable container) should exist."""
        logger.info("\n=== HOME: Banner Carousel ===")
        _ensure_home(driver)

        # Banner is a scrollable View containing clickable sub-views
        carousel = driver.find_elements(AppiumBy.XPATH,
            "//android.widget.ScrollView//android.view.View[@scrollable='true']")
        assert len(carousel) > 0, "Banner carousel not found"
        logger.info("✅ Banner carousel exists")

    def test_banner_has_indicators(self, driver):
        """Banner dot indicators should be present (Buttons without content-desc)."""
        logger.info("\n=== HOME: Banner Indicators ===")
        _ensure_home(driver)

        # From XML: 6 small Button elements (carousel dots)
        # They're at y≈1054, small width (bounds like [433,1054][449,1070])
        dots = driver.find_elements(AppiumBy.XPATH,
            "//android.widget.ScrollView/android.widget.Button[not(@content-desc)]")
        assert len(dots) >= 3, f"Expected ≥3 indicator dots, found {len(dots)}"
        logger.info(f"✅ Found {len(dots)} banner indicator dots")

    def test_banner_swipe(self, driver):
        """Swiping left on the banner should work."""
        logger.info("\n=== HOME: Banner Swipe ===")
        _ensure_home(driver)

        # From XML: banner bounds [0,342][1080,1029]
        s = driver.get_window_size()
        y_center = 685  # (342+1029)/2
        x_start = int(s['width'] * 0.8)
        x_end = int(s['width'] * 0.2)

        driver.swipe(x_start, y_center, x_end, y_center, 600)
        time.sleep(1)

        # Verify still on home (banner swipe shouldn't navigate away)
        welcome = driver.find_elements(AppiumBy.XPATH,
            "//*[contains(@content-desc, 'Welcome,')]")
        assert len(welcome) > 0, "Left home after banner swipe"
        logger.info("✅ Banner swipe works without leaving home")


# ══════════════════════════════════════════════
# TEST CLASS: Service Cards
# ══════════════════════════════════════════════

class TestServiceCards:
    """Verify the 6 service menu cards on home screen."""

    def test_open_trip_card(self, driver):
        """Open Trip service card should be visible."""
        logger.info("\n=== HOME: Open Trip Card ===")
        _ensure_home(driver)

        card = driver.find_elements(AppiumBy.XPATH,
            "//*[starts-with(@content-desc, 'Open Trip')]")
        assert len(card) > 0, "Open Trip card not found"
        logger.info("✅ Open Trip card visible")

    def test_flight_card(self, driver):
        """Flight card (Soon) should be visible."""
        card = driver.find_elements(AppiumBy.XPATH,
            "//*[contains(@content-desc, 'Flight')]")
        assert len(card) > 0, "Flight card not found"
        logger.info("✅ Flight card visible (Soon)")

    def test_train_card(self, driver):
        """Train card (Soon) should be visible."""
        card = driver.find_elements(AppiumBy.XPATH,
            "//*[contains(@content-desc, 'Train')]")
        assert len(card) > 0, "Train card not found"
        logger.info("✅ Train card visible (Soon)")

    def test_bus_card(self, driver):
        """Bus card (Soon) should be visible."""
        card = driver.find_elements(AppiumBy.XPATH,
            "//*[contains(@content-desc, 'Bus')]")
        assert len(card) > 0, "Bus card not found"
        logger.info("✅ Bus card visible (Soon)")

    def test_hotel_card(self, driver):
        """Hotel card (Soon) should be visible."""
        card = driver.find_elements(AppiumBy.XPATH,
            "//*[contains(@content-desc, 'Hotel')]")
        assert len(card) > 0, "Hotel card not found"
        logger.info("✅ Hotel card visible (Soon)")

    def test_promo_deals_card(self, driver):
        """Promo Deals card (Soon) should be visible."""
        card = driver.find_elements(AppiumBy.XPATH,
            "//*[contains(@content-desc, 'Promo Deals')]")
        assert len(card) > 0, "Promo Deals card not found"
        logger.info("✅ Promo Deals card visible (Soon)")

    def test_show_all_button(self, driver):
        """'Show All' button should be visible below service cards."""
        show_all = driver.find_elements(AppiumBy.XPATH,
            "//*[@content-desc='Show All']")
        assert len(show_all) > 0, "Show All button not found"
        logger.info("✅ Show All button visible")


# ══════════════════════════════════════════════
# TEST CLASS: Create Itinerary CTA
# ══════════════════════════════════════════════

class TestCreateItineraryCTA:
    """Verify the 'Create New Itinerary' call-to-action section."""

    def test_cta_text_visible(self, driver):
        """CTA intro text should be visible."""
        logger.info("\n=== HOME: Create Itinerary CTA ===")
        _ensure_home(driver)

        cta = driver.find_elements(AppiumBy.XPATH,
            "//*[contains(@content-desc, 'create a new itinerary')]")
        assert len(cta) > 0, "CTA text not found"
        logger.info("✅ CTA text visible")

    def test_cta_button_visible(self, driver):
        """'Create New Itinerary' button should be visible and clickable."""
        btn = driver.find_elements(AppiumBy.XPATH,
            "//*[@content-desc='Create New Itinerary']")
        assert len(btn) > 0, "Create New Itinerary button not found"
        assert btn[0].get_attribute("clickable") == "true", "Button not clickable"
        logger.info("✅ Create New Itinerary button visible & clickable")


# ══════════════════════════════════════════════
# TEST CLASS: Scrollable Sections
# ══════════════════════════════════════════════

class TestScrollableSections:
    """Verify sections revealed by scrolling down on home."""

    def test_popular_city_chips(self, driver):
        """Popular city chips should appear after scrolling."""
        logger.info("\n=== HOME: Popular City Chips ===")
        _ensure_home(driver)
        _swipe_up(driver)
        _swipe_up(driver)

        # From XML: HorizontalScrollView with city names
        cities = driver.find_elements(AppiumBy.XPATH,
            "//*[@content-desc='Depok' or @content-desc='Tebet' "
            "or @content-desc='Sulawesi' or @content-desc='Surabaya' "
            "or @content-desc='Jakarta' or @content-desc='Makassar']")
        assert len(cities) >= 1, "No popular city chips found"
        city_names = [c.get_attribute("content-desc") for c in cities]
        logger.info(f"✅ Found {len(cities)} city chips: {city_names}")

    def test_open_trip_with_us_section(self, driver):
        """'Open Trip with Us' section should be visible."""
        logger.info("\n=== HOME: Open Trip With Us ===")

        section = driver.find_elements(AppiumBy.XPATH,
            "//*[@content-desc='Open Trip with Us']")
        assert len(section) > 0, "Open Trip with Us section not found"
        logger.info("✅ 'Open Trip with Us' section visible")

    def test_see_all_link(self, driver):
        """'See all' link should be present in Open Trip section."""
        see_all = driver.find_elements(AppiumBy.XPATH,
            "//*[@content-desc='See all']")
        assert len(see_all) > 0, "'See all' link not found"
        assert see_all[0].get_attribute("clickable") == "true"
        logger.info("✅ 'See all' link visible & clickable")

    def test_recommended_itinerary_section(self, driver):
        """'Recommended Itinerary' section should be visible."""
        logger.info("\n=== HOME: Recommended Itinerary ===")

        rec = driver.find_elements(AppiumBy.XPATH,
            "//*[@content-desc='Recommended Itinerary']")
        assert len(rec) > 0, "Recommended Itinerary section not found"
        logger.info("✅ 'Recommended Itinerary' section visible")

    def test_partnership_banner(self, driver):
        """Partnership banner should be visible at bottom."""
        logger.info("\n=== HOME: Partnership Banner ===")
        _swipe_up(driver)

        partner = driver.find_elements(AppiumBy.XPATH,
            "//*[contains(@content-desc, 'Apply for Partnership')]")
        assert len(partner) > 0, "Partnership banner not found"
        logger.info("✅ Partnership banner visible")
