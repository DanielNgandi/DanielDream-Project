import tkinter as tk
import tkinter.messagebox as messagebox
import sqlite3

class ResetWindow:
    def __init__(self, root, username):
        self.root = root
        self.root.title("Reset Password")
        self.root.geometry("400x400+400+200")
        self.root.resizable(False, False)
        self.root.configure(bg="#f7f7f7")
        self.username = username

        # Reset Frame
        frame = tk.Frame(self.root, bg="#f7f7f7")
        frame.place(x=50, y=50, width=300, height=300)

        title = tk.Label(frame, text="Reset Password", font=("Verdana", 18), bg="#f7f7f7", fg="green")
        title.place(x=20, y=10)

        # Security Answer Label
        lbl_security_answer = tk.Label(frame, text="Security Answer:", font=("Verdana", 10), bg="#f7f7f7", fg="gray")
        lbl_security_answer.place(x=20, y=60)
        self.security_answer_entry = tk.Entry(frame, font=("Verdana", 12))
        self.security_answer_entry.place(x=20, y=90, width=260)

        # New Password Label
        lbl_new_password = tk.Label(frame, text="New Password:", font=("Verdana", 10), bg="#f7f7f7", fg="gray")
        lbl_new_password.place(x=20, y=120)
        self.new_password_entry = tk.Entry(frame, font=("Verdana", 12), show="*")
        self.new_password_entry.place(x=20, y=150, width=260)

        # Confirm Password Label
        lbl_confirm_password = tk.Label(frame, text="Confirm Password:", font=("Verdana", 10), bg="#f7f7f7", fg="gray")
        lbl_confirm_password.place(x=20, y=180)
        self.confirm_password_entry = tk.Entry(frame, font=("Verdana", 12), show="*")
        self.confirm_password_entry.place(x=20, y=210, width=260)

        # Reset Button
        btn_reset = tk.Button(frame, text="Reset", font=("Verdana", 12), bg="orange", fg="white", command=self.reset_password)
        btn_reset.place(x=20, y=250, width=260)


    def reset_password(self):
        security_answer = self.security_answer_entry.get()
        new_password = self.new_password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if not security_answer or not new_password or not confirm_password:
            messagebox.showerror("Error", "All fields are required")
            return

        if new_password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return

        # Retrieving the username
        username = self.username

        conn = sqlite3.connect('dream_waters_inventory.db')
        c = conn.cursor()
        c.execute("SELECT security_question, security_answer FROM accounts WHERE username=?", (username,))
        result = c.fetchone()

        if not result:
            messagebox.showerror("Error", "Username not found")
            conn.close()
            return

        security_question, correct_security_answer = result

        if security_question is None or correct_security_answer is None:
            messagebox.showerror("Error", "No security question or answer found for the username")
            conn.close()
            return

        if security_answer != correct_security_answer:
            messagebox.showerror("Error", "Incorrect security answer")
            conn.close()
            return

        # Update the password in the database
        c.execute("UPDATE accounts SET password=? WHERE username=?", (new_password, username))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Password reset successful")

        self.root.destroy()
