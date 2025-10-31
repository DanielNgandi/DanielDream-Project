import tempfile
import tkinter as tk
import sqlite3
import datetime
import tkinter.messagebox as messagebox
from datetime import datetime
import webbrowser

class SaleManager:
    def __init__(self):
        self.sale_window = tk.Toplevel()
        self.sale_window.title('Billing Area')

        # calculate screen dimensions
        screen_width = self.sale_window.winfo_screenwidth()
        screen_height = self.sale_window.winfo_screenheight()

        # calculate window dimensions and position
        window_width = 1020
        window_height = 450
        x = screen_width - window_width - 50
        y = (screen_height - window_height) // 2

        # set the window dimensions and position
        self.sale_window.geometry("{}x{}+{}+{}".format(window_width, window_height, x, y))
        self.sale_window.configure(bg='sky blue')

        # create the stock display frame
        stock_frame = tk.Frame(self.sale_window, relief=tk.RIDGE, bd=1, bg='sky blue')
        stock_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        # configure grid weights
        self.sale_window.grid_rowconfigure(1, weight=1)

        # create a label for the stock display
        stock_label = tk.Label(stock_frame, text='Stock', font=('Arial', 16, 'bold'), bg='sky blue')
        stock_label.grid(row=0, column=0, padx=10, pady=10)

        # create a search label
        search_label = tk.Label(stock_frame, text='Search:', bg='sky blue')
        search_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")

        # create an entry field for search
        search_var = tk.StringVar()
        search_entry = tk.Entry(stock_frame, textvariable=search_var)
        search_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # create a search button
        search_button = tk.Button(stock_frame, text='Search', command=lambda: self.search_stock(search_var.get()), bg='sky blue')
        search_button.grid(row=1, column=2, padx=10, pady=5, sticky="w")

        # create a treeview to display stock details
        self.stock_treeview = tk.ttk.Treeview(stock_frame, columns=('Unit Price', 'Quantity'))
        self.stock_treeview.heading('#0', text='Product Name')
        self.stock_treeview.heading('Unit Price', text='Price')
        self.stock_treeview.heading('Quantity', text='Quantity')
        self.stock_treeview.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        # configure column widths
        self.stock_treeview.column('#0', width=100)
        self.stock_treeview.column('Unit Price', width=50)
        self.stock_treeview.column('Quantity', width=80)
        
        # bind the select_stock function to the treeview selection event
        self.stock_treeview.bind('<<TreeviewSelect>>', self.select_stock)

        # create vertical scrollbar
        scrollbar = tk.Scrollbar(stock_frame, orient='vertical', command=self.stock_treeview.yview)
        scrollbar.grid(row=2, column=3, sticky='ns')

        # configure treeview to use scrollbar
        self.stock_treeview.configure(yscrollcommand=scrollbar.set)

        # configure grid weights
        stock_frame.grid_rowconfigure(2, weight=1)
        stock_frame.grid_columnconfigure(0, weight=1)


        # populate the stock treeview
        conn = sqlite3.connect('dream_waters_inventory.db')
        c = conn.cursor()
        for row in c.execute('SELECT product_name, unit_price, quantity FROM products'):
            self.stock_treeview.insert('', tk.END, text=row[0], values=(row[1], row[2]))
        conn.close()

        # create the customer details frame
        details_frame = tk.Frame(self.sale_window, relief=tk.RIDGE, bd=1, bg='sky blue')
        details_frame.place(x=325, y=10, width=330, height=70)

        # create a label for the customer details
        details_label = tk.Label(details_frame, text='Customer Details', font=('Arial', 16, 'bold'), bg='sky blue')
        details_label.pack(padx=0, pady=0)

        # create a label for customer name and telephone
        customer_name_label = tk.Label(details_frame, text='Name:', bg='sky blue')
        customer_name_label.place(x=5, y=35)
        customer_telephone_label = tk.Label(details_frame, text='Tel:', bg='sky blue')
        customer_telephone_label.place(x=180, y=35)

        # create an entry field for customer name and telephone
        customer_name_var = tk.StringVar()
        customer_name_entry = tk.Entry(details_frame, textvariable=customer_name_var)
        customer_name_entry.place(x=50, y=35, width=120)
        customer_telephone_var = tk.StringVar()
        customer_telephone_entry = tk.Entry(details_frame, textvariable=customer_telephone_var)
        customer_telephone_entry.place(x=210, y=35, width=110)

        # create the cart frame
        self.cart_frame = tk.Frame(self.sale_window, relief=tk.RIDGE, bd=1, bg='sky blue')
        self.cart_frame.place(x=325, y=80, width=340, height=365)

        # create a treeview to display cart details
        self.cart_treeview = tk.ttk.Treeview(self.cart_frame, columns=( 'Unit Price', 'Quantity', 'Total Price'))
        self.cart_treeview.heading('#0', text='Product Name')
        self.cart_treeview.heading('Unit Price', text='Unit Price')
        self.cart_treeview.heading('Quantity', text='Quantity')
        self.cart_treeview.heading('Total Price', text='Total Price')

        # configure column widths
        self.cart_treeview.column('#0', width=100)
        self.cart_treeview.column('Unit Price', width=80)
        self.cart_treeview.column('Quantity', width=60)
        self.cart_treeview.column('Total Price', width=80)

        # calculate the height of the treeview based on label positions
        treeview_height = 240 - self.cart_treeview.winfo_y() - 10
        self.cart_treeview.place(x=5, y=5, width=320, height=treeview_height)

        # create labels for product name, unit price, and quantity
        product_name_label = tk.Label(self.cart_frame, text='Product Name:', bg='sky blue')
        unit_price_label = tk.Label(self.cart_frame, text='Unit Price:', bg='sky blue')
        quantity_label = tk.Label(self.cart_frame, text='Quantity:', bg='sky blue')
        #total_price_label = tk.Label(cart_frame, text='Total Price')

        # position the labels using place
        product_name_label.place(x=10, y=240)
        unit_price_label.place(x=10, y=270)
        quantity_label.place(x=10, y=300)

        # create entry fields for product name, unit price, and quantity
        self.product_name_var = tk.StringVar()
        self.product_name_entry = tk.Entry(self.cart_frame, textvariable=self.product_name_var)
        self.unit_price_var = tk.StringVar()
        self.unit_price_entry = tk.Entry(self.cart_frame, textvariable=self.unit_price_var)
        self.quantity_var = tk.StringVar()
        self.quantity_entry = tk.Entry(self.cart_frame, textvariable=self.quantity_var)

        # position the entry fields using place
        self.product_name_entry.place(x=120, y=240)
        self.unit_price_entry.place(x=120, y=270)
        self.quantity_entry.place(x=120, y=300)

        # create buttons to add/update cart and clear cart
        add_to_cart_button = tk.Button(self.cart_frame, text='Add to Cart', command=self.add_to_cart)

        clear_cart_button = tk.Button(self.cart_frame, text='Clear Cart', command=lambda: self.clear_cart(self.cart_treeview), bg='red', fg='white')

        # position the buttons using place
        add_to_cart_button.place(x=120, y=330)
        clear_cart_button.place(x=240, y=330)

        # create the billing frame
        billing_frame = tk.Frame(self.sale_window, relief=tk.RIDGE, bd=1, bg='sky blue')
        billing_frame.place(x=680, y=10, width=330, height=430)

        # create a label for the billing area
        billing_label = tk.Label(billing_frame, text='Billing Area', font=('Arial', 16, 'bold'), bg='sky blue')
        billing_label.pack(padx=10, pady=0)

        # create a text widget for the bill
        bill_text = tk.Text(billing_frame, height=15, width=39)
        bill_text.place(x=5, y=30)

        # create labels and entry fields for bill amount, discount, and net pay
        bill_amount_label = tk.Label(billing_frame, text='Bill Amount:', bg='sky blue')
        bill_amount_label.place(x=10, y=300)

        discount_label = tk.Label(billing_frame, text='Discount:', bg='sky blue')
        discount_label.place(x=10, y=330)

        net_pay_label = tk.Label(billing_frame, text='Net Pay:', bg='sky blue')
        net_pay_label.place(x=10, y=360)

        self.bill_amount_var = tk.StringVar()
        self.bill_amount_entry = tk.Entry(billing_frame, textvariable=self.bill_amount_var, state='readonly')
        self.bill_amount_entry.place(x=120, y=300)

        self.discount_var = tk.StringVar()
        self.discount_entry = tk.Entry(billing_frame, textvariable=self.discount_var)
        self.discount_entry.place(x=120, y=330)

        self.net_pay_var = tk.StringVar()
        self.net_pay_entry = tk.Entry(billing_frame, textvariable=self.net_pay_var, state='readonly')
        self.net_pay_entry.place(x=120, y=360)

        # create buttons to print bill, clear billing area, and generate bill
        #print_bill_button = tk.Button(billing_frame, text='Print Bill', command=lambda: self.print_bill(bill_text, customer_name_var.get(), customer_telephone_var.get(), discount_var.get(), net_pay_var.get()), bg='blue', fg='white')
        #print_bill_button.place(x=10, y=390)
        print_bill_button = tk.Button(billing_frame, text="Print Bill", command=lambda: self.print_bill(bill_text), bg='blue', fg='white')
        print_bill_button.place(x=10, y=390)

        clear_billing_button = tk.Button(billing_frame, text='Clear', command=lambda: self.clear_billing(bill_text), bg='orange')
        clear_billing_button.place(x=100, y=390)

        generate_bill_button = tk.Button(billing_frame, text='Generate Bill', command=lambda: self.generate_bill(self.bill_amount_var.get(), self.discount_var.get(), self.net_pay_var, bill_text, customer_name_var.get(), customer_telephone_var.get(), self.product_name_var.get(), self.quantity_var.get()), bg='purple', fg='white')
        generate_bill_button.place(x=160, y=390)

        self.sale_window.mainloop()

    def search_stock(self, search_term):
        self.stock_treeview.delete(*self.stock_treeview.get_children())
        conn = sqlite3.connect('dream_waters_inventory.db')
        c = conn.cursor()
        query = 'SELECT product_name, unit_price, quantity FROM products WHERE product_name LIKE ?'
        c.execute(query, ('%' + search_term + '%',))
        for row in c.fetchall():
            self.stock_treeview.insert('', tk.END, text=row[0], values=(row[1], row[2]))
        conn.close()


        
    def select_stock(self, event):
        selection = self.stock_treeview.focus()
        values = self.stock_treeview.item(selection, 'values')
        self.product_name_entry.config(state='normal')
        self.unit_price_entry.config(state='normal')
        self.quantity_entry.delete(0, tk.END)
        if values:
            self.product_name_entry.delete(0, tk.END)
            self.product_name_entry.insert(tk.END, self.stock_treeview.item(selection, 'text'))
            self.unit_price_entry.delete(0, tk.END)
            self.unit_price_entry.insert(tk.END, values[0])
        else:
            self.product_name_entry.delete(0, tk.END)
            self.unit_price_entry.delete(0, tk.END)
        self.product_name_entry.config(state='readonly')
        self.unit_price_entry.config(state='readonly')

    #def add_to_cart(self, product_name, unit_price, quantity, total_price, cart_treeview):
        #total_price = unit_price * quantity
        #self.cart_treeview.insert('', tk.END, text=product_name, values=(product_name, unit_price, quantity, total_price))

    def clear_cart(self, cart_treeview):
        self.cart_treeview.delete(*cart_treeview.get_children())

    def add_to_cart(self):
        product_name = self.product_name_entry.get()
        unit_price = float(self.unit_price_entry.get())
        quantity = int(self.quantity_entry.get())

        if not product_name or not unit_price or not quantity:
            messagebox.showwarning('Warning', 'Please enter all the required fields.')
            return

        total_price = unit_price * quantity
        self.cart_treeview.insert('', tk.END, text=product_name, values=(unit_price, quantity, total_price))
        self.update_bill_amount()  # Call the function to update the bill amount
        
    def update_bill_amount(self):
        selected_items = self.cart_treeview.get_children()

        total_amount = 0.0
        for item in selected_items:
            total_price = float(self.cart_treeview.item(item, 'values')[2])
            total_amount += total_price

        self.bill_amount_var.set("{:.2f}".format(total_amount))
        
    def update_bill(self, bill_text, customer_name, customer_telephone, discount, net_pay):
        # Get the current date and time
        current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Get the selected items from the treeview
        selected_items = self.cart_treeview.get_children()

        if not selected_items:
            messagebox.showwarning('Warning', 'The cart is empty. Please add items to generate a bill.')
            return

        # Create a bill string
        company_details = "Dream Waters Investments\n"
        company_details += "P.O Box 298-90400, Mwingi\n"
        company_details += "Phone: 0768 142 174\n"
        company_details += "Email: dreamwaters21@gmail.com\n\n"

        # Center the company details
        centered_company_details = company_details.center(50)  # Adjust the width (50) as needed

        # Concatenate the centered company details with the rest of the bill string
        bill = centered_company_details
        bill += f"{'Customer Name:':<15}{customer_name}\n"
        bill += f"{'Telephone:':<15}{customer_telephone}\n"
        bill += f"{'Bill generated on:':<15}{current_datetime}\n\n"
        bill += "Item\tPrice\tQty\tT-Price\n"
        bill += "--------------------------------------------------\n"

        for item in selected_items:
            product_name = self.cart_treeview.item(item, 'text')
            unit_price = self.cart_treeview.item(item, 'values')[0]
            quantity = self.cart_treeview.item(item, 'values')[1]
            total_price = self.cart_treeview.item(item, 'values')[2]
            bill += f"{product_name}\t{unit_price}\t{quantity}\t{total_price}\n"

        bill += "--------------------------------------------------\n"

        # Add the total bill amount, discount, and net pay
        bill += f"Total Bill Amount: {self.bill_amount_var.get()}\n"
        bill += f"Discount: {discount}%\n"
        bill += f"Net Pay: {net_pay}\n"

        # Insert the bill into the text widget
        bill_text.delete("1.0", tk.END)
        bill_text.insert(tk.END, bill)
    
    def clear_billing(self, bill_text):
        # Clear the text widget
        bill_text.delete("1.0", tk.END)
            
            
    def generate_bill(self, bill_amount, discount, net_pay_var, bill_text, customer_name, customer_telephone, product_name_var, quantity):
        try:
            bill_amount = float(bill_amount)
            discount = float(discount)
            net_pay = bill_amount - (bill_amount * discount / 100)
            net_pay_var.set(net_pay)

            # Call the update_bill function to display the bill in the text widget
            self.update_bill(bill_text, customer_name, customer_telephone, discount, net_pay)

            # Remove the details from the cart treeview
            self.clear_cart(self.cart_treeview)

            # Deduct the entered quantities from the product database
            conn = sqlite3.connect('dream_waters_inventory.db')
            c = conn.cursor()

            # get the product ID from the product name
            c.execute('SELECT product_id FROM products WHERE product_name=?', (product_name_var,))
            product_id = c.fetchone()[0]

            # check if there is enough quantity of the product
            c.execute('SELECT quantity FROM products WHERE product_id=?', (product_id,))
            available_quantity = c.fetchone()[0]
            quantity= int(quantity)
            if quantity > available_quantity:
                messagebox.showerror('Error', 'Not enough quantity available')
                return

            # calculate the total price and insert the sale into the database
            c.execute('SELECT unit_price FROM products WHERE product_id=?', (product_id,))
            unit_price = c.fetchone()[0]
            total_price = net_pay
            date_sold = datetime.now()
            formatted_date_sold = date_sold.strftime("%Y-%m-%d %H:%M")
            print(formatted_date_sold)
            c.execute('INSERT INTO sales (product_id, quantity, total_price, date_sold) VALUES (?, ?, ?, ?)',
                    (product_id, quantity, total_price, formatted_date_sold))
            conn.commit()
            
            # update the product quantity
            new_quantity = available_quantity - quantity
            c.execute('UPDATE products SET quantity=? WHERE product_id=?', (new_quantity, product_id))
            conn.commit()
            
            # Clear the stock treeview
            self.stock_treeview.delete(*self.stock_treeview.get_children())

            # populate the stock treeview with updated data
            for row in c.execute('SELECT product_name, unit_price, quantity FROM products'):
                self.stock_treeview.insert('', tk.END, text=row[0], values=(row[1], row[2]))

            conn.close()

            # Clear the labels
            self.bill_amount_var.set("")
            self.discount_var.set("")
            self.net_pay_var.set("")

            # Clear the label entries
            self.product_name_entry.config(state='normal')
            self.product_name_entry.delete(0, tk.END)
            self.product_name_entry.config(state='readonly')

            self.unit_price_entry.config(state='normal')
            self.unit_price_entry.delete(0, tk.END)
            self.unit_price_entry.config(state='readonly')
            self.quantity_entry.delete(0, tk.END)

            # Show a success message
            messagebox.showinfo("Bill Generated", "Bill generated successfully.", parent=self.sale_window)

        except ValueError:
            messagebox.showwarning('Warning', 'Invalid bill amount or discount.', parent=self.sale_window)


    
    def print_bill(self, bill_text):
        # Get the bill details from the text widget
        bill_details = bill_text.get("1.0", tk.END)

        # Create a temporary HTML file
        temp_html = tempfile.NamedTemporaryFile(suffix=".html", delete=False)
        temp_html_path = temp_html.name
        temp_html.close()

        # Define the HTML template
        html_template = """
        <!DOCTYPE html>
        <html>
            <head>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        margin: 20px;
                    }}
                    h1 {{
                        margin-bottom: 10px;
                    }}
                    p {{
                        margin: 5px 0;
                    }}
                </style>
            </head>
            <body>
                <h1>Receipts Bill</h1>
                {}
            </body>
        </html>
        """

        # Format the bill details in HTML
        formatted_bill = "<p>{}</p>".format(bill_details.replace("\n", "</p><p>"))

        # Write the HTML content to the file
        with open(temp_html_path, "w") as file:
            file.write(html_template.format(formatted_bill))

        # Open the HTML file in the default web browser
        webbrowser.open(temp_html_path)

        # Clear the bill details from the text widget
        bill_text.delete("1.0", tk.END)



