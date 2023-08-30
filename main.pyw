import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import tkinter.messagebox
import os
from datetime import datetime
import sys

def initialize_app():
    # Create the SavvyBudgets folder inside Documents
    folder_path = os.path.join(os.path.expanduser("~"), "Documents", "SavvyBudgets")
    os.makedirs(folder_path, exist_ok=True)
    
    # Check if examplebudget.txt exists, if not, create it
    example_file_path = os.path.join(folder_path, "example.txt")
    if not os.path.exists(example_file_path):
        with open(example_file_path, 'w') as file:
            file.write("Income,Salary,5000,None\n")
            file.write("expense,Housing,1200,Rent\n")
            file.write("expense,Utilities,150,Electricity, Water, Gas\n")
            file.write("expense,Food,200,Groceries\n")
            file.write("expense,Transport,100,Public Transport\n")
            file.write("Income,Freelance Income,1000,None\n")
            file.write("expense,Healthcare,200,Doctor Visit\n")
            file.write("expense,Insurance,150,Car Insurance\n")
            file.write("expense,Education,300,Online Courses\n")
            file.write("expense,Debt Payments,200,Credit Card Payment\n")
            file.write("Income,Dividends,200,None\n")
            file.write("expense,Entertainment,100,Movie Tickets\n")
            file.write("Income,Interest Income,50,None\n")
            file.write("expense,Self Help,50,Books\n")
            file.write("expense,Other,100,Household Items\n")

# Call the initialize_app function when the app starts
initialize_app()


if getattr(sys, 'frozen', False):
    base_dir = os.path.dirname(sys.executable)
else:
    base_dir = os.path.dirname(os.path.abspath(__file__))

icon_path = os.path.join(base_dir, 'assets', 'icon.ico')

def save_budget():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    folder_path = os.path.join(os.path.expanduser("~"), "Documents", "SavvyBudgets")
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, f"budget_info_{timestamp}.txt")
    
    with open(file_path, 'w') as file:
        for t_type, category, amount, description in transactions: # Include the description
            file.write(f'{t_type},{category},{amount},{description}\n') # Include the description
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
    budgets_folder = os.path.join(os.path.expanduser("~"), "Documents", "SavvyBudgets")
    file_path = filedialog.askopenfilename(initialdir=budgets_folder, defaultextension=".txt", filetypes=[("Text Files", "*.txt")])

    if file_path:
        try:
            with open(file_path, 'r') as file:
                transactions = []
                for line in file:
                    t_type, category, amount, *description = line.strip().split(',')
                    description = ', '.join(description)
                    transactions.append((t_type, category, float(amount.strip()), description)) # Include the description
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
        description = transaction_description.get() if transaction_description.get() else 'None'
        category = transaction_category.get() if transaction_category.get() else 'No Category'

        transactions.append((transaction_type, category, amount, description))
        update_balance()
        update_log()
    except ValueError:
        tk.messagebox.showerror("Error", "Please enter a valid amount.")


def update_log():
    log_text.config(state=tk.NORMAL)
    log_text.delete(1.0, tk.END)
    for t_type, category, amount, description in transactions: # Include the description
        category_text = category if category else 'No Category'
        log_text.tag_configure("bold", font=("Helvetica", 10, "bold"))
        log_text.insert(tk.END, f"${abs(amount)} ", "bold")
        log_text.insert(tk.END, f"- {t_type.capitalize()}: {category_text} - Description: {description}\n")

    log_text.config(state=tk.DISABLED)

def update_balance():
    global balance
    balance = 0.0
    for t_type, category, amount, description in transactions:
        if t_type.lower() == 'income':
            balance += amount
        elif t_type.lower() == 'expense':
            balance -= amount
    balance_label.config(text="Current Balance: $" + str(balance))



def show_report():
    global transactions
    expenses = {}

    for transaction in transactions:
        print(transaction)  # Debugging line to print the structure
        type, category, amount_str, description = transaction  # Include the description

        if type != "Expense":  # You might want to handle incomes differently
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
root.geometry('600x700') # Adjusted size
root.configure(bg='#333333')
root.iconbitmap(icon_path)

