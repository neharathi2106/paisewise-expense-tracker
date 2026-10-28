"""Thin expense-management interface over the database module."""
from database import add_expense, update_expense, get_expenses, delete_expense, validate_expense

__all__ = ["add_expense", "update_expense", "get_expenses", "delete_expense", "validate_expense"]
