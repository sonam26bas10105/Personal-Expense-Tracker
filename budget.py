"""Budget tracking: store one monthly budget and compare it with spending."""
from datetime import datetime

from database import StorageError, connect, data_rows, save_book
from logger import get_logger
from validators import ValidationError, validate_amount

logger = get_logger(__name__)


def set_budget(amount=None, path: str = None) -> str:
    """Store the monthly budget, replacing any previous value."""
    if amount is None:
        amount = input("Enter monthly budget: ")

    try:
        clean_amount = validate_amount(amount)
    except ValidationError as exc:
        logger.warning("Rejected budget input: %s", exc)
        print(f"Error: {exc}")
        return f"Error: {exc}"

    try:
        wb = connect(path)
        ws = wb["Budget"]
        ws.delete_rows(2, ws.max_row)  # keep the header, drop the old value
        ws.append([clean_amount])
        save_book(wb, path)
    except StorageError as exc:
        print(f"Error: {exc}")
        return f"Error: {exc}"

    logger.info("Budget set to %s", clean_amount)
    print("Budget saved.")
    return "Budget saved."


def check_budget(path: str = None, month: str = None) -> dict:
    """Compare the budget with spending in one calendar month.

    month is "YYYY-MM" and defaults to the current month. Only expenses whose
    date falls in that month count as spent. Returns a dict with the keys
    budget, spent and remaining (budget and remaining are None when no budget
    has been set).
    """
    month = month or datetime.now().strftime("%Y-%m")
    wb = connect(path)

    budget_rows = data_rows(wb["Budget"])
    spent = round(
        sum(row[1] for row in data_rows(wb["Expenses"]) if str(row[4])[:7] == month), 2
    )

    if not budget_rows:
        print("\nNo budget has been set yet. Use 'Set Budget' first.")
        return {"budget": None, "spent": spent, "remaining": None}

    budget = budget_rows[0][0]
    remaining = round(budget - spent, 2)

    print(f"\nMonth    : {month}")
    print("Budget   :", budget)
    print("Spent    :", spent)
    print("Remaining:", remaining)
    if remaining < 0:
        print("Warning: you have exceeded your monthly budget!")

    return {"budget": budget, "spent": spent, "remaining": remaining}
