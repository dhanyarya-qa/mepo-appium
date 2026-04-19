"""
Deep Explorer — Open Trip & Full App
======================================
Explores deeper into Open Trip (banners, Custom Your Trip, itinerary references)
and other undiscovered features.
"""
import time, logging, os
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(message)s')
logger = logging.getLogger(__name__)

DIR = "reports/exploration_deep"
os.makedirs(DIR, exist_ok=True)

def ss(driver, name):
    path = f"{DIR}/{name}.png"
    driver.save_screenshot(path)
    logger.info(f"📸 {path}")

def xml(driver, name):
    with open(f"{DIR}/{name}.xml", "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    logger.info(f"📄 {DIR}/{name}.xml")

def present(driver, locator, timeout=3):
    try:
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located(locator))
        return True
    except: return False

def click(driver, locator, timeout=5):
    try:
        el = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(locator))
        el.click(); time.sleep(2); return True
    except: return False

def swipe_up(driver, pct=0.6):
    s = driver.get_window_size()
    driver.swipe(s['width']//2, int(s['height']*0.8), s['width']//2, int(s['height']*(0.8-pct)), 800)
    time.sleep(1.5)

def swipe_down(driver, pct=0.6):
    s = driver.get_window_size()
    driver.swipe(s['width']//2, int(s['height']*0.2), s['width']//2, int(s['height']*(0.2+pct)), 800)
    time.sleep(1.5)

def main():
    caps = {
        "platformName": "Android",
        "appium:automationName": "UiAutomator2",
        "appium:deviceName": "Pixel 6a",
        "appium:platformVersion": "14",
        "appium:appPackage": "com.mepo",
        "appium:appActivity": "com.mepo.MainActivity",
        "appium:noReset": True,
        "appium:fullReset": False,
        "appium:newCommandTimeout": 300,
        "appium:autoGrantPermissions": True,
    }
    options = UiAutomator2Options().load_capabilities(caps)
    driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
    logger.info("✅ Connected")
    time.sleep(5)

    try:
        # ══════════════════════════════════════
        # HOME SCREEN — full exploration
        # ══════════════════════════════════════
        logger.info("══ HOME SCREEN ══")
        ss(driver, "home_01_top")
        xml(driver, "home_01")
        
        # Scroll down to see everything on home
        swipe_up(driver, 0.5)
        ss(driver, "home_02_mid")
        xml(driver, "home_02")
        
        swipe_up(driver, 0.5)
        ss(driver, "home_03_bottom")
        xml(driver, "home_03")
        
        swipe_up(driver, 0.5)
        ss(driver, "home_04_more")
        xml(driver, "home_04")
        
        # Scroll back up
        for _ in range(4): swipe_down(driver, 0.5)
        time.sleep(1)

        # ══════════════════════════════════════
        # OPEN TRIP — deep exploration
        # ══════════════════════════════════════
        logger.info("══ OPEN TRIP — DEEP ══")
        if click(driver, (AppiumBy.XPATH, "//*[@text='Open Trip']")) or \
           click(driver, (AppiumBy.XPATH, "//*[contains(@content-desc, 'Open Trip')]")):
            time.sleep(3)
            ss(driver, "opentrip_01_top")
            xml(driver, "opentrip_01")
            
            # Scroll through Open Trip page
            for i in range(8):
                swipe_up(driver, 0.5)
                ss(driver, f"opentrip_{i+2:02d}_scroll")
                xml(driver, f"opentrip_{i+2:02d}")
                logger.info(f"  Scroll #{i+1}")
            
            # Scroll back to top
            for _ in range(10): swipe_down(driver, 0.5)
            time.sleep(1)
            
            # Back to home
            driver.back()
            time.sleep(2)
        
        # ══════════════════════════════════════
        # PROFILE — deep exploration
        # ══════════════════════════════════════
        logger.info("══ PROFILE — DEEP ══")
        # Try the profile icon (person icon top right)
        profile_clicked = False
        # Try various profile entry points
        for loc in [
            (AppiumBy.XPATH, "(//android.widget.ImageView)[last()]"),
            (AppiumBy.XPATH, "//*[contains(@content-desc, 'profile')]"),
            (AppiumBy.XPATH, "//*[contains(@content-desc, 'Profile')]"),
            (AppiumBy.XPATH, "//*[contains(@content-desc, 'Account')]"),
        ]:
            if click(driver, loc, timeout=3):
                time.sleep(3)
                ss(driver, "profile_01_main")
                xml(driver, "profile_01")
                profile_clicked = True
                
                # Scroll through profile
                for i in range(4):
                    swipe_up(driver, 0.5)
                    ss(driver, f"profile_{i+2:02d}_scroll")
                    xml(driver, f"profile_{i+2:02d}")
                
                # Look for Edit Profile, Settings, Logout
                for _ in range(5): swipe_down(driver, 0.5)
                
                # Look for any buttons/links
                try:
                    buttons = driver.find_elements(AppiumBy.XPATH, "//android.widget.Button")
                    logger.info(f"  Found {len(buttons)} buttons on profile")
                    for btn in buttons:
                        desc = btn.get_attribute("content-desc") or btn.text or "no-desc"
                        logger.info(f"    Button: {desc}")
                except: pass
                
                # Try settings
                for settings_loc in [
                    (AppiumBy.XPATH, "//*[contains(@content-desc, 'Settings')]"),
                    (AppiumBy.XPATH, "//*[contains(@content-desc, 'Setting')]"),
                    (AppiumBy.XPATH, "//*[contains(@content-desc, 'Pengaturan')]"),
                ]:
                    if click(driver, settings_loc, timeout=2):
                        time.sleep(2)
                        ss(driver, "settings_01")
                        xml(driver, "settings_01")
                        
                        swipe_up(driver, 0.5)
                        ss(driver, "settings_02")
                        xml(driver, "settings_02")
                        
                        driver.back()
                        time.sleep(1)
                        break
                
                # Look for Logout
                for logout_loc in [
                    (AppiumBy.XPATH, "//*[contains(@content-desc, 'Logout')]"),
                    (AppiumBy.XPATH, "//*[contains(@content-desc, 'Log Out')]"),
                    (AppiumBy.XPATH, "//*[contains(@content-desc, 'Sign Out')]"),
                    (AppiumBy.XPATH, "//*[contains(@content-desc, 'Keluar')]"),
                    (AppiumBy.XPATH, "//*[contains(@text, 'Logout')]"),
                    (AppiumBy.XPATH, "//*[contains(@text, 'Log out')]"),
                ]:
                    if present(driver, logout_loc, timeout=2):
                        logger.info(f"  🔍 Found Logout: {logout_loc}")
                        break
                
                driver.back()
                time.sleep(2)
                break
        
        if not profile_clicked:
            logger.warning("⚠ Could not find profile entry point")

        # ══════════════════════════════════════
        # BOTTOM NAVIGATION TABS
        # ══════════════════════════════════════
        logger.info("══ BOTTOM NAV ══")
        # Check for bottom navigation
        for tab_name in ["Home", "Itinerary", "Wishlist", "Chat", "Profile"]:
            loc = (AppiumBy.ACCESSIBILITY_ID, tab_name)
            if present(driver, loc, timeout=2):
                logger.info(f"  Tab found: {tab_name}")
                if tab_name != "Home":
                    if click(driver, loc, timeout=3):
                        time.sleep(3)
                        ss(driver, f"tab_{tab_name.lower()}_01")
                        xml(driver, f"tab_{tab_name.lower()}_01")
                        
                        swipe_up(driver, 0.5)
                        ss(driver, f"tab_{tab_name.lower()}_02")
                        xml(driver, f"tab_{tab_name.lower()}_02")

        # Go back to Home
        click(driver, (AppiumBy.ACCESSIBILITY_ID, "Home"), timeout=3)
        time.sleep(2)

        logger.info("✅ Deep exploration complete!")

    finally:
        driver.quit()
        logger.info("🔚 Done")

if __name__ == "__main__":
    main()
