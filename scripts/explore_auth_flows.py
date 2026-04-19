import time
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.options.android import UiAutomator2Options

caps = {
    "platformName": "Android",
    "appium:automationName": "UiAutomator2",
    "appium:udid": "192.168.1.62:42733",
    "appium:appPackage": "com.mepo",
    "appium:appActivity": "com.mepo.MainActivity",
    "appium:noReset": True
}
options = UiAutomator2Options()
for k, v in caps.items(): options.set_capability(k, v)

driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
driver.implicitly_wait(10)
time.sleep(5)

# Tap Register
register_btn = driver.find_element(AppiumBy.XPATH, "//*[@content-desc='Register']")
register_btn.click()
time.sleep(3)

# Dump Register Screen
xml = driver.page_source
with open("register_screen.xml", "w", encoding="utf-8") as f:
    f.write(xml)

# Go back to login
driver.back()
time.sleep(2)

# Tap Forgot Password
forgot_btn = driver.find_element(AppiumBy.XPATH, "//*[@content-desc='Forgot Password?']")
forgot_btn.click()
time.sleep(3)

# Dump Forgot Password Screen
xml2 = driver.page_source
with open("forgot_screen.xml", "w", encoding="utf-8") as f:
    f.write(xml2)

print("Screens dumped to register_screen.xml and forgot_screen.xml")
driver.quit()
