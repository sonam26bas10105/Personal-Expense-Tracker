"""Reporting: category totals, CSV export and a category bar chart."""
import csv
import os

from database import DB_NAME, connect, data_rows
from logger import get_logger

logger = get_logger(__name__)


def _category_totals(wb) -> list:
    """Return [(category, total), ...] sorted by total, highest first."""
    totals = {}
    for row in data_rows(wb["Expenses"]):
        totals[row[2]] = totals.get(row[2], 0) + row[1]
    return sorted(totals.items(), key=lambda item: item[1], reverse=True)


def category_report(path: str = None) -> list:
    """Print spending per category (highest first) and return the rows."""
    wb = connect(path)
    rows = _category_totals(wb)

    print("\nExpense by Category")
    print("-" * 30)
    if not rows:
        print("No expenses recorded yet.")
    for category, total in rows:
        print(f"{category} : Rs.{total:.2f}")

    return rows


def export_to_csv(output_dir: str = None, path: str = None) -> str:
    """Write all expenses to Expense_Report.csv and return the file path.

    Returns None when there is nothing to export or the file cannot be written.
    """
    wb = connect(path)
    rows = sorted(data_rows(wb["Expenses"]), key=lambda r: r[0])

    if not rows:
        print("\nNo expenses found to export.")
        return None

    # Default to the project folder (next to expenses.xlsx), not the current
    # working directory, which may be a protected folder such as System32.
    directory = output_dir or os.path.dirname(DB_NAME)
    file_path = os.path.join(directory, "Expense_Report.csv")

    try:
        with open(file_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Amount", "Category", "Description", "Date"])
            writer.writerows(rows)
    except OSError as exc:
        logger.error("Failed to write export file %s: %s", file_path, exc)
        print(f"Error: could not write export file ({exc}).")
        return None

    logger.info("Exported %d expenses to %s", len(rows), file_path)
    print("\nExport successful!")
    print(f"File saved at:\n{file_path}")
    return file_path


def category_chart(output_dir: str = None, path: str = None) -> str:
    """Save a bar chart of spending per category as Category_Report.png.

    Returns the image path, or None when there is no data, matplotlib is not
    installed, or the file cannot be written.
    """
    wb = connect(path)
    rows = _category_totals(wb)

    if not rows:
        print("\nNo expenses recorded yet, nothing to chart.")
        return None

    try:
        import matplotlib

        matplotlib.use("Agg")  # file output only, no GUI window needed
        import matplotlib.pyplot as plt
    except ImportError:
        logger.error("matplotlib is not installed; chart skipped.")
        print("Error: matplotlib is required for charts (pip install matplotlib).")
        return None

    directory = output_dir or os.path.dirname(DB_NAME)
    file_path = os.path.join(directory, "Category_Report.png")

    labels = [category for category, _ in rows]
    values = [total for _, total in rows]

    fig, ax = plt.subplots(figsize=(7, 4))
    try:
        bars = ax.bar(labels, values, color="#4472C4")
        ax.bar_label(bars, fmt="Rs.%.2f", padding=3, fontsize=8)
        ax.set_title("Spending by Category")
        ax.set_ylabel("Total (Rs.)")
        ax.margins(y=0.12)
        fig.tight_layout()
        fig.savefig(file_path, dpi=120)
    except OSError as exc:
        logger.error("Failed to write chart %s: %s", file_path, exc)
        print(f"Error: could not write chart file ({exc}).")
        return None
    finally:
        plt.close(fig)

    logger.info("Category chart saved to %s", file_path)
    print(f"\nChart saved at:\n{file_path}")
    return file_path
