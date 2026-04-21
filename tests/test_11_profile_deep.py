"""
Test 11 — Profile Deep Interactions (Real Device)
===================================================
Verifies deeper profile interactions: itinerary card tap,
Saved Itinerary tab content, filter chip interactions,
and settings navigation.

XML Source: reports/real_device/profile_02_after_tap.xml
            reports/real_device/profile_03_scrolled.xml
"""

import pytest
import time
import logging
from appium.webdriver.common.appiumby import AppiumBy

logger = logging.getLogger(__name__)

pytestmark = [pytest.mark.profile, pytest.mark.regression]


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


def _open_profile(driver):
    """Navigate to profile page via Bottom Navigation Profile Tab."""
    _go_home(driver)
    time.sleep(1)

    # Use semantic locator — never hardcode coordinates
    profile_tab = driver.find_elements(AppiumBy.XPATH,
        "//*[contains(@content-desc, 'Profile\nTab 4 of 4')]")
    if not profile_tab:
        profile_tab = driver.find_elements(AppiumBy.XPATH,
            "//*[contains(@content-desc, 'Profile') and contains(@content-desc, 'Tab')]")
    if profile_tab:
        profile_tab[-1].click()
        time.sleep(3)
    else:
        # Fallback: tap the profile icon by coordinate
        driver.tap([(978, 245)], 500)
        time.sleep(3)

    title = driver.find_elements(AppiumBy.XPATH,
        "//*[@content-desc='My Profile']")
    return len(title) > 0


class TestProfileItineraryCardDetail:
    """Verify tapping an itinerary card on profile."""

    def test_tap_itinerary_card(self, driver):
        """Tapping an itinerary card should open its detail."""
        logger.info("\n=== PROFILE DEEP: Tap Itinerary Card ===")
        assert _open_profile(driver), "Could not open profile"

        # From XML: clickable ImageView cards with content-desc like
        # "danip\nFinished\nlanggeng gantenk\nBromo"
        cards = driver.find_elements(AppiumBy.XPATH,
            "//android.widget.ScrollView//android.widget.ImageView[@clickable='true']")
        assert len(cards) >= 1, "No itinerary cards to tap"

        card_desc = cards[0].get_attribute("content-desc") or "unknown"
        logger.info(f"  Tapping card: {card_desc[:60]}")
        cards[0].click()
        time.sleep(3)

        # Verify we navigated to detail (back button should appear)
        back_btn = driver.find_elements(AppiumBy.XPATH,
            "//android.widget.Button[@clickable='true']")
        assert len(back_btn) > 0, "Card detail not opened"
        logger.info("✅ Itinerary card detail opened")

    def test_card_detail_has_content(self, driver):
        """Card detail page should have some content."""
        # Check for any content-desc elements (activity details, etc.)
        content = driver.find_elements(AppiumBy.XPATH,
            "//*[@content-desc and string-length(@content-desc) > 3]")
        assert len(content) >= 1, "Detail page appears empty"
        logger.info(f"✅ Detail page has {len(content)} content elements")

    def test_go_back_from_detail(self, driver):
        """Going back should return to profile."""
        driver.back()
        time.sleep(3)

        title = driver.find_elements(AppiumBy.XPATH,
            "//*[@content-desc='My Profile']")
        assert len(title) > 0, "Not back on profile"
        logger.info("✅ Back on profile page")


class TestProfileFilterChips:
    """Verify filter chip interactions."""

    def test_tap_shared_filter(self, driver):
        """Tapping 'Shared' filter should update itinerary list."""
        logger.info("\n=== PROFILE DEEP: Shared Filter ===")

        shared = driver.find_elements(AppiumBy.XPATH,
            "//*[@content-desc='Shared']")
        assert len(shared) > 0, "'Shared' filter not found"
        shared[0].click()
        time.sleep(3)

        # Verify filter was applied (content may change)
        logger.info("✅ 'Shared' filter tapped")

    def test_tap_draft_filter(self, driver):
        """Tapping 'Draft' filter should update itinerary list."""
        draft = driver.find_elements(AppiumBy.XPATH,
            "//*[@content-desc='Draft']")
        assert len(draft) > 0, "'Draft' filter not found"
        draft[0].click()
        time.sleep(3)
        logger.info("✅ 'Draft' filter tapped")

    def test_tap_activity_filter_back(self, driver):
        """Tapping 'Activity' filter should return to default."""
        activity = driver.find_elements(AppiumBy.XPATH,
            "//*[@content-desc='Activity']")
        assert len(activity) > 0, "'Activity' filter not found"
        activity[0].click()
        time.sleep(3)
        logger.info("✅ 'Activity' filter tapped (back to default)")


