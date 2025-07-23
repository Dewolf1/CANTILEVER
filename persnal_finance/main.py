import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# --------------------------
# Database setup
# --------------------------

conn = sqlite3.connect('finance_dashboard.db')
cursor = conn.cursor()

# Create income table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS income (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL,
        date TEXT,
        description TEXT
    )
''')

# Create expenses table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL,
        date TEXT,
        category TEXT,
        description TEXT
    )
''')

conn.commit()

# --------------------------
# Main window setup
# --------------------------

root = tk.Tk()
root.title("Personal Finance Dashboard")

# --------------------------
# Income section
# --------------------------

tk.Label(root, text="Add Income").grid(row=0, column=0, columnspan=2, pady=5)

tk.Label(root, text="Amount:").grid(row=1, column=0)
income_amount_entry = tk.Entry(root)
income_amount_entry.grid(row=1, column=1)

tk.Label(root, text="Description:").grid(row=2, column=0)
income_desc_entry = tk.Entry(root)
income_desc_entry.grid(row=2, column=1)

def add_income():
    try:
        amt = float(income_amount_entry.get())
        desc = income_desc_entry.get()
        today = datetime.now().strftime("%Y-%m-%d")
        cursor.execute("INSERT INTO income (amount, date, description) VALUES (?, ?, ?)", (amt, today, desc))
        conn.commit()
        income_amount_entry.delete(0, tk.END)
        income_desc_entry.delete(0, tk.END)
        update_dashboard()
    except:
        messagebox.showerror("Error", "Enter valid income amount!")

tk.Button(root, text="Add Income", command=add_income).grid(row=3, column=0, columnspan=2, pady=5)

# --------------------------
# Expense section
# --------------------------

tk.Label(root, text="Add Expense").grid(row=4, column=0, columnspan=2, pady=5)

tk.Label(root, text="Amount:").grid(row=5, column=0)
expense_amount_entry = tk.Entry(root)
expense_amount_entry.grid(row=5, column=1)

tk.Label(root, text="Category:").grid(row=6, column=0)
expense_cat_entry = tk.Entry(root)
expense_cat_entry.grid(row=6, column=1)

tk.Label(root, text="Description:").grid(row=7, column=0)
expense_desc_entry = tk.Entry(root)
expense_desc_entry.grid(row=7, column=1)

def add_expense():
    try:
        amt = float(expense_amount_entry.get())
        cat = expense_cat_entry.get()
        desc = expense_desc_entry.get()
        today = datetime.now().strftime("%Y-%m-%d")
        cursor.execute("INSERT INTO expenses (amount, date, category, description) VALUES (?, ?, ?, ?)",
                       (amt, today, cat, desc))
        conn.commit()
        expense_amount_entry.delete(0, tk.END)
        expense_cat_entry.delete(0, tk.END)
        expense_desc_entry.delete(0, tk.END)
        update_dashboard()
    except:
        messagebox.showerror("Error", "Enter valid expense amount!")

tk.Button(root, text="Add Expense", command=add_expense).grid(row=8, column=0, columnspan=2, pady=5)

# --------------------------
# Summary section
# --------------------------

income_label = tk.Label(root, text="Total Income: ₹0.00", font=("Arial", 12, "bold"))
income_label.grid(row=9, column=0, columnspan=2, pady=2)

expenses_label = tk.Label(root, text="Total Expenses: ₹0.00", font=("Arial", 12, "bold"))
expenses_label.grid(row=10, column=0, columnspan=2, pady=2)

balance_label = tk.Label(root, text="Balance: ₹0.00", font=("Arial", 12, "bold"))
balance_label.grid(row=11, column=0, columnspan=2, pady=2)

# --------------------------
# Charts frames side by side
# --------------------------

chart_frame = tk.Frame(root)
chart_frame.grid(row=12, column=0, columnspan=2, pady=10)

bar_chart_frame = tk.Frame(chart_frame)
bar_chart_frame.pack(side=tk.LEFT, padx=20)

pie_chart_frame = tk.Frame(chart_frame)
pie_chart_frame.pack(side=tk.LEFT, padx=20)

# --------------------------
# Dashboard update function
# --------------------------

def update_dashboard():
    # Update summary
    cursor.execute("SELECT SUM(amount) FROM income")
    total_income = cursor.fetchone()[0] or 0

    cursor.execute("SELECT SUM(amount) FROM expenses")
    total_expenses = cursor.fetchone()[0] or 0

    balance = total_income - total_expenses

    income_label.config(text=f"Total Income: ₹{total_income:.2f}")
    expenses_label.config(text=f"Total Expenses: ₹{total_expenses:.2f}")
    balance_label.config(text=f"Balance: ₹{balance:.2f}")

    # Clear old charts
    for widget in bar_chart_frame.winfo_children():
        widget.destroy()
    for widget in pie_chart_frame.winfo_children():
        widget.destroy()

    # Bar chart: Expenses by Category
    cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    data = cursor.fetchall()
    categories = [row[0] for row in data]
    amounts = [row[1] for row in data]

    if categories:
        fig1, ax1 = plt.subplots(figsize=(4, 3))
        ax1.bar(categories, amounts, color='skyblue')
        ax1.set_title("Expenses by Category")
        ax1.set_xlabel("Category")
        ax1.set_ylabel("Amount (₹)")
        ax1.tick_params(axis='x', rotation=45)
        bar_canvas = FigureCanvasTkAgg(fig1, master=bar_chart_frame)
        bar_canvas.draw()
        bar_canvas.get_tk_widget().pack()

        # Pie chart: Expense Distribution
        fig2, ax2 = plt.subplots(figsize=(4, 3))
        ax2.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=140)
        ax2.set_title("Expense Distribution")
        ax2.axis('equal')
        pie_canvas = FigureCanvasTkAgg(fig2, master=pie_chart_frame)
        pie_canvas.draw()
        pie_canvas.get_tk_widget().pack()

# --------------------------
# Initialize
# --------------------------

update_dashboard()
root.mainloop()
