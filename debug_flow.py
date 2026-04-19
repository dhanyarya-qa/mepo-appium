import time
import sys
from appium import webdriver
from appium.options.android import UiAutomator2Options
from tests.test_04_create_itinerary import TestCompleteItineraryCreation

def main():
    caps = {
        "platformName": "Android",
        "appium:automationName": "UiAutomator2",
        "appium:udid": "192.168.1.62:38549",
        "appium:appPackage": "com.mepo",
        "appium:appActivity": "com.mepo.MainActivity",
        "appium:noReset": True
    }
    options = UiAutomator2Options()
    for k, v in caps.items(): options.set_capability(k, v)
    
    driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
    driver.implicitly_wait(10)
    time.sleep(3)
    
    # Reset app manually
    print("Resetting app...")
    try: driver.terminate_app("com.mepo")
    except: pass
    time.sleep(2)
    driver.activate_app("com.mepo")
    time.sleep(5)
    
    test_obj = TestCompleteItineraryCreation()
    
    try:
        test_obj.test_z_fill_form_and_save(driver)
        print("SUCCESS test_z_fill_form_and_save")
    except Exception as e:
        import traceback
        traceback.print_exc()
        print("FAILED test_z_fill_form_and_save")
        
    driver.quit()

if __name__ == "__main__":
    main()
