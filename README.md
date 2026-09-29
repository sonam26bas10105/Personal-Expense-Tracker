# Personal Expense Tracker

A menu-driven Python command-line application that helps users record daily expenses, organise them into categories, track spending against a monthly budget, and produce reports. All data is stored offline in a single Excel workbook (`expenses.xlsx`).

## Overview

Keeping track of daily spending is difficult when expenses are spread across phone notes, messages, or memory. This project offers a simple, private, offline solution: record each expense, group it by category, compare the current month's spending with a budget, and export the records to CSV or a chart whenever needed. Inputs are validated, important actions are written to a log file, and invalid input or storage problems are handled without crashing the program.

## Features

| Module | What it does |
|---|---|
| **Expense management (CRUD)** | Add, view (newest first, as a table), update (blank = keep current) and delete expenses |
| **Category management** | Add categories (duplicates rejected, case-insensitive) and view them alphabetically. Categories used on expenses are registered automatically |
| **Budget tracking** | Set a monthly budget; see budget / spent / remaining **for the current month** and get a warning when exceeded |
| **Reporting** | Category-wise totals sorted highest first, optional bar chart (`Category_Report.png`), and export of all expenses to `Expense_Report.csv` |
| **Input validation** | Amounts must be positive, finite numbers (`nan`/`inf` rejected); text fields cannot be blank; IDs must be positive integers; text starting with `=`, `+`, `-` or `@` is stored as plain text, never as an Excel formula |
| **Error handling** | Storage errors (workbook open in Excel, unwritable export folder) are caught and reported; unexpected errors never end the program |
| **Logging** | Actions, warnings and errors are written to `expense_tracker.log` |

## Technologies used

- **Python 3.9+**
- **openpyxl**: reads/writes the Excel workbook used as storage
- **matplotlib**: draws the category bar chart
- **csv, logging, datetime, os, math**: Python standard library
- **unittest**: test framework (standard library)
- **Git / GitHub**: version control

## Project structure

```
expense-tracker/
├── main.py            
├── expense.py
├── categories.py     
├── budget.py          
├── report.py          
├── database.py        
├── validators.py      
├── logger.py          
├── utils.py           
├── requirements.txt
├── statement.md       
├── tests/             
└── docs/
    ├── diagrams/      
    ├── screenshots/
    └── Project_Report.pdf
```

## Installation and running

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd expense-tracker

# 2. (Optional) create a virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run
python main.py
```

`expenses.xlsx`, `Expense_Report.csv` and `Category_Report.png` are all created in the project folder (next to the source files), so it does not matter which directory you launch the program from.

### Menu

```
1.  Add Expense          6.  View Categories
2.  View Expenses        7.  Set Budget
3.  Update Expense       8.  Check Budget
4.  Delete Expense       9.  Category Report (offers a bar chart)
5.  Add Category         10. Export to CSV
                         11. Exit
```

## Testing

The test suite uses only the standard library (the chart tests use matplotlib) and runs against temporary workbooks, so your real `expenses.xlsx` is never touched.

```bash
python -m unittest discover -s tests -t . -v
```

Expected result: `Ran 74 tests ... OK`.

| Test file | Tests | Covers |
|---|---|---|
| `test_validators.py` | 14 | amount (incl. `nan`/`inf`), non-empty, formula sanitising, date, positive-int |
| `test_database.py` | 6 | table creation, idempotency, id generation, row lookup |
| `test_expense.py` | 24 | add / view / update / delete, invalid input, missing ids, category linking, formula safety |
| `test_categories.py` | 9 | add, duplicate rejection (case-insensitive), trimming, sorted listing, `ensure_category` |
| `test_budget.py` | 8 | set, replace, check, overspend warning, invalid input, per-month spending |
| `test_report.py` | 9 | category totals, CSV export, chart output, unwritable-folder handling |
| `test_main.py` | 4 | menu routing, invalid choices, category feedback, crash protection |

## Screenshots

| | |
|---|---|
| ![Menu](docs/screenshots/01_main_menu.png.png) | ![Categories](docs/screenshots/02_categories.png.png) |
| ![Expenses](docs/screenshots/03_add_view_expenses.png.png) | ![Update and delete](docs/screenshots/04_update_delete.png.png) |
| ![Budget and report](docs/screenshots/05_budget_report_export.png.png) | ![Unit tests](docs/screenshots/06_unit_tests.png.png) |
| ![Log](docs/screenshots/07_log_file.png) | |