from ttkthemes import ThemedTk

# Create a notebook
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill='both')

# Create frames for each tab
tab1 = ttk.Frame(notebook)
tab2 = ttk.Frame(notebook)

# Add the frames to the notebook
notebook.add(tab1, text="Logs")
notebook.add(tab2, text="Comming Soon")

# Configure the style
style = ttk.Style()
style.theme_create('custom', parent='alt', settings={
    "TNotebook": {"configure": {"background": '#333333', "tabmargins": [0, 0, 0, 0]}},
    "TNotebook.Tab": {
        "configure": {"background": '#555555', "foreground": 'white', "borderwidth": 1, "padding": [10, 5], "highlightthickness": 0},
        "map": {"background": [("selected", "#333333")], "foreground": [("selected", 'white')], "expand": [("selected", [1, 1, 1, 0])]}
    },
    "TFrame": {"configure": {"background": '#333333', "borderwidth": 0}},
    "TCombobox": {
        "configure": {
            "selectbackground": '#333333', 
            "selectforeground": '#ffffff',
            "fieldbackground": '#555555', 
            "background": '#555555', 
            "foreground": '#ffffff'
        },
        "map": {
            "fieldbackground": [("readonly", '#555555')],
            "selectbackground": [("readonly", '#333333'), ("readonly focus", '#333333'), ("!readonly focus", '#333333')],
            "selectforeground": [("readonly", '#ffffff')],
            "foreground": [("readonly", '#ffffff')]
        },
    },
})

style.theme_use('custom')



# Create a style
style = ttk.Style()

# Transaction type
transaction_type_label = tk.Label(tab1, text="Transaction Type:", bg='#333333', fg='#ffffff', font=bold_font)
transaction_type_label.grid(row=0, column=0, pady=5, padx=5, sticky='w')
transaction_type = tk.StringVar(value='Income')
transaction_type_menu = ttk.Combobox(tab1, textvariable=transaction_type, values=['Income', 'Expense'], state="readonly")
transaction_type_menu.grid(row=0, column=1, pady=5, padx=5, columnspan=3, sticky='ew')

def clear_category(event=None):
    transaction_category_menu.config(state='normal')
    transaction_category_menu.config(state='readonly')
    if transaction_type.get() == 'income':
        transaction_category.set(None) # Clear the category


# Binding an event to the Combobox
transaction_type_menu.bind('<<ComboboxSelected>>', clear_category)

# Categories
transaction_category_label = tk.Label(tab1, text="Select Category:", bg='#333333', fg='#ffffff', font=bold_font)
transaction_category_label.grid(row=1, column=0, pady=5, padx=5, sticky='w')
transaction_category = tk.StringVar()
transaction_category_menu = ttk.Combobox(tab1, textvariable=transaction_category, values=['Food', 'Transport', 'Salary', 'Entertainment', 'Rent/Mortgage', 'Utilities', 'Groceries', 'Healthcare', 'Insurance', 'Dining Out', 'Clothing and Accessories', 'Personal Care', 'Other'], state="readonly")
transaction_category_menu.grid(row=1, column=1, pady=5, padx=5, columnspan=3, sticky='ew')

transaction_category_menu.bind('<<ComboboxSelected>>', clear_category)

# Amount
transaction_amount_label = tk.Label(tab1, text="Enter Amount:", bg='#333333', fg='#ffffff', font=bold_font)
transaction_amount_label.grid(row=2, column=0, pady=5, padx=5, sticky='w')
transaction_amount = tk.Entry(tab1, bg='#555555', fg='#ffffff', insertbackground='white')
transaction_amount.grid(row=2, column=1, pady=5, padx=5, columnspan=3, sticky='ew')

# Description
transaction_description_label = tk.Label(tab1, text="Description:", bg='#333333', fg='#ffffff', font=bold_font)
transaction_description_label.grid(row=3, column=0, pady=5, padx=5, sticky='w')
transaction_description = tk.Entry(tab1, bg='#555555', fg='#ffffff', insertbackground='white')
transaction_description.grid(row=3, column=1, pady=5, padx=5, columnspan=3, sticky='ew')

