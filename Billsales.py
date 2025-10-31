import tkinter as tk
import sqlite3
import datetime
import tkinter.messagebox as messagebox


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
        search_button = tk.Button(stock_frame, text='Search', command=lambda: self.search_stock(search_var.get(), self.stock_treeview), bg='sky blue')
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
        self.product_name_entry = tk.Entry(self.cart_frame, textvariable=self.product_name_var, state='readonly')
        self.unit_price_var = tk.StringVar()
        self.unit_price_entry = tk.Entry(self.cart_frame, textvariable=self.unit_price_var, state='readonly')
        self.quantity_var = tk.StringVar()
        self.quantity_entry = tk.Entry(self.cart_frame, textvariable=self.quantity_var)

        # position the entry fields using place
        self.product_name_entry.place(x=120, y=240)
        self.unit_price_entry.place(x=120, y=270)
        self.quantity_entry.place(x=120, y=300)

        # create buttons to add/update cart and clear cart
        add_to_cart_button = tk.Button(self.cart_frame,text='Add/Update Cart',command=lambda: self.add_to_cart(self.product_name_var.get(),
        float(self.unit_price_var.get()),
        int(self.quantity_var.get()),
        float(self.unit_price_var.get()) * int(self.quantity_var.get())
    ),
    bg='green',
    fg='white'
)

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

        bill_amount_var = tk.StringVar()
        bill_amount_entry = tk.Entry(billing_frame, textvariable=bill_amount_var, state='readonly')
        bill_amount_entry.place(x=120, y=300)

        discount_var = tk.StringVar()
        discount_entry = tk.Entry(billing_frame, textvariable=discount_var)
        discount_entry.place(x=120, y=330)

        net_pay_var = tk.StringVar()
        net_pay_entry = tk.Entry(billing_frame, textvariable=net_pay_var, state='readonly')
        net_pay_entry.place(x=120, y=360)

        # create buttons to print bill, clear billing area, and generate bill
        print_bill_button = tk.Button(billing_frame, text='Print Bill', command=lambda: self.print_bill(), bg='blue', fg='white')
        print_bill_button.place(x=10, y=390)

        clear_billing_button = tk.Button(billing_frame, text='Clear', command=lambda: self.clear_billing(), bg='orange')
        clear_billing_button.place(x=100, y=390)

        generate_bill_button = tk.Button(billing_frame, text='Generate Bill', command=lambda: self.generate_bill(bill_amount_var.get(), discount_var.get(), net_pay_var), bg='purple', fg='white')
        generate_bill_button.place(x=160, y=390)

        self.sale_window.mainloop()

    def search_stock(self, search_term, treeview):
        treeview.delete(*treeview.get_children())
        conn = sqlite3.connect('dream_waters_inventory.db')
        c = conn.cursor()
        query = 'SELECT product_name, quantity FROM products WHERE product_name LIKE ?'
        c.execute(query, ('%' + search_term + '%',))
        for row in c.fetchall():
            treeview.insert('', tk.END, text=row[0], values=(row[1]))
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

    def add_to_cart(self, product_name, unit_price, quantity, total_price, cart_treeview):
        total_price = unit_price * quantity
        self.cart_treeview.insert('', tk.END, text=product_name, values=(product_name, unit_price, quantity, total_price))

    def clear_cart(self, cart_treeview):
        self.cart_treeview.delete(*cart_treeview.get_children())


    def add_to_cart(self, product_name, unit_price, quantity, total_price):
        selection = self.stock_treeview.selection()
        if not selection:
            messagebox.showwarning('Warning', 'Please select a product from the stock.')
            return

        stock_quantity = float(self.stock_treeview.item(selection, 'values')[1])
        if quantity <= stock_quantity:
            self.cart_item_id = self.cart_treeview.insert("", "end", values=(product_name, unit_price, quantity, total_price))
            self.stock_treeview.item(selection, values=(product_name, stock_quantity - quantity))
        else:
            messagebox.showwarning('Warning', 'Insufficient quantity in stock.')




    def print_bill(self, cart_treeview):
        # Get the current date and time
        current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Get the selected items from the treeview
        selected_items = cart_treeview.get_children()

        if not selected_items:
            messagebox.showwarning('Warning', 'The cart is empty. Please add items to generate a bill.')
            return

        # Create a bill string
        bill = f"Bill generated on: {current_datetime}\n\n"
        bill += "Product Name\tUnit Price\tQuantity\tTotal Price\n"
        bill += "--------------------------------------------------\n"

        for item in selected_items:
            product_name = cart_treeview.item(item, 'text')
            unit_price = cart_treeview.item(item, 'values')[0]
            quantity = cart_treeview.item(item, 'values')[1]
            total_price = cart_treeview.item(item, 'values')[2]
            bill += f"{product_name}\t{unit_price}\t\t{quantity}\t\t{total_price}\n"

        bill += "--------------------------------------------------\n"

        # Add the total bill amount
        bill += f"Total Bill Amount: {self.bill_amount_var.get()}\n"

        # Show the bill in a message box
        messagebox.showinfo('Bill', bill)
        pass

    def clear_billing(self, cart_treeview):
        # Clear the treeview
        cart_treeview.delete(*cart_treeview.get_children())

        # Reset the bill amount variable
        self.bill_amount_var.set(0.0)
        pass

    def generate_bill(self, bill_amount, discount, net_pay_var):
        try:
            bill_amount = float(bill_amount)
            discount = float(discount)
            net_pay = bill_amount - (bill_amount * discount / 100)
            net_pay_var.set(net_pay)
        except ValueError:
            messagebox.showwarning('Warning', 'Invalid bill amount or discount.')

        pass


#SaleManager()
