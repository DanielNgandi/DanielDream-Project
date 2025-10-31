
import tkinter.messagebox as messagebox
import sqlite3
from Register import RegisterWindow
from Dashboard import DashboardUI
from Admindashboard import AdminDashboardUI
from tkinter import *
from Reset import ResetWindow
import tkinter as tk

class Login:
    def __init__(self, root):
        self.root = root
        self.reset_username = tk.StringVar()
        self.root.title("Dream Waters Inventory Login")
        self.root.geometry("400x450+400+200")
        self.root.resizable(False, False)
        self.root.configure(bg="#f7f7f7")

        # Variables
        self.username = StringVar()
        self.password = StringVar()
        self.security_question = StringVar()
        self.security_answer = StringVar()

        # Login Frame
        frame1 = Frame(self.root, bg="#f7f7f7")
        frame1.place(x=50, y=50, width=300, height=300)

        title = Label(frame1, text="Login", font=("Verdana", 18), bg="#f7f7f7", fg="green").place(x=20, y=10)

        lbl_username = Label(frame1, text="Username", font=("Verdana", 10), bg="#f7f7f7", fg="gray").place(x=20, y=60)
        txt_username = Entry(frame1, font=("Verdana", 12), bg="#f7f7f7", textvariable=self.username).place(x=20, y=90, width=260)

        lbl_password = Label(frame1, text="Password", font=("Verdana", 10), bg="#f7f7f7", fg="gray").place(x=20, y=120)
        txt_password = Entry(frame1, font=("Verdana", 12), bg="#f7f7f7", textvariable=self.password, show="*").place(x=20, y=150, width=260)
        
        btn_login = Button(frame1, text="Login", font=("Verdana", 12), bg="green", fg="white", command=self.login).place(x=20, y=200, width=120, height=35)
        btn_register = Button(frame1, text="Register", font=("Verdana", 12), bg="blue", fg="white", command=self.register).place(x=160, y=200, width=120, height=35)
        
        lbl_reset = Label(frame1, text="Click to Reset Password", font=("Verdana", 12), bg="#f7f7f7", fg="red", cursor="hand2")
        lbl_reset.place(x=50, y=250)
        lbl_reset.bind("<Button-1>", self.reset_password)

        
    def login(self):
        username = self.username.get()
        password = self.password.get()

        conn = sqlite3.connect('dream_waters_inventory.db')
        c = conn.cursor()
        c.execute("SELECT * FROM accounts WHERE username=? AND password=?", (username, password))
        result = c.fetchone()

        if result:
            role = result[6]
            username = result[1]
            
            if role == "user":
                messagebox.showinfo("Login Successful", f"Hello User {username}. Welcome to Dream waters")
                self.root.destroy()
                master = tk.Tk()
                master.geometry("1250x630+0+0")
                dashboard = DashboardUI(master)
                dashboard.update_user_name(username)
                master.mainloop()
                
            elif role == "admin":
                messagebox.showinfo("Login Successful", f"Hello Admin {username}. Welcome to Dream waters")
                self.root.destroy()
                admin_master = tk.Tk()
                admin_master.geometry("1250x630+0+0")
                admin_dashboard = AdminDashboardUI(admin_master)
                admin_dashboard.update_user_name(username)
                admin_master.mainloop()
                
            else:
                messagebox.showerror("Login Error", "Invalid role")

        else:
            messagebox.showerror("Login Error", "Invalid username or password")

        conn.close()
            
    def register(self):
        self.register_window = tk.Toplevel(self.root)
        RegisterWindow(self.register_window)
        
    def reset_password(self, event=None):
        reset_window = tk.Toplevel(self.root)
        ResetWindow(reset_window, self.username.get())
        
if __name__ == '__main__':
    root = Tk()
    app = Login(root)
    root.mainloop()