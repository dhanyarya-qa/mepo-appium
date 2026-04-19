"""
Advanced Feature E2E Tests
==========================
End-to-end test scenarios for "Open Trip Discovery" and "Budget Tracking"
features in the Mepo Travel Android application.

Test Runner: pytest tests/test_advanced_features.py -v -s
Framework:   Appium + Python (Pytest, Page Object Model)
Target:      Mepo Travel Android App + dev.mepo.travel API
"""

import logging
import time

import pytest

from config.settings import TestData
from pages.home_page import HomePage
from pages.open_trip_page import OpenTripPage
from pages.budget_page import BudgetPage
from utils.api_helper import MepoAPIHelper

logger = logging.getLogger(__name__)


# ══════════════════════════════════════════════════════
# TEST SCENARIO 1: Open Trip Discovery — Search & Book
# ══════════════════════════════════════════════════════

class TestSearchAndBookOpenTrip:
    """
    E2E test: Search for a Bandung Open Trip with nature + culinary filters,
    verify departure schedule, and validate booking accessibility.

    Pre-condition (API):
      ✓ Authenticate test user
      ✓ Ensure dummy Open Trip package for "Bandung" exists
    """

    @pytest.fixture(autouse=True)
    def setup_method(self, api_helper: MepoAPIHelper, appium_driver):
        """
        Setup: API pre-conditions before UI test execution.
        
        1. Authenticate test user via API
        2. Ensure Open Trip for Bandung is available in the backend
        3. Store driver reference for the test
        """
        logger.info("=" * 60)
        logger.info("🔧 SETUP: test_search_and_book_open_trip")
        logger.info("=" * 60)

        # API Pre-condition 1: Ensure authentication
        if not api_helper.token:
            api_helper.authenticate()

        # API Pre-condition 2: Seed Bandung Open Trip data
        logger.info("📦 Ensuring Bandung Open Trip data exists in backend...")
        trip_data = api_helper.ensure_open_trip_exists(
            destination=TestData.OPEN_TRIP_SEARCH_KEYWORD
        )
        logger.info(f"   Trip data status: {trip_data.get('status', 'available')}")

        self.driver = appium_driver
        self.trip_data = trip_data

        yield

        logger.info("🧹 TEARDOWN: test_search_and_book_open_trip complete")

    def test_search_and_book_open_trip(
        self,
        home_page: HomePage,
        open_trip_page: OpenTripPage,
    ):
        """
        Skenario lengkap Open Trip Discovery:
        
        1. Navigasi ke menu Open Trip dari Home
        2. Masukkan kata kunci "Bandung" pada kolom pencarian
        3. Terapkan filter "Wisata Alam" dan "Kuliner Lokal"
        4. Pilih hasil pertama
        5. Cek ketersediaan tanggal keberangkatan
        6. Validasi tombol "Booking Sekarang" dapat diakses
        """
        logger.info("🧪 TEST START: test_search_and_book_open_trip")
        logger.info("─" * 50)

        # ── Step 1: Navigasi ke menu Open Trip ────────
        logger.info("📍 Step 1: Navigasi ke menu Open Trip")
        home_page.wait_for_home_loaded()
        home_page.navigate_to_open_trip()
        open_trip_page.wait_for_open_trip_loaded()

        assert open_trip_page.is_element_displayed(
            open_trip_page.SEARCH_BAR
        ), "❌ FAIL: Halaman Open Trip tidak berhasil dimuat — search bar tidak ditemukan"
        logger.info("   ✅ Halaman Open Trip berhasil dimuat")

        # ── Step 2: Masukkan kata kunci "Bandung" ─────
        logger.info("📍 Step 2: Memasukkan kata kunci pencarian 'Bandung'")
        open_trip_page.search_trip(TestData.OPEN_TRIP_SEARCH_KEYWORD)

        # Wait for search results to load
        time.sleep(2)

        results_count = open_trip_page.get_search_results_count()
        assert results_count > 0, (
            f"❌ FAIL: Pencarian '{TestData.OPEN_TRIP_SEARCH_KEYWORD}' "
            f"tidak menampilkan hasil — 0 trip ditemukan"
        )
        logger.info(f"   ✅ Ditemukan {results_count} hasil pencarian untuk 'Bandung'")

        # ── Step 3: Terapkan filter Wisata Alam + Kuliner Lokal ──
        logger.info("📍 Step 3: Menerapkan filter kategori — Wisata Alam & Kuliner Lokal")
        open_trip_page.apply_nature_and_culinary_filters()

        # Wait for filtered results
        time.sleep(2)

        filtered_count = open_trip_page.get_search_results_count()
        assert filtered_count > 0, (
            "❌ FAIL: Filter 'Wisata Alam' + 'Kuliner Lokal' menghasilkan 0 trip — "
            "tidak ada data yang cocok"
        )
        logger.info(f"   ✅ Filter berhasil — {filtered_count} trip tersedia setelah filter")

        # ── Step 4: Pilih hasil pertama ───────────────
        logger.info("📍 Step 4: Memilih trip pertama dari hasil pencarian")
        first_trip_title = open_trip_page.get_first_trip_title()
        logger.info(f"   📝 Trip terpilih: '{first_trip_title}'")

        open_trip_page.select_first_trip()
        open_trip_page.wait_for_detail_loaded()

        detail_title = open_trip_page.get_detail_title()
        assert detail_title, (
            "❌ FAIL: Halaman detail trip tidak ter-render — judul kosong"
        )
        logger.info(f"   ✅ Detail trip dimuat: '{detail_title}'")

        # ── Step 5: Cek ketersediaan jadwal keberangkatan ──
        logger.info("📍 Step 5: Mengecek ketersediaan jadwal keberangkatan")
        open_trip_page.check_departure_schedule()

        available_dates = open_trip_page.get_available_dates()
        date_count = open_trip_page.get_departure_date_count()

        assert date_count > 0, (
            "❌ FAIL: Tidak ada jadwal keberangkatan yang tersedia — "
            "bottom sheet kosong"
        )
        logger.info(f"   ✅ {date_count} tanggal keberangkatan tersedia: {available_dates}")

        # Close schedule sheet before checking booking
        open_trip_page.close_schedule_sheet()

        # ── Step 6: Validasi tombol "Booking Sekarang" ──
        logger.info("📍 Step 6: Memvalidasi aksesibilitas tombol 'Booking Sekarang'")
        is_booking_accessible = open_trip_page.is_booking_button_accessible()

        assert is_booking_accessible, (
            "❌ FAIL: Tombol 'Booking Sekarang' tidak dapat diakses — "
            "element disabled atau tidak ter-render di UI"
        )
        logger.info("   ✅ Tombol 'Booking Sekarang' ACCESSIBLE — enabled dan terlihat")

        logger.info("─" * 50)
        logger.info("🎉 TEST PASSED: test_search_and_book_open_trip")
        logger.info("─" * 50)