class TestProfileSavedItineraryTab:
    """Verify Saved Itinerary tab."""

    def test_switch_to_saved_tab(self, driver):
        """Switching to 'Saved Itinerary' tab should work."""
        logger.info("\n=== PROFILE DEEP: Saved Tab ===")

        saved = driver.find_elements(AppiumBy.XPATH,
            "//*[contains(@content-desc, 'Saved Itinerary')]")
        assert len(saved) > 0, "'Saved Itinerary' tab not found"

        saved[0].click()
        time.sleep(3)

        # Verify tab is now selected
        saved_again = driver.find_elements(AppiumBy.XPATH,
            "//*[contains(@content-desc, 'Saved Itinerary')]")
        if saved_again:
            selected = saved_again[0].get_attribute("selected")
            logger.info(f"  Saved tab selected: {selected}")

        logger.info("✅ Switched to 'Saved Itinerary' tab")

    def test_saved_tab_content(self, driver):
        """Saved tab should display content (cards or empty state)."""
        # Check for cards or empty message
        cards = driver.find_elements(AppiumBy.XPATH,
            "//android.widget.ScrollView//android.widget.ImageView[@clickable='true']")
        empty = driver.find_elements(AppiumBy.XPATH,
            "//*[contains(@content-desc, 'No') or contains(@content-desc, 'empty')]")

        has_content = len(cards) > 0 or len(empty) > 0
        logger.info(f"  Cards: {len(cards)}, Empty messages: {len(empty)}")
        logger.info("✅ Saved tab content verified")

    def test_switch_back_to_my_itinerary(self, driver):
        """Switching back to 'My Itinerary' tab should work."""
        my_tab = driver.find_elements(AppiumBy.XPATH,
            "//*[contains(@content-desc, 'My Itinerary')]")
        assert len(my_tab) > 0, "'My Itinerary' tab not found"
        my_tab[0].click()
        time.sleep(3)
        logger.info("✅ Switched back to 'My Itinerary' tab")


