"""SQLite persistence for the AI-powered expense tracker."""
from __future__ import annotations
import os
import sqlite3
from contextlib import contextmanager
from datetime import date
from pathlib import Path
from typing import Iterator

DB_PATH = Path(os.environ.get("EXPENSE_TRACKER_DB", Path(__file__).with_name("expenses.db")))
CATEGORIES = ("Food", "Travel", "Shopping", "Education", "Bills", "Healthcare", "Entertainment", "Other")

@contextmanager
def connection(db_path: str | Path | None = None) -> Iterator[sqlite3.Connection]:
    path = Path(db_path) if db_path else DB_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def initialize_database(db_path: str | Path | None = None) -> None:
    with connection(db_path) as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            amount REAL NOT NULL CHECK(amount > 0),
            category TEXT NOT NULL,
            expense_date TEXT NOT NULL,
            notes TEXT NOT NULL DEFAULT '',
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )""")
        conn.execute("""CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY, value TEXT NOT NULL
        )""")

def validate_expense(title: str, amount: float, category: str, expense_date: str) -> None:
    if not title or not title.strip(): raise ValueError("Title is required.")
    try: amount = float(amount)
    except (TypeError, ValueError): raise ValueError("Amount must be a valid number.")
    if amount <= 0: raise ValueError("Amount must be greater than zero.")
    if not category or not category.strip(): raise ValueError("Category is required.")
    try: date.fromisoformat(str(expense_date))
    except (TypeError, ValueError): raise ValueError("Date must be a valid ISO date (YYYY-MM-DD).")

def add_expense(title: str, amount: float, category: str, expense_date: str, notes: str = "", db_path=None) -> int:
    validate_expense(title, amount, category, expense_date)
    with connection(db_path) as conn:
        cur = conn.execute("INSERT INTO expenses(title, amount, category, expense_date, notes) VALUES (?, ?, ?, ?, ?)",
                           (title.strip(), float(amount), category.strip(), str(expense_date), (notes or "").strip()))
        return int(cur.lastrowid)

def update_expense(expense_id: int, title: str, amount: float, category: str, expense_date: str, notes: str = "", db_path=None) -> bool:
    validate_expense(title, amount, category, expense_date)
    with connection(db_path) as conn:
        cur = conn.execute("UPDATE expenses SET title=?, amount=?, category=?, expense_date=?, notes=? WHERE id=?",
                           (title.strip(), float(amount), category.strip(), str(expense_date), (notes or "").strip(), int(expense_id)))
        return cur.rowcount > 0

def get_expenses(db_path=None):
    with connection(db_path) as conn:
        rows = conn.execute("SELECT id,title,amount,category,expense_date,notes FROM expenses ORDER BY expense_date DESC, id DESC").fetchall()
    return [dict(r) for r in rows]

def delete_expense(expense_id: int, db_path=None) -> bool:
    with connection(db_path) as conn:
        cur = conn.execute("DELETE FROM expenses WHERE id=?", (int(expense_id),))
        return cur.rowcount > 0

def get_monthly_budget(db_path=None) -> float:
    with connection(db_path) as conn:
        row = conn.execute("SELECT value FROM settings WHERE key='monthly_budget'").fetchone()
    return float(row[0]) if row else 0.0

def set_monthly_budget(amount: float, db_path=None) -> None:
    try: amount = float(amount)
    except (TypeError, ValueError): raise ValueError("Budget must be a valid number.")
    if amount <= 0: raise ValueError("Budget must be greater than zero.")
    with connection(db_path) as conn:
        conn.execute("INSERT INTO settings(key,value) VALUES('monthly_budget',?) ON CONFLICT(key) DO UPDATE SET value=excluded.value", (str(amount),))
