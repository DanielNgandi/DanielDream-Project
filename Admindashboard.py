import tkinter as tk
import sqlite3
from datetime import date
from datetime import date as dt
from tkinter import ttk
import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from scipy import signal
from Salesreport import SalesReportWindow
from ManageAccounts import ManageAccountsWindow
from Stockreport import StockReportWindow
from AdminAddstock import AdminAddStockWindow
from AddSale import SaleManager
from PIL import Image, ImageTk


class AdminDashboardUI:
    def __init__(self, master):
        self.master = master
        master.title("Dream Inventory System|Developed by daniel mwangangi")

        # set background color
        self.master.configure(bg="#e6f2ff")
        
         # create a top-level frame
        self.top_frame = tk.Frame(master, bg="#003366", pady=0)
        self.top_frame.pack(side=tk.TOP, fill=tk.X)
     
        # Create a top-level frame for the title and icon
        self.top_frame = tk.Frame(master, bg="#4da6ff", pady=0)
        self.top_frame.pack(side=tk.TOP, fill=tk.X)

        # Create a label for the title and icon
        self.icon_image = tk.PhotoImage(file=r"C:\Users\DanielDream Project\Images\Dreamlogo1.png")
        self.icon_image = self.icon_image.subsample(8, 8)
        self.title_label = tk.Label(self.top_frame, text="Dream Waters Investments", font=("Arial", 21), image=self.icon_image, compound="left", bg="#4da6ff", fg="white", padx=0, pady=0)
        self.title_label.pack(side=tk.LEFT)

        # Create a frame for the current date, time, and user name
        self.user_frame = tk.Frame(master, bg="#f2f2f2", padx=10, pady=5)
        self.user_frame.pack(side=tk.TOP, fill=tk.X)

        # Get current date and time
        current_date = dt.today().strftime("%B %d, %Y")
        current_time = datetime.datetime.now().strftime("%H:%M:%S")

        #Initialize the username
        self.user_name = "" 
        
        # Create labels for current date, time, and user name
        self.date_label = tk.Label(self.user_frame, text="Date: " + current_date, font=("Arial", 12), bg="#f2f2f2")
        self.date_label.pack(side=tk.LEFT, padx=10)
        
        self.time_label = tk.Label(self.user_frame, text="Time: " + current_time, font=("Arial", 12), bg="#f2f2f2")
        self.time_label.pack(side=tk.LEFT, padx=10)
        
        self.user_label = tk.Label(self.user_frame, text="Hi " +  self.user_name, font=("Arial", 12), bg="#f2f2f2")
        self.user_label.pack(side=tk.RIGHT, padx=10)
        
        # Update the time label every second
        self.update_time()

         # create a frame for the buttons
        self.button_frame = tk.Frame(master, bg="#f2f2f2", padx=10, pady=10)
        self.button_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        # Create a canvas for the animation
        self.canvas = tk.Canvas(self.button_frame, width=150, height=100, bg="#f2f2f2")
        self.canvas.pack()

        # Create a list of image paths
        self.image_paths = [r"C:\Users\DanielDream Project\Images\Dream1.png", r"C:\Users\DanielDream Project\Images\Dreamlogo.png", r"C:\Users\DanielDream Project\Images\Dreamlogo1.png"]

        # Create a list to store the image objects
        self.images = []
        self.resized_images =[]

        # Load the images and store them in the list
        for path in self.image_paths:
            image = Image.open(path)
            resized_image = image.resize((150, 100), Image.ANTIALIAS)
            tk_image = ImageTk.PhotoImage(resized_image)
            self.images.append(tk_image)
            self.resized_images.append(resized_image)

        # Set the index for the current image
        self.current_image_index = 0

        # Display the first image on the canvas
        self.display_current_image()


        # Create a button to add a new product
        self.add_product_button = tk.Button(self.button_frame, text="Manage Stock", command=self.add_product, bg="#4da6ff", fg="white", padx=10, pady=10, width=15)
        self.add_product_button.pack(pady=5)

        # create a button to view products
        self.view_products_button = tk.Button(self.button_frame, text="View Products", command=self.view_products, bg="#4da6ff", fg="white", padx=10, pady=10, width=15)
        self.view_products_button.pack(pady=5)

        # create a button to add a new sale
        self.add_sale_button = tk.Button(self.button_frame, text="Add New Sale", command=self.add_sale, bg="#4da6ff", fg="white", padx=10, pady=10, width=15)
        self.add_sale_button.pack(pady=5)

        # create a button to view sales
        self.view_sales_button = tk.Button(self.button_frame, text="View Sales", command=self.view_sales, bg="#4da6ff", fg="white", padx=10, pady=10, width=15)
        self.view_sales_button.pack(pady=5)

        # create a button to view stock report
        self.stock_report_button = tk.Button(self.button_frame, text="View Stock Report", command=self.stock_report, bg="#4da6ff", fg="white", padx=10, pady=10, width=15)
        self.stock_report_button.pack(pady=5)

        # create a button to view sales report
        self.sales_report_button = tk.Button(self.button_frame, text="View Sales Report", command=self.sales_report, bg="#4da6ff", fg="white", padx=10, pady=10, width=15)
        self.sales_report_button.pack(pady=5)

        # create a button to view user accounts
        self.manage_accounts_button = tk.Button(self.button_frame, text="Manage Accounts", command=self.manage_accounts, bg="#4da6ff", fg="white", padx=10, pady=10, width=15)
        self.manage_accounts_button.pack(pady=5)
        
        # create a button to log out
        self.logout_button = tk.Button(self.master, text="Log Out", command=self.logout, bg="#4da6ff", fg="white", padx=10, pady=10, width=15)
        self.logout_button.pack(side=tk.TOP, anchor=tk.NE)
        
        # Create the right frame for graphs
        self.right_frame = tk.Frame(master, bg="#f2f2f2", padx=10, pady=10)
        self.right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create a figure for sales line chart
        self.sales_figure = plt.Figure(figsize=(3, 2), dpi=100)
        self.sales_ax = self.sales_figure.add_subplot(111)
        self.sales_canvas = FigureCanvasTkAgg(self.sales_figure, self.right_frame)
        self.sales_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Define a method to update the sales graph
        def update_sales_graph():
            # Fetch sales data from the database
            conn = sqlite3.connect('dream_waters_inventory.db')
            c = conn.cursor()
            sales_data = []
            for row in c.execute('SELECT strftime("%Y-%m-%d", date_sold), SUM(total_price) FROM sales GROUP BY strftime("%Y-%m-%d", date_sold) ORDER BY date_sold DESC LIMIT 6'):
                sales_data.append(row)
            conn.close()

            # Prepare the data for the line chart
            dates = [datetime.datetime.strptime(data[0], "%Y-%m-%d") for data in sales_data]
            total_sales = [data[1] for data in sales_data]

            # Generate the list of all dates within the date range
            start_date = min(dates)
            end_date = max(dates)
            all_dates = [start_date + datetime.timedelta(days=i) for i in range((end_date - start_date).days + 1)]

            # Create a dictionary to hold the sales data for each date
            sales_dict = dict(sales_data)

            # Fill in missing dates with 0 sales
            for date in all_dates:
                date_str = date.strftime("%Y-%m-%d")
                if date_str not in sales_dict:
                    sales_dict[date_str] = 0

            # Sort the sales data by date
            sorted_sales = sorted(sales_dict.items(), key=lambda x: x[0])

            # Extract the sorted dates and total sales
            dates = [datetime.datetime.strptime(date, "%Y-%m-%d") for date, _ in sorted_sales]
            total_sales = [sales for _, sales in sorted_sales]

            # Clear the previous line chart
            self.sales_ax.clear()

            # Plot the updated line chart
            self.sales_ax.plot(dates, total_sales, marker='o', markersize=5, linestyle='-', color='blue')
            self.sales_ax.set_xlabel('Date')
            self.sales_ax.set_ylabel('Total Sales')
            self.sales_ax.set_title('Sales Chart')

            # Find the peaks in the data
            peak_indices = signal.argrelextrema(np.array(total_sales), np.greater)[0]
            peak_dates = [dates[i] for i in peak_indices]
            peak_sales = [total_sales[i] for i in peak_indices]

            # Add markers at the peaks
            self.sales_ax.plot(peak_dates, peak_sales, marker='o', markersize=8, linestyle='none', color='red')

            # Set the X-axis tick labels to display only the dates
            date_labels = [date.strftime("%m-%d") for date in dates]
            self.sales_ax.set_xticks(dates)
            self.sales_ax.set_xticklabels(date_labels)

            # Rotate the X-axis tick labels for better readability
            plt.xticks(rotation=45)

            # Update the canvas to reflect the changes
            self.sales_canvas.draw()

            # Schedule the next update after 5 seconds
            self.sales_canvas.get_tk_widget().after(5000, update_sales_graph)

        # Start the initial update
        update_sales_graph()

        # Create a frame for the bar chart and pie chart
        graph_frame = tk.Frame(self.right_frame)
        graph_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Create a figure for the stock bar chart
        self.stock_figure = plt.Figure(figsize=(4, 3), dpi=100)
        self.stock_ax = self.stock_figure.add_subplot(111)
        self.stock_canvas = FigureCanvasTkAgg(self.stock_figure, graph_frame)
        self.stock_canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Define a method to update the stock graph
        def update_stock_graph():
            # Fetch stock data from the database
            conn = sqlite3.connect('dream_waters_inventory.db')
            c = conn.cursor()
            stock_data = []
            for row in c.execute('SELECT product_name, quantity FROM products'):
                stock_data.append(row)
            conn.close()

            # Prepare the data for the bar chart
            products = [data[0] for data in stock_data]
            quantities = [data[1] for data in stock_data]

            # Clear the previous bar chart
            self.stock_ax.clear()

            # Plot the updated bar chart
            self.stock_ax.bar(products, quantities)
            self.stock_ax.set_xlabel('Product')
            self.stock_ax.set_ylabel('Quantity')
            self.stock_ax.set_title('Stock Chart')

            # Update the canvas to reflect the changes
            self.stock_canvas.draw()

            # Schedule the next update after 5 seconds
            self.stock_canvas.get_tk_widget().after(5000, update_stock_graph)

        # Start the initial update
        update_stock_graph()

        # Create a figure for the pie chart
        self.pie_figure = plt.Figure(figsize=(4, 3), dpi=100)
        self.pie_ax = self.pie_figure.add_subplot(111)

        # Create a canvas for the pie chart
        self.pie_canvas = FigureCanvasTkAgg(self.pie_figure, graph_frame)
        self.pie_canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Define a method to update the pie chart
        def update_pie_chart():
            # Fetch sales data from the database for the pie chart
            conn = sqlite3.connect('dream_waters_inventory.db')
            c = conn.cursor()
            c.execute("SELECT products.product_name, SUM(sales.quantity) FROM sales JOIN products ON sales.product_id = products.product_id GROUP BY products.product_name ORDER BY SUM(sales.quantity) DESC LIMIT 5")
            pie_data = c.fetchall()
            conn.close()

            # Extract the item names and quantities for the pie chart
            item_names = [item[0] for item in pie_data]
            quantities = [item[1] for item in pie_data]

            # Clear the previous pie chart
            self.pie_ax.clear()

            # Plot the updated pie chart
            self.pie_ax.pie(quantities, labels=item_names, autopct='%1.1f%%')
            self.pie_ax.set_title('Most Sold Items')

            # Update the canvas to reflect the changes
            self.pie_canvas.draw()

            # Schedule the next update after 5 seconds
            self.pie_canvas.get_tk_widget().after(5000, update_pie_chart)

        # Start the initial update
        update_pie_chart()


        # Render the graphs
        self.sales_canvas.draw()
        self.stock_canvas.draw()
        self.pie_canvas.draw()
 
    def display_current_image(self):
            # Clear the canvas
        self.canvas.delete("all")

        # Get the current image
        current_image = self.images[self.current_image_index]

        # Display the image on the canvas
        self.canvas.create_image(0, 0, anchor=tk.NW, image=current_image)

        # Increment the index for the next image
        self.current_image_index = (self.current_image_index + 1) % len(self.images)

        # Schedule the next image to be displayed after 3 seconds
        self.master.after(3000, self.display_current_image)
        
    def update_time(self):
        current_date = date.today().strftime("%B %d, %Y")
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        self.date_label.config(text="Date: " + current_date)
        self.time_label.config(text="Time: " + current_time)
        self.master.after(1000, self.update_time)
    
    def update_user_name(self, name):
        self.user_name = name  # Update the user name
        self.user_label.config(text="Hi " + self.user_name)    
        
    def add_product(self):
        add_product_window =AdminAddStockWindow()
        pass

    def view_products(self):
        # create a new top-level window for viewing products
        view_products_window = tk.Toplevel(self.master)
        view_products_window.title("View Products")

        # calculate screen dimensions
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        # calculate window dimensions and position
        window_width = 800
        window_height = 400
        x = screen_width - window_width - 50
        y = (screen_height - window_height) // 2

        # set the window dimensions and position
        view_products_window.geometry("{}x{}+{}+{}".format(window_width, window_height, x, y))
        view_products_window.configure(bg='sky blue')

        # create a label for the title
        tk.Label(view_products_window, text="Products", bg='sky blue', font=("Arial", 16), padx=20, pady=10).pack()

        # create a frame for the products treeview and scrollbar
        products_frame = tk.Frame(view_products_window)
        products_frame.pack(fill=tk.BOTH, expand=1, padx=20, pady=10)

        # create a treeview to display the products
        self.product_treeview = ttk.Treeview(products_frame, columns=("ID", "category", "name", "quantity", "price", "date_added"),
                                            show="headings")
        self.product_treeview.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        # add headings to the columns
        self.product_treeview.heading("ID",text="ID")
        self.product_treeview.heading("category", text="Category")
        self.product_treeview.heading("name", text="Name")
        self.product_treeview.heading("quantity", text="Quantity")
        self.product_treeview.heading("price", text="Price")
        self.product_treeview.heading("date_added", text="Date Added")

        # set column widths
        self.product_treeview.column("ID", width=50, anchor=tk.CENTER)
        self.product_treeview.column("category", width=150, anchor=tk.CENTER)
        self.product_treeview.column("name", width=150, anchor=tk.CENTER)
        self.product_treeview.column("quantity", width=100, anchor=tk.CENTER)
        self.product_treeview.column("price", width=100, anchor=tk.CENTER)
        self.product_treeview.column("date_added", width=150, anchor=tk.CENTER)

        # create a scrollbar for the treeview
        scrollbar = tk.Scrollbar(products_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # set the scrollbar to control the treeview
        self.product_treeview.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.product_treeview.yview)

        # fetch all the products
        conn = sqlite3.connect("dream_waters_inventory.db")
        cursor = conn.cursor()
        cursor.execute("SELECT Product_ID, category, product_name, quantity, unit_price, date_added FROM products")
        products = cursor.fetchall()
        conn.close()

        # insert the products into the treeview
        for product in products:
            self.product_treeview.insert("", tk.END, values=(product[0], product[1], product[2], product[3], product[4], product[5]))
   
        pass


    def add_sale(self):
        sale_window  = SaleManager()

        pass

    def view_sales(self):
        # create a new window for viewing sales
        view_sales_window = tk.Toplevel(self.master)
        view_sales_window.title('View Sales')
        
        # create a treeview to display the sales
        sales_tree = ttk.Treeview(view_sales_window)
        sales_tree.pack(fill='both', expand=True)
        
        # define the columns
        sales_tree['columns'] = ('sale_id', 'category', 'product_name', 'quantity', 'total_price', 'date_sold')
        sales_tree.column('#0', width=0, stretch='no')
        sales_tree.column('sale_id', width=50)
        sales_tree.column('category', width=150)
        sales_tree.column('product_name', width=150)
        sales_tree.column('quantity', width=100)
        sales_tree.column('total_price', width=100)
        sales_tree.column('date_sold', width=200)
        
        # add headings
        sales_tree.heading('#0', text='', anchor='w')
        sales_tree.heading('sale_id', text='Sales ID', anchor='w')
        sales_tree.heading('category', text='Category', anchor='w')
        sales_tree.heading('product_name', text='Product Name', anchor='w')
        sales_tree.heading('quantity', text='Quantity', anchor='w')
        sales_tree.heading('total_price', text='Total Price', anchor='w')
        sales_tree.heading('date_sold', text='Date Sold', anchor='w')
        
        # populate the treeview with data from the database
        conn = sqlite3.connect('dream_waters_inventory.db')
        c = conn.cursor()
        sales_data = []
        for row in c.execute('SELECT sales.sale_id, products.category, products.product_name, sales.quantity, sales.total_price, sales.date_sold FROM sales JOIN products ON sales.product_id=products.product_id'):
            sales_data.append(row)
        conn.close()
        for sale in sales_data:
            sales_tree.insert(parent='', index='end', iid=sale[0], text='', values=(sale[0], sale[1], sale[2], sale[3], sale[4], sale[5]))
            
        view_sales_window.mainloop()


        pass

    # code to generate the stock report
    def stock_report(self):
        stock_report_window = StockReportWindow()
        pass

    def sales_report(self):
        sales_report_window = SalesReportWindow()
        sales_report_window.fetch_sales()
        pass

    def manage_accounts(self):
        manage_accounts_window = ManageAccountsWindow()
        
        pass
    
    def logout(self):
        # close the dashboard window
        self.master.destroy()
        pass
#root = tk.Tk()
#root.geometry("1250x630+0+0")
#dashboard = DashboardUI(root)
#root.mainloop()