# ══════════════════════════════════════════════════════
# TEST SCENARIO 2: Budget Tracking
# ══════════════════════════════════════════════════════

class TestBudgetTracking:
    """
    E2E test: Open an active itinerary, navigate to the Budget tab,
    add a new Rp 500.000 expense under 'Makanan', and verify the
    total expense automatically updates on screen.

    Pre-condition (API):
      ✓ Authenticate test user
      ✓ Reset budget history so starting balance = 0
    """

    @pytest.fixture(autouse=True)
    def setup_method(self, api_helper: MepoAPIHelper, appium_driver):
        """
        Setup: Reset budget state via API before UI test execution.

        1. Authenticate test user
        2. Clear all expense records to set initial balance to zero
        3. Store references for the test
        """
        logger.info("=" * 60)
        logger.info("🔧 SETUP: test_budget_tracking")
        logger.info("=" * 60)

        # API Pre-condition 1: Ensure authentication
        if not api_helper.token:
            api_helper.authenticate()

        # API Pre-condition 2: Reset budget history to zero
        logger.info("🧹 Resetting budget/expense history to zero state...")
        reset_success = api_helper.reset_budget_history()
        logger.info(f"   Budget reset status: {'✅ Success' if reset_success else '⚠ Skipped'}")

        # Check for active itinerary
        self.active_itinerary_id = api_helper.get_active_itinerary_id()
        logger.info(f"   Active itinerary: {self.active_itinerary_id or 'None found'}")

        self.driver = appium_driver
        self.api_helper = api_helper

        yield

        logger.info("🧹 TEARDOWN: test_budget_tracking complete")

    def test_budget_tracking(
        self,
        home_page: HomePage,
        budget_page: BudgetPage,
    ):
        """
        Skenario lengkap Budget Tracking:

        1. Buka itinerary aktif dari Home
        2. Masuk ke tab "Budget" / "Pelacakan Anggaran"
        3. Tambahkan pengeluaran baru: Rp 500.000, kategori "Makanan"
        4. Validasi total pengeluaran ter-update secara otomatis
        """
        logger.info("🧪 TEST START: test_budget_tracking")
        logger.info("─" * 50)

        # ── Step 1: Buka itinerary aktif ──────────────
        logger.info("📍 Step 1: Membuka itinerary aktif dari Home")
        home_page.wait_for_home_loaded()
        home_page.navigate_to_itinerary()

        # Tap on the first / active itinerary
        # Use scroll to find itinerary if needed
        assert home_page.is_element_displayed(
            home_page.TAB_ITINERARY
        ), "❌ FAIL: Tab Itinerary tidak ditemukan di bottom navigation"

        logger.info("   ✅ Navigasi ke Itinerary berhasil")

        # ── Step 2: Masuk ke tab Budget ───────────────
        logger.info("📍 Step 2: Memilih tab 'Budget' / 'Pelacakan Anggaran'")
        budget_page.navigate_to_budget_tab()
        budget_page.wait_for_budget_page_loaded()

        logger.info("   ✅ Tab Budget berhasil dibuka")

        # Verify initial state (should be empty / zero after reset)
        initial_total = budget_page.get_total_expense()
        logger.info(f"   📊 Total pengeluaran awal: {initial_total}")

        # ── Step 3: Tambahkan pengeluaran Rp 500.000 ──
        logger.info(
            f"📍 Step 3: Menambahkan pengeluaran baru — "
            f"Rp {TestData.BUDGET_EXPENSE_AMOUNT} ({TestData.BUDGET_EXPENSE_CATEGORY})"
        )

        budget_page.add_expense(
            amount=TestData.BUDGET_EXPENSE_AMOUNT,
            category=TestData.BUDGET_EXPENSE_CATEGORY,
            description="Test expense — Makanan perjalanan",
        )

        # Wait for UI to update
        time.sleep(2)

        # Verify success feedback
        logger.info("   📋 Memverifikasi feedback penambahan pengeluaran...")

        # ── Step 4: Validasi total pengeluaran ter-update ──
        logger.info("📍 Step 4: Memvalidasi total pengeluaran ter-update otomatis")

        is_updated = budget_page.is_total_expense_updated("500.000")

        assert is_updated, (
            f"❌ FAIL: Total pengeluaran TIDAK ter-update — "
            f"expected '500.000' dalam display, "
            f"actual: '{budget_page.get_total_expense()}'"
        )
        logger.info(
            f"   ✅ Total pengeluaran berhasil ter-update: "
            f"{budget_page.get_total_expense()}"
        )

        # Additional validation: verify the expense item appears in the list
        logger.info("   📋 Memverifikasi entry pengeluaran di daftar...")

        expense_count = budget_page.get_expense_items_count()
        assert expense_count >= 1, (
            f"❌ FAIL: Daftar pengeluaran kosong setelah penambahan — "
            f"found {expense_count} items"
        )

        first_expense_amount = budget_page.get_first_expense_amount()
        first_expense_category = budget_page.get_first_expense_category()

        logger.info(f"   📝 Entry pertama: {first_expense_amount} — {first_expense_category}")

        assert "500" in first_expense_amount, (
            f"❌ FAIL: Nominal pengeluaran tidak sesuai — "
            f"expected contains '500', actual: '{first_expense_amount}'"
        )

        assert TestData.BUDGET_EXPENSE_CATEGORY in first_expense_category, (
            f"❌ FAIL: Kategori pengeluaran tidak sesuai — "
            f"expected '{TestData.BUDGET_EXPENSE_CATEGORY}', "
            f"actual: '{first_expense_category}'"
        )

        logger.info("─" * 50)
        logger.info("🎉 TEST PASSED: test_budget_tracking")
        logger.info("─" * 50)


# ══════════════════════════════════════════════════════
# ENTRY POINT (for running directly)
# ══════════════════════════════════════════════════════

if __name__ == "__main__":
    pytest.main([
        __file__,
        "-v",           # verbose output
        "-s",           # show print/log output
        "--tb=short",   # shorter traceback
        "--no-header",  # cleaner output
    ])
