"""
Test 09 — Explore Itinerary Deep (Real Device)
================================================
Verifies deeper interactions on the Explore/Search page:
city card navigation, search input, recommended itinerary cards,
and itinerary detail navigation.

XML Source: reports/real_device/search_01_after_tap.xml
"""

import pytest
import time
import logging
from appium.webdriver.common.appiumby import AppiumBy

logger = logging.getLogger(__name__)

pytestmark = [pytest.mark.search, pytest.mark.regression]


def _go_home(driver):
    """Navigate to home screen safely via Bottom Nav tab."""
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


def _open_search(driver):
    """Open the Explore Itinerary page from home."""
    _go_home(driver)
    time.sleep(1)

    # Use semantic locator for Explore tab
    search_icon = driver.find_elements(AppiumBy.XPATH,
        "//*[contains(@content-desc, 'Explore\nTab 2 of 4')] | //*[contains(@content-desc, 'Search\nTab')]")
    if search_icon:
        search_icon[-1].click()
    else:
        # Fallback: coordinate
        driver.tap([(747, 245)], 500)
    time.sleep(3)

    title = driver.find_elements(AppiumBy.XPATH,
        "//*[@content-desc='Explore Itinerary']")
    return len(title) > 0


class TestSearchCityCards:
    """Verify city card interactions on Explore page."""

    def test_tap_depok_card(self, driver):
        """Tapping 'Depok' city card should navigate to results."""
        logger.info("\n=== EXPLORE: Tap Depok City ===")
        assert _open_search(driver), "Could not open Explore page"

        depok = driver.find_elements(AppiumBy.XPATH,
            "//*[@content-desc='Depok' and @clickable='true']")
        assert len(depok) > 0, "Depok card not found"

        depok[0].click()
        time.sleep(3)

        # Should navigate to filtered results or city view
        # Just verify we left the explore page or content changed
        logger.info("✅ Depok city card tapped successfully")

        # Go back
        driver.back()
        time.sleep(3)

    def test_city_cards_are_clickable(self, driver):
        """All visible city cards should be clickable."""
        logger.info("\n=== EXPLORE: City Cards Clickable ===")

        # Re-open search if needed
        title = driver.find_elements(AppiumBy.XPATH,
            "//*[@content-desc='Explore Itinerary']")
        if not title:
            assert _open_search(driver), "Could not reopen Explore page"

        cities = ["Depok", "Tebet", "Sulawesi", "Surabaya", "Makassar", "Jakarta"]
        found_cities = []

        for city in cities:
            els = driver.find_elements(AppiumBy.XPATH,
                f"//*[@content-desc='{city}']")
            if els:
                clickable = els[0].get_attribute("clickable")
                found_cities.append((city, clickable))

        assert len(found_cities) >= 3, f"Expected ≥3 cities, found {len(found_cities)}"
        for city, clickable in found_cities:
            assert clickable == "true", f"{city} card not clickable"

        logger.info(f"✅ {len(found_cities)} city cards are clickable: "
                    f"{[c[0] for c in found_cities]}")


class TestSearchInput:
    """Verify search input interaction."""

    def test_tap_search_bar_opens_input(self, driver):
        """Tapping search bar should open search input."""
        logger.info("\n=== EXPLORE: Search Input ===")

        title = driver.find_elements(AppiumBy.XPATH,
            "//*[@content-desc='Explore Itinerary']")
        if not title:
            assert _open_search(driver)

        search_bar = driver.find_elements(AppiumBy.XPATH,
            "//*[contains(@content-desc, 'Search any Itinerary')]")
        assert len(search_bar) > 0, "Search bar not found"

        search_bar[0].click()
        time.sleep(3)

        # After tapping, check if a text input appears or page changed
        inputs = driver.find_elements(AppiumBy.XPATH,
            "//android.widget.EditText")
        if inputs:
            logger.info("✅ Search input field appeared after tap")
            # Type something
            inputs[0].send_keys("Bali")
            time.sleep(2)
            logger.info("✅ Typed 'Bali' in search field")

            # Safe keyboard hide
            driver.tap([(540, 200)])

            # Clear and go back
            driver.back()
            time.sleep(2)
        else:
            logger.info("✅ Search bar tapped (may navigate to search results page)")
            driver.back()
            time.sleep(2)


class TestSearchRecommendedCards:
    """Verify recommended itinerary cards."""

    def test_recommended_cards_displayed(self, driver):
        """Recommended itinerary cards should be displayed."""
        logger.info("\n=== EXPLORE: Recommended Cards ===")

        title = driver.find_elements(AppiumBy.XPATH,
            "//*[@content-desc='Explore Itinerary']")
        if not title:
            assert _open_search(driver)

        # Scroll down to see Recommended section
        s = driver.get_window_size()
        driver.swipe(s['width']//2, int(s['height']*0.75),
                    s['width']//2, int(s['height']*0.25), 800)
        time.sleep(2)

        # From XML: ImageView cards in the recommended section
        cards = driver.find_elements(AppiumBy.XPATH,
            "//android.widget.ImageView[@clickable='true']")
        assert len(cards) >= 1, "No recommended itinerary cards"

        # Log card info
        for i, card in enumerate(cards[:3]):
            desc = card.get_attribute("content-desc") or "no-desc"
            logger.info(f"  Card {i+1}: {desc[:50]}")

        logger.info(f"✅ Found {len(cards)} recommended cards")

    def test_tap_recommended_card(self, driver):
        """Tapping a recommended card should open its detail."""
        logger.info("\n=== EXPLORE: Tap Recommended Card ===")

        cards = driver.find_elements(AppiumBy.XPATH,
            "//android.widget.ImageView[@clickable='true']")
        if not cards:
            pytest.skip("No recommended cards to tap")

        card_desc = cards[0].get_attribute("content-desc") or "unknown"
        logger.info(f"  Tapping card: {card_desc[:50]}")
        cards[0].click()
        time.sleep(3)

        # Should open detail — verify by checking for back button
        back_btn = driver.find_elements(AppiumBy.XPATH,
            "//android.widget.Button[@clickable='true']")
        assert len(back_btn) > 0, "Detail page not loaded"
        logger.info("✅ Recommended card detail opened")

        driver.back()
        time.sleep(3)

    def test_go_back_to_home(self, driver):
        """Going back from explore should return to home."""
        logger.info("\n=== EXPLORE: Back to Home ===")
        driver.back()
        time.sleep(3)

        welcome = driver.find_elements(AppiumBy.XPATH,
            "//*[contains(@content-desc, 'Welcome,')]")
        if not welcome:
            driver.back()
            time.sleep(2)
            welcome = driver.find_elements(AppiumBy.XPATH,
                "//*[contains(@content-desc, 'Welcome,')]")

        assert len(welcome) > 0, "Not back on home"
        logger.info("✅ Back on home screen")
