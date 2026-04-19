"""
Mepo Travel App - Test Configuration Settings
===============================================
Centralized configuration for Appium capabilities, API endpoints,
and test environment parameters.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class AppiumConfig:
    """Appium server and desired capabilities configuration."""

    SERVER_URL = os.getenv("APPIUM_SERVER_URL", "http://127.0.0.1:4723")

    DESIRED_CAPS = {
        "platformName": "Android",
        "appium:automationName": "UiAutomator2",
        "appium:deviceName": os.getenv("ANDROID_DEVICE_NAME", "23124RA7EO"),
        "appium:platformVersion": os.getenv("ANDROID_PLATFORM_VERSION", "15"),
        "appium:udid": os.getenv("ANDROID_UDID", "192.168.1.62:38549"),
        # No "appium:app" — app is pre-installed via Firebase App Tester
        "appium:appPackage": "com.mepo",
        "appium:appActivity": "com.mepo.MainActivity",
        "appium:noReset": True,            # Persist app data — stay logged in between tests
        "appium:fullReset": False,         # Don't uninstall app
        "appium:newCommandTimeout": 300,
        "appium:autoGrantPermissions": True,
        "appium:autoAcceptAlerts": True,
        "appium:disableWindowAnimation": True,
        "appium:ignoreUnimportantViews": True,
        "appium:dontStopAppOnReset": False,
        "appium:forceAppLaunch": True,     # Force restart app  
        "appium:appWaitDuration": 30000,   # Wait up to 30s for Flutter app
    }


class APIConfig:
    """API configuration for dev.mepo.travel backend."""

    BASE_URL = os.getenv("MEPO_API_BASE_URL", "https://dev.mepo.travel/api/v1")
    TEST_USER_EMAIL = os.getenv("MEPO_TEST_USER_EMAIL", "danip1@yopmail.com")
    TEST_USER_PASSWORD = os.getenv("MEPO_TEST_USER_PASSWORD", "Sandi123!")
    TEST_USER_TOKEN = os.getenv("MEPO_TEST_USER_TOKEN", "dummy_token_123")

    # API Endpoints
    ENDPOINTS = {
        "auth_login": "/auth/login",
        "open_trips": "/open-trips",
        "open_trip_search": "/open-trips/search",
        "open_trip_availability": "/open-trips/{trip_id}/availability",
        "budget_expenses": "/itineraries/{itinerary_id}/expenses",
        "budget_reset": "/itineraries/{itinerary_id}/expenses/reset",
        "itineraries": "/itineraries",
        "user_profile": "/users/me",
    }

    @classmethod
    def get_endpoint(cls, name: str, **kwargs) -> str:
        """Get full API URL for a given endpoint name with path params."""
        path = cls.ENDPOINTS.get(name, "")
        if kwargs:
            path = path.format(**kwargs)
        return f"{cls.BASE_URL}{path}"

    @classmethod
    def get_headers(cls, token: str = None) -> dict:
        """Return authorization headers for API calls."""
        auth_token = token or cls.TEST_USER_TOKEN
        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {auth_token}",
        }


class TestData:
    """Test data constants used across test scenarios."""

    # Open Trip Search
    OPEN_TRIP_SEARCH_KEYWORD = "Bandung"
    OPEN_TRIP_CATEGORY_WISATA_ALAM = "Wisata Alam"
    OPEN_TRIP_CATEGORY_KULINER_LOKAL = "Kuliner Lokal"

    # Budget Tracking
    BUDGET_EXPENSE_AMOUNT = "500000"
    BUDGET_EXPENSE_AMOUNT_DISPLAY = "Rp 500.000"
    BUDGET_EXPENSE_CATEGORY = "Makanan"
    BUDGET_EXPENSE_CATEGORY_TRANSPORT = "Transportasi"

    # Dummy Open Trip data for API seeding
    DUMMY_OPEN_TRIP = {
        "title": "Explore Bandung - Wisata Alam & Kuliner",
        "destination": "Bandung",
        "categories": ["Wisata Alam", "Kuliner Lokal"],
        "price": 1500000,
        "currency": "IDR",
        "max_participants": 20,
        "departure_dates": [
            "2026-05-01",
            "2026-05-15",
            "2026-06-01",
        ],
        "description": "Jelajahi keindahan alam Bandung dan cicipi kuliner lokal terbaik.",
        "status": "active",
    }


class LoginCredentials:
    """Login credentials for the Mepo Travel app UI login."""

    EMAIL = os.getenv("MEPO_LOGIN_EMAIL", "danip1@yopmail.com")
    PASSWORD = os.getenv("MEPO_LOGIN_PASSWORD", "Sandi123!")
