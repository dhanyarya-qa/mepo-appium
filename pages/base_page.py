"""
Base Page Object
================
Abstract base class providing common Appium interactions
shared across all page objects in the Mepo Travel test suite.
"""

import logging
from typing import List, Tuple

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    StaleElementReferenceException,
)

logger = logging.getLogger(__name__)


class BasePage:
    """
    Base Page Object providing reusable mobile interaction helpers.

    All page objects inherit from this class to gain access to
    common wait, find, tap, scroll, and assertion utilities.
    """

    DEFAULT_TIMEOUT = 15  # seconds
    SHORT_TIMEOUT = 5
    LONG_TIMEOUT = 30

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(
            driver,
            self.DEFAULT_TIMEOUT,
            ignored_exceptions=[StaleElementReferenceException],
        )

    # ──────────────────────────────────────────────
    # Element Locating
    # ──────────────────────────────────────────────

    def find_element(self, locator: Tuple[str, str], timeout: int = None) -> WebElement:
        """Wait for and return a single element."""
        wait = self._get_wait(timeout)
        try:
            element = wait.until(EC.presence_of_element_located(locator))
            logger.debug(f"✔ Found element: {locator}")
            return element
        except TimeoutException:
            logger.error(f"✘ Element NOT found within {timeout or self.DEFAULT_TIMEOUT}s: {locator}")
            self._capture_screenshot(f"element_not_found_{locator[1][:30]}")
            raise

    def find_elements(self, locator: Tuple[str, str], timeout: int = None) -> List[WebElement]:
        """Wait for and return multiple elements."""
        wait = self._get_wait(timeout)
        try:
            wait.until(EC.presence_of_element_located(locator))
            elements = self.driver.find_elements(*locator)
            logger.debug(f"✔ Found {len(elements)} elements: {locator}")
            return elements
        except TimeoutException:
            logger.warning(f"⚠ No elements found for: {locator}")
            return []

    def find_clickable_element(self, locator: Tuple[str, str], timeout: int = None) -> WebElement:
        """Wait for an element to be clickable and return it."""
        wait = self._get_wait(timeout)
        try:
            element = wait.until(EC.element_to_be_clickable(locator))
            logger.debug(f"✔ Clickable element ready: {locator}")
            return element
        except TimeoutException:
            logger.error(f"✘ Element NOT clickable within {timeout or self.DEFAULT_TIMEOUT}s: {locator}")
            self._capture_screenshot(f"not_clickable_{locator[1][:30]}")
            raise

    def is_element_present(self, locator: Tuple[str, str], timeout: int = None) -> bool:
        """Check if an element exists on screen without raising. Silent — no logs/screenshots."""
        t = timeout if timeout is not None else self.SHORT_TIMEOUT
        try:
            WebDriverWait(
                self.driver, t,
                ignored_exceptions=[StaleElementReferenceException],
            ).until(EC.presence_of_element_located(locator))
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def is_element_displayed(self, locator: Tuple[str, str], timeout: int = None) -> bool:
        """Check if an element is visible on screen. Silent — no logs/screenshots."""
        t = timeout if timeout is not None else self.SHORT_TIMEOUT
        try:
            element = WebDriverWait(
                self.driver, t,
                ignored_exceptions=[StaleElementReferenceException],
            ).until(EC.presence_of_element_located(locator))
            return element.is_displayed()
        except (TimeoutException, NoSuchElementException):
            return False

    def wait_for_any_locator(self, locators: List[Tuple[str, str]], timeout: int = None):
        """
        Wait until ANY of the given locators is present, bounded by a SINGLE
        shared timeout instead of `timeout` per locator.

        Looping each locator with a full timeout means the worst case (page not
        loaded) costs `timeout * len(locators)` seconds. Here all XPath locators
        are merged into one union XPath (`a | b | c`) and resolved in a single
        wait, so the worst case is just `timeout`. Non-XPath locators are checked
        only as a quick fallback.

        Returns the first matching locator, or None if none appear in time.
        """
        t = timeout if timeout is not None else self.DEFAULT_TIMEOUT

        xpaths = []      # (original_locator, xpath_string)
        others = []      # locators that can't be expressed as XPath
        for loc in locators:
            xp = self._locator_to_xpath(loc)
            if xp:
                xpaths.append((loc, xp))
            else:
                others.append(loc)

        if xpaths:
            union = " | ".join(xp for _, xp in xpaths)
            if self.is_element_present((AppiumBy.XPATH, union), timeout=t):
                # Union matched — identify which locator it was (elements are
                # already present, so these probes return immediately).
                for loc, xp in xpaths:
                    try:
                        if self.driver.find_elements(AppiumBy.XPATH, xp):
                            return loc
                    except Exception:
                        continue
                return xpaths[0][0]

        # Rare fallback: only reached if the union did not match.
        for loc in others:
            if self.is_element_present(loc, timeout=self.SHORT_TIMEOUT):
                return loc

        return None

    def _locator_to_xpath(self, locator: Tuple[str, str]):
        """Convert a locator to an equivalent XPath string, or None if not possible."""
        by, value = locator
        if by == AppiumBy.XPATH:
            return value
        if by == AppiumBy.ACCESSIBILITY_ID:
            return f"//*[@content-desc={self._xpath_literal(value)}]"
        if by == AppiumBy.ID:
            return f"//*[@resource-id={self._xpath_literal(value)}]"
        return None

    @staticmethod
    def _xpath_literal(s: str) -> str:
        """Safely quote a string for use as an XPath literal (handles quotes)."""
        if "'" not in s:
            return f"'{s}'"
        if '"' not in s:
            return f'"{s}"'
        parts = s.split("'")
        return "concat(" + ", \"'\", ".join(f"'{p}'" for p in parts) + ")"

    # ──────────────────────────────────────────────
    # Interactions
    # ──────────────────────────────────────────────

    def tap(self, locator: Tuple[str, str], timeout: int = None):
        """Tap on an element after waiting for it to be clickable."""
        element = self.find_clickable_element(locator, timeout)
        element.click()
        logger.info(f"👆 Tapped: {locator}")

    def type_text(self, locator: Tuple[str, str], text: str, clear_first: bool = True, timeout: int = None):
        """Type text into an input field."""
        element = self.find_element(locator, timeout)
        if clear_first:
            element.clear()
        element.send_keys(text)
        logger.info(f"⌨ Typed '{text}' into: {locator}")

    def get_text(self, locator: Tuple[str, str], timeout: int = None) -> str:
        """Retrieve text content from an element."""
        element = self.find_element(locator, timeout)
        text = element.text
        logger.debug(f"📝 Got text '{text}' from: {locator}")
        return text

    def get_attribute(self, locator: Tuple[str, str], attribute: str, timeout: int = None) -> str:
        """Get a specific attribute from an element."""
        element = self.find_element(locator, timeout)
        return element.get_attribute(attribute)

    # ──────────────────────────────────────────────
    # Scrolling & Swiping
    # ──────────────────────────────────────────────

    def scroll_to_element(self, locator: Tuple[str, str], max_swipes: int = 5) -> WebElement:
        """Scroll down until the target element is visible."""
        for attempt in range(max_swipes):
            if self.is_element_present(locator, timeout=2):
                logger.info(f"📜 Element found after {attempt} swipe(s): {locator}")
                return self.find_element(locator)
            self._swipe_up()
        raise NoSuchElementException(
            f"Element not found after {max_swipes} swipes: {locator}"
        )

    def scroll_to_text(self, text: str):
        """
        Use UiScrollable to scroll until text is visible (Android-only).
        More reliable than coordinate-based swiping.
        """
        try:
            self.driver.find_element(
                AppiumBy.ANDROID_UIAUTOMATOR,
                f'new UiScrollable(new UiSelector().scrollable(true))'
                f'.scrollIntoView(new UiSelector().textContains("{text}"))',
            )
            logger.info(f"📜 Scrolled to text: '{text}'")
        except NoSuchElementException:
            logger.warning(f"⚠ Could not scroll to text: '{text}'")
            raise

    def _swipe_up(self):
        """Perform a single upward swipe gesture."""
        size = self.driver.get_window_size()
        start_x = size["width"] // 2
        start_y = int(size["height"] * 0.75)
        end_y = int(size["height"] * 0.25)
        self.driver.swipe(start_x, start_y, start_x, end_y, duration=800)

    def _swipe_down(self):
        """Perform a single downward swipe gesture."""
        size = self.driver.get_window_size()
        start_x = size["width"] // 2
        start_y = int(size["height"] * 0.25)
        end_y = int(size["height"] * 0.75)
        self.driver.swipe(start_x, start_y, start_x, end_y, duration=800)

    # ──────────────────────────────────────────────
    # Wait & Navigation Helpers
    # ──────────────────────────────────────────────

    def wait_for_page_load(self, indicator_locator: Tuple[str, str], timeout: int = None):
        """Wait for a page-specific indicator element to appear."""
        self.find_element(indicator_locator, timeout=timeout or self.LONG_TIMEOUT)
        logger.info(f"✅ Page loaded (indicator: {indicator_locator})")

    def navigate_back(self):
        """Press the Android back button."""
        self.driver.back()
        logger.info("⬅ Navigated back")

    def hide_keyboard(self):
        """Hide the on-screen keyboard if visible."""
        try:
            if self.driver.is_keyboard_shown():
                self.driver.hide_keyboard()
                logger.debug("⌨ Keyboard hidden")
        except Exception:
            pass  # Keyboard was not shown

    # ──────────────────────────────────────────────
    # Permission / Dialog Handling
    # ──────────────────────────────────────────────

    def dismiss_permission_dialog(self):
        """
        Dismiss any Android permission dialog that appears.
        Attempts to tap 'Allow' / 'ALLOW' / 'While using the app'.
        """
        permission_buttons = [
            (AppiumBy.ID, "com.android.permissioncontroller:id/permission_allow_button"),
            (AppiumBy.ID, "com.android.permissioncontroller:id/permission_allow_foreground_only_button"),
            (AppiumBy.XPATH, "//*[@text='Allow']"),
            (AppiumBy.XPATH, "//*[@text='ALLOW']"),
            (AppiumBy.XPATH, "//*[@text='While using the app']"),
            (AppiumBy.XPATH, "//*[@text='Izinkan']"),
        ]
        for btn in permission_buttons:
            try:
                if self.is_element_present(btn, timeout=2):
                    element = self.driver.find_element(*btn)
                    element.click()
                    logger.info(f"🔓 Dismissed permission dialog: {btn}")
                    return True
            except Exception:
                continue
        return False

    def dismiss_all_dialogs(self, max_attempts: int = 3):
        """Try to dismiss any stacked dialogs/permissions."""
        import time
        for i in range(max_attempts):
            time.sleep(0.3)
            if not self.dismiss_permission_dialog():
                break
            logger.info(f"  Dialog #{i+1} dismissed")

    # ──────────────────────────────────────────────
    # Utility
    # ──────────────────────────────────────────────

    def _get_wait(self, timeout: int = None) -> WebDriverWait:
        """Return a WebDriverWait with the given or default timeout."""
        if timeout and timeout != self.DEFAULT_TIMEOUT:
            return WebDriverWait(
                self.driver, timeout,
                ignored_exceptions=[StaleElementReferenceException],
            )
        return self.wait

    def _capture_screenshot(self, name: str):
        """Save a screenshot for debugging failed steps."""
        try:
            filepath = f"reports/screenshots/{name}.png"
            self.driver.save_screenshot(filepath)
            logger.info(f"📸 Screenshot saved: {filepath}")
        except Exception as e:
            logger.warning(f"⚠ Could not save screenshot: {e}")
