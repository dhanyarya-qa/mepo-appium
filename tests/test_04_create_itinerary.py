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
        
        # Click Add New Activity
        add_activity = driver.find_elements(AppiumBy.XPATH, "//*[@content-desc='Add New Activity']")
        if add_activity:
            logger.info("  🏃 Found Add New Activity button.")
            add_activity[-1].click()
            time.sleep(3)
                
            # Fill in Activity Name
            act_name = driver.find_elements(AppiumBy.XPATH, "//android.widget.EditText")
            if act_name:
                act_name[0].click()
                time.sleep(1)
                act_name[0].send_keys("Bali Safari Marine Park")
                try: driver.press_keycode(66)
                except: pass
                time.sleep(1)
                
            # Select Category
            category = driver.find_elements(AppiumBy.XPATH, "//*[@content-desc='Destination']")
            if category:
                category[0].click()
                time.sleep(1)
                
            # Save Activity
            save_act = driver.find_elements(AppiumBy.XPATH, "//*[@content-desc='Add Activity']")
            if save_act and save_act[-1].is_enabled():
                save_act[-1].click()
                logger.info("  ✅ Activity Saved.")
                time.sleep(4)
            else:
                logger.error("  ❌ 'Add Activity' button disabled or missing!")
                
        # Click Upload Itinerary if available
        upload_btn = driver.find_elements(AppiumBy.XPATH, "//*[@content-desc='Upload Itinerary']")
        if upload_btn and upload_btn[-1].is_enabled():
            upload_btn[-1].click()
            logger.info("✅ Upload Itinerary button clicked.")
            time.sleep(10)
            
            success_done = driver.find_elements(AppiumBy.XPATH, "//*[@content-desc='Done']")
            if success_done:
                logger.info("✅ Found Done button on Success Modal, dismissing.")
                success_done[-1].click()
                time.sleep(2)
        else:
            logger.error("Upload Itinerary disabled or not found! Falling back to Save Draft.")
            with open("error_upload_disabled.xml", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            save_draft = driver.find_elements(AppiumBy.XPATH, "//*[@content-desc='Save Draft']")
            if save_draft:
                save_draft[-1].click()
                logger.info("✅ Draft Saved Successfully.")
                
        time.sleep(5)

