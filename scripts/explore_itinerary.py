import time
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy

def main():
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
    time.sleep(3)
    
    # Click confirmation Save & Create
    print("Clicking confirmation Save & Create")
    confirm = driver.find_elements(AppiumBy.XPATH, "//*[@content-desc='Save & Create']")
    if confirm:
        confirm[-1].click() # Click the button not the text wrapper
        time.sleep(10)
            
    # Dump Screen
    print("Dumping Screen...")
    xml = driver.page_source
    with open("activity_screen.xml", "w", encoding="utf-8") as f:
        f.write(xml)
    print("Done")
    driver.quit()

if __name__ == "__main__":
    main()
