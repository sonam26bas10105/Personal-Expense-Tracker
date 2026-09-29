"""Command-line entry point: shows the menu and routes choices to the modules."""
from database import create_tables
from expense import add_expense, show_expenses, update_expense, delete_expense
from budget import set_budget, check_budget
from report import category_chart, category_report, export_to_csv
from categories import add_category, show_categories
from utils import line
from logger import get_logger

logger = get_logger(__name__)


MENU = """
1.  Add Expense
2.  View Expenses
3.  Update Expense
4.  Delete Expense
5.  Add Category
6.  View Categories
7.  Set Budget
8.  Check Budget
9.  Category Report
10. Export to CSV
11. Exit
"""


def run():
    """Main loop: show the menu until the user chooses Exit (11)."""
    create_tables()
    logger.info("Application started.")

    while True:
        line()
        print("PERSONAL EXPENSE TRACKER")
        line()
        print(MENU)

        choice = input("Enter choice: ").strip()

        try:
            if choice == "1":
                add_expense()
            elif choice == "2":
                show_expenses()
            elif choice == "3":
                expense_id = input("Expense ID to update: ")
                amount = input("New amount (leave blank to keep current): ").strip() or None
                category = input("New category (leave blank to keep current): ").strip() or None
                description = input("New description (leave blank to keep current): ").strip() or None
                print(update_expense(expense_id, amount, category, description))
            elif choice == "4":
                expense_id = input("Expense ID to delete: ")
                print(delete_expense(expense_id))
            elif choice == "5":
                print(add_category())
            elif choice == "6":
                show_categories()
            elif choice == "7":
                set_budget()
            elif choice == "8":
                check_budget()
            elif choice == "9":
                category_report()
                if input("\nAlso save a bar chart? (y/n): ").strip().lower() == "y":
                    category_chart()
            elif choice == "10":
                export_to_csv()
            elif choice == "11":
                print("Thank you.")
                logger.info("Application exited normally.")
                break
            else:
                print("Invalid choice.")
        except Exception as exc:
            logger.error("Unhandled error for menu choice %s: %s", choice, exc)
            print(f"Something went wrong: {exc}")


if __name__ == "__main__":
    run()
