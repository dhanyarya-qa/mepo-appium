"""
Mepo Travel API Helper
======================
Provides HTTP client methods for backend API calls used as
pre-conditions and post-conditions in E2E test scenarios.

Target: dev.mepo.travel API
"""

import logging
from typing import Optional, Dict, Any

import requests

from config.settings import APIConfig, TestData

logger = logging.getLogger(__name__)


class MepoAPIHelper:
    """
    Wrapper around `requests` library for Mepo Travel API interactions.

    Used in test setup/teardown to:
    - Authenticate test user and obtain JWT token
    - Seed dummy data (Open Trip packages)
    - Reset budget/expense history to clean state
    - Validate backend state post-action
    """

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
        })
        self.token: Optional[str] = None
        self.base_url = APIConfig.BASE_URL

    # ══════════════════════════════════════════════
    # AUTHENTICATION
    # ══════════════════════════════════════════════

    def authenticate(self, email: str = None, password: str = None) -> str:
        """
        Authenticate test user and store the JWT token.

        Args:
            email: User email (defaults to test user).
            password: User password (defaults to test user).

        Returns:
            JWT token string.
        """
        url = APIConfig.get_endpoint("auth_login")
        payload = {
            "email": email or APIConfig.TEST_USER_EMAIL,
            "password": password or APIConfig.TEST_USER_PASSWORD,
        }

        logger.info(f"🔐 Authenticating user: {payload['email']}")

        try:
            response = self.session.post(url, json=payload, timeout=30)
            response.raise_for_status()

            data = response.json()
            self.token = data.get("data", {}).get("token") or data.get("token", "")
            self.session.headers["Authorization"] = f"Bearer {self.token}"

            logger.info("✅ Authentication successful")
            return self.token

        except requests.exceptions.ConnectionError:
            logger.warning(
                "⚠ Could not connect to API server. "
                "Running in offline mode — API pre-conditions will be skipped."
            )
            self.token = APIConfig.TEST_USER_TOKEN or "offline-mock-token"
            return self.token

        except requests.exceptions.HTTPError as e:
            logger.error(f"❌ Authentication failed: {e}")
            logger.error(f"   Response: {e.response.text if e.response else 'N/A'}")
            # Fall back to env token if available
            if APIConfig.TEST_USER_TOKEN:
                self.token = APIConfig.TEST_USER_TOKEN
                self.session.headers["Authorization"] = f"Bearer {self.token}"
                logger.info("⚠ Using fallback token from environment")
                return self.token
            raise

    # ══════════════════════════════════════════════
    # OPEN TRIP DATA SEEDING
    # ══════════════════════════════════════════════

    def ensure_open_trip_exists(self, destination: str = "Bandung") -> Dict[str, Any]:
        """
        Verify a dummy Open Trip package exists for the target destination.
        If not found, attempt to create one via the API.

        Args:
            destination: Trip destination city name.

        Returns:
            Dict with trip data or empty dict on failure.
        """
        logger.info(f"🔍 Checking Open Trip availability for: {destination}")

        # Step 1: Search for existing trip
        existing = self._search_open_trip(destination)
        if existing:
            logger.info(f"✅ Open Trip for '{destination}' already exists (ID: {existing.get('id')})")
            return existing

        # Step 2: Create dummy trip if not found
        logger.info(f"📝 Creating dummy Open Trip for: {destination}")
        return self._create_dummy_open_trip(destination)

    def _search_open_trip(self, destination: str) -> Optional[Dict]:
        """Search for an existing open trip by destination."""
        url = APIConfig.get_endpoint("open_trip_search")
        params = {"q": destination, "status": "active"}

        try:
            response = self.session.get(url, params=params, timeout=15)
            response.raise_for_status()

            data = response.json()
            trips = data.get("data", {}).get("trips", [])

            if trips:
                return trips[0]
            return None

        except requests.exceptions.RequestException as e:
            logger.warning(f"⚠ Open Trip search failed: {e}")
            return None

    def _create_dummy_open_trip(self, destination: str) -> Dict[str, Any]:
        """Create a dummy open trip via API for test purposes."""
        url = APIConfig.get_endpoint("open_trips")

        payload = TestData.DUMMY_OPEN_TRIP.copy()
        payload["destination"] = destination

        try:
            response = self.session.post(url, json=payload, timeout=15)
            response.raise_for_status()

            data = response.json()
            trip = data.get("data", {})
            logger.info(f"✅ Dummy Open Trip created (ID: {trip.get('id')})")
            return trip

        except requests.exceptions.RequestException as e:
            logger.warning(f"⚠ Could not create dummy Open Trip: {e}")
            return {"status": "skipped", "reason": str(e)}

    def check_trip_availability(self, trip_id: str) -> Dict[str, Any]:
        """Check departure date availability for a specific trip."""
        url = APIConfig.get_endpoint("open_trip_availability", trip_id=trip_id)

        try:
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            return response.json().get("data", {})
        except requests.exceptions.RequestException as e:
            logger.warning(f"⚠ Trip availability check failed: {e}")
            return {}

    # ══════════════════════════════════════════════
    # BUDGET / EXPENSE MANAGEMENT
    # ══════════════════════════════════════════════

    def reset_budget_history(self, itinerary_id: str = None) -> bool:
        """
        Clear all expense/budget history for the test user so that
        the starting balance is zero before test execution.

        Args:
            itinerary_id: Target itinerary ID. If None, resets all.

        Returns:
            True if reset was successful.
        """
        logger.info("🧹 Resetting budget history for test user...")

        if itinerary_id:
            return self._reset_itinerary_expenses(itinerary_id)

        # Reset all itineraries
        itineraries = self._get_user_itineraries()
        if not itineraries:
            logger.info("ℹ No itineraries found — nothing to reset")
            return True

        success = True
        for itin in itineraries:
            itin_id = itin.get("id", "")
            if itin_id:
                result = self._reset_itinerary_expenses(itin_id)
                success = success and result

        return success

    def _reset_itinerary_expenses(self, itinerary_id: str) -> bool:
        """Reset expenses for a specific itinerary."""
        url = APIConfig.get_endpoint("budget_reset", itinerary_id=itinerary_id)

        try:
            response = self.session.delete(url, timeout=15)
            if response.status_code in (200, 204):
                logger.info(f"✅ Budget reset for itinerary: {itinerary_id}")
                return True
            else:
                logger.warning(
                    f"⚠ Budget reset returned {response.status_code} "
                    f"for itinerary: {itinerary_id}"
                )
                return False

        except requests.exceptions.RequestException as e:
            logger.warning(f"⚠ Budget reset failed for {itinerary_id}: {e}")
            return False

    def _get_user_itineraries(self) -> list:
        """Fetch all itineraries belonging to the test user."""
        url = APIConfig.get_endpoint("itineraries")

        try:
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            return response.json().get("data", {}).get("itineraries", [])
        except requests.exceptions.RequestException as e:
            logger.warning(f"⚠ Could not fetch itineraries: {e}")
            return []

    def get_active_itinerary_id(self) -> Optional[str]:
        """Return the ID of the first active itinerary, if any."""
        itineraries = self._get_user_itineraries()
        active = [i for i in itineraries if i.get("status") == "active"]
        if active:
            itin_id = active[0].get("id")
            logger.info(f"📋 Active itinerary found: {itin_id}")
            return itin_id

        logger.warning("⚠ No active itinerary found")
        return None

    def get_expense_total(self, itinerary_id: str) -> float:
        """Fetch current total expense amount from API."""
        url = APIConfig.get_endpoint("budget_expenses", itinerary_id=itinerary_id)

        try:
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            data = response.json().get("data", {})
            total = float(data.get("total_expense", 0))
            logger.info(f"💰 API expense total: {total}")
            return total
        except requests.exceptions.RequestException as e:
            logger.warning(f"⚠ Could not fetch expense total: {e}")
            return 0.0

    # ══════════════════════════════════════════════
    # HEALTH CHECK
    # ══════════════════════════════════════════════

    def health_check(self) -> bool:
        """Verify the API backend is reachable and responsive."""
        try:
            response = self.session.get(
                f"{self.base_url}/health",
                timeout=10,
            )
            is_healthy = response.status_code == 200
            logger.info(f"{'✅' if is_healthy else '❌'} API health check: {response.status_code}")
            return is_healthy
        except requests.exceptions.RequestException as e:
            logger.warning(f"⚠ API health check failed: {e}")
            return False

    def close(self):
        """Close the underlying HTTP session."""
        self.session.close()
        logger.info("🔒 API session closed")
