"""Input validation helpers.

Every function either returns a cleaned value or raises ValidationError with a
message that is safe to show directly to the user.
"""
import math
from datetime import datetime


class ValidationError(Exception):
    """Raised when user input is missing, malformed or out of range."""


# Characters that make Excel treat a text cell as a formula.
_FORMULA_PREFIXES = ("=", "+", "-", "@")


def validate_amount(value) -> float:
    """Convert value to a positive, finite float rounded to 2 decimals."""
    try:
        amount = float(value)
    except (TypeError, ValueError):
        raise ValidationError("Amount must be a valid number (e.g. 250.50).")

    # float() happily accepts "nan" and "inf", which would corrupt every total.
    if not math.isfinite(amount):
        raise ValidationError("Amount must be a finite number (e.g. 250.50).")

    if amount <= 0:
        raise ValidationError("Amount must be greater than zero.")

    return round(amount, 2)


def validate_non_empty(value, field_name: str = "Field") -> str:
    """Return value stripped of whitespace; reject None/blank input."""
    if value is None or not str(value).strip():
        raise ValidationError(f"{field_name} cannot be empty.")
    return str(value).strip()


def sanitize_text(value) -> str:
    """Strip text and neutralise spreadsheet formulas ("=1+1", "@cmd", ...).

    A leading apostrophe forces Excel to treat the cell as plain text, so user
    input can never be executed as a formula when the workbook is opened.
    """
    text = str(value).strip() if value is not None else ""
    if text.startswith(_FORMULA_PREFIXES):
        text = "'" + text
    return text


def validate_date(value: str) -> str:
    """Check that value is a real calendar date in YYYY-MM-DD format."""
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except (TypeError, ValueError):
        raise ValidationError("Date must be in YYYY-MM-DD format (e.g. 2026-09-28).")
    return value


def validate_positive_int(value, field_name: str = "Value") -> int:
    """Convert value to an int greater than zero (used for record ids)."""
    try:
        number = int(value)
    except (TypeError, ValueError):
        raise ValidationError(f"{field_name} must be a whole number.")
    if number <= 0:
        raise ValidationError(f"{field_name} must be a positive number.")
    return number
