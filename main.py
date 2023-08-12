import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import tkinter.messagebox
import os
from datetime import datetime

def save_budget():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    folder_name = "budgets"  # Name of the folder within the script's directory
    folder_path = os.path.join(os.path.dirname(__file__), folder_name)
    os.makedirs(folder_path, exist_ok=True)  # Create the folder if it doesn't exist
    file_path = os.path.join(folder_path, f"budget_info_{timestamp}.txt")
    
    with open(file_path, 'w') as file:
        for t_type, category, amount in transactions:
            file.write(f'{t_type},{category},{amount}\n')
    tk.messagebox.showinfo("Success", "Budget information saved successfully.")

def reset_budget():
    global transactions
    transactions = []
    update_balance()
    update_log()
    tk.messagebox.showinfo("Success", "Budget has been reset.")

from tkinter import filedialog

def load_budget():
    global transactions
    budgets_folder = os.path.join(os.path.dirname(__file__), "budgets") # Path to the budgets folder
    file_path = filedialog.askopenfilename(initialdir=budgets_folder, defaultextension=".txt", filetypes=[("Text Files", "*.txt")])

    if file_path:
        try:
            with open(file_path, 'r') as file:
                transactions = []
                for line in file:
                    t_type, category, amount = line.strip().split(',')
                    transactions.append((t_type, category, float(amount)))
                update_balance()
                update_log()
            tk.messagebox.showinfo("Success", "Budget information loaded successfully.")
        except Exception as e:
            tk.messagebox.showerror("Error", str(e))
    else:
        tk.messagebox.showwarning("Canceled", "Budget loading was canceled.")

def add_transaction(transaction_type):
    try:
        amount = float(transaction_amount.get())
        category = transaction_category.get() if transaction_type == 'expense' else 'No Category' # If income, set category to 'No Category'
        if transaction_type == 'expense':
            amount = -amount

        transactions.append((transaction_type, category, amount))
        update_balance()
        update_log()
    except ValueError:
        tk.messagebox.showerror("Error", "Please enter a valid amount.")

def update_log():
    log_text.config(state=tk.NORMAL)  # Temporarily enable the widget
    log_text.delete(1.0, tk.END)
    for t_type, category, amount in transactions:
        category_text = category if category else 'No Category' # If category is empty, set to 'No Category'
        log_text.insert(tk.END, f"{t_type.capitalize()}: {category_text} - ${abs(amount)}\n")
    log_text.config(state=tk.DISABLED)  # Disable the widget again

def update_balance():
    global balance
    balance = 0.0
    for t_type, _, amount in transactions:
        if t_type == 'expense':
            balance -= amount
        else:
            balance += amount
    balance_label.config(text="Current Balance: $" + str(balance))

import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox

def show_report():
    global transactions
    expenses = {}

    for transaction in transactions:
        print(transaction)  # Debugging line to print the structure
        type, category, amount_str = transaction  # Example unpacking

        if type != "expense":  # You might want to handle incomes differently
            continue

        try:
            amount = float(amount_str)  # Convert amount to float
        except ValueError:
            print(f"Could not convert amount for category {category}: {amount_str}")
            continue

        expenses[category] = expenses.get(category, 0) + amount

    positive_expenses = {k: v for k, v in expenses.items() if v > 0}

    if positive_expenses:
        plt.pie(positive_expenses.values(), labels=positive_expenses.keys(), autopct='%1.1f%%')
        plt.show()
    else:
        tk.messagebox.showinfo("No Expenses", "No expenses to show in the report.")

# Initialize
balance = 0.0
transactions = []
bold_font = ("Helvetica", 10, "bold")

# Create window
root = tk.Tk()
root.title("Savvy")
root.geometry('600x600') # Adjusted size
root.configure(bg='#333333')
icon_path = os.path.join(os.path.dirname(__file__), 'icon.ico')
root.iconbitmap(icon_path)