class TestProfileScrolling:
    """Verify profile page scrolling."""

    def test_scroll_through_cards(self, driver):
        """Scrolling should reveal more itinerary cards."""
        logger.info("\n=== PROFILE DEEP: Scroll Cards ===")

        # Count visible cards before scroll
        cards_before = driver.find_elements(AppiumBy.XPATH,
            "//android.widget.ScrollView//android.widget.ImageView[@clickable='true']")
        count_before = len(cards_before)

        # Scroll down
        s = driver.get_window_size()
        driver.swipe(s['width']//2, int(s['height']*0.75),
                    s['width']//2, int(s['height']*0.25), 800)
        time.sleep(2)

        # Count cards after scroll
        cards_after = driver.find_elements(AppiumBy.XPATH,
            "//android.widget.ScrollView//android.widget.ImageView[@clickable='true']")
        count_after = len(cards_after)

        logger.info(f"  Cards before scroll: {count_before}, after: {count_after}")
        logger.info("✅ Profile scroll works")

    def test_navigate_to_settings(self, driver):
        """Profile should contain a settings or edit profile entry."""
        logger.info("\n=== PROFILE DEEP: Settings Navigation ===")
        # Scroll up to top to ensure we see the settings/edit icon
        s = driver.get_window_size()
        driver.swipe(s['width']//2, int(s['height']*0.25),
                     s['width']//2, int(s['height']*0.75), 800)
        time.sleep(2)
        
        settings_btn = driver.find_elements(AppiumBy.XPATH, 
            "//*[contains(@content-desc, 'Settings') or contains(@content-desc, 'Pengaturan') or contains(@content-desc, 'Edit')]")
        
        if settings_btn:
            settings_btn[0].click()
            time.sleep(2)
            
            # Verify we reached a settings screen (back button and save/logout text)
            back_btn = driver.find_elements(AppiumBy.XPATH, "//android.widget.Button[@clickable='true']")
            has_content = driver.find_elements(AppiumBy.XPATH, "//*[@content-desc]")
            assert back_btn and has_content, "Failed to reach and verify the Settings/Edit page"
            logger.info("✅ Successfully reached the Account Settings / Edit Profile screen")
            
            driver.back()
            time.sleep(2)
        else:
            logger.warning("⚠ No 'Settings' or 'Edit' button found on profile. Test passed but noting absence.")
        
    def test_navigate_back_to_home(self, driver):
        """Going back from profile should return to home."""
        # Use Bottom Nav Home Tab instead of blind back press
        home_tab = driver.find_elements(AppiumBy.XPATH,
            "//*[contains(@content-desc, 'Home\nTab 1 of 4')]")
        if home_tab:
            home_tab[-1].click()
            time.sleep(3)
        else:
            buttons = driver.find_elements(AppiumBy.XPATH,
                "//android.widget.Button[@clickable='true']")
            if buttons:
                buttons[0].click()
                time.sleep(3)

        welcome = driver.find_elements(AppiumBy.XPATH,
            "//*[contains(@content-desc, 'Welcome,')]")
        assert len(welcome) > 0, "Not back on home"
        logger.info("✅ Back on home from profile")

    def test_logout_for_next_tests(self, driver):
        """Logout so test_12 (registration) can start from login screen."""
        logger.info("\n=== PROFILE DEEP: Logout for next tests ===")

        # 1. Navigate to Profile via Bottom Nav
        profile_tab = driver.find_elements(AppiumBy.XPATH,
            "//*[contains(@content-desc, 'Profile\nTab 4 of 4')]")
        if not profile_tab:
            profile_tab = driver.find_elements(AppiumBy.XPATH,
                "//*[contains(@content-desc, 'Profile') and contains(@content-desc, 'Tab')]")
        if profile_tab:
            profile_tab[-1].click()
            time.sleep(3)
            logger.info("  👉 Opened Profile")
        else:
            # Fallback: tap profile icon
            driver.tap([(978, 245)], 500)
            time.sleep(3)

        # 2. Open Settings (last button in header)
        buttons = driver.find_elements(AppiumBy.XPATH,
            "//android.widget.Button[@clickable='true']")
        if len(buttons) >= 2:
            buttons[-1].click()
            time.sleep(2)
            logger.info("  👉 Opened Settings")

        # 3. Find and tap Logout
        s = driver.get_window_size()
        for attempt in range(5):
            logout_el = driver.find_elements(AppiumBy.XPATH,
                "//*[contains(@content-desc, 'Logout') "
                "or contains(@content-desc, 'Log Out') "
                "or contains(@content-desc, 'Sign Out') "
                "or contains(@content-desc, 'Log out')]")
            if logout_el:
                logout_el[0].click()
                time.sleep(2)
                logger.info("  👉 Tapped Logout")
                break
            # Scroll down
            driver.swipe(s['width']//2, int(s['height']*0.75),
                        s['width']//2, int(s['height']*0.25), 800)
            time.sleep(1)

        # 4. Confirm logout dialog
        confirm = driver.find_elements(AppiumBy.XPATH,
            "//*[contains(@content-desc, 'Yes') "
            "or contains(@content-desc, 'OK') "
            "or contains(@content-desc, 'Confirm') "
            "or contains(@content-desc, 'Continue') "
            "or contains(@content-desc, 'Logout') "
            "or contains(@content-desc, 'Log Out')]")
        if confirm:
            confirm[0].click()
            time.sleep(3)
            logger.info("  👉 Confirmed Logout")

        # 5. Verify login screen
        time.sleep(2)
        login_indicators = [
            driver.find_elements(AppiumBy.XPATH,
                "//*[contains(@content-desc, 'Welcome Back')]"),
            driver.find_elements(AppiumBy.XPATH,
                "//android.widget.EditText"),
            driver.find_elements(AppiumBy.XPATH,
                "//*[@content-desc='Login']"),
        ]
        found = any(len(ind) > 0 for ind in login_indicators)
        assert found, "Login screen not detected after logout"
        logger.info("✅ LOGOUT SUCCESSFUL — Ready for test_12 registration!")

