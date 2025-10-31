import tkinter as tk
import tkinter.messagebox as messagebox
import sqlite3

class RegisterWindow:
    def __init__(self, parent):
        self.parent = parent
        self.parent.title("Register")
        self.parent.configure(bg="#f7f7f7")
        
        # create the form labels and entries
        tk.Label(self.parent, text="Username:").grid(row=0, column=0, sticky="e")
        self.username_entry = tk.Entry(self.parent)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(self.parent, text="Password:").grid(row=1, column=0, sticky="e")
        self.password_entry = tk.Entry(self.parent, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(self.parent, text="Confirm Password:").grid(row=2, column=0, sticky="e")
        self.confirm_password_entry = tk.Entry(self.parent, show="*")
        self.confirm_password_entry.grid(row=2, column=1, padx=5, pady=5)
        
        tk.Label(self.parent, text="Email:").grid(row=3, column=0, sticky="e")
        self.email_entry = tk.Entry(self.parent)
        self.email_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(self.parent, text="Security Question:").grid(row=4, column=0, sticky="e")
        self.security_question_var = tk.StringVar(self.parent)
        self.security_question_var.set("What is your favorite color?") # default value
        self.security_question_dropdown = tk.OptionMenu(self.parent, self.security_question_var, "What is your favorite color?", "What is your pet's name?", "What is your mother's maiden name?")
        self.security_question_dropdown.grid(row=4, column=1, padx=5, pady=5)
        
        tk.Label(self.parent, text="Security Answer:").grid(row=5, column=0, sticky="e")
        self.security_answer_entry = tk.Entry(self.parent)
        self.security_answer_entry.grid(row=5, column=1, padx=5, pady=5)
        
        tk.Label(self.parent, text="Role:").grid(row=6, column=0, sticky="e")
        self.role_var = tk.StringVar(self.parent)
        self.role_var.set("user") # default value
        self.role_dropdown = tk.OptionMenu(self.parent, self.role_var, "user", "admin")
        self.role_dropdown.grid(row=6, column=1, padx=5, pady=5)

        # create the register and cancel buttons
        register_button = tk.Button(self.parent, text="Register", command=self.register_user)
        register_button.grid(row=7, column=0, padx=5, pady=5)
        
        cancel_button = tk.Button(self.parent, text="Cancel", command=self.parent.destroy)
        cancel_button.grid(row=7, column=1, padx=5, pady=5)
        
        # focus on the username entry by default
        self.username_entry.focus()
        
    def register_user(self):

        # get the entered username, passwords, and role
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        email = self.email_entry.get()
        security_question = self.security_question_var.get()
        security_answer = self.security_answer_entry.get()
        role = self.role_var.get()
        
        # check if any of the fields are empty
        if not username or not password or not confirm_password or not security_question or not security_answer:
            messagebox.showerror("Error", "Please fill in all the fields")
            return

        # check if the passwords match
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return
            
        # check if the username is already taken
        conn = sqlite3.connect('dream_waters_inventory.db')
        c = conn.cursor()
        c.execute("SELECT * FROM accounts WHERE username=?", (username,))
        result = c.fetchone()
        if result is not None:
            messagebox.showerror("Error", "Username is already taken")
            conn.close()
            return
            
        # add the new user to the database
        
        if role == "admin":
            # check if there are already 3 admins in the database
            c.execute("SELECT COUNT(*) FROM accounts WHERE role=?", ("admin",))
            count = c.fetchone()[0]
            if count >= 3:
                messagebox.showerror("Error", "There can only be 3 admins")
                conn.close()
                return
            
            
        c.execute("INSERT INTO accounts (username, password, role, email, security_question, security_answer) VALUES (?, ?, ?, ?, ?, ?)", (username, password, role, email, security_question, security_answer))
        conn.commit()
        conn.close()
            
        messagebox.showinfo("Success", "Account created successfully")
        self.parent.destroy()
