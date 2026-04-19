"""
App Explorer Script
====================
Navigates through the Mepo Travel app and captures screenshots
of every reachable screen to map out all forms and fields.
"""

import time
import logging
import os
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(message)s')
logger = logging.getLogger(__name__)

SCREENSHOT_DIR = "reports/exploration"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

def screenshot(driver, name):
    path = f"{SCREENSHOT_DIR}/{name}.png"
    driver.save_screenshot(path)
    logger.info(f"📸 {path}")
    return path

def find_and_click(driver, locator, timeout=5):
    """Try to find and click an element, return True if success."""
    try:
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        el = WebDriverWait(driver, timeout).until(EC.presence_of_element_located(locator))
        el.click()
        time.sleep(2)
        return True
    except Exception:
        return False

def is_present(driver, locator, timeout=3):
    try:
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located(locator))
        return True
    except Exception:
        return False

def dump_page_source(driver, name):
    """Save page source XML for element inspection."""
    try:
        source = driver.page_source
        path = f"{SCREENSHOT_DIR}/{name}_source.xml"
        with open(path, "w", encoding="utf-8") as f:
            f.write(source)
        logger.info(f"📄 Page source saved: {path}")
    except Exception as e:
        logger.warning(f"⚠ Could not save page source: {e}")

def main():
    caps = {
        "platformName": "Android",
        "appium:automationName": "UiAutomator2",
        "appium:deviceName": "Pixel 6a",
        "appium:platformVersion": "14",
        "appium:appPackage": "com.mepo",
        "appium:appActivity": "com.mepo.MainActivity",
        "appium:noReset": True,   # Keep logged-in state
        "appium:fullReset": False,
        "appium:newCommandTimeout": 300,
        "appium:autoGrantPermissions": True,
    }

    logger.info("🚀 Starting Appium session...")
    options = UiAutomator2Options().load_capabilities(caps)
    driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
    logger.info("✅ Connected!")

    try:
        # Wait for app
        time.sleep(5)

        # ── 1. HOME SCREEN ──
        logger.info("═══ HOME SCREEN ═══")
        screenshot(driver, "01_home_screen")
        dump_page_source(driver, "01_home")

        # Scroll down to see more content
        size = driver.get_window_size()
        driver.swipe(size['width']//2, int(size['height']*0.8), 
                     size['width']//2, int(size['height']*0.2), 800)
        time.sleep(1)
        screenshot(driver, "01b_home_scrolled")
        dump_page_source(driver, "01b_home_scrolled")

        # Scroll back up
        driver.swipe(size['width']//2, int(size['height']*0.2),
                     size['width']//2, int(size['height']*0.8), 800)
        time.sleep(1)

        # ── 2. OPEN TRIP ──
        logger.info("═══ OPEN TRIP ═══")
        if find_and_click(driver, (AppiumBy.XPATH, "//*[@text='Open Trip']")):
            time.sleep(3)
            screenshot(driver, "02_open_trip_list")
            dump_page_source(driver, "02_open_trip")

            # Scroll to see more trips
            driver.swipe(size['width']//2, int(size['height']*0.8),
                         size['width']//2, int(size['height']*0.2), 800)
            time.sleep(1)
            screenshot(driver, "02b_open_trip_scrolled")

            # Try to tap the first trip card
            try:
                cards = driver.find_elements(AppiumBy.XPATH, 
                    "//android.widget.ImageView[contains(@content-desc, '')]")
                if not cards:
                    cards = driver.find_elements(AppiumBy.XPATH, "//android.view.View")
                if len(cards) > 5:
                    cards[5].click()
                    time.sleep(3)
                    screenshot(driver, "02c_trip_detail")
                    dump_page_source(driver, "02c_trip_detail")
                    # Back
                    driver.back()
                    time.sleep(2)
            except Exception as e:
                logger.warning(f"Could not open trip detail: {e}")

            driver.back()
            time.sleep(2)

        # ── 3. CREATE NEW ITINERARY ──
        logger.info("═══ CREATE NEW ITINERARY ═══")
        if find_and_click(driver, (AppiumBy.XPATH, "//*[contains(@text, 'Create New Itinerary')]")) or \
           find_and_click(driver, (AppiumBy.XPATH, "//*[contains(@content-desc, 'Create New Itinerary')]")):
            time.sleep(3)
            screenshot(driver, "03_create_itinerary")
            dump_page_source(driver, "03_create_itinerary")

            # Scroll form
            driver.swipe(size['width']//2, int(size['height']*0.8),
                         size['width']//2, int(size['height']*0.2), 800)
            time.sleep(1)
            screenshot(driver, "03b_create_itinerary_scrolled")
            dump_page_source(driver, "03b_create_itinerary_scrolled")

            driver.back()
            time.sleep(2)

        # ── 4. PROFILE ──
        logger.info("═══ PROFILE ═══")
        # Try profile icon (top right) or tab
        profile_found = find_and_click(driver, (AppiumBy.ACCESSIBILITY_ID, "Profile"))
        if not profile_found:
            # Try the profile icon on top right
            profile_found = find_and_click(driver, (AppiumBy.XPATH, "//*[contains(@content-desc, 'Profile')]"))
        if not profile_found:
            # Try person icon
            profile_found = find_and_click(driver, (AppiumBy.XPATH, "(//*[contains(@content-desc, '')])[last()]"))
        
        if profile_found:
            time.sleep(3)
            screenshot(driver, "04_profile")
            dump_page_source(driver, "04_profile")

            # Scroll profile
            driver.swipe(size['width']//2, int(size['height']*0.8),
                         size['width']//2, int(size['height']*0.2), 800)
            time.sleep(1)
            screenshot(driver, "04b_profile_scrolled")
            dump_page_source(driver, "04b_profile_scrolled")

            # Look for Edit Profile button
            if find_and_click(driver, (AppiumBy.XPATH, "//*[contains(@text, 'Edit')]")) or \
               find_and_click(driver, (AppiumBy.XPATH, "//*[contains(@content-desc, 'Edit')]")):
                time.sleep(2)
                screenshot(driver, "04c_edit_profile")
                dump_page_source(driver, "04c_edit_profile")

                # Scroll edit profile form
                driver.swipe(size['width']//2, int(size['height']*0.8),
                             size['width']//2, int(size['height']*0.2), 800)
                time.sleep(1)
                screenshot(driver, "04d_edit_profile_scrolled")
                dump_page_source(driver, "04d_edit_profile_scrolled")

                driver.back()
                time.sleep(2)

            driver.back()
            time.sleep(2)

        # ── 5. SEARCH ──
        logger.info("═══ SEARCH ═══")
        if find_and_click(driver, (AppiumBy.XPATH, "//*[contains(@content-desc, 'Search')]")):
            time.sleep(2)
            screenshot(driver, "05_search")
            dump_page_source(driver, "05_search")
            driver.back()
            time.sleep(2)

        # ── 6. NOTIFICATION ──
        logger.info("═══ NOTIFICATION ═══")
        if find_and_click(driver, (AppiumBy.XPATH, "//*[contains(@content-desc, 'Notification')]")):
            time.sleep(2)
            screenshot(driver, "06_notification")
            dump_page_source(driver, "06_notification")
            driver.back()
            time.sleep(2)

        logger.info("✅ Exploration complete!")

    finally:
        driver.quit()
        logger.info("🔚 Session closed")

if __name__ == "__main__":
    main()
