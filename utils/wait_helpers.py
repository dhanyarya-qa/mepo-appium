"""
Smart WebDriverWait utilities for Mepo Travel Appium Tests.

Provides dynamic waits (instead of fixed time.sleep) for finding elements,
waiting for conditions, and waiting for any of multiple possible states.

Timeout constants:
    FAST   —  3s  (quick assertions, obvious elements)
    NORMAL —  5s  (standard interaction wait)
    SLOW   — 10s  (network-dependent actions)
    XSLOW  — 20s  (app boot, login, registration flows)
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy

# ── Timeout constants ─────────────────────────────────────────────────────────
FAST   =  3   # Quick assertions — element should already be visible
NORMAL =  5   # Standard interaction wait
SLOW   = 10   # Network or animation dependent
XSLOW  = 20   # App boot / login / OTP flows


def wait_for(driver, xpath: str, timeout: int = NORMAL):
    """
    Wait until an element matching `xpath` is present in the DOM.

    Returns the element if found, or None on timeout.
    Does NOT raise an exception on timeout.

    Args:
        driver:  Appium WebDriver instance
        xpath:   XPath locator string
        timeout: Max seconds to wait (default: NORMAL = 5s)

    Returns:
        WebElement if found, None otherwise
    """
    try:
        return WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((AppiumBy.XPATH, xpath))
        )
    except Exception:
        return None


def wait_find(driver, xpath: str, timeout: int = NORMAL):
    """
    Wait until at least one element matching `xpath` is present,
    then return ALL matching elements as a list.

    If nothing is found within `timeout`, returns an empty list [].
    This mirrors the behavior of driver.find_elements() but with a wait.

    Args:
        driver:  Appium WebDriver instance
        xpath:   XPath locator string
        timeout: Max seconds to wait (default: NORMAL = 5s)

    Returns:
        List[WebElement] — empty list if not found
    """
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((AppiumBy.XPATH, xpath))
        )
        return driver.find_elements(AppiumBy.XPATH, xpath)
    except Exception:
        return []


def wait_and_click(driver, xpath: str, timeout: int = NORMAL) -> bool:
    """
    Wait for an element to be clickable, then click it.

    Args:
        driver:  Appium WebDriver instance
        xpath:   XPath locator string
        timeout: Max seconds to wait (default: NORMAL = 5s)

    Returns:
        True if element was found and clicked, False otherwise
    """
    try:
        el = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((AppiumBy.XPATH, xpath))
        )
        el.click()
        return True
    except Exception:
        return False


def wait_for_any(driver, xpaths: list, timeout: int = NORMAL):
    """
    Wait until ANY of the given XPath locators matches an element.
    Returns as soon as the first match is found.

    Useful for handling multiple possible app states (e.g., login screen OR home screen).

    Args:
        driver:  Appium WebDriver instance
        xpaths:  List of XPath locator strings to try
        timeout: Max total seconds to wait across all locators (default: NORMAL = 5s)

    Returns:
        Tuple (index, elements) where:
          - index    is the 0-based index of the first matching xpath
          - elements is the list of matching WebElements for that xpath
        Returns (-1, []) if none matched within timeout.

    Example:
        idx, els = wait_for_any(driver, [
            "//android.widget.EditText",           # Login screen
            "//*[contains(@content-desc, 'Welcome,')]",  # Home screen
        ], timeout=10)
        if idx == 0: ...  # on login screen
        if idx == 1: ...  # on home screen
    """
    import time

    deadline = time.time() + timeout
    poll_interval = 0.3

    while time.time() < deadline:
        for i, xpath in enumerate(xpaths):
            try:
                els = driver.find_elements(AppiumBy.XPATH, xpath)
                if els:
                    return i, els
            except Exception:
                pass
        time.sleep(poll_interval)

    return -1, []
