"""Quick test — click Open Trip and check what happens"""
import time, logging
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(message)s')
logger = logging.getLogger(__name__)

caps = {
    "platformName": "Android",
    "appium:automationName": "UiAutomator2",
    "appium:deviceName": "Pixel 6a",
    "appium:platformVersion": "14",
    "appium:appPackage": "com.mepo",
    "appium:appActivity": "com.mepo.MainActivity",
    "appium:noReset": True,
    "appium:newCommandTimeout": 300,
}
options = UiAutomator2Options().load_capabilities(caps)
driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
logger.info("✅ Connected")
time.sleep(5)

# Take screenshot
driver.save_screenshot("reports/exploration_deep/test_click_01_before.png")
logger.info("📸 Before click")

# Get current package
pkg = driver.current_package
logger.info(f"Current package BEFORE: {pkg}")

# Try to click Open Trip
try:
    el = driver.find_element(AppiumBy.XPATH, "//*[@text='Open Trip']")
    logger.info(f"Found 'Open Trip' element: {el.text}")
    el.click()
    logger.info("✅ Clicked Open Trip")
except Exception as e:
    logger.error(f"❌ Could not find/click Open Trip by text: {e}")
    try:
        el = driver.find_element(AppiumBy.XPATH, "//*[contains(@content-desc, 'Open Trip')]")
        logger.info(f"Found by content-desc: {el.get_attribute('content-desc')}")
        el.click()
        logger.info("✅ Clicked Open Trip (content-desc)")
    except Exception as e2:
        logger.error(f"❌ Also failed by content-desc: {e2}")

time.sleep(5)

# Check where we are now
pkg2 = driver.current_package
activity = driver.current_activity
logger.info(f"Current package AFTER: {pkg2}")
logger.info(f"Current activity AFTER: {activity}")

driver.save_screenshot("reports/exploration_deep/test_click_02_after.png")
logger.info("📸 After click")

# Get page source for debugging
with open("reports/exploration_deep/test_click_after_source.xml", "w", encoding="utf-8") as f:
    f.write(driver.page_source)
logger.info("📄 Page source saved")

driver.quit()
logger.info("Done!")
