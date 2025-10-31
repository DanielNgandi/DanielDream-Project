import tkinter as tk
from tkinter import ttk
import sqlite3

class StockReportWindow:
    def __init__(self):
        self.stock_report_window = tk.Toplevel()
        self.stock_report_window.title("Stock Report")

        # calculate screen dimensions
        screen_width = self.stock_report_window.winfo_screenwidth()
        screen_height = self.stock_report_window.winfo_screenheight()

        # calculate window dimensions and position
        window_width = 800
        window_height = 400
        x = screen_width - window_width - 50
        y = (screen_height - window_height) // 2

        # set the window dimensions and position
        self.stock_report_window.geometry("{}x{}+{}+{}".format(window_width, window_height, x, y))
        self.stock_report_window.configure(bg='sky blue')

        # create a label for the title
        tk.Label(self.stock_report_window, text="Stock Report", bg='sky blue', font=("Arial", 16), padx=20, pady=10).pack()

        # create a frame for search and stock treeview
        search_frame = tk.Frame(self.stock_report_window, bg='sky blue')
        search_frame.pack(padx=20, pady=10)

        # create a label and dropdown for search category
        search_label = tk.Label(search_frame, text="Search By:", bg='sky blue')
        search_label.pack(side=tk.LEFT)

        self.category_var = tk.StringVar()
        category_dropdown = ttk.Combobox(search_frame, textvariable=self.category_var, values=["Category", "Product Name"])
        category_dropdown.pack(side=tk.LEFT, padx=10)

        # create an entry for search
        self.product_entry = tk.Entry(search_frame)
        self.product_entry.pack(side=tk.LEFT)

        # create a button for search
        search_button = tk.Button(search_frame, text="Search", command=self.search_stock, bg='sky blue')
        search_button.pack(side=tk.LEFT, padx=10)

        # create a frame for the stock treeview and scrollbar
        stock_frame = tk.Frame(self.stock_report_window)
        stock_frame.pack(fill=tk.BOTH, expand=1, padx=20, pady=10)

        # create a treeview to display the stock report
        self.stock_treeview = ttk.Treeview(stock_frame, columns=("ID", "Category", "Name", "Quantity", "Unit Price", "Date Added", "Total Value"), show="headings")
        self.stock_treeview.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        # add headings to the columns
        self.stock_treeview.heading("ID", text="ID")
        self.stock_treeview.heading("Category", text="Category")
        self.stock_treeview.heading("Name", text="Name")
        self.stock_treeview.heading("Quantity", text="Quantity")
        self.stock_treeview.heading("Unit Price", text="Unit Price")
        self.stock_treeview.heading("Date Added", text="Date Added")
        self.stock_treeview.heading("Total Value", text="Total Value")

        # set column widths
        self.stock_treeview.column("ID", width=50, anchor=tk.CENTER)
        self.stock_treeview.column("Category", width=100, anchor=tk.CENTER)
        self.stock_treeview.column("Name", width=100, anchor=tk.CENTER)
        self.stock_treeview.column("Quantity", width=100, anchor=tk.CENTER)
        self.stock_treeview.column("Unit Price", width=100, anchor=tk.CENTER)
        self.stock_treeview.column("Date Added", width=100, anchor=tk.CENTER)
        self.stock_treeview.column("Total Value", width=150, anchor=tk.CENTER)

        # fetch products and calculate total stock value
        self.fetch_products()
        self.calculate_total_stock_value()

    def fetch_products(self):
        # Fetch products from the database and populate the treeview
        conn = sqlite3.connect("dream_waters_inventory.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()
        conn.close()

        for product in products:
            product_id = product[0]
            category = product[5] if product[1] is not None else "Unknown Category"
            product_name = product[1]
            quantity = int(product[2])
            unit_price = float(product[3])
            date_added = product[4]
            total_value = quantity * unit_price
            self.stock_treeview.insert("", tk.END, values=(product_id, category, product_name, quantity, unit_price, date_added, total_value))

        # create a label for the total stock value
        self.total_value_label = tk.Label(self.stock_report_window, text="Total Stock Value: ", font=("Arial", 12), bg='sky blue')
        self.total_value_label.pack(pady=10)

    def calculate_total_stock_value(self, products=None):
        # Calculate the total stock value from the given products or all products if not provided
        if products is None:
            conn = sqlite3.connect("dream_waters_inventory.db")
            cursor = conn.cursor()
            cursor.execute("SELECT SUM(quantity * unit_price) FROM products")
            total_stock_value = cursor.fetchone()[0]
            conn.close()
        else:
            total_stock_value = sum(product[2] * product[3] for product in products)

        # Update the label to display the total stock value
        self.total_value_label.config(text="Total Stock Value: Kes{:,.2f}".format(total_stock_value))

    def search_stock(self):
        category = self.category_var.get()
        product_name = self.product_entry.get()

        # Clear the current treeview
        self.stock_treeview.delete(*self.stock_treeview.get_children())

        # Fetch products from the database based on the search criteria
        conn = sqlite3.connect("dream_waters_inventory.db")
        cursor = conn.cursor()

        if category == "Category":
            cursor.execute("SELECT * FROM products WHERE category LIKE ?", ('%' + product_name + '%',))
        elif category == "Product Name":
            cursor.execute("SELECT * FROM products WHERE name LIKE ?", ('%' + product_name + '%',))
        else:
            cursor.execute("SELECT * FROM products")

        products = cursor.fetchall()
        conn.close()

        for product in products:
            product_id = product[0]
            category = product[5] if product[1] is not None else "Unknown Category"
            product_name = product[1]
            quantity = int(product[2])
            unit_price = float(product[3])
            date_added = product[4]
            total_value = quantity * unit_price

            # Check if the search text contains a date range
            if "-" in product_name:
                from_date, to_date = product_name.split("-")
                if from_date.strip() <= date_added <= to_date.strip():
                    self.stock_treeview.insert("", tk.END, values=(product_id, category, product_name, quantity, unit_price, date_added, total_value))
            else:
                self.stock_treeview.insert("", tk.END, values=(product_id, category, product_name, quantity, unit_price, date_added, total_value))

        # Calculate the total stock value after the search
        self.calculate_total_stock_value(products)
