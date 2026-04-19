"""
Splash / Welcome Page Object
=============================
Locators and actions for the Mepo Travel app's initial launch screen.
Handles splash screen, onboarding, and navigation to login/register.
"""

import logging
from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class SplashPage(BasePage):
    """Page Object for the Splash / Welcome / Onboarding screen."""

    # ──────────────────────────────────────────────
    # Locators — Multiple strategies for Flutter app
    # ──────────────────────────────────────────────

    # Splash Screen Indicators
    APP_LOGO = (AppiumBy.ACCESSIBILITY_ID, "Mepo")
    APP_LOGO_ALT = (AppiumBy.XPATH, "//*[contains(@content-desc, 'Mepo')]")
    SPLASH_IMAGE = (AppiumBy.XPATH, "//*[contains(@content-desc, 'splash')]")

    # Welcome / Onboarding Buttons
    BTN_MASUK = (AppiumBy.ACCESSIBILITY_ID, "Masuk")
    BTN_MASUK_ALT = (AppiumBy.XPATH, "//*[contains(@content-desc, 'Masuk')]")
    BTN_LOGIN = (AppiumBy.ACCESSIBILITY_ID, "Login")
    BTN_LOGIN_ALT = (AppiumBy.XPATH, "//*[contains(@content-desc, 'Login')]")

    BTN_DAFTAR = (AppiumBy.ACCESSIBILITY_ID, "Daftar")
    BTN_DAFTAR_ALT = (AppiumBy.XPATH, "//*[contains(@content-desc, 'Daftar')]")
    BTN_REGISTER = (AppiumBy.ACCESSIBILITY_ID, "Register")
    BTN_SIGN_UP = (AppiumBy.ACCESSIBILITY_ID, "Sign Up")

    # "Mulai" / "Get Started" button (common in onboarding)
    BTN_MULAI = (AppiumBy.ACCESSIBILITY_ID, "Mulai")
    BTN_GET_STARTED = (AppiumBy.ACCESSIBILITY_ID, "Get Started")
    BTN_LANJUT = (AppiumBy.ACCESSIBILITY_ID, "Lanjut")
    BTN_NEXT = (AppiumBy.ACCESSIBILITY_ID, "Next")
    BTN_SKIP = (AppiumBy.ACCESSIBILITY_ID, "Skip")
    BTN_LEWATI = (AppiumBy.ACCESSIBILITY_ID, "Lewati")

    # Generic text-based fallbacks for any clickable "login" element
    ANY_LOGIN_TEXT = (AppiumBy.XPATH,
        "//*[contains(@text, 'Masuk') or contains(@text, 'Login') "
        "or contains(@text, 'Sign In') or contains(@text, 'Sign in')]"
    )
    ANY_REGISTER_TEXT = (AppiumBy.XPATH,
        "//*[contains(@text, 'Daftar') or contains(@text, 'Register') "
        "or contains(@text, 'Sign Up') or contains(@text, 'Sign up')]"
    )

    # Actual login page elements (from screenshot)
    WELCOME_BACK = (AppiumBy.XPATH, "//*[contains(@text, 'Welcome Back')]")
    WELCOME_BACK_DESC = (AppiumBy.XPATH, "//*[contains(@content-desc, 'Welcome Back')]")
    INPUT_EMAIL_HINT = (AppiumBy.XPATH, "//*[contains(@text, 'Input your email')]")
    INPUT_EMAIL_DESC = (AppiumBy.XPATH, "//*[contains(@content-desc, 'Input your email')]")
    FIRST_EDIT_TEXT = (AppiumBy.XPATH, "//android.widget.EditText[1]")

    # Home screen indicators (if already logged in)
    HOME_WELCOME = (AppiumBy.XPATH, "//*[contains(@text, 'Welcome,')]")
    HOME_WELCOME_DESC = (AppiumBy.XPATH, "//*[contains(@content-desc, 'Welcome,')]")
    HOME_OPEN_TRIP = (AppiumBy.XPATH, "//*[contains(@text, 'Open Trip')]")

    # ──────────────────────────────────────────────
    # Actions
    # ──────────────────────────────────────────────

    def wait_for_app_launched(self, timeout: int = 30):
        """
        Wait for the app to fully launch past the native splash screen.
        Detects either login screen or home screen.
        """
        import time
        self.dismiss_all_dialogs()
        logger.info("🚀 Waiting for app to launch...")

        # Quick scan (3s each) — prioritize actual UI elements
        quick_indicators = [
            self.WELCOME_BACK,       # Login page header
            self.INPUT_EMAIL_HINT,   # Login email field
            self.FIRST_EDIT_TEXT,     # Any EditText (login form)
            self.HOME_WELCOME,       # Home screen (already logged in)
            self.HOME_OPEN_TRIP,     # Home screen menu
            self.BTN_LOGIN,          # Login button
            self.ANY_LOGIN_TEXT,      # Any login-related text
        ]

        for indicator in quick_indicators:
            if self.is_element_present(indicator, timeout=3):
                logger.info(f"✅ App launched — detected: {indicator}")
                return True

        # Longer wait — try broader patterns
        logger.info("⏳ No quick indicator found, waiting longer...")
        broad_indicators = [
            self.WELCOME_BACK, self.FIRST_EDIT_TEXT,
            self.HOME_WELCOME, self.HOME_OPEN_TRIP,
            self.ANY_LOGIN_TEXT,
        ]
        for indicator in broad_indicators:
            if self.is_element_present(indicator, timeout=timeout):
                logger.info(f"✅ App launched (long wait) — detected: {indicator}")
                return True

        logger.warning("⚠ Could not detect app launch indicator")
        return False

    def skip_onboarding(self):
        """
        Skip any onboarding / tutorial screens if present.
        Taps 'Skip' / 'Lewati' or swipes through pages.
        """
        skip_buttons = [self.BTN_SKIP, self.BTN_LEWATI]
        for btn in skip_buttons:
            if self.is_element_present(btn, timeout=3):
                self.tap(btn)
                logger.info(f"⏭ Onboarding skipped via: {btn}")
                return True

        # Try swiping through onboarding pages
        next_buttons = [self.BTN_NEXT, self.BTN_LANJUT]
        for _ in range(5):  # max 5 onboarding pages
            for btn in next_buttons:
                if self.is_element_present(btn, timeout=2):
                    self.tap(btn)
                    logger.info(f"➡ Onboarding next tapped: {btn}")
                    break
            else:
                break  # No next button found, likely past onboarding

        logger.info("📋 Onboarding handling complete")
        return True

    def navigate_to_login(self):
        """
        Navigate to the login screen from splash/welcome.
        Tries multiple locator strategies for the login button.
        """
        login_buttons = [
            self.BTN_MASUK, self.BTN_LOGIN,
            self.BTN_MASUK_ALT, self.BTN_LOGIN_ALT,
            self.ANY_LOGIN_TEXT,
        ]

        for btn in login_buttons:
            if self.is_element_present(btn, timeout=3):
                self.tap(btn)
                logger.info(f"🔐 Navigating to Login via: {btn}")
                return True

        logger.warning("⚠ Could not find login button on splash screen")
        return False

    def navigate_to_register(self):
        """
        Navigate to the register screen from splash/welcome.
        """
        register_buttons = [
            self.BTN_DAFTAR, self.BTN_REGISTER, self.BTN_SIGN_UP,
            self.BTN_DAFTAR_ALT, self.ANY_REGISTER_TEXT,
        ]

        for btn in register_buttons:
            if self.is_element_present(btn, timeout=3):
                self.tap(btn)
                logger.info(f"📝 Navigating to Register via: {btn}")
                return True

        logger.warning("⚠ Could not find register button on splash screen")
        return False

    def is_on_splash_screen(self) -> bool:
        """Check if we're currently on the splash/welcome screen."""
        splash_indicators = [
            self.BTN_MASUK, self.BTN_LOGIN, self.BTN_DAFTAR,
            self.APP_LOGO, self.ANY_LOGIN_TEXT,
        ]
        return any(
            self.is_element_present(ind, timeout=2) for ind in splash_indicators
        )
