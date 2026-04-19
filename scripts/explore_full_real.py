"""
Full App Exploration — Real Device
===================================
Login → Home → Open Trip → Itinerary → Profile → Map all UI elements
"""
import time, logging, os
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(message)s')
logger = logging.getLogger(__name__)

OUT = "reports/real_device"
os.makedirs(OUT, exist_ok=True)

import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.settings import AppiumConfig

caps = AppiumConfig.DESIRED_CAPS.copy()
caps['appium:udid'] = '192.168.1.62:39845'

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

def swipe_down(driver):
    s = driver.get_window_size()
    driver.swipe(s['width']//2, int(s['height']*0.25), s['width']//2, int(s['height']*0.75), 800)

# ──────────────────────────────────────────────────
logger.info("🔗 Connecting...")
options = UiAutomator2Options().load_capabilities(caps)
driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
logger.info("✅ Connected")
time.sleep(8)

# ══════════════════════════════════════════════════
# 1. LOGIN SCREEN
# ══════════════════════════════════════════════════
logger.info("\n══ LOGIN SCREEN ══")
save(driver, "explore_01_login")
save_xml(driver, "explore_01_login")

# Login
try:
    edits = driver.find_elements(AppiumBy.XPATH, "//android.widget.EditText")
    logger.info(f"Found {len(edits)} EditText fields")
    if len(edits) >= 2:
        edits[0].click(); time.sleep(0.3); edits[0].send_keys("danip1@yopmail.com")
        logger.info("📧 Email entered")
        edits[1].click(); time.sleep(0.3); edits[1].send_keys("Sandi123!")
        logger.info("🔑 Password entered")
        try: driver.hide_keyboard()
        except: pass
        
        # Find and click Login button
        for loc in [
            (AppiumBy.ACCESSIBILITY_ID, "Login"),
            (AppiumBy.XPATH, "//*[@text='Login']"),
            (AppiumBy.XPATH, "//*[contains(@content-desc, 'Login')]"),
        ]:
            try:
                el = driver.find_element(*loc)
                el.click()
                logger.info(f"🔓 Login clicked via {loc[0]}")
                break
            except: continue
        
        time.sleep(8)
        save(driver, "explore_02_after_login")
        save_xml(driver, "explore_02_after_login")
        logger.info(f"📱 After login: {driver.current_package}")
except Exception as e:
    logger.error(f"Login error: {e}")

# ══════════════════════════════════════════════════
# 2. HOME SCREEN — Full scroll
# ══════════════════════════════════════════════════
logger.info("\n══ HOME SCREEN ══")
save(driver, "explore_03_home_top")
save_xml(driver, "explore_03_home")

for i in range(6):
    swipe_up(driver)
    time.sleep(1.5)
    save(driver, f"explore_04_home_scroll_{i+1}")
    if i == 2:
        save_xml(driver, f"explore_04_home_mid")

# Save bottom XML
save_xml(driver, "explore_04_home_bottom")

# Scroll back to top
for _ in range(6):
    swipe_down(driver)
    time.sleep(0.5)

# ══════════════════════════════════════════════════
# 3. OPEN TRIP TAB
# ══════════════════════════════════════════════════
logger.info("\n══ OPEN TRIP TAB ══")
try:
    for loc in [
        (AppiumBy.ACCESSIBILITY_ID, "Open Trip"),
        (AppiumBy.XPATH, "//*[contains(@content-desc, 'Open Trip')]"),
    ]:
        try:
            els = driver.find_elements(*loc)
            # Click the LAST match (likely the bottom tab, not the card)
            if els:
                els[-1].click()
                logger.info(f"🧭 Clicked Open Trip tab")
                break
        except: continue
    
    time.sleep(5)
    save(driver, "explore_05_opentrip_top")
    save_xml(driver, "explore_05_opentrip")
    
    for i in range(8):
        swipe_up(driver)
        time.sleep(1.5)
        save(driver, f"explore_06_opentrip_scroll_{i+1}")
        if i == 4:
            save_xml(driver, "explore_06_opentrip_mid")
    
    save_xml(driver, "explore_06_opentrip_bottom")
    
except Exception as e:
    logger.error(f"Open Trip error: {e}")

# ══════════════════════════════════════════════════
# 4. ITINERARY TAB  
# ══════════════════════════════════════════════════
logger.info("\n══ ITINERARY TAB ══")
try:
    for loc in [
        (AppiumBy.ACCESSIBILITY_ID, "Itinerary"),
        (AppiumBy.XPATH, "//*[contains(@content-desc, 'Itinerary')]"),
    ]:
        try:
            els = driver.find_elements(*loc)
            if els:
                els[-1].click()
                logger.info("📋 Clicked Itinerary tab")
                break
        except: continue
    
    time.sleep(5)
    save(driver, "explore_07_itinerary_top")
    save_xml(driver, "explore_07_itinerary")
    
    for i in range(4):
        swipe_up(driver)
        time.sleep(1.5)
        save(driver, f"explore_08_itinerary_scroll_{i+1}")
    
    save_xml(driver, "explore_08_itinerary_scroll")
    
except Exception as e:
    logger.error(f"Itinerary error: {e}")

# ══════════════════════════════════════════════════
# 5. PROFILE TAB
# ══════════════════════════════════════════════════
logger.info("\n══ PROFILE TAB ══")
try:
    for loc in [
        (AppiumBy.ACCESSIBILITY_ID, "Profile"),
        (AppiumBy.XPATH, "//*[contains(@content-desc, 'Profile')]"),
    ]:
        try:
            els = driver.find_elements(*loc)
            if els:
                els[-1].click()
                logger.info("👤 Clicked Profile tab")
                break
        except: continue
    
    time.sleep(5)
    save(driver, "explore_09_profile_top")
    save_xml(driver, "explore_09_profile")
    
    for i in range(4):
        swipe_up(driver)
        time.sleep(1.5)
        save(driver, f"explore_10_profile_scroll_{i+1}")
    
    save_xml(driver, "explore_10_profile_bottom")
    
except Exception as e:
    logger.error(f"Profile error: {e}")

# ══════════════════════════════════════════════════
# DONE
# ══════════════════════════════════════════════════
driver.quit()
logger.info("\n✅ EXPLORATION COMPLETE!")
