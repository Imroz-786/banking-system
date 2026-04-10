import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from client import APIClient


class LoginWindow(tk.Toplevel):
    """Login window for existing users"""

    def __init__(self, parent, on_success):
        super().__init__(parent)
        self.client = APIClient()
        self.on_success = on_success
        self.title("Banking System – Login")
        self.resizable(False, False)
        self._build_ui()
        self.grab_set()

    def _build_ui(self):
        frame = ttk.Frame(self, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Banking System", font=("Helvetica", 18, "bold")).grid(
            row=0, column=0, columnspan=2, pady=(0, 15)
        )

        ttk.Label(frame, text="Username:").grid(row=1, column=0, sticky=tk.W, pady=4)
        self.username_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.username_var, width=28).grid(
            row=1, column=1, pady=4
        )

        ttk.Label(frame, text="Password:").grid(row=2, column=0, sticky=tk.W, pady=4)
        self.password_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.password_var, show="*", width=28).grid(
            row=2, column=1, pady=4
        )

        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=12)
        ttk.Button(btn_frame, text="Login", command=self._login, width=12).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(btn_frame, text="Cancel", command=self.destroy, width=12).pack(
            side=tk.LEFT, padx=5
        )

    def _login(self):
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()
        if not username or not password:
            messagebox.showwarning("Warning", "Please fill in all fields.", parent=self)
            return

        data, status = self.client.login(username, password)
        if status == 200:
            self.destroy()
            self.on_success(data['user'])
        else:
            messagebox.showerror(
                "Login Failed", data.get('error', 'Invalid credentials'), parent=self
            )


class RegisterWindow(tk.Toplevel):
    """Registration window for new users"""

    def __init__(self, parent, on_success):
        super().__init__(parent)
        self.client = APIClient()
        self.on_success = on_success
        self.title("Banking System – Register")
        self.resizable(False, False)
        self._build_ui()
        self.grab_set()

    def _build_ui(self):
        frame = ttk.Frame(self, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Create Account", font=("Helvetica", 16, "bold")).grid(
            row=0, column=0, columnspan=2, pady=(0, 15)
        )

        fields = [
            ("Full Name:", "full_name_var"),
            ("Username:", "username_var"),
            ("Email:", "email_var"),
            ("Password:", "password_var"),
            ("Confirm Password:", "confirm_var"),
        ]
        self.full_name_var = tk.StringVar()
        self.username_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.confirm_var = tk.StringVar()

        for idx, (label, attr) in enumerate(fields, start=1):
            ttk.Label(frame, text=label).grid(row=idx, column=0, sticky=tk.W, pady=4)
            show = "*" if "password" in attr.lower() or "confirm" in attr.lower() else ""
            ttk.Entry(frame, textvariable=getattr(self, attr), show=show, width=28).grid(
                row=idx, column=1, pady=4
            )

        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=len(fields) + 1, column=0, columnspan=2, pady=12)
        ttk.Button(btn_frame, text="Register", command=self._register, width=12).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(btn_frame, text="Cancel", command=self.destroy, width=12).pack(
            side=tk.LEFT, padx=5
        )

    def _register(self):
        full_name = self.full_name_var.get().strip()
        username = self.username_var.get().strip()
        email = self.email_var.get().strip()
        password = self.password_var.get().strip()
        confirm = self.confirm_var.get().strip()

        if not all([full_name, username, email, password, confirm]):
            messagebox.showwarning("Warning", "Please fill in all fields.", parent=self)
            return
        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match.", parent=self)
            return

        data, status = self.client.register(username, email, password, full_name)
        if status == 201:
            messagebox.showinfo(
                "Success", "Registration successful! Please log in.", parent=self
            )
            self.destroy()
            self.on_success()
        else:
            messagebox.showerror(
                "Registration Failed", data.get('error', 'Registration failed'), parent=self
            )
