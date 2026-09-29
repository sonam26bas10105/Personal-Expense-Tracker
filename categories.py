"""Category management: add, list and resolve category names."""
from database import StorageError, connect, data_rows, next_id, save_book
from logger import get_logger
from validators import ValidationError, sanitize_text, validate_non_empty

logger = get_logger(__name__)


def ensure_category(wb, name: str) -> str:
    """Return the canonical spelling of a category, registering it if new.

    Matching is case-insensitive, so "Food" and "food" are the same category.
    The workbook is modified in memory only; the caller is responsible for
    saving it. This links the free-text category on an expense to the
    Categories sheet.
    """
    ws = wb["Categories"]
    for row in data_rows(ws):
        if row[1].lower() == name.lower():
            return row[1]
    ws.append([next_id(ws), name])
    logger.info("Category auto-registered: %s", name)
    return name


def add_category(name=None, path: str = None):
    """Add a unique category. Prompts for the name when none is given.

    Returns a message string (also used by the menu to show feedback).
    """
    if name is None:
        name = input("Enter category name: ")

    try:
        clean_name = sanitize_text(validate_non_empty(name, "Category name"))
    except ValidationError as e:
        logger.warning("Rejected category input: %s", e)
        return f"Error: {e}"

    try:
        wb = connect(path)
        ws = wb["Categories"]

        existing = [row[1].lower() for row in data_rows(ws)]
        if clean_name.lower() in existing:
            logger.warning("Duplicate category rejected: %s", clean_name)
            return f"Category '{clean_name}' already exists."

        ws.append([next_id(ws), clean_name])
        save_book(wb, path)
    except StorageError as exc:
        return f"Error: {exc}"

    logger.info("Category added: %s", clean_name)
    return f"Category '{clean_name}' added."


def show_categories(path: str = None):
    """Print all categories alphabetically and return them as a list."""
    wb = connect(path)
    names = sorted(row[1] for row in data_rows(wb["Categories"]))

    print("\nCategories")
    print("-" * 16)

    if not names:
        print("(none yet)")
    else:
        for name in names:
            print(name)

    return names
