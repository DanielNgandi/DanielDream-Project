import tkinter as tk
import sqlite3
from tkinter import messagebox
from datetime import date
from tkinter import ttk
import getpass
import datetime

class AdminAddStockWindow:
    def __init__(self):
       # create a new top-level window for adding a product
        self.add_product_window = tk.Toplevel()
        self.add_product_window.title("Manage Stock")
        
         # calculate screen dimensions
        screen_width = self.add_product_window.winfo_screenwidth()
        screen_height = self.add_product_window.winfo_screenheight()

        # calculate window dimensions and position
        window_width = 650
        window_height = 450
        x = screen_width - window_width - 50
        y = (screen_height - window_height) // 2

        # set the window dimensions and position
        self.add_product_window.geometry("{}x{}+{}+{}".format(window_width, window_height, x, y))
        self.add_product_window.configure(bg='sky blue')
        
        # create a form for adding a product
        tk.Label(self.add_product_window, text="Category:", bg='sky blue').grid(row=0, column=0, padx=5, pady=5)
        category_entry = tk.Entry(self.add_product_window)
        category_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(self.add_product_window, text="Product Name:", bg='sky blue').grid(row=2, column=0, padx=5, pady=5)
        product_name_entry = tk.Entry(self.add_product_window)
        product_name_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.add_product_window, text="Quantity:", bg='sky blue').grid(row=4, column=0, padx=5, pady=5)
        quantity_entry = tk.Entry(self.add_product_window)
        quantity_entry.grid(row=4, column=1, padx=5, pady=5)

        tk.Label(self.add_product_window, text="Unit Price:", bg='sky blue').grid(row=6, column=0, padx=5, pady=5)
        unit_price_entry = tk.Entry(self.add_product_window)
        unit_price_entry.grid(row=6, column=1, padx=5, pady=5)
        
        # create a treeview to display products
        products_frame = tk.Frame(self.add_product_window)
        products_frame.grid(row=12, column=0, columnspan=10, padx=5, pady=5)

        products_treeview = ttk.Treeview(products_frame)
        products_treeview.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)

        # create scrollbars for the treeview
        x_scrollbar = ttk.Scrollbar(products_frame, orient=tk.HORIZONTAL, command=products_treeview.xview)
        x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        y_scrollbar = ttk.Scrollbar(products_frame, orient=tk.VERTICAL, command=products_treeview.yview)
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # configure the treeview
        products_treeview.configure(xscrollcommand=x_scrollbar.set, yscrollcommand=y_scrollbar.set)
        products_treeview["columns"] = ("Sale_ID", "category", "name", "quantity", "price", "date_added")
        products_treeview.heading("#0", text="")
        products_treeview.heading("Sale_ID",text="Sale_ID")
        products_treeview.heading("category", text="Category")
        products_treeview.heading("name", text="Product Name")
        products_treeview.heading("quantity", text="Quantity")
        products_treeview.heading("price", text="Unit Price")
        products_treeview.heading("date_added", text="Date Added")
        products_treeview.column("#0", width=0, stretch="no")
        products_treeview.column("Sale_ID", width=50, anchor=tk.CENTER)
        products_treeview.column("category", width=100, anchor=tk.CENTER)
        products_treeview.column("name", width=150, anchor=tk.CENTER)
        products_treeview.column("quantity", width=100, anchor=tk.CENTER)
        products_treeview.column("price", width=100, anchor=tk.CENTER)
        products_treeview.column("date_added", width=100, anchor=tk.CENTER)

        # populate the treeview with existing products
        conn = sqlite3.connect('dream_waters_inventory.db')
        c = conn.cursor()
        c.execute("SELECT Product_ID, category, product_name, quantity, unit_price, date_added FROM products")
        products = c.fetchall()
        for product in products:
            products_treeview.insert("", tk.END, values=(product[0], product[1], product[2], product[3], product[4], product[5]))
            
        # create a function to update the form with product data when a product is clicked in the treeview
        def update_form(event):
            selected_item = products_treeview.focus()
            if not selected_item:
                return

            selected_product = products_treeview.item(selected_item)["values"]
            if not selected_product or len(selected_product) < 5:
                return
            #selected_product = products_treeview.item(products_treeview.focus())["values"]
            category_entry.delete(0, tk.END)
            product_name_entry.delete(0, tk.END)
            quantity_entry.delete(0, tk.END)
            unit_price_entry.delete(0, tk.END)

            category_entry.insert(0, selected_product[1])
            product_name_entry.insert(0, selected_product[2])
            quantity_entry.insert(0, selected_product[3])
            unit_price_entry.insert(0, selected_product[4])

        # bind the update_form function to clicks on the treeview
        products_treeview.bind("<<TreeviewSelect>>", update_form)
        
        def get_current_username():
            return getpass.getuser()

        def get_current_datetime():
            return datetime.datetime.now()
        
        # create a function to update the selected product in the database
        def update_product():
            selected_product = products_treeview.item(products_treeview.focus())["values"]
            product_id = selected_product[0]
            new_category = category_entry.get()
            new_product_name = product_name_entry.get()
            new_quantity = quantity_entry.get()
            new_unit_price = unit_price_entry.get()

            # update the product in the database
            conn = sqlite3.connect('dream_waters_inventory.db')
            c = conn.cursor()
            c.execute("UPDATE products SET category = ?, product_name = ?, quantity = ?, unit_price = ? WHERE product_id = ?",
                    (new_category, new_product_name, new_quantity, new_unit_price, product_id))
            conn.commit()

            # clear the form and update the treeview with the new data
            category_entry.delete(0, tk.END)
            product_name_entry.delete(0, tk.END)
            quantity_entry.delete(0, tk.END)
            unit_price_entry.delete(0, tk.END)
            products_treeview.delete(*products_treeview.get_children())

            c.execute("SELECT Product_ID, category, product_name, quantity, unit_price, date_added FROM products")
            products = c.fetchall()
            for product in products:
                products_treeview.insert("", tk.END, values=product)

            # Log the history entry
            action = "Update"  # Action type for update operation
            product_name = new_product_name  # Get the updated product name
            category = new_category  # Get the updated product category
            username = get_current_username()  # Get the username of the current user
            date = get_current_datetime()  # Get the current date and time
            self.log_history(action, product_id, product_name, category, username, date)

            conn.close()

        # create an update button
        update_button = tk.Button(self.add_product_window, text="Update Product", command=update_product, bg='grey')
        update_button.grid(row=8, column=2, padx=5, pady=5, columnspan=2)
        
        def delete_product():
        # Get the selected product from the treeview
            selected_item = products_treeview.focus()
            if not selected_item:
                return

            selected_product = products_treeview.item(selected_item)["values"]
            if not selected_product or len(selected_product) < 5:
                return

            product_id = selected_product[0]

            # Ask for confirmation
            confirmation = messagebox.askyesno(parent=self.add_product_window, title="Confirmation", message="Are you sure you want to delete this product?")
            if not confirmation:
                return

            # Delete the product from the database
            conn = sqlite3.connect('dream_waters_inventory.db')
            c = conn.cursor()

            # Retrieve the current username and datetime
            current_username = get_current_username()
            current_datetime = get_current_datetime()

            # Delete the product
            c.execute("DELETE FROM products WHERE Product_ID = ?", (product_id,))
            conn.commit()

            # Record the deletion in the history
            self.log_history("Delete", product_id, selected_product[2], selected_product[1], current_username, current_datetime)

            conn.close()

            # Update the treeview by removing the deleted product
            products_treeview.delete(products_treeview.focus())

        # create a delete button
        delete_button = tk.Button(self.add_product_window, text="Delete Product", command=delete_product, bg='red')
        delete_button.grid(row=8, column=0, padx=5, pady=5, columnspan=2)


        #create a function to save the product data to the database
        def save_product():
            # get the values from the form
            category = category_entry.get()
            product_name = product_name_entry.get()
            quantity = quantity_entry.get()
            unit_price = unit_price_entry.get()

            # validate the input
            if not category or not product_name or not quantity or not unit_price:
                tk.messagebox.showerror("Error", "All fields are required")
                return

            try:
                quantity = int(quantity)
                unit_price = float(unit_price)
            except ValueError:
                tk.messagebox.showerror("Error", "Quantity and unit price must be numbers")
                return

            if quantity < 0 or unit_price < 0:
                tk.messagebox.showerror("Error", "Quantity and unit price cannot be negative")
                return

            # insert the product into the database
            conn = sqlite3.connect('dream_waters_inventory.db')
            c = conn.cursor()

            # Retrieve the current username and datetime
            current_username = get_current_username()
            current_datetime = get_current_datetime()

            # Insert the product
            c.execute("INSERT INTO products (category, product_name, quantity, unit_price, date_added) VALUES (?, ?, ?, ?, ?)", (category, product_name, quantity, unit_price, date.today()))
            conn.commit()

            # Record the addition in the history
            self.log_history("Add", c.lastrowid, product_name, category, current_username, current_datetime)

            conn.close()

            # close the window
            self.add_product_window.destroy()

            # show a success message
            tk.messagebox.showinfo("Success", "Product added successfully")
                    
          
        def clear_fields():
            category_entry.delete(0, tk.END)
            product_name_entry.delete(0, tk.END)
            quantity_entry.delete(0, tk.END)
            unit_price_entry.delete(0, tk.END)
        def cancel():
            self.add_product_window.destroy()

        # create a button to cancel adding a product
        cancel_button = tk.Button(self.add_product_window, text="Cancel", command=cancel, bg="sky blue", fg="black", padx=10, pady=5)
        cancel_button.grid(row=7, column=1)
        
        # create a button to clear the text fields
        clear_button = tk.Button(self.add_product_window, text="Clear", command=clear_fields, bg='sky blue', fg='black', padx=10, pady=5)
        clear_button.grid(row=7, column=0)  

        # create a button to save the product
        tk.Button(self.add_product_window, text="Save", bg='green', fg='white', command=save_product).grid(row=7, column=2, padx=5, pady=5)
        
        #History button
        #history_button = tk.Button(self.add_product_window, text="View History", command=self.view_history, bg="sky blue", fg="black", padx=10, pady=5)
        #history_button.grid(row=0, column=7)
        
        
    def log_history(self, action, product_id, product_name, category, username, date):
            # connect to the database
            conn = sqlite3.connect("dream_waters_inventory.db")
            cursor = conn.cursor()

            # insert the history entry into the database
            cursor.execute("INSERT INTO history (action_type, product_id, product_name, category, user, action_date) "
                        "VALUES (?, ?, ?, ?, ?, ?)",
                        (action, product_id, product_name, category, username, date))
            conn.commit()

            # close the database connection
            conn.close()

    def view_history(self):
        # Create a new top-level window for displaying the history
        history_window = tk.Toplevel()
        history_window.title("Action History")

        # Create search labels and entry fields
        search_label1 = ttk.Label(history_window, text="Search by:")
        search_label1.pack(anchor=tk.W, padx=10, pady=5)

        # Create a dropdown menu for selecting the search category
        search_categories = ["User", "Category", "Product Name"]
        search_category_var = tk.StringVar()
        search_category_dropdown = ttk.Combobox(history_window, textvariable=search_category_var, values=search_categories)
        search_category_dropdown.pack(anchor=tk.W, padx=10, pady=5)

        search_entry1 = ttk.Entry(history_window)
        search_entry1.pack(anchor=tk.W, padx=10, pady=5)
        search_label2 = ttk.Label(history_window, text="Search by Date (From - To):")
        search_label2.pack(anchor=tk.W, padx=10, pady=5)
        search_entry2 = ttk.Entry(history_window)
        search_entry2.pack(anchor=tk.W, padx=10, pady=5)

        # Create a treeview to display the history
        history_treeview = ttk.Treeview(history_window)
        history_treeview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create scrollbars for the treeview
        x_scrollbar = ttk.Scrollbar(history_window, orient=tk.HORIZONTAL, command=history_treeview.xview)
        x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        y_scrollbar = ttk.Scrollbar(history_window, orient=tk.VERTICAL, command=history_treeview.yview)
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure the treeview
        history_treeview.configure(xscrollcommand=x_scrollbar.set, yscrollcommand=y_scrollbar.set)
        history_treeview["columns"] = ("Action", "Product_ID", "Product_Name", "Category", "User", "Date")
        history_treeview.heading("#0", text="")
        history_treeview.heading("Action", text="Action")
        history_treeview.heading("Product_ID", text="Product ID")
        history_treeview.heading("Product_Name", text="Product Name")
        history_treeview.heading("Category", text="Category")
        history_treeview.heading("User", text="User")
        history_treeview.heading("Date", text="Date")
        history_treeview.column("#0", width=0, stretch="no")
        history_treeview.column("Action", width=100, anchor=tk.CENTER)
        history_treeview.column("Product_ID", width=100, anchor=tk.CENTER)
        history_treeview.column("Product_Name", width=150, anchor=tk.CENTER)
        history_treeview.column("Category", width=100, anchor=tk.CENTER)
        history_treeview.column("User", width=100, anchor=tk.CENTER)
        history_treeview.column("Date", width=100, anchor=tk.CENTER)

        # Populate the treeview with the history data
        conn = sqlite3.connect('dream_waters_inventory.db')
        c = conn.cursor()

        # Get search parameters
        def populate_treeview():
            search_text1 = search_entry1.get().strip()
            search_text2 = search_entry2.get().strip()

            # Print search parameters for debugging
            print("Search Text 1:", search_text1)
            print("Search Text 2:", search_text2)

            # Construct the query based on the search parameters
            if search_text1:
                query = "SELECT action_type, h.product_id, p.product_name, p.category, u.username, h.action_date " \
                        "FROM history h " \
                        "JOIN products p ON h.product_id = p.product_id " \
                        "JOIN accounts u ON h.user = u.username " \
                        "WHERE u.username LIKE ? " \
                        "OR p.category LIKE ? " \
                        "OR p.product_name LIKE ?"
                search_param = f"%{search_text1}%"
                c.execute(query, (search_param, search_param, search_param))
            elif search_text2:
                query = "SELECT action_type, h.product_id, p.product_name, p.category, u.username, h.action_date " \
                        "FROM history h " \
                        "JOIN products p ON h.product_id = p.product_id " \
                        "JOIN accounts u ON h.user = u.username " \
                        "WHERE h.action_date BETWEEN ? AND ?"
                from_date, to_date = search_text2.split("-")
                c.execute(query, (from_date.strip(), to_date.strip()))
            else:
                query = "SELECT action_type, h.product_id, p.product_name, p.category, u.username, h.action_date " \
                        "FROM history h " \
                        "JOIN products p ON h.product_id = p.product_id " \
                        "JOIN accounts u ON h.user = u.username"
                c.execute(query)

            history = c.fetchall()

            # Print the retrieved history for debugging
            print("Retrieved History:")
            for entry in history:
                print(entry)

            for entry in history:
                history_treeview.insert("", tk.END, values=entry)

