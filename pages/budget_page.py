"""
Budget Page Object
==================
Locators and actions for the "Budget Tracking" (Pelacakan Anggaran) feature
within the Mepo Travel Android application.

Covers: adding expenses, category selection, total validation, and expense history.
"""

import logging
from typing import List

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.remote.webelement import WebElement

from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class BudgetPage(BasePage):
    """Page Object for the Budget Tracking / Pelacakan Anggaran screen."""

    # ══════════════════════════════════════════════
    # LOCATORS — prioritizing accessibility_id
    # ══════════════════════════════════════════════

    # ── Page & Navigation ─────────────────────────
    PAGE_TITLE = (AppiumBy.ACCESSIBILITY_ID, "Pelacakan Anggaran")
    TAB_BUDGET = (AppiumBy.ACCESSIBILITY_ID, "Budget")
    TAB_BUDGET_ALT = (AppiumBy.ACCESSIBILITY_ID, "Pelacakan Anggaran")
    BACK_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "Navigate up")

    # ── Budget Summary ────────────────────────────
    TOTAL_BUDGET_AMOUNT = (AppiumBy.ID, "travel.mepo.app:id/tv_total_budget")
    TOTAL_EXPENSE_AMOUNT = (AppiumBy.ID, "travel.mepo.app:id/tv_total_expense")
    REMAINING_BUDGET = (AppiumBy.ID, "travel.mepo.app:id/tv_remaining_budget")
    BUDGET_PROGRESS_BAR = (AppiumBy.ID, "travel.mepo.app:id/progress_budget")
    BUDGET_PERCENTAGE = (AppiumBy.ID, "travel.mepo.app:id/tv_budget_percentage")

    # ── Add Expense ───────────────────────────────
    BTN_TAMBAH_ANGGARAN = (AppiumBy.ACCESSIBILITY_ID, "Tambah Anggaran")
    BTN_TAMBAH_PENGELUARAN = (AppiumBy.ACCESSIBILITY_ID, "Tambah Pengeluaran")
    INPUT_NOMINAL = (AppiumBy.ACCESSIBILITY_ID, "Masukkan jumlah pengeluaran")
    INPUT_NOMINAL_FIELD = (AppiumBy.ID, "travel.mepo.app:id/et_expense_amount")
    INPUT_DESCRIPTION = (AppiumBy.ID, "travel.mepo.app:id/et_expense_description")

    # ── Category Dropdown ─────────────────────────
    DROPDOWN_KATEGORI = (AppiumBy.ID, "travel.mepo.app:id/spinner_expense_category")
    DROPDOWN_KATEGORI_ALT = (AppiumBy.ACCESSIBILITY_ID, "Pilih Kategori")
    CATEGORY_TRANSPORTASI = (AppiumBy.ACCESSIBILITY_ID, "Transportasi")
    CATEGORY_MAKANAN = (AppiumBy.ACCESSIBILITY_ID, "Makanan")
    CATEGORY_PENGINAPAN = (AppiumBy.ACCESSIBILITY_ID, "Penginapan")
    CATEGORY_TIKET_WISATA = (AppiumBy.ACCESSIBILITY_ID, "Tiket Wisata")
    CATEGORY_LAINNYA = (AppiumBy.ACCESSIBILITY_ID, "Lainnya")

    # Category items in dropdown list (alternative XPath)
    CATEGORY_ITEM_XPATH = (
        AppiumBy.XPATH,
        "//android.widget.CheckedTextView[@text='{category}']"
    )

    # ── Save / Submit ─────────────────────────────
    BTN_SIMPAN_PENGELUARAN = (AppiumBy.ACCESSIBILITY_ID, "Simpan Pengeluaran")
    BTN_SIMPAN_ALT = (AppiumBy.ID, "travel.mepo.app:id/btn_save_expense")

    # ── Expense History List ──────────────────────
    EXPENSE_LIST = (AppiumBy.ID, "travel.mepo.app:id/rv_expense_list")
    EXPENSE_ITEM_FIRST = (AppiumBy.XPATH,
        "//androidx.recyclerview.widget.RecyclerView[@resource-id='travel.mepo.app:id/rv_expense_list']"
        "/android.view.ViewGroup[1]"
    )
    EXPENSE_ITEM_AMOUNT = (AppiumBy.ID, "travel.mepo.app:id/tv_expense_item_amount")
    EXPENSE_ITEM_CATEGORY = (AppiumBy.ID, "travel.mepo.app:id/tv_expense_item_category")
    EXPENSE_ITEM_DATE = (AppiumBy.ID, "travel.mepo.app:id/tv_expense_item_date")
    EMPTY_EXPENSE_STATE = (AppiumBy.ID, "travel.mepo.app:id/layout_empty_expense")

    # ── Edit / Delete Expense ─────────────────────
    BTN_EDIT_EXPENSE = (AppiumBy.ACCESSIBILITY_ID, "Edit Pengeluaran")
    BTN_DELETE_EXPENSE = (AppiumBy.ACCESSIBILITY_ID, "Hapus Pengeluaran")
    DELETE_CONFIRM_DIALOG = (AppiumBy.ID, "travel.mepo.app:id/dialog_delete_confirm")
    BTN_CONFIRM_DELETE = (AppiumBy.ACCESSIBILITY_ID, "Hapus")
    BTN_CANCEL_DELETE = (AppiumBy.ACCESSIBILITY_ID, "Batal")

    # ── Snackbar / Toast ──────────────────────────
    SUCCESS_SNACKBAR = (AppiumBy.ID, "travel.mepo.app:id/snackbar_text")
    TOAST_MESSAGE = (AppiumBy.XPATH, "//android.widget.Toast")

    # ── Loading ───────────────────────────────────
    LOADING_INDICATOR = (AppiumBy.ID, "travel.mepo.app:id/progress_budget_loading")

    # ══════════════════════════════════════════════
    # ACTIONS
    # ══════════════════════════════════════════════

    def wait_for_budget_page_loaded(self):
        """Wait until the Budget Tracking page is fully rendered."""
        self.dismiss_all_dialogs()
        # Try both possible page title locators
        if self.is_element_present(self.PAGE_TITLE, timeout=3):
            self.wait_for_page_load(self.PAGE_TITLE)
        else:
            self.wait_for_page_load(self.TAB_BUDGET)
        logger.info("💰 Budget page loaded")

    def navigate_to_budget_tab(self):
        """
        Tap on the 'Budget' / 'Pelacakan Anggaran' tab
        from within an itinerary detail view.
        """
        if self.is_element_present(self.TAB_BUDGET, timeout=3):
            self.tap(self.TAB_BUDGET)
        else:
            self.tap(self.TAB_BUDGET_ALT)
        logger.info("📊 Budget tab selected")

    # ── Read Budget Summary ───────────────────────

    def get_total_expense(self) -> str:
        """Return the total expense amount displayed on screen."""
        text = self.get_text(self.TOTAL_EXPENSE_AMOUNT)
        logger.info(f"💸 Total expense displayed: {text}")
        return text

    def get_total_budget(self) -> str:
        """Return the total budget amount displayed."""
        return self.get_text(self.TOTAL_BUDGET_AMOUNT)

    def get_remaining_budget(self) -> str:
        """Return the remaining budget amount displayed."""
        return self.get_text(self.REMAINING_BUDGET)

    # ── Add Expense Flow ──────────────────────────

    def tap_tambah_anggaran(self):
        """Tap the 'Tambah Anggaran' button to open expense form."""
        self.scroll_to_element(self.BTN_TAMBAH_ANGGARAN)
        self.tap(self.BTN_TAMBAH_ANGGARAN)
        logger.info("➕ 'Tambah Anggaran' tapped — expense form opening")

    def tap_tambah_pengeluaran(self):
        """Tap alternate 'Tambah Pengeluaran' button."""
        self.tap(self.BTN_TAMBAH_PENGELUARAN)
        logger.info("➕ 'Tambah Pengeluaran' tapped")

    def enter_expense_amount(self, amount: str):
        """
        Enter the expense nominal amount.

        Args:
            amount: Numeric string (e.g., '500000').
        """
        # Try accessibility_id first, fallback to resource ID
        if self.is_element_present(self.INPUT_NOMINAL, timeout=3):
            self.type_text(self.INPUT_NOMINAL, amount)
        else:
            self.type_text(self.INPUT_NOMINAL_FIELD, amount)
        self.hide_keyboard()
        logger.info(f"💵 Entered expense amount: {amount}")

    def enter_expense_description(self, description: str):
        """Enter a description for the expense."""
        self.type_text(self.INPUT_DESCRIPTION, description)
        self.hide_keyboard()
        logger.info(f"📝 Entered expense description: {description}")

    def select_category(self, category: str):
        """
        Select an expense category from the dropdown.

        Args:
            category: Category name (e.g., 'Makanan', 'Transportasi').
        """
        # Open dropdown
        if self.is_element_present(self.DROPDOWN_KATEGORI, timeout=3):
            self.tap(self.DROPDOWN_KATEGORI)
        else:
            self.tap(self.DROPDOWN_KATEGORI_ALT)
        logger.info(f"🔽 Category dropdown opened")

        # Select the requested category
        category_map = {
            "Transportasi": self.CATEGORY_TRANSPORTASI,
            "Makanan": self.CATEGORY_MAKANAN,
            "Penginapan": self.CATEGORY_PENGINAPAN,
            "Tiket Wisata": self.CATEGORY_TIKET_WISATA,
            "Lainnya": self.CATEGORY_LAINNYA,
        }

        if category in category_map:
            self.tap(category_map[category])
        else:
            # Fallback: scroll to category text
            self.scroll_to_text(category)
            category_locator = (
                AppiumBy.XPATH,
                f"//android.widget.CheckedTextView[@text='{category}']",
            )
            self.tap(category_locator)

        logger.info(f"✅ Category selected: {category}")

    def select_category_makanan(self):
        """Shortcut: select 'Makanan' category."""
        self.select_category("Makanan")

    def select_category_transportasi(self):
        """Shortcut: select 'Transportasi' category."""
        self.select_category("Transportasi")

    def tap_simpan_pengeluaran(self):
        """Tap the 'Simpan Pengeluaran' button to save the expense."""
        if self.is_element_present(self.BTN_SIMPAN_PENGELUARAN, timeout=3):
            self.tap(self.BTN_SIMPAN_PENGELUARAN)
        else:
            self.tap(self.BTN_SIMPAN_ALT)
        logger.info("💾 'Simpan Pengeluaran' tapped — saving expense")

    def add_expense(self, amount: str, category: str, description: str = ""):
        """
        Complete end-to-end flow: add a new expense.

        Args:
            amount: Numeric string (e.g., '500000').
            category: Category name (e.g., 'Makanan').
            description: Optional description text.
        """
        self.tap_tambah_anggaran()
        self.enter_expense_amount(amount)
        self.select_category(category)
        if description:
            self.enter_expense_description(description)
        self.tap_simpan_pengeluaran()
        logger.info(f"✅ Expense added: {amount} — {category}")

    # ── Expense List Validation ───────────────────

    def get_expense_items_count(self) -> int:
        """Return the number of expense items in the list."""
        items = self.find_elements(self.EXPENSE_ITEM_AMOUNT)
        count = len(items)
        logger.info(f"📋 Expense items count: {count}")
        return count

    def get_first_expense_amount(self) -> str:
        """Return the amount text of the first expense in the list."""
        return self.get_text(self.EXPENSE_ITEM_AMOUNT)

    def get_first_expense_category(self) -> str:
        """Return the category text of the first expense in the list."""
        return self.get_text(self.EXPENSE_ITEM_CATEGORY)

    def is_expense_empty_state(self) -> bool:
        """Check if the expense list is empty (no expenses recorded)."""
        return self.is_element_displayed(self.EMPTY_EXPENSE_STATE, timeout=self.SHORT_TIMEOUT)

    # ── Validation Helpers ────────────────────────

    def is_total_expense_updated(self, expected_substring: str) -> bool:
        """
        Verify the total expense display contains the expected value.

        Args:
            expected_substring: Partial text to match (e.g., '500.000').
        """
        total_text = self.get_total_expense()
        contains = expected_substring in total_text
        logger.info(
            f"{'✅' if contains else '❌'} Total expense check — "
            f"expected '{expected_substring}' in '{total_text}'"
        )
        return contains

    def is_success_message_displayed(self) -> bool:
        """Check if a success snackbar/toast is displayed after saving."""
        if self.is_element_present(self.SUCCESS_SNACKBAR, timeout=5):
            return True
        return self.is_element_present(self.TOAST_MESSAGE, timeout=3)

    # ── Delete Expense ────────────────────────────

    def delete_first_expense(self):
        """Long-press and delete the first expense item."""
        if self.is_element_present(self.EXPENSE_ITEM_FIRST):
            self.tap(self.EXPENSE_ITEM_FIRST)
            self.tap(self.BTN_DELETE_EXPENSE)
            self.find_element(self.DELETE_CONFIRM_DIALOG)
            self.tap(self.BTN_CONFIRM_DELETE)
            logger.info("🗑 First expense deleted")
