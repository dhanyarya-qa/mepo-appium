"""Quick test — connect to real device & click Open Trip"""
import time, logging
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(message)s')
logger = logging.getLogger(__name__)

caps = {
    "platformName": "Android",
    "appium:automationName": "UiAutomator2",
    "appium:deviceName": "23124RA7EO",
    "appium:platformVersion": "15",
    "appium:udid": "192.168.1.62:39845",
    "appium:appPackage": "com.mepo",
    "appium:appActivity": "com.mepo.MainActivity",
    "appium:noReset": True,
    "appium:newCommandTimeout": 300,
    "appium:forceAppLaunch": True,
    "appium:appWaitDuration": 30000,
}

options = UiAutomator2Options().load_capabilities(caps)
logger.info("🔗 Connecting to real device via WiFi...")
driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
logger.info(f"✅ Connected! Session: {driver.session_id}")
time.sleep(5)

# Screenshot home
driver.save_screenshot("reports/real_device/01_home.png")
pkg = driver.current_package
logger.info(f"📱 Current package: {pkg}")

# Click Open Trip
try:
    for loc in [
        (AppiumBy.XPATH, "//*[contains(@content-desc, 'Open Trip')]"),
        (AppiumBy.XPATH, "//*[@text='Open Trip']"),
    ]:
        try:
            el = driver.find_element(*loc)
            logger.info(f"Found Open Trip: {loc}")
            el.click()
            logger.info("✅ Clicked Open Trip!")
            break
        except:
            continue
    
    time.sleep(5)
    pkg2 = driver.current_package
    logger.info(f"📱 Package AFTER click: {pkg2}")
    
    if pkg2 == "com.mepo":
        logger.info("🎉 APP DID NOT CRASH! Open Trip is working!")
        driver.save_screenshot("reports/real_device/02_open_trip.png")
        
        # Scroll down to explore
        size = driver.get_window_size()
        for i in range(5):
            driver.swipe(size['width']//2, int(size['height']*0.8),
                        size['width']//2, int(size['height']*0.3), 800)
            time.sleep(1.5)
            driver.save_screenshot(f"reports/real_device/03_scroll_{i+1}.png")
            logger.info(f"📸 Scroll #{i+1}")
        
        # Save page source
        with open("reports/real_device/open_trip_source.xml", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        logger.info("📄 Page source saved")
    else:
        logger.error(f"❌ App crashed! Now at: {pkg2}")

except Exception as e:
    logger.error(f"❌ Error: {e}")

driver.quit()
logger.info("Done!")
