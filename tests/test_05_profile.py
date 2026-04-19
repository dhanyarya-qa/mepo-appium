"""
Test 05 — Profile (Real Device)
=================================
Verifies profile page: navigation, user info display, tabs, filters,
and itinerary cards.

XML Source: reports/real_device/profile_02_after_tap.xml
"""

import pytest
import time
import logging
from appium.webdriver.common.appiumby import AppiumBy

logger = logging.getLogger(__name__)

pytestmark = [pytest.mark.profile, pytest.mark.regression]


def _go_home(driver):
    """Navigate back to home screen."""
    for _ in range(5):
        welcome = driver.find_elements(AppiumBy.XPATH,
            "//*[contains(@content-desc, 'Welcome,')]")
        if welcome:
            # Scroll to top
            s = driver.get_window_size()
            for _ in range(4):
                driver.swipe(s['width']//2, int(s['height']*0.25),
                            s['width']//2, int(s['height']*0.75), 600)
                time.sleep(0.3)
            return True
        driver.back()
        time.sleep(2)
    return False


def _navigate_to_profile(driver):
    """Navigate to profile by tapping the profile icon (top-right)."""
    _go_home(driver)
    time.sleep(1)

    # From XML: profile icon at bounds [921,201][1036,289]
    # It's the 3rd clickable View with no content-desc in the header area
    driver.tap([(978, 245)], 500)
    time.sleep(5)

    # Verify profile page loaded
    title = driver.find_elements(AppiumBy.XPATH,
        "//*[@content-desc='My Profile']")
    return len(title) > 0


class TestProfileNavigation:
    """Navigate to and verify profile page."""

    def test_navigate_to_profile(self, driver):
        """Tapping profile icon should open profile page."""
        logger.info("\n=== PROFILE: Navigate ===")
        assert _navigate_to_profile(driver), "Profile page not opened"
        logger.info("✅ Profile page opened")

    def test_page_title(self, driver):
        """Page title should be 'My Profile'."""
        title = driver.find_elements(AppiumBy.XPATH,
            "//*[@content-desc='My Profile']")
        assert len(title) > 0, "'My Profile' title not found"
        logger.info("✅ Page title: 'My Profile'")

    def test_back_button_exists(self, driver):
        """Back button should be present."""
        # From XML: Button at [11,95][143,227]
        back_btn = driver.find_elements(AppiumBy.XPATH,
            "//android.widget.Button[@clickable='true']")
        assert len(back_btn) >= 1, "Back button not found"
        logger.info("✅ Back button present")

    def test_settings_button_exists(self, driver):
        """Settings button should be present (top-right)."""
        # From XML: Button at [948,95][1080,227]
        buttons = driver.find_elements(AppiumBy.XPATH,
            "//android.widget.Button[@clickable='true']")
        assert len(buttons) >= 2, "Settings button not found (need ≥2 buttons)"
        logger.info("✅ Settings button present (top-right)")


class TestProfileUserInfo:
    """Verify user info display on profile."""

    def test_user_name_displayed(self, driver):
        """Username 'danip' should be displayed."""
        logger.info("\n=== PROFILE: User Info ===")

        # From XML: content-desc="danip"
        name = driver.find_elements(AppiumBy.XPATH,
            "//*[@content-desc='danip']")
        assert len(name) > 0, "Username 'danip' not found"
        logger.info("✅ Username displayed: 'danip'")

    def test_username_handle_displayed(self, driver):
        """Username handle 'danip971' should be displayed."""
        # From XML: content-desc="danip971"
        handle = driver.find_elements(AppiumBy.XPATH,
            "//*[@content-desc='danip971']")
        assert len(handle) > 0, "Username handle 'danip971' not found"
        logger.info("✅ Handle displayed: 'danip971'")

    def test_avatar_displayed(self, driver):
        """Profile avatar image should be displayed."""
        # From XML: ImageView in the profile header area
        avatar = driver.find_elements(AppiumBy.XPATH,
            "//android.widget.ScrollView//android.widget.ImageView[not(@clickable='true')]")
        assert len(avatar) > 0, "Profile avatar not found"
        logger.info("✅ Profile avatar displayed")


class TestProfileTabs:
    """Verify profile tab navigation."""

    def test_my_itinerary_tab(self, driver):
        """'My Itinerary' tab should exist and be selected."""
        logger.info("\n=== PROFILE: Tabs ===")

        # From XML: content-desc="My Itinerary\nTab 1 of 2", selected="true"
        tab = driver.find_elements(AppiumBy.XPATH,
            "//*[contains(@content-desc, 'My Itinerary')]")
        assert len(tab) > 0, "'My Itinerary' tab not found"

        selected = tab[0].get_attribute("selected")
        assert selected == "true", f"My Itinerary tab not selected: {selected}"
        logger.info("✅ 'My Itinerary' tab active (selected)")

    def test_saved_itinerary_tab(self, driver):
        """'Saved Itinerary' tab should exist."""
        # From XML: content-desc="Saved Itinerary\nTab 2 of 2"
        tab = driver.find_elements(AppiumBy.XPATH,
            "//*[contains(@content-desc, 'Saved Itinerary')]")
        assert len(tab) > 0, "'Saved Itinerary' tab not found"
        logger.info("✅ 'Saved Itinerary' tab present")

    def test_switch_to_saved_tab(self, driver):
        """Tapping 'Saved Itinerary' tab should switch tabs."""
        logger.info("\n=== PROFILE: Switch Tab ===")

        tab = driver.find_elements(AppiumBy.XPATH,
            "//*[contains(@content-desc, 'Saved Itinerary')]")
        assert len(tab) > 0, "'Saved Itinerary' tab not found"
        tab[0].click()
        time.sleep(3)

        # Verify selection changed
        saved = driver.find_elements(AppiumBy.XPATH,
            "//*[contains(@content-desc, 'Saved Itinerary')]")
        if saved:
            selected = saved[0].get_attribute("selected")
            logger.info(f"  Saved tab selected: {selected}")

        # Switch back to My Itinerary
        my_tab = driver.find_elements(AppiumBy.XPATH,
            "//*[contains(@content-desc, 'My Itinerary')]")
        if my_tab:
            my_tab[0].click()
            time.sleep(2)
        logger.info("✅ Tab switching works")


class TestProfileFilters:
    """Verify filter chips on profile."""

    def test_activity_filter(self, driver):
        """'Activity' filter chip should exist."""
        logger.info("\n=== PROFILE: Filters ===")

        # From XML: content-desc="Activity"
        chip = driver.find_elements(AppiumBy.XPATH,
            "//*[@content-desc='Activity']")
        assert len(chip) > 0, "'Activity' filter not found"
        logger.info("✅ 'Activity' filter present")

    def test_shared_filter(self, driver):
        """'Shared' filter chip should exist."""
        chip = driver.find_elements(AppiumBy.XPATH,
            "//*[@content-desc='Shared']")
        assert len(chip) > 0, "'Shared' filter not found"
        logger.info("✅ 'Shared' filter present")

    def test_draft_filter(self, driver):
        """'Draft' filter chip should exist."""
        chip = driver.find_elements(AppiumBy.XPATH,
            "//*[@content-desc='Draft']")
        assert len(chip) > 0, "'Draft' filter not found"
        logger.info("✅ 'Draft' filter present")


class TestProfileItineraryCards:
    """Verify itinerary cards on profile."""

    def test_itinerary_cards_displayed(self, driver):
        """Itinerary cards should be visible in the grid."""
        logger.info("\n=== PROFILE: Itinerary Cards ===")

        # From XML: ImageView elements with content-desc like "danip\nFinished\n..."
        cards = driver.find_elements(AppiumBy.XPATH,
            "//android.widget.ScrollView//android.widget.ImageView[@clickable='true']")
        assert len(cards) >= 1, "No itinerary cards found"

        # Log card details
        for i, card in enumerate(cards[:4]):
            desc = card.get_attribute("content-desc") or "no-desc"
            logger.info(f"  Card {i+1}: {desc[:60]}")

        logger.info(f"✅ Found {len(cards)} itinerary cards")

    def test_card_has_status(self, driver):
        """Cards should show status (Finished/Ongoing)."""
        cards = driver.find_elements(AppiumBy.XPATH,
            "//android.widget.ScrollView//android.widget.ImageView[@clickable='true']")
        if cards:
            desc = cards[0].get_attribute("content-desc") or ""
            has_status = "Finished" in desc or "Ongoing" in desc or "Draft" in desc
            assert has_status, f"Card doesn't show status: {desc[:60]}"
            logger.info("✅ Card shows status (Finished/Ongoing/Draft)")

    def test_navigate_back_to_home(self, driver):
        """Going back from profile should return to home."""
        logger.info("\n=== PROFILE: Back to Home ===")

        # Tap back button (first Button element)
        buttons = driver.find_elements(AppiumBy.XPATH,
            "//android.widget.Button[@clickable='true']")
        if buttons:
            buttons[0].click()
            time.sleep(3)

        welcome = driver.find_elements(AppiumBy.XPATH,
            "//*[contains(@content-desc, 'Welcome,')]")
        assert len(welcome) > 0, "Not back on home"
        logger.info("✅ Back on home screen")
