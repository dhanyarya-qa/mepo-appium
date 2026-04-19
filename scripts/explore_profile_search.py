"""
Explore Profile & Search — Real Device
========================================
Navigate via top-right icons (not tabs) to profile and search.
"""
import time, logging, os
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(message)s')
logger = logging.getLogger(__name__)

OUT = "reports/real_device"
os.makedirs(OUT, exist_ok=True)

caps = {
    "platformName": "Android",
    "appium:automationName": "UiAutomator2",
    "appium:deviceName": "23124RA7EO",
    "appium:platformVersion": "15",
    "appium:udid": "192.168.1.62:41821",
    "appium:appPackage": "com.mepo",
    "appium:appActivity": "com.mepo.MainActivity",
    "appium:noReset": True,  # Keep logged in from previous run
    "appium:newCommandTimeout": 300,
    "appium:forceAppLaunch": True,
    "appium:appWaitDuration": 30000,
    "appium:autoGrantPermissions": True,
}

def save(driver, name):
    path = f"{OUT}/{name}.png"
    driver.save_screenshot(path)
    logger.info(f"📸 {path}")

def save_xml(driver, name):
    path = f"{OUT}/{name}.xml"
    with open(path, "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    logger.info(f"📄 {path}")

def swipe_up(driver):
    s = driver.get_window_size()
    driver.swipe(s['width']//2, int(s['height']*0.75), s['width']//2, int(s['height']*0.25), 800)

logger.info("🔗 Connecting...")
options = UiAutomator2Options().load_capabilities(caps)
driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
logger.info("✅ Connected")
time.sleep(5)

save(driver, "profile_01_home")
save_xml(driver, "profile_01_home")

# ══════════════════════════════════════════════════
# PROFILE — Click person icon at top-right (bounds [921,201][1036,289])
# ══════════════════════════════════════════════════
logger.info("\n══ PROFILE ICON ══")
try:
    # The third clickable icon in top-right area
    # From XML: bounds="[921,201][1036,289]" — person icon
    driver.tap([(978, 245)], 500)  # Center of [921,201][1036,289]
    time.sleep(5)
    save(driver, "profile_02_after_tap")
    save_xml(driver, "profile_02_after_tap")
    
    # Scroll down on profile page
    for i in range(3):
        swipe_up(driver)
        time.sleep(1.5)
        save(driver, f"profile_03_scroll_{i+1}")
    
    save_xml(driver, "profile_03_scrolled")
    
    # Go back to home
    driver.back()
    time.sleep(3)
    save(driver, "profile_04_back_home")
    
except Exception as e:
    logger.error(f"Profile error: {e}")
    driver.back()
    time.sleep(2)

# ══════════════════════════════════════════════════
# SEARCH — Click search icon at top (bounds [690,201][805,289])
# ══════════════════════════════════════════════════
logger.info("\n══ SEARCH ICON ══")
try:
    driver.tap([(747, 245)], 500)  # Center of [690,201][805,289]
    time.sleep(5)
    save(driver, "search_01_after_tap")
    save_xml(driver, "search_01_after_tap")
    
    # Go back
    driver.back()
    time.sleep(3)
    
except Exception as e:
    logger.error(f"Search error: {e}")
    driver.back()
    time.sleep(2)

# ══════════════════════════════════════════════════
# NOTIFICATIONS — Click bell icon (bounds [805,201][921,289])
# ══════════════════════════════════════════════════
logger.info("\n══ NOTIFICATIONS ICON ══")
try:
    driver.tap([(863, 245)], 500)  # Center of [805,201][921,289]
    time.sleep(5)
    save(driver, "notif_01_after_tap")
    save_xml(driver, "notif_01_after_tap")
    
    # Go back
    driver.back()
    time.sleep(3)
    
except Exception as e:
    logger.error(f"Notification error: {e}")
    driver.back()
    time.sleep(2)

# ══════════════════════════════════════════════════
# CREATE ITINERARY — Click the CTA button
# ══════════════════════════════════════════════════
logger.info("\n══ CREATE ITINERARY ══")
try:
    # Scroll down to find Create New Itinerary
    for _ in range(3):
        el = driver.find_elements(AppiumBy.XPATH, "//*[@content-desc='Create New Itinerary']")
        if el:
            el[0].click()
            logger.info("✅ Create New Itinerary clicked")
            time.sleep(5)
            save(driver, "itinerary_01_create_page")
            save_xml(driver, "itinerary_01_create_page")
            
            # Scroll create itinerary page
            for i in range(3):
                swipe_up(driver)
                time.sleep(1.5)
                save(driver, f"itinerary_02_scroll_{i+1}")
            
            save_xml(driver, "itinerary_02_scrolled")
            break
        swipe_up(driver)
        time.sleep(1.5)
    
    driver.back()
    time.sleep(3)
    
except Exception as e:
    logger.error(f"Itinerary error: {e}")
    driver.back()
    time.sleep(2)

# ══════════════════════════════════════════════════
# OPEN TRIP CARD — Click the Open Trip service card
# ══════════════════════════════════════════════════
logger.info("\n══ OPEN TRIP CARD ══")
try:
    # Go to home first
    save(driver, "opentrip_00_current")
    
    # Find Open Trip card (content-desc="Open Trip\nOpen Trip")
    el = driver.find_elements(AppiumBy.XPATH, 
        "//*[starts-with(@content-desc, 'Open Trip')]")
    if el:
        el[0].click()
        logger.info("✅ Open Trip card clicked")
        time.sleep(5)
        save(driver, "opentrip_01_page")
        save_xml(driver, "opentrip_01_page")
        
        # Click a trip card
        trip_cards = driver.find_elements(AppiumBy.XPATH,
            "//*[contains(@content-desc, 'Ke madura') or contains(@content-desc, 'Trip ke')]")
        if trip_cards:
            trip_cards[0].click()
            time.sleep(5)
            save(driver, "opentrip_02_detail")
            save_xml(driver, "opentrip_02_detail")
            
            # Scroll trip detail
            for i in range(3):
                swipe_up(driver)
                time.sleep(1.5)
                save(driver, f"opentrip_03_detail_scroll_{i+1}")
            
            save_xml(driver, "opentrip_03_detail_scrolled")
            driver.back()
            time.sleep(3)
        
        # Click Custom Your Trip
        custom = driver.find_elements(AppiumBy.XPATH,
            "//*[contains(@content-desc, 'Custom Your Trip')]")
        if not custom:
            for _ in range(5):
                swipe_up(driver)
                time.sleep(1)
                custom = driver.find_elements(AppiumBy.XPATH,
                    "//*[contains(@content-desc, 'Custom Your Trip')]")
                if custom:
                    break
        
        if custom:
            custom[0].click()
            time.sleep(5)
            save(driver, "opentrip_04_custom_trip")
            save_xml(driver, "opentrip_04_custom_trip")
            
            for i in range(3):
                swipe_up(driver)
                time.sleep(1.5)
                save(driver, f"opentrip_05_custom_scroll_{i+1}")
            
            save_xml(driver, "opentrip_05_custom_scrolled")
            driver.back()
            time.sleep(3)
        
        driver.back()
        time.sleep(3)
        
except Exception as e:
    logger.error(f"Open Trip error: {e}")
    driver.back()
    time.sleep(2)

driver.quit()
logger.info("\n✅ DEEP EXPLORATION COMPLETE!")
