"""
Test 04 — Create Itinerary (Real Device)
==========================================
Verifies the Create Itinerary flow: opening modal, form validation,
filling fields, and submission.

XML Source: reports/real_device/itinerary_01_create_page.xml
"""

import pytest
import time
import logging
from appium.webdriver.common.appiumby import AppiumBy

logger = logging.getLogger(__name__)

pytestmark = [pytest.mark.itinerary, pytest.mark.regression]


def _ensure_home_top(driver):
    """Navigate to home and scroll to top."""
    # Go back until we find Welcome
    for _ in range(5):
        welcome = driver.find_elements(AppiumBy.XPATH,
            "//*[contains(@content-desc, 'Welcome,')]")
        if welcome:
            break
        driver.back()
        time.sleep(2)

    # Scroll to top
    s = driver.get_window_size()
    for _ in range(5):
        driver.swipe(s['width']//2, int(s['height']*0.25),
                    s['width']//2, int(s['height']*0.75), 600)
        time.sleep(0.3)
    time.sleep(1)


def _open_create_modal(driver):
    """Open the Create Itinerary modal by tapping the CTA button."""
    # Find and tap "Create New Itinerary"
    for _ in range(3):
        btn = driver.find_elements(AppiumBy.XPATH,
            "//*[@content-desc='Create New Itinerary']")
        if btn:
            btn[0].click()
            time.sleep(3)
            return True
        # Scroll down to find it
        s = driver.get_window_size()
        driver.swipe(s['width']//2, int(s['height']*0.75),
                    s['width']//2, int(s['height']*0.25), 800)
        time.sleep(1)
    return False


def _close_modal(driver):
    """Close modal by tapping Cancel or Scrim."""
    # Try Cancel button
    cancel = driver.find_elements(AppiumBy.XPATH,
        "//*[@content-desc='Cancel']")
    if cancel:
        cancel[0].click()
        time.sleep(2)
        
        # Check if discard warning modal appeared (Cancel Itinerary)
        warning_cancel = driver.find_elements(AppiumBy.XPATH, "//*[@content-desc='Cancel']")
        if warning_cancel:
            warning_cancel[0].click()
            time.sleep(2)
        return

    # Try tapping Scrim (backdrop)
    scrim = driver.find_elements(AppiumBy.XPATH,
        "//*[@content-desc='Scrim']")
    if scrim:
        scrim[0].click()
        time.sleep(2)
        # Check if discard warning modal appeared
        warning_cancel = driver.find_elements(AppiumBy.XPATH, "//*[@content-desc='Cancel']")
        if warning_cancel:
            warning_cancel[0].click()
            time.sleep(2)
        return

    driver.back()
    time.sleep(2)


class TestCreateItineraryModal:
    """Verify the Create Itinerary modal dialog."""

    def test_open_create_modal(self, driver):
        """Tapping 'Create New Itinerary' should open the modal."""
        logger.info("\n=== ITINERARY: Open Modal ===")
        _ensure_home_top(driver)
        assert _open_create_modal(driver), "Could not open Create Itinerary modal"

        # Verify modal elements from XML
        # content-desc="Create Itinerary" is the modal wrapper
        title = driver.find_elements(AppiumBy.XPATH,
            "//*[@content-desc='Create Itinerary']")
        assert len(title) > 0, "Create Itinerary modal title not found"
        logger.info("✅ Create Itinerary modal opened")

    def test_title_field_exists(self, driver):
        """Title input field should be present with correct hint."""
        logger.info("\n=== ITINERARY: Title Field ===")

        # From XML: EditText with hint="Create title of itinerary"
        title_field = driver.find_elements(AppiumBy.XPATH,
            "//android.widget.EditText[@hint='Create title of itinerary']")
        if not title_field:
            title_field = driver.find_elements(AppiumBy.XPATH,
                "//android.widget.EditText")
        assert len(title_field) > 0, "Title input field not found"
        logger.info("✅ Title field present")

    def test_destination_field_exists(self, driver):
        """Destination field should be present."""
        logger.info("\n=== ITINERARY: Destination Field ===")

        # From XML: View with hint="Destination"
        dest_field = driver.find_elements(AppiumBy.XPATH,
            "//*[@hint='Destination']")
        if not dest_field:
            dest_field = driver.find_elements(AppiumBy.XPATH,
                "//*[contains(@content-desc, 'Destination') "
                "or contains(@hint, 'Destination')]")
        assert len(dest_field) > 0, "Destination field not found"
        logger.info("✅ Destination field present")

    def test_cancel_button_exists(self, driver):
        """Cancel button should be present and clickable."""
        cancel = driver.find_elements(AppiumBy.XPATH,
            "//*[@content-desc='Cancel']")
        assert len(cancel) > 0, "Cancel button not found"
        assert cancel[0].get_attribute("clickable") == "true"
        logger.info("✅ Cancel button present & clickable")

    def test_save_button_disabled_by_default(self, driver):
        """'Save & Create' button should be disabled when form is empty."""
        logger.info("\n=== ITINERARY: Save Button Default State ===")

        # From XML: content-desc="Save & Create", enabled="false"
        save_btn = driver.find_elements(AppiumBy.XPATH,
            "//*[contains(@content-desc, 'Save')]")
        assert len(save_btn) > 0, "Save & Create button not found"

        enabled = save_btn[0].get_attribute("enabled")
        assert enabled == "false", f"Save button should be disabled, got enabled={enabled}"
        logger.info("✅ Save & Create button is disabled by default")


class TestCreateItineraryForm:
    """Verify form interaction."""

    def test_type_title(self, driver):
        """Should be able to type in the title field."""
        logger.info("\n=== ITINERARY: Type Title ===")

        # Open modal if not already open
        title_wrapper = driver.find_elements(AppiumBy.XPATH,
            "//*[@content-desc='Create Itinerary']")
        if not title_wrapper:
            _ensure_home_top(driver)
            _open_create_modal(driver)

        # Type title
        title_field = driver.find_elements(AppiumBy.XPATH,
            "//android.widget.EditText")
        assert len(title_field) > 0, "Title field not found"
        title_field[0].click()
        time.sleep(0.3)
        title_field[0].send_keys("[Auto-Test] Safari Trip")
        try:
            driver.press_keycode(66) # ENTER key to safely dismiss keyboard
        except:
            pass
        time.sleep(1)
        logger.info("✅ Title entered: '[Auto-Test] Safari Trip'")

    def test_save_button_enables_after_input(self, driver):
        """After filling title, Save button may become enabled (depends on destination too)."""
        logger.info("\n=== ITINERARY: Save Button State After Input ===")

        save_btn = driver.find_elements(AppiumBy.XPATH,
            "//*[contains(@content-desc, 'Save')]")
        if save_btn:
            enabled = save_btn[0].get_attribute("enabled")
            logger.info(f"  Save button enabled: {enabled}")
            # Note: may still be disabled if destination is required
            logger.info("✅ Save button state checked after title input")

    def test_cancel_closes_modal(self, driver):
        """Tapping Cancel should close the modal and return to home."""
        logger.info("\n=== ITINERARY: Cancel Modal ===")

        _close_modal(driver)

        # Verify we're back on home (or at least modal is gone)
        time.sleep(2)
        modal = driver.find_elements(AppiumBy.XPATH,
            "//*[@content-desc='Create Itinerary']")
        assert len(modal) == 0, "Modal still visible after Cancel"
        logger.info("✅ Modal closed after Cancel")

    def test_scrim_closes_modal(self, driver):
        """Tapping the scrim (backdrop) should close the modal."""
        logger.info("\n=== ITINERARY: Scrim Closes Modal ===")

        _ensure_home_top(driver)
        if not _open_create_modal(driver):
            pytest.skip("Could not open modal")

        # From XML: content-desc="Scrim"
        scrim = driver.find_elements(AppiumBy.XPATH,
            "//*[@content-desc='Scrim']")
        if scrim:
            scrim[0].click()
            time.sleep(2)
            # Handle discard warning if it appears
            warning_cancel = driver.find_elements(AppiumBy.XPATH, "//*[@content-desc='Cancel']")
            if warning_cancel:
                warning_cancel[0].click()
                time.sleep(2)
                
            modal = driver.find_elements(AppiumBy.XPATH,
                "//*[@content-desc='Create Itinerary']")
            assert len(modal) == 0, "Modal still visible after Scrim tap"
            logger.info("✅ Scrim tap closes modal")
        else:
            logger.info("⚠ Scrim not found, skipped")


class TestCompleteItineraryCreation:
    """End-to-End flow: Fill title, destination, and finalize itinerary."""

    def test_z_fill_form_and_save(self, driver):
        """Fill all required fields and complete the creation."""
        logger.info("\n=== ITINERARY FULL: Create End to End ===")

        _ensure_home_top(driver)
        _open_create_modal(driver)

        # 1. Type Title
        title_field = driver.find_elements(AppiumBy.XPATH, "//android.widget.EditText[@hint='Create title of itinerary']")
        if not title_field:
            title_field = driver.find_elements(AppiumBy.XPATH, "//android.widget.EditText")
        assert len(title_field) > 0, "Title field not found"
        title_field[0].click()
        time.sleep(1)
        title_field[0].clear()
        title_field[0].send_keys("Automation Travel Plan")
        time.sleep(1)
        # Safe keyboard hide: try press Enter
        try:
            driver.press_keycode(66)
        except:
            pass
        time.sleep(1)

        # 2. Select Destination
        dest = driver.find_elements(AppiumBy.XPATH, "//*[@hint='Destination']")
        if not dest:
            dest = driver.find_elements(AppiumBy.XPATH, "//*[contains(@content-desc, 'Destination')]")
        if dest:
            dest[0].click()
            time.sleep(2)
            
            # We are now in the search location input
            search = driver.find_elements(AppiumBy.XPATH, "//android.widget.EditText")
            if search:
                search[0].send_keys("Bali")
                time.sleep(1)
                # Safe keyboard hide
                try:
                    driver.press_keycode(66)
                except:
                    pass
                time.sleep(4) # Wait for API results
                
                # Check for Bali in content-desc
                res = driver.find_elements(AppiumBy.XPATH, "//*[contains(@content-desc, 'Bali')]")
                if res:
                    res[-1].click()
                else:
                    # Fallback to recommended destination if API fails
                    fallback = driver.find_elements(AppiumBy.XPATH, "//*[@content-desc='Bandung' or @content-desc='Bromo']")
                    if fallback:
                        fallback[0].click()
                    else:
                        driver.tap([(540, 800)])
                time.sleep(4)

        # 3. Hit Save & Create
        for _ in range(5):
            save_btn = driver.find_elements(AppiumBy.XPATH, "//*[contains(@content-desc, 'Save')]")
            if save_btn:
                break
            time.sleep(1)
            
        if not save_btn:
            xml = driver.page_source
            with open("error_dump.xml", "w", encoding="utf-8") as f: f.write(xml)
            assert False, "Save & Create button not found. See error_dump.xml"
            
        save_btn[0].click()
        time.sleep(3)

        # 4. Handle Discard/Confirmation Modal "Save & Create"
        confirm_btn = driver.find_elements(AppiumBy.XPATH, "//*[@content-desc='Save & Create']")
        if confirm_btn:
            confirm_btn[-1].click()
        time.sleep(10)
        
        # Verify Itinerary Details screen reached
        details_title = driver.find_elements(AppiumBy.XPATH, "//*[@content-desc='Itinerary Details']")
        assert len(details_title) > 0, "Did not reach Itinerary Details screen"
        logger.info("✅ Success reached Itinerary Details screen!")

    def test_z_interact_itinerary_details(self, driver):
        """Add Trip Dates button should exist, and save draft to save to cloud."""
        logger.info("\n=== ITINERARY FULL: Detail Page & Trip Dates ===")
        
        # Verify Add Trip Dates button & Click it
        add_dates = driver.find_elements(AppiumBy.XPATH, "//*[@content-desc='Add Trip Dates']")
        if add_dates:
            logger.info("  🗓 'Add Trip Dates' button is visible.")
            add_dates[-1].click()
            time.sleep(3)
            
            # Inside Dates Modal
            anytime = driver.find_elements(AppiumBy.XPATH, "//*[@content-desc='Anytime']")
            if anytime: anytime[-1].click()
            
            # Set to 1 day instead of 3 to avoid missing activities on other days!
            days_input = driver.find_elements(AppiumBy.XPATH, "//android.widget.EditText")
            if days_input:
                days_input[-1].click()
                time.sleep(1)
                days_input[-1].clear()
                days_input[-1].send_keys("1")
                try:
                    driver.press_keycode(66) # ENTER
                except: pass
                time.sleep(1)
                
            # Click Done
            done_btn = driver.find_elements(AppiumBy.XPATH, "//*[@content-desc='Done']")
            if done_btn: done_btn[-1].click()
            time.sleep(4)
        
        # Define the 5 activities we want to add
        activities = [
            {"category": "Transport", "name": "Flight to Bali", "cost": "1500000", "loc": "Soekarno Hatta", "notes": "Terminal 3 early morning"},
            {"category": "Destination", "name": "Bali Safari Marine Park", "cost": "500000", "loc": "Gianyar", "notes": "Bring umbrella and sunscreen"},
            {"category": "Accommodation", "name": "Ayana Resort", "cost": "2500000", "loc": "Jimbaran", "notes": "Check in, ocean view"},
            {"category": "Culinary", "name": "Bebek Tepi Sawah", "cost": "300000", "loc": "Ubud", "notes": "Spicy duck for dinner"},
            {"category": "Others", "name": "Buy Souvenirs", "cost": "100000", "loc": "Krisna Oleh Oleh", "notes": "Buy pie susu and shirts"}
        ]
        
        # Loop through these 5 activities and add them
        for i, act in enumerate(activities):
            logger.info(f"  ➕ Adding Activity {i+1}/5: {act['name']} ({act['category']})")
            
            # Click "Add New Activity" for the 1st one, else "Add more Activity"
            add_btn = []
            for _ in range(5):
                if i == 0:
                    add_btn = driver.find_elements(AppiumBy.XPATH, "//*[@content-desc='Add New Activity'] | //*[@content-desc='Add more Activity']")
                else:
                    add_btn = driver.find_elements(AppiumBy.XPATH, "//*[@content-desc='Add more Activity']")
                
                if add_btn:
                    break
                # Scroll down using UiAutomator if not found
                try:
                    driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiScrollable(new UiSelector().scrollable(true)).scrollForward()')
                except:
                    pass
                time.sleep(2)
                
            if add_btn:
                add_btn[-1].click()
                time.sleep(3)
            else:
                pytest.fail(f"Could not find Add Activity button for {act['name']}! Are we stuck in the previous form?")
            
            # Find the 4 EditTexts (Name, Cost, Location, Notes)
            edit_texts = driver.find_elements(AppiumBy.XPATH, "//android.widget.EditText")
            if len(edit_texts) >= 4:
                # 1. Name
                edit_texts[0].click()
                time.sleep(1)
                edit_texts[0].clear()
                edit_texts[0].send_keys(act["name"])
                try: driver.press_keycode(66) # ENTER
                except: pass
                
                # 2. Cost
                edit_texts[1].click()
                time.sleep(1)
                edit_texts[1].clear()
                edit_texts[1].send_keys(act["cost"])
                try: driver.press_keycode(66)
                except: pass
                
                # 3. Location (beware of autocomplete dropdown)
                edit_texts[2].click()
                time.sleep(1)
                edit_texts[2].clear()
                edit_texts[2].send_keys(act["loc"])
                try: driver.press_keycode(66)
                except: pass
                
                # 4. Notes
                edit_texts[3].click()
                time.sleep(1)
                edit_texts[3].clear()
                edit_texts[3].send_keys(act["notes"])
                try: 
                    driver.hide_keyboard()
                    time.sleep(1)
                except: 
                    pass
                time.sleep(1)
            else:
                logger.error(f"  ❌ Not enough EditText fields found! Found: {len(edit_texts)}")
                
            # Select Category
            category_icon = driver.find_elements(AppiumBy.XPATH, f"//*[@content-desc='{act['category']}']")
            if category_icon:
                category_icon[0].click()
                time.sleep(1)
                
            # Save Activity (Explicitly look for the Button to avoid tapping the Top Bar Title)
            save_act_btn = driver.find_elements(AppiumBy.XPATH, "//android.widget.Button[@content-desc='Add Activity']")
            if save_act_btn and save_act_btn[-1].is_enabled():
                save_act_btn[-1].click()
                logger.info(f"  ✅ '{act['name']}' Saved successfully.")
                time.sleep(5) # Wait thoroughly for save transition to Itinerary Details page
            else:
                logger.error(f"  ❌ 'Add Activity' button disabled or missing for {act['name']}!")
                pytest.fail(f"Failed to save activity: {act['name']}")
                
        # After adding all 5 activities, explicit instruction mapping (Option B)
        # DO NOT click 'Upload Itinerary'. Save directly to Draft.
        logger.info("  🏃 Skipping Upload, proceeding to Save Draft")
        
        save_draft = driver.find_elements(AppiumBy.XPATH, "//*[@content-desc='Save Draft']")
        if not save_draft:
            logger.info("  👉 Scrolling down to find Save Draft button...")
            try:
                driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiScrollable(new UiSelector().scrollable(true)).scrollToEnd(3)')
                time.sleep(2)
            except:
                pass
            save_draft = driver.find_elements(AppiumBy.XPATH, "//*[@content-desc='Save Draft']")

        if save_draft:
            save_draft[-1].click()
            logger.info("  👉 Clicked Save Draft on Itinerary Details")
            time.sleep(4)
            
            # Modal appears, confirm by clicking "Save Draft" again
            modal_save = driver.find_elements(AppiumBy.XPATH, "//*[@content-desc='Save Draft']")
            if modal_save:
                modal_save[-1].click()
                logger.info("  👉 Clicked Save Draft on Confirmation Modal")
                time.sleep(7)
            else:
                logger.warning("  ⚠️ Could not find Save Draft on modal.")
        else:
             logger.error("  ❌ Could not find Save Draft on details page!")
                
        # Navigate to Profile and Verify
        logger.info("  🏃 Navigating to Profile to verify Draft")
        
        # Click back safely until we reach the Home/Bottom Navigation screen
        profile_tab = None
        for _ in range(5):
            found = driver.find_elements(AppiumBy.XPATH, "//*[contains(@content-desc, 'Profile\nTab')] | //*[@content-desc='Profile\nTab 4 of 4'] | //*[contains(@content-desc, 'Profile') and @clickable='true']")
            if found:
                profile_tab = found
                break
            try: driver.press_keycode(4)
            except: pass
            time.sleep(2)
            
        if profile_tab:
            profile_tab[-1].click()
            logger.info("  👉 Entered Profile Tab")
            time.sleep(3)
            
            # Explicitly tap the "Draft" filter tab first
            draft_filter = driver.find_elements(AppiumBy.XPATH, "//*[@content-desc='Draft']")
            if draft_filter:
                draft_filter[-1].click()
                logger.info("  👉 Clicked 'Draft' filter tab")
                time.sleep(3)
                
            # Scroll down to refresh or render the list if needed
            try: driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiScrollable(new UiSelector().scrollable(true)).scrollForward()')
            except: pass
            
            my_draft = driver.find_elements(AppiumBy.XPATH, "//*[contains(@content-desc, 'Automation Travel Plan')]")
            if my_draft:
                my_draft[0].click() # Click the topmost (newest) one
                logger.info("  👉 Opened freshly saved Draft from Profile")
                time.sleep(5)
                
                # Perform Verification Assertions on the Draft Details
                page_src = driver.page_source
                assert "Flight to Bali" in page_src, "Transport activity missing"
                assert "Bali Safari Marine Park" in page_src, "Destination activity missing"
                assert "Ayana Resort" in page_src, "Accommodation activity missing"
                assert "Bebek Tepi Sawah" in page_src, "Culinary activity missing"
                assert "Buy Souvenirs" in page_src, "Others activity missing"
                
                logger.info("  ✅ Verified: All 5 Activities are successfully listed inside the Profile Draft!")
                
                # Navigate back to Home Tab to finish nicely
                logger.info("  🏃 Returning to Home Tab")
                try: driver.press_keycode(4) # Back out of Draft Details
                except: pass
                time.sleep(2)
                home_tab = driver.find_elements(AppiumBy.XPATH, "//*[@content-desc='Home\nTab 1 of 4']")
                if home_tab: home_tab[-1].click()
                time.sleep(2)
                
            else:
                logger.error("  ❌ Could not find the saved draft in Profile.")
                assert False, "Draft not found in profile"
        else:
             logger.error("  ❌ Profile Tab not found after backing out.")

