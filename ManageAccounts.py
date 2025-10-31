import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

class UpdateUserWindow:
    def __init__(self, user_id, parent):
        self.update_user_window = tk.Toplevel(parent)
        self.update_user_window.title('Update User')
        self.update_user_window.configure(bg='sky blue')
        
        # Store the user_id for updating the database
        self.user_id = user_id

        # Retrieve the user details from the database
        conn = sqlite3.connect('dream_waters_inventory.db')
        c = conn.cursor()
        c.execute("SELECT username, email, role FROM accounts WHERE user_id=?", (user_id,))
        user = c.fetchone()
        conn.close()

        # Create labels and entry fields
        username_label = ttk.Label(self.update_user_window, text="Username:")
        username_label.grid(row=0, column=0, padx=5, pady=5)
        username_label.configure(background='sky blue')

        self.username_entry = ttk.Entry(self.update_user_window, width=30)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        email_label = ttk.Label(self.update_user_window, text="Email:")
        email_label.grid(row=1, column=0, padx=5, pady=5)
        email_label.configure(background='sky blue')

        self.email_entry = ttk.Entry(self.update_user_window, width=30)
        self.email_entry.grid(row=1, column=1, padx=5, pady=5)

        role_label = ttk.Label(self.update_user_window, text="Role:")
        role_label.grid(row=2, column=0, padx=5, pady=5)
        role_label.configure(background='sky blue')

        self.role_entry = ttk.Entry(self.update_user_window, width=30)
        self.role_entry.grid(row=2, column=1, padx=5, pady=5)

        # If user details are found, populate the entry fields with the values
        if user:
            self.username_entry.insert(tk.END, user[0])  # Display the current username
            if user[1]:
                self.email_entry.insert(tk.END, user[1])  # Display the current email
            self.role_entry.insert(tk.END, user[2])  # Display the current role

        # Update button
        update_button = ttk.Button(self.update_user_window, text="Update",command=self.update_user)
        update_button.grid(row=3, column=0, columnspan=2, padx=5, pady=10)
        update_button.configure(bg='sky blue')

        # Store the user_id for updating the database
        self.user_id = user_id


    def update_user(self):
        # Check if the role is being changed to admin
        role = self.role_entry.get()
        is_admin = role.lower() == 'admin'

        if is_admin:
            # Check the current number of admins
            conn = sqlite3.connect('dream_waters_inventory.db')
            c = conn.cursor()
            c.execute("SELECT COUNT(*) FROM accounts WHERE role='admin'")
            admin_count = c.fetchone()[0]
            conn.close()

            if admin_count >= 3:
                messagebox.showwarning("Maximum Admin Limit Reached", "You cannot update user details to be an admin as the maximum limit of 3 admins has been reached.")
                return  # Stop the update process if the limit is reached

        # If the role is not being changed to admin or the admin limit is not reached,
        # continue with the update process
        username = self.username_entry.get()
        email = self.email_entry.get()

        # Update the user in the database
        conn = sqlite3.connect('dream_waters_inventory.db')
        c = conn.cursor()
        c.execute("UPDATE accounts SET username=?, email=?, role=? WHERE user_id=?", (username, email, role, self.user_id))
        conn.commit()
        conn.close()

        # Show a success message box
        messagebox.showinfo("Update User", "User details updated successfully.", parent=self.update_user_window)

        # Close the update window
        self.update_user_window.destroy()


class ManageAccountsWindow:
    def __init__(self):
        self.manage_account_window = tk.Toplevel()
        self.manage_account_window.title('Accounts Management')
        self.manage_account_window.configure(bg='sky blue')
        
        # calculate screen dimensions
        screen_width = self.manage_account_window.winfo_screenwidth()
        screen_height = self.manage_account_window.winfo_screenheight()

        # calculate window dimensions and position
        window_width = 750
        window_height = 450
        x = screen_width - window_width - 50
        y = (screen_height - window_height) // 2

        # set the window dimensions and position
        self.manage_account_window.geometry("{}x{}+{}+{}".format(window_width, window_height, x, y))

        # Create the treeview
        self.users_treeview = ttk.Treeview(self.manage_account_window, selectmode="browse")
        self.users_treeview.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

        # Define the columns
        self.users_treeview["columns"] = ("user_id", "username", "email", "security_question", "role")

        # Format the columns
        self.users_treeview.column("#0", width=0, stretch=tk.NO)  # Hide the default first column
        self.users_treeview.column("user_id", anchor=tk.CENTER, width=80)
        self.users_treeview.column("username", anchor=tk.W, width=120)
        self.users_treeview.column("email", anchor=tk.W, width=200)
        self.users_treeview.column("security_question", anchor=tk.CENTER, width=220)
        self.users_treeview.column("role", anchor=tk.CENTER, width=80)

        # Create the headings
        self.users_treeview.heading("user_id", text="User ID")
        self.users_treeview.heading("username", text="Username")
        self.users_treeview.heading("email", text="Email")
        self.users_treeview.heading("security_question", text="Security Question")
        self.users_treeview.heading("role", text="Role")

        # Populate the treeview
        self.fetch_users()

        # Create a custom style for the buttons
        style = ttk.Style()
        style.configure("LightGreen.TButton", background="light green")
        style.configure("Red.TButton", background="red")

        # Add the buttons
        button_frame = ttk.Frame(self.manage_account_window)
        button_frame.pack(pady=10)

        update_button = ttk.Button(button_frame, text="Update", style="LightGreen.TButton", command=self.open_update_user_window)
        update_button.pack(side=tk.LEFT, padx=5)

        remove_button = ttk.Button(button_frame, text="Remove", style="Red.TButton", command=self.remove_user)
        remove_button.pack(side=tk.LEFT, padx=5)
        
    def fetch_users(self):
        # Clear the existing records
        self.users_treeview.delete(*self.users_treeview.get_children())

        # Fetch the users from the database
        conn = sqlite3.connect('dream_waters_inventory.db')  
        c = conn.cursor()
        c.execute("SELECT user_id, username, email, security_question, role FROM accounts")
        users = c.fetchall()
        conn.close()

        # Populate the treeview with the retrieved records
        for user in users:
            self.users_treeview.insert("", tk.END, values=user)

    def open_update_user_window(self):
        selected_item = self.users_treeview.focus()
        if selected_item:
            user_id = self.users_treeview.item(selected_item)["values"][0]
            UpdateUserWindow(user_id=user_id, parent=self.manage_account_window)
        else:
            messagebox.showwarning("No User Selected", "Please select a user.")


    def remove_user(self):
        selected_item = self.users_treeview.focus()
        if selected_item:
            user_id = self.users_treeview.item(selected_item)["values"][0]
            confirm = messagebox.askyesno("Caution", "Are you sure you want to remove this user?")
            if confirm:
                # Remove the user from the database
                conn = sqlite3.connect('dream_waters_inventory.db')
                c = conn.cursor()
                c.execute("DELETE FROM accounts WHERE user_id=?", (user_id,))
                conn.commit()
                conn.close()

                # Refresh the treeview after removing the user
                self.fetch_users()

                messagebox.showinfo("Remove User", "User removed successfully.")
        else:
            messagebox.showwarning("No User Selected", "Please select a user.")
