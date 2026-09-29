# Project – Personal Expense Tracker

## Problem statement

Many people struggle to keep track of their daily spending because expenses are often scattered across notes or memory. This makes it hard to monitor a monthly budget, and manually maintained spreadsheets can easily lead to errors such as negative amounts, missing categories or duplicate entries. A simple expense tracker helps by keeping records organized, validating inputs, and providing clear spending summaries.

## Scope of the project

**In scope**
- A single-user, offline, command-line application written in Python
- Expense CRUD (add, view, update, delete)
- Category creation and listing (case-insensitive, linked to expenses)
- Setting a monthly budget and checking budget / spent / remaining for the current month
- Category-wise spending report, bar chart and CSV export
- Input validation, structured error handling and file logging
- Persistent storage in an Excel workbook (`expenses.xlsx`) with three sheets: Expenses, Categories, Budget
- Automated unit tests

## Target users

- College students managing a monthly allowance
- Individuals who want a simple, private, offline expense log
- Anyone who prefers to keep data in Excel so it can be opened, filtered and shared

## High-level features

1. **Expense management**: add, view, update and delete expenses with automatic ids and dates
2. **Category management**: add unique categories and list them alphabetically; new categories used on expenses are registered automatically
3. **Budget tracking**: set a monthly budget, view the remaining balance for the current month, warning on overspend
4. **Reports and export**: totals by category (highest first), bar chart, and CSV export
5. **Validation and error handling**: rejects invalid amounts (including `nan`/`inf`), blank fields and bad ids; neutralises spreadsheet formulas in text
6. **Logging**: every action, warning and error recorded in `expense_tracker.log`
7. **Testing**: 74 automated unit tests using `unittest`, run on temporary workbooks
