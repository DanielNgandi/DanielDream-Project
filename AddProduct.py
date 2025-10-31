import tkinter as tk

import sqlite3
from datetime import datetime
from tkinter import messagebox

# connect to the database
conn = sqlite3.connect('dream_waters_inventory.db')
c = conn.cursor()

# create the main window
root = tk.Tk()
root.title("Dream Waters Inventory System")
root.geometry("400x400")

# function to add a sale to the database
def add_sale():
    # get the values from the entry widgets
    product_id = product_id_entry.get()
    quantity = quantity_entry.get()

    # check if the product id and quantity are valid
    if not product_id.isdigit():
        messagebox.showerror("Error", "Product ID must be a number.")
        return
    if not quantity.isdigit():
        messagebox.showerror("Error", "Quantity must be a number.")
        return

    # get the unit price of the product
    c.execute("SELECT unit_price FROM products WHERE product_id=?", (product_id,))
    result = c.fetchone()
    if result is None:
        messagebox.showerror("Error", "Product ID not found.")
        return
    unit_price = result[0]

    # calculate the total price of the sale
    total_price = float(quantity) * unit_price

    # insert the sale into the sales table
    date_sold = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.execute("INSERT INTO sales (product_id, quantity, total_price, date_sold) VALUES (?, ?, ?, ?)", (product_id, quantity, total_price, date_sold))
    conn.commit()

    # show a success message
    messagebox.showinfo("Success", "Sale added successfully.")

    # clear the entry widgets
    product_id_entry.delete(0, tk.END)
    quantity_entry.delete(0, tk.END)

# create the entry widgets
product_id_label = tk.Label(root, text="Product ID:")
product_id_label.pack()
product_id_entry = tk.Entry(root)
product_id_entry.pack()

quantity_label = tk.Label(root, text="Quantity:")
quantity_label.pack()
quantity_entry = tk.Entry(root)
quantity_entry.pack()

# create the add sale button
add_sale_button = tk.Button(root, text="Add Sale", command=add_sale)
add_sale_button.pack()

# start the main event loop
root.mainloop()

# close the database connection
conn.close()