# Transaction type
transaction_type_label = tk.Label(root, text="Transaction Type:", bg='#333333', fg='#ffffff', font=bold_font)
transaction_type_label.grid(row=0, column=0, pady=5, padx=5, sticky='w')
transaction_type = tk.StringVar(value='income')
transaction_type_menu = ttk.Combobox(root, textvariable=transaction_type, values=['income', 'expense'], state="readonly")
transaction_type_menu.grid(row=0, column=1, pady=5, padx=5, columnspan=3, sticky='ew')

# Clear category when income is selected
def clear_category(event=None):
    if transaction_type.get() == 'income':
        transaction_category.set('') # Clear the category

# Binding an event to the Combobox
transaction_type_menu.bind('<<ComboboxSelected>>', clear_category)

# Categories
transaction_category_label = tk.Label(root, text="Select Category:", bg='#333333', fg='#ffffff', font=bold_font)
transaction_category_label.grid(row=1, column=0, pady=5, padx=5, sticky='w')
transaction_category = tk.StringVar()
transaction_category_menu = ttk.Combobox(root, textvariable=transaction_category, values=['Food', 'Transport', 'Salary', 'Entertainment', 'Other'], state="readonly")
transaction_category_menu.grid(row=1, column=1, pady=5, padx=5, columnspan=3, sticky='ew')

# Amount
transaction_amount_label = tk.Label(root, text="Enter Amount:", bg='#333333', fg='#ffffff', font=bold_font)
transaction_amount_label.grid(row=2, column=0, pady=5, padx=5, sticky='w')
transaction_amount = tk.Entry(root, bg='#555555', fg='#ffffff', insertbackground='white')
transaction_amount.grid(row=2, column=1, pady=5, padx=5, columnspan=3, sticky='ew')

# Add buttons
add_button = tk.Button(root, text="Add Transaction", command=lambda: add_transaction(transaction_type.get()), bg='#4caf50', fg='#ffffff')
add_button.grid(row=3, column=0, pady=5, padx=5, sticky='ew')

# Report button
report_button = tk.Button(root, text="Show Report", command=show_report, bg='#f44336', fg='#ffffff')
report_button.grid(row=3, column=1, pady=5, padx=5, sticky='ew')

# Save button
save_button = tk.Button(root, text="Save Budget", command=save_budget, bg='#2196f3', fg='#ffffff')
save_button.grid(row=3, column=2, pady=5, padx=5, sticky='ew')

# Load button
load_button = tk.Button(root, text="Load Budget", command=load_budget, bg='#2196f3', fg='#ffffff')
load_button.grid(row=3, column=3, pady=5, padx=5, sticky='ew')

# Create a frame for the log
log_frame = tk.Frame(root, bg='#333333')
log_frame.grid(row=5, column=0, pady=5, padx=5, columnspan=4, sticky='nsew') # Include padding

# Log label inside the frame
log_label = tk.Label(log_frame, text="Transactions Log:", bg='#333333', fg='#ffffff', font=bold_font)
log_label.pack(side='top', fill='x', pady=0, padx=5) # Using pack inside the frame

# Log text inside the frame
log_text = tk.Text(log_frame, wrap=tk.WORD, height=15, bg='#555555', fg='#ffffff')
log_text.pack(side='top', fill='both', expand=True) # Using pack inside the frame

# Balance label
balance_label = tk.Label(root, text="Current Balance: $" + str(balance), bg='#333333', fg='#ffffff', font=("Helvetica", 14, "bold"))
balance_label.grid(row=6, column=0, pady=10, columnspan=4, sticky='w') # Moved down one row

# Reset Budget button
reset_button = tk.Button(root, text="Reset Budget", command=reset_budget, bg='#ff5722', fg='#ffffff')
reset_button.grid(row=6, column=3, pady=5, padx=5, sticky='e') # Positioned at the bottom right corner

# Adjust column weights
for i in range(4):
    root.grid_columnconfigure(i, weight=1)

# Adjust row weights
root.grid_rowconfigure(5, weight=1) # Keep the log growing

root.mainloop()