# Add buttons
add_button = tk.Button(tab1, text="Add Transaction", command=lambda: add_transaction(transaction_type.get()), bg='#4caf50', fg='#ffffff')
add_button.grid(row=4, column=0, pady=5, padx=5, sticky='ew')

# Report button
report_button = tk.Button(tab1, text="Show Report", command=show_report, bg='#f44336', fg='#ffffff')
report_button.grid(row=4, column=1, pady=5, padx=5, sticky='ew')

# Save button
save_button = tk.Button(tab1, text="Save Budget", command=save_budget, bg='#2196f3', fg='#ffffff')
save_button.grid(row=4, column=2, pady=5, padx=5, sticky='ew')

# Load button
load_button = tk.Button(tab1, text="Load Budget", command=load_budget, bg='#2196f3', fg='#ffffff')
load_button.grid(row=4, column=3, pady=5, padx=5, sticky='ew')

# Create a frame for the log
log_frame = tk.Frame(tab1, bg='#333333')
log_frame.grid(row=5, column=0, pady=5, padx=5, columnspan=4, sticky='nsew') # Include padding

# Log label inside the frame
log_label = tk.Label(log_frame, text="Transactions Log:", bg='#333333', fg='#ffffff', font=bold_font)
log_label.pack(side='top', fill='x', pady=0, padx=5) # Using pack inside the frame

# Log text inside the frame
log_text = tk.Text(log_frame, wrap=tk.WORD, height=15, bg='#555555', fg='#ffffff')
log_text.pack(side='top', fill='both', expand=True) # Using pack inside the frame
log_text.config(state=tk.DISABLED) # disable editing

# Balance label
balance_label = tk.Label(tab1, text="Current Balance: $" + str(balance), bg='#333333', fg='#ffffff', font=("Helvetica", 14, "bold"))
balance_label.grid(row=6, column=0, pady=10, columnspan=4, sticky='w') # Moved down one row

# Reset Budget button
reset_button = tk.Button(tab1, text="Reset Budget", command=reset_budget, bg='#ff5722', fg='#ffffff')
reset_button.grid(row=6, column=3, pady=5, padx=5, sticky='e') # Positioned at the bottom right corner

# Clear category and update category options when transaction type is selected
def update_category_options(event=None):
    selected_type = transaction_type.get()
    if selected_type == 'Income':
        transaction_category_menu['values'] = [
            'Salary', 'Overtime', 'Investments',
            'Bonus', 'Dividends', 'Interest Income',
            'Rental Income', 'Freelance Income', 'Business Income',
            'Pension', 'Social Security', 'Other'
        ]
        transaction_category.set('')
    elif selected_type == 'Expense':
        transaction_category_menu['values'] = [
            'Food', 'Transport', 'Entertainment', 'Self Help',
            'Housing', 'Utilities', 'Healthcare',
            'Insurance', 'Education', 'Debt Payments',
            'Other'
        ]
        transaction_category.set('')

def on_combobox_selected(event):
    event.widget.selection_clear()
    update_category_options()
    
    

transaction_type_menu.bind('<<ComboboxSelected>>', on_combobox_selected)
transaction_category_menu.bind('<<ComboboxSelected>>', clear_category)

# Categories
transaction_category_label = tk.Label(tab1, text="Select Category:", bg='#333333', fg='#ffffff', font=bold_font)
transaction_category_label.grid(row=1, column=0, pady=5, padx=5, sticky='w')
transaction_category = tk.StringVar()
transaction_category_menu = ttk.Combobox(tab1, textvariable=transaction_category, state="readonly")
transaction_category_menu.grid(row=1, column=1, pady=5, padx=5, columnspan=3, sticky='ew')

# Set initial category options
update_category_options()

# Adjust column weights
for i in range(4):
    tab1.grid_columnconfigure(i, weight=1)

# Adjust row weights
tab1.grid_rowconfigure(5, weight=1) # Keep the log growing


root.mainloop()
