import tkinter as tk
from tkinter import ttk
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from gui.login_window import LoginWindow, RegisterWindow
from gui.dashboard_window import DashboardWindow


class MainWindow(tk.Tk):
    """Main application window – entry point for the banking system GUI"""

    def __init__(self):
        super().__init__()
        self.title("Banking System")
        self.geometry("400x280")
        self.resizable(False, False)
        self._build_ui()

    def _build_ui(self):
        frame = ttk.Frame(self, padding=30)
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="🏦 Banking System",
                  font=("Helvetica", 22, "bold")).pack(pady=(0, 8))
        ttk.Label(frame, text="Secure. Simple. Reliable.",
                  font=("Helvetica", 11)).pack(pady=(0, 24))

        ttk.Button(frame, text="Login", command=self._open_login, width=20).pack(pady=6)
        ttk.Button(frame, text="Register", command=self._open_register, width=20).pack(pady=6)
        ttk.Button(frame, text="Exit", command=self.destroy, width=20).pack(pady=6)

    def _open_login(self):
        LoginWindow(self, on_success=self._on_login_success)

    def _open_register(self):
        RegisterWindow(self, on_success=self._open_login)

    def _on_login_success(self, user):
        DashboardWindow(self, user)
