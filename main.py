import sqlite3
from backend.database import DatabaseManager
from backend.transactions import Transaction
db = DatabaseManager()
t = Transaction(500, "Food", "Expense", "2026-04-09", "Swiggy")
db.add_transaction(t)
data =db.get_transactions()
print(data)
for i in data:
    print(i)