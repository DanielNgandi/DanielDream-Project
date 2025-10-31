import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
import sqlite3
import datetime
from datetime import datetime
import webbrowser
from babel import numbers

class SalesReportWindow:
    def __init__(self):
        # Create the sales report window
        self.sales_report_window = tk.Toplevel()
        self.sales_report_window.title("Sales Report")
        

        # calculate screen dimensions
        screen_width = self.sales_report_window.winfo_screenwidth()
        screen_height = self.sales_report_window.winfo_screenheight()
        # calculate window dimensions and position
        window_width = 800
        window_height = 400
        x = screen_width - window_width - 50
        y = (screen_height - window_height) // 2

        # set the window dimensions and position
        self.sales_report_window.geometry("{}x{}+{}+{}".format(window_width, window_height, x, y))
        self.sales_report_window.configure(bg='sky blue')

        # create a label for the title
        tk.Label(self.sales_report_window, text="Sales Report", bg='sky blue', font=("Arial", 16), padx=20, pady=10).pack()

        # create a frame for the search options and search button
        search_frame = tk.Frame(self.sales_report_window, bg='sky blue')
        search_frame.pack(pady=10)

        # create a label for the search options
        tk.Label(search_frame, text="Search by:", bg='sky blue').pack(side=tk.LEFT)

        # create a combobox for the search options
        self.search_option = ttk.Combobox(search_frame, values=["Category", "Product Name"])
        self.search_option.pack(side=tk.LEFT)

        # create a frame for the search entry and search button
        search_entry_frame = tk.Frame(self.sales_report_window, bg='sky blue')
        search_entry_frame.pack(pady=10)

        # create an entry for the search
        self.search_entry = tk.Entry(search_entry_frame)
        self.search_entry.pack(side=tk.LEFT)

        # create a search button
        search_button = tk.Button(search_entry_frame, text="Search", command=self.search_sales, bg='sky blue')
        search_button.pack(side=tk.LEFT)

        # create a frame for the date range search
        date_frame = tk.Frame(self.sales_report_window, bg='sky blue')
        date_frame.pack(pady=10)

        # create a label for the date range search
        tk.Label(date_frame, text="Search by Date Range:", bg='sky blue').pack(side=tk.LEFT)

        # create an entry for the "from" date
        self.from_date_entry = DateEntry(date_frame)
        self.from_date_entry.pack(side=tk.LEFT, padx=5)

        # create an entry for the "to" date
        self.to_date_entry = DateEntry(date_frame)
        self.to_date_entry.pack(side=tk.LEFT, padx=5)

        # create a search button for date range search
        date_search_button = tk.Button(date_frame, text="Search", bg='sky blue', command=self.search_sales_by_date_range)
        date_search_button.pack(side=tk.LEFT)
        
        # create a frame for the print button
        print_frame = tk.Frame(self.sales_report_window, bg='sky blue')
        print_frame.pack(pady=10)

        # create a print button
        print_button = tk.Button(print_frame, text="Print", command=self.print_sales, bg='sky blue')
        print_button.pack(side=tk.LEFT)


        # create a frame for the sales treeview and scrollbar
        sales_frame = tk.Frame(self.sales_report_window)
        sales_frame.pack(fill=tk.BOTH, expand=1, padx=20, pady=10)

        # create a treeview to display the sales
        self.sales_treeview = ttk.Treeview(sales_frame, columns=("ID", "category", "product_name", "quantity", "total_price", "date_sold"),
                                            show="headings")
        self.sales_treeview.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        # add headings to the columns
        self.sales_treeview.heading("ID", text="ID")
        self.sales_treeview.heading("category", text="Category")
        self.sales_treeview.heading("product_name", text="Product Name")
        self.sales_treeview.heading("quantity", text="Quantity")
        self.sales_treeview.heading("total_price", text="Total Price")
        self.sales_treeview.heading("date_sold", text="Date Sold")

        # set column widths
        self.sales_treeview.column("ID", width=50, anchor=tk.CENTER)
        self.sales_treeview.column("category", width=100, anchor=tk.CENTER)
        self.sales_treeview.column("product_name", width=100, anchor=tk.CENTER)
        self.sales_treeview.column("quantity", width=100, anchor=tk.CENTER)
        self.sales_treeview.column("total_price", width=100, anchor=tk.CENTER)
        self.sales_treeview.column("date_sold", width=150, anchor=tk.CENTER)

        # create a scrollbar for the treeview
        scrollbar = tk.Scrollbar(sales_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # set the scrollbar to control the treeview
        self.sales_treeview.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.sales_treeview.yview)

        # fetch and populate sales data
        self.fetch_sales()

    def fetch_sales(self):
        # Fetch all sales from the database and populate the treeview
        conn = sqlite3.connect("dream_waters_inventory.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT sales.sale_id, products.category, products.product_name, sales.quantity, sales.total_price, sales.date_sold FROM sales JOIN products ON sales.product_id=products.product_id")
        sales = cursor.fetchall()
        conn.close()

        self.populate_sales_treeview(sales)

    def populate_sales_treeview(self, sales):
        # Clear the treeview before populating with new sales data
        self.sales_treeview.delete(*self.sales_treeview.get_children())

        # Populate the treeview with the sales data
        for sale in sales:
            self.sales_treeview.insert("", tk.END, values=sale)

    def search_sales(self):
        # Get the selected search option and search query
        search_option = self.search_option.get()
        search_query = self.search_entry.get()

        if search_option == "Category":
            self.search_sales_by_category(search_query)
        elif search_option == "Product Name":
            self.search_sales_by_product_name(search_query)

    def search_sales_by_category(self, category):
        # Fetch sales with the specified category from the database
        conn = sqlite3.connect("dream_waters_inventory.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT sales.sale_id, products.category, products.product_name, sales.quantity, sales.total_price, sales.date_sold FROM sales JOIN products ON sales.product_id=products.product_id WHERE products.category LIKE ?", ('%' + category + '%',))
        sales = cursor.fetchall()
        conn.close()

        self.populate_sales_treeview(sales)

    def search_sales_by_product_name(self, product_name):
        # Fetch sales with the specified product name from the database
        conn = sqlite3.connect("dream_waters_inventory.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT sales.sale_id, products.category, products.product_name, sales.quantity, sales.total_price, sales.date_sold FROM sales JOIN products ON sales.product_id=products.product_id WHERE products.product_name LIKE ?", ('%' + product_name + '%',))
        sales = cursor.fetchall()
        conn.close()

        self.populate_sales_treeview(sales)

    def search_sales_by_date_range(self):
        # Get the "from" and "to" dates
        from_date = self.from_date_entry.get()
        to_date = self.to_date_entry.get()

        # Convert input date format to the format expected by the query
        from_date = datetime.strptime(from_date, "%m/%d/%y").strftime("%Y-%m-%d 00:00:00")
        to_date = datetime.strptime(to_date, "%m/%d/%y").strftime("%Y-%m-%d 23:59:59")

        # Fetch sales within the specified date range from the database
        conn = sqlite3.connect("dream_waters_inventory.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT sales.sale_id, products.category, products.product_name, sales.quantity, sales.total_price, sales.date_sold FROM sales JOIN products ON sales.product_id=products.product_id WHERE sales.date_sold BETWEEN ? AND ?",
            (from_date, to_date))
        sales = cursor.fetchall()
        conn.close()

        # Populate the sales treeview with the fetched sales data
        self.populate_sales_treeview(sales)

        
    def show_date_range_search(self):
        # Create a new window for date range selection
        date_window = tk.Toplevel(self.sales_report_window)
        date_window.title("Date Range Selection")

        # Create a label for the "from" date entry
        from_label = tk.Label(date_window, text="From:")
        from_label.pack(pady=10)

        # Create an entry for the "from" date
        self.from_date_entry = DateEntry(date_window, date_pattern="yyyy-mm-dd HH:MM")
        self.from_date_entry.pack(pady=5)

        # Create a label for the "to" date entry
        to_label = tk.Label(date_window, text="To:")
        to_label.pack(pady=10)

        # Create an entry for the "to" date
        self.to_date_entry = DateEntry(date_window, date_pattern="yyyy-mm-dd HH:MM")
        self.to_date_entry.pack(pady=5)

        # Create a search button
        search_button = tk.Button(date_window, text="Search", command=self.search_sales_by_date_range)
        search_button.pack(pady=10)
        
    def print_sales(self):
        # Create an HTML table with the sales data
        html = "<html><head><title>Sales Report</title></head><body><table border='1' cellspacing='0' cellpadding='5'><thead><tr><th>ID</th><th>Category</th><th>Product Name</th><th>Quantity</th><th>Total Price</th><th>Date Sold</th></tr></thead><tbody>"

        # Get all the sales data from the treeview
        sales = self.sales_treeview.get_children()

        for sale in sales:
            values = self.sales_treeview.item(sale)['values']
            html += "<tr>"
            for value in values:
                html += "<td>{}</td>".format(value)
            html += "</tr>"

        html += "</tbody></table></body></html>"

        # Create a temporary HTML file
        with open("sales_report.html", "w") as file:
            file.write(html)

        # Open the HTML file in a web browser for printing
        webbrowser.open("sales_report.html")