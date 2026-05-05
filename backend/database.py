import sqlite3
from backend.transactions import Transaction
class DatabaseManager():
    def __init__(self):
        self.conn = sqlite3.connect("finance.db")
        self.cursor=self.conn.cursor()
        self.create_table()
    
    def create_table(self):

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS TRANSACTIONS(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL,
            category TEXT,
            t_type TEXT,
            date TEXT,
            description TEXT
            )
        """)
        self.conn.commit()
    def add_transaction(self,t):
        self.cursor.execute('''INSERT INTO TRANSACTIONS(amount,category,t_type,date,description) values(?,?,?,?,?)''',(t.amount,t.category,t.t_type,t.date,t.description))
        self.conn.commit()
    def get_transactions(self):
        self.cursor.execute("""SELECT * FROM TRANSACTIONS""")
        rows = self.cursor.fetchall()
        Transactions = []
        for row in rows:
            t=Transaction(
                amount=row[1],
                category=row[2],
                t_type=row[3],
                date=row[4],
                description=row[5],
                id=row[0]

            )
            Transactions.append(t)
        return Transactions
    def delete_transaction(self, id):
        self.cursor.execute("DELETE FROM TRANSACTIONS WHERE ID = ?", (id,))
        self.conn.commit()
    def update_transaction(self, id, amount, category, t_type, date, description):
        self.cursor.execute("""
            UPDATE TRANSACTIONS
            SET amount=?, category=?, t_type=?, date=?, description=?
            WHERE id=?
        """, (amount, category, t_type, date, description, id))
        self.conn.commit()