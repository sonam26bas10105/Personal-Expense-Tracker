"""Expense management: the Create / Read / Update / Delete operations."""
from datetime import datetime

from database import StorageError, connect, data_rows, find_row, next_id, save_book
from categories import ensure_category
from logger import get_logger
from validators import (
    ValidationError,
    sanitize_text,
    validate_amount,
    validate_non_empty,
    validate_positive_int,
)

logger = get_logger(__name__)


def add_expense(amount=None, category=None, description=None, path: str = None):
    """Validate and store a new expense dated today.

    Any argument left as None is asked for interactively. The category is
    matched case-insensitively against the Categories sheet and registered
    automatically if it is new. Returns a result message.
    """
    if amount is None:
        amount = input("Enter amount: ")
    if category is None:
        category = input("Enter category: ")
    if description is None:
        description = input("Description: ")

    try:
        clean_amount = validate_amount(amount)
        clean_category = sanitize_text(validate_non_empty(category, "Category"))
        clean_description = sanitize_text(description) if description else ""
    except ValidationError as exc:
        logger.warning("Rejected expense input: %s", exc)
        print(f"Error: {exc}")
        return f"Error: {exc}"

    today = datetime.now().strftime("%Y-%m-%d")

    try:
        wb = connect(path)
        ws = wb["Expenses"]
        clean_category = ensure_category(wb, clean_category)
        ws.append([next_id(ws), clean_amount, clean_category, clean_description, today])
        save_book(wb, path)
    except StorageError as exc:
        logger.error("Storage error while adding expense: %s", exc)
        print(f"Error: {exc}")
        return f"Error: {exc}"

    logger.info("Expense added: amount=%s category=%s", clean_amount, clean_category)
    print("Expense saved.")
    return "Expense saved."


def show_expenses(path: str = None) -> list:
    """Print all expenses (newest first) as a table and return the raw rows."""
    wb = connect(path)
    rows = sorted(data_rows(wb["Expenses"]), key=lambda r: r[0], reverse=True)

    print("\nAll Expenses")
    print("-" * 66)
    if not rows:
        print("No expenses recorded yet.")
    else:
        print(f"{'ID':<5}{'Amount':>10}  {'Category':<14}{'Date':<12}Description")
        for rid, amount, category, description, date in rows:
            print(f"{rid:<5}{amount:>10.2f}  {str(category):<14}{str(date):<12}{description or ''}")

    return rows


def update_expense(expense_id, amount=None, category=None, description=None, path: str = None) -> str:
    """Change the given fields of an expense; None means "keep current value"."""
    try:
        clean_id = validate_positive_int(expense_id, "Expense ID")
    except ValidationError as exc:
        return f"Error: {exc}"

    try:
        wb = connect(path)
        ws = wb["Expenses"]
        row = find_row(ws, clean_id)
        if row is None:
            logger.warning("Attempted to update missing expense id=%s", clean_id)
            return f"Error: no expense found with ID {clean_id}."

        updates = {}

        if amount is not None:
            try:
                updates[2] = validate_amount(amount)
            except ValidationError as exc:
                return f"Error: {exc}"

        if category is not None:
            try:
                updates[3] = ensure_category(
                    wb, sanitize_text(validate_non_empty(category, "Category"))
                )
            except ValidationError as exc:
                return f"Error: {exc}"

        if description is not None:
            updates[4] = sanitize_text(description)

        if not updates:
            return "Nothing to update."

        for column, value in updates.items():
            ws.cell(row=row, column=column, value=value)
        save_book(wb, path)
    except StorageError as exc:
        return f"Error: {exc}"

    logger.info("Expense %s updated.", clean_id)
    return f"Expense {clean_id} updated."


def delete_expense(expense_id, path: str = None) -> str:
    """Delete the expense with the given id. Returns a result message."""
    try:
        clean_id = validate_positive_int(expense_id, "Expense ID")
    except ValidationError as exc:
        return f"Error: {exc}"

    try:
        wb = connect(path)
        ws = wb["Expenses"]
        row = find_row(ws, clean_id)
        if row is None:
            return f"Error: no expense found with ID {clean_id}."

        ws.delete_rows(row)
        save_book(wb, path)
    except StorageError as exc:
        return f"Error: {exc}"

    logger.info("Expense %s deleted.", clean_id)
    return f"Expense {clean_id} deleted."
