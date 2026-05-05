import tkinter as tk
from backend.database import DatabaseManager
from backend.transactions import Transaction

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("FinSight")
        self.root.geometry("600x500")

        self.db = DatabaseManager()

        tk.Label(root, text="FinSight", font=("Arial", 20)).pack(pady=10)

        frame = tk.Frame(root)
        frame.pack(pady=10)
        self.summary_label = tk.Label(root, text="", font=("Arial", 14))
        self.summary_label.pack(pady=5)
        # Amount
        tk.Label(frame, text="Amount").grid(row=0, column=0)
        self.amount = tk.Entry(frame)
        self.amount.grid(row=0, column=1)

        # Category
        tk.Label(frame, text="Category").grid(row=1, column=0)
        self.category = tk.Entry(frame)
        self.category.grid(row=1, column=1)

        # Type
        tk.Label(frame, text="Type").grid(row=2, column=0)
        self.t_type = tk.Entry(frame)
        self.t_type.grid(row=2, column=1)

        # Date
        tk.Label(frame, text="Date").grid(row=3, column=0)
        self.date = tk.Entry(frame)
        self.date.grid(row=3, column=1)

        # Description
        tk.Label(frame, text="Description").grid(row=4, column=0)
        self.description = tk.Entry(frame)
        self.description.grid(row=4, column=1)

        # Button
        tk.Button(root, text="Add Transaction", command=self.add_transaction).pack(pady=10)
        tk.Button(root, text="Show Chart", command=self.show_chart).pack(pady=5)
        tk.Label(root, text="Delete by ID").pack()
        self.delete_entry = tk.Entry(root)
        self.delete_entry.pack(pady=5)

        tk.Button(root, text="Delete", command=self.delete_transaction).pack(pady=5)
        self.filter_var = tk.StringVar(value="All")

        tk.OptionMenu(root, self.filter_var, "All", "Income", "Expense").pack(pady=5)
        tk.Label(root, text="Update by ID").pack()
        self.update_id_entry = tk.Entry(root)
        self.update_id_entry.pack(pady=5)

        tk.Button(root, text="Update Transaction", command=self.update_transaction).pack(pady=5)
        # Output
        self.output = tk.Text(root, height=10)
        self.output.pack(pady=10)
        self.filter_var.trace("w", lambda *args: self.refresh_transactions())
        self.refresh_transactions() 

    def add_transaction(self):
        try:
            t = Transaction(
                self.amount.get(),
                self.category.get(),
                self.t_type.get(),
                self.date.get(),
                self.description.get()
            )

            self.db.add_transaction(t)
            self.refresh_transactions()
            self.amount.delete(0, tk.END)
            self.category.delete(0, tk.END)
            self.t_type.delete(0, tk.END)
            self.date.delete(0, tk.END)
            self.description.delete(0, tk.END)
        except Exception as e:
            self.output.insert(tk.END, f"Error: {e}\n")
    def refresh_transactions(self):
        self.output.delete("1.0", tk.END)

        data = self.db.get_transactions()

        filtered_data = []

        for t in data:
            if self.filter_var.get() == "All" or t.t_type.lower() == self.filter_var.get().lower():
                self.output.insert(tk.END, f"{t}\n")
                filtered_data.append(t)

        self.update_summary(filtered_data)
    def update_summary(self,data):
        data = self.db.get_transactions()

        income = 0
        expense = 0

        for t in data:
            if t.t_type.lower() == "income":
                income += t.amount
            else:
                expense += t.amount

        balance = income - expense

        self.summary_label.config(
            text=f"Balance: ₹{balance} | Income: ₹{income} | Expense: ₹{expense}"
        )
    def show_chart(self):
        import matplotlib.pyplot as plt
        data = self.db.get_transactions()
        category_data= {}
        for t in data:
            if t.t_type.lower()== "expense":
                if t.category in category_data:
                    category_data[t.category] +=t.amount
                else:
                    category_data[t.category] =t.amount
        if not category_data:
            self.output.insert(tk.END,"No expense data for chart \n")
            return 
        labels = list(category_data.keys())    
        values = list(category_data.values())    

        plt.figure()
        plt.pie(values,labels=labels,autopct='%1.1f%%')
        plt.title("expenses by category")
        plt.show()
    def delete_transaction(self):
        try:
            id = int(self.delete_entry.get())

            self.db.delete_transaction(id)
            self.refresh_transactions()

            self.delete_entry.delete(0, tk.END)

        except Exception as e:
            self.output.insert(tk.END, f"Error: {e}\n")
    def update_transaction(self):
        try:
            id = int(self.update_id_entry.get())

            self.db.update_transaction(
                id,
                float(self.amount.get()),
                self.category.get(),
                self.t_type.get(),
                self.date.get(),
                self.description.get()
            )

            self.refresh_transactions()
            self.update_id_entry.delete(0, tk.END)

        except Exception as e:
            self.output.insert(tk.END, f"Error: {e}\n")
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()