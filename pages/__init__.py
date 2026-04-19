"""
Mepo Travel App — Page Objects
===============================
Page Object Model (POM) classes for the Mepo Travel app.
"""

from pages.base_page import BasePage
from pages.login_page import LoginPage
from pages.home_page import HomePage
from pages.open_trip_page import OpenTripPage
from pages.profile_page import ProfilePage
from pages.create_itinerary_page import CreateItineraryPage
from pages.splash_page import SplashPage
from pages.budget_page import BudgetPage

__all__ = [
    "BasePage",
    "LoginPage",
    "HomePage",
    "OpenTripPage",
    "ProfilePage",
    "CreateItineraryPage",
    "SplashPage",
    "BudgetPage",
]
