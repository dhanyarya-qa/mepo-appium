import time
from appium import webdriver
from appium.options.android import UiAutomator2Options

caps = {
    "platformName": "Android",
    "appium:automationName": "UiAutomator2",
    "appium:udid": "192.168.1.62:39845",
    "appium:appPackage": "com.mepo",
    "appium:appActivity": "com.mepo.MainActivity",
    "appium:noReset": True
}
options = UiAutomator2Options()
for k, v in caps.items(): options.set_capability(k, v)

driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
driver.implicitly_wait(10)
time.sleep(5)

# Try dumping the current screen
xml = driver.page_source
with open("current_screen.xml", "w", encoding="utf-8") as f:
    f.write(xml)

print("Screen dumped to current_screen.xml")
driver.quit()
