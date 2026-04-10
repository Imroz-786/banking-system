import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from client import APIClient


class DashboardWindow(tk.Toplevel):
    """Dashboard window – account management, deposit, withdraw, transactions"""

    def __init__(self, parent, user):
        super().__init__(parent)
        self.client = APIClient()
        self.user = user
        self.selected_account = None
        self.title(f"Banking System – {user['full_name']}")
        self.geometry("720x540")
        self._build_ui()
        self.grab_set()
        self._refresh_accounts()

    # ── UI Construction ───────────────────────────────────────────────────────

    def _build_ui(self):
        # Top info bar
        top = ttk.Frame(self, padding=(10, 6))
        top.pack(fill=tk.X)
        ttk.Label(top, text=f"Welcome, {self.user['full_name']}",
                  font=("Helvetica", 13, "bold")).pack(side=tk.LEFT)
        ttk.Button(top, text="Logout", command=self.destroy).pack(side=tk.RIGHT)

        ttk.Separator(self, orient=tk.HORIZONTAL).pack(fill=tk.X)

        main = ttk.Frame(self, padding=10)
        main.pack(fill=tk.BOTH, expand=True)

        # Left: accounts list
        left = ttk.LabelFrame(main, text="My Accounts", padding=8)
        left.grid(row=0, column=0, sticky=tk.NSEW, padx=(0, 8))

        self.accounts_list = tk.Listbox(left, width=28, height=14)
        self.accounts_list.pack(fill=tk.BOTH, expand=True)
        self.accounts_list.bind("<<ListboxSelect>>", self._on_account_select)

        ttk.Button(left, text="New Account", command=self._create_account_dialog).pack(
            fill=tk.X, pady=(6, 0)
        )

        # Right: actions + transactions
        right = ttk.Frame(main)
        right.grid(row=0, column=1, sticky=tk.NSEW)

        action_frame = ttk.LabelFrame(right, text="Actions", padding=8)
        action_frame.pack(fill=tk.X)

        self.balance_label = ttk.Label(action_frame, text="Select an account",
                                       font=("Helvetica", 11))
        self.balance_label.pack(anchor=tk.W)

        btn_row = ttk.Frame(action_frame)
        btn_row.pack(fill=tk.X, pady=6)
        ttk.Button(btn_row, text="Deposit", command=self._deposit_dialog, width=12).pack(
            side=tk.LEFT, padx=4
        )
        ttk.Button(btn_row, text="Withdraw", command=self._withdraw_dialog, width=12).pack(
            side=tk.LEFT, padx=4
        )
        ttk.Button(btn_row, text="Refresh", command=self._refresh_transactions, width=12).pack(
            side=tk.LEFT, padx=4
        )

        tx_frame = ttk.LabelFrame(right, text="Recent Transactions", padding=8)
        tx_frame.pack(fill=tk.BOTH, expand=True, pady=(8, 0))

        cols = ("Type", "Amount", "Description", "Date")
        self.tx_tree = ttk.Treeview(tx_frame, columns=cols, show="headings", height=10)
        for col in cols:
            self.tx_tree.heading(col, text=col)
            self.tx_tree.column(col, width=120)
        self.tx_tree.pack(fill=tk.BOTH, expand=True)

        main.columnconfigure(0, weight=1)
        main.columnconfigure(1, weight=2)
        main.rowconfigure(0, weight=1)

    # ── Data helpers ──────────────────────────────────────────────────────────

    def _refresh_accounts(self):
        self.accounts_data = []
        self.accounts_list.delete(0, tk.END)
        data, status = self.client.get_accounts(self.user['user_id'])
        if status == 200:
            for acct in data.get('accounts', []):
                self.accounts_data.append(acct)
                self.accounts_list.insert(
                    tk.END,
                    f"{acct['account_type']}  –  ${acct['balance']:.2f}"
                )

    def _on_account_select(self, _event):
        selection = self.accounts_list.curselection()
        if not selection:
            return
        self.selected_account = self.accounts_data[selection[0]]
        self.balance_label.config(
            text=(
                f"{self.selected_account['account_type']} – "
                f"Balance: ${self.selected_account['balance']:.2f}"
            )
        )
        self._refresh_transactions()

    def _refresh_transactions(self):
        if not self.selected_account:
            return
        for row in self.tx_tree.get_children():
            self.tx_tree.delete(row)
        data, status = self.client.get_transactions(
            self.selected_account['account_id']
        )
        if status == 200:
            for tx in data.get('transactions', []):
                self.tx_tree.insert("", tk.END, values=(
                    tx['transaction_type'],
                    f"${tx['amount']:.2f}",
                    tx['description'],
                    str(tx['timestamp'])[:16],
                ))

    # ── Dialogs ───────────────────────────────────────────────────────────────

    def _require_account(self):
        if not self.selected_account:
            messagebox.showwarning("Warning", "Please select an account first.",
                                   parent=self)
            return False
        return True

    def _create_account_dialog(self):
        dlg = tk.Toplevel(self)
        dlg.title("Create New Account")
        dlg.resizable(False, False)
        dlg.grab_set()

        frame = ttk.Frame(dlg, padding=16)
        frame.pack()

        ttk.Label(frame, text="Account Type:").grid(row=0, column=0, sticky=tk.W, pady=4)
        account_type_var = tk.StringVar(value="Savings")
        ttk.Combobox(frame, textvariable=account_type_var,
                     values=["Savings", "Checking", "Money Market"],
                     state="readonly", width=18).grid(row=0, column=1, pady=4)

        ttk.Label(frame, text="Initial Deposit ($):").grid(row=1, column=0, sticky=tk.W, pady=4)
        deposit_var = tk.StringVar(value="0.00")
        ttk.Entry(frame, textvariable=deposit_var, width=20).grid(row=1, column=1, pady=4)

        def _submit():
            try:
                initial = float(deposit_var.get())
            except ValueError:
                messagebox.showerror("Error", "Invalid deposit amount.", parent=dlg)
                return
            data, status = self.client.create_account(
                self.user['user_id'], account_type_var.get(), initial
            )
            if status == 201:
                messagebox.showinfo("Success", "Account created!", parent=dlg)
                dlg.destroy()
                self._refresh_accounts()
            else:
                messagebox.showerror(
                    "Error", data.get('error', 'Failed to create account'), parent=dlg
                )

        btn_row = ttk.Frame(frame)
        btn_row.grid(row=2, column=0, columnspan=2, pady=10)
        ttk.Button(btn_row, text="Create", command=_submit, width=10).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_row, text="Cancel", command=dlg.destroy, width=10).pack(side=tk.LEFT, padx=4)

    def _deposit_dialog(self):
        if not self._require_account():
            return
        self._amount_dialog("Deposit", self.client.deposit)

    def _withdraw_dialog(self):
        if not self._require_account():
            return
        self._amount_dialog("Withdraw", self.client.withdraw)

    def _amount_dialog(self, title, api_call):
        dlg = tk.Toplevel(self)
        dlg.title(title)
        dlg.resizable(False, False)
        dlg.grab_set()

        frame = ttk.Frame(dlg, padding=16)
        frame.pack()

        ttk.Label(frame, text="Amount ($):").grid(row=0, column=0, sticky=tk.W, pady=4)
        amount_var = tk.StringVar()
        ttk.Entry(frame, textvariable=amount_var, width=18).grid(row=0, column=1, pady=4)

        ttk.Label(frame, text="Description:").grid(row=1, column=0, sticky=tk.W, pady=4)
        desc_var = tk.StringVar(value=title)
        ttk.Entry(frame, textvariable=desc_var, width=18).grid(row=1, column=1, pady=4)

        def _submit():
            try:
                amount = float(amount_var.get())
            except ValueError:
                messagebox.showerror("Error", "Invalid amount.", parent=dlg)
                return
            data, status = api_call(
                self.selected_account['account_id'], amount, desc_var.get()
            )
            if status == 200:
                messagebox.showinfo("Success", f"{title} successful!", parent=dlg)
                dlg.destroy()
                self._refresh_accounts()
                if self.selected_account:
                    for acct in self.accounts_data:
                        if acct['account_id'] == self.selected_account['account_id']:
                            acct['balance'] = data['new_balance']
                            self.selected_account = acct
                            self.balance_label.config(
                                text=(
                                    f"{acct['account_type']} – "
                                    f"Balance: ${acct['balance']:.2f}"
                                )
                            )
                            break
                self._refresh_transactions()
            else:
                messagebox.showerror(
                    "Error", data.get('error', f'{title} failed'), parent=dlg
                )

        btn_row = ttk.Frame(frame)
        btn_row.grid(row=2, column=0, columnspan=2, pady=10)
        ttk.Button(btn_row, text=title, command=_submit, width=10).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_row, text="Cancel", command=dlg.destroy, width=10).pack(side=tk.LEFT, padx=4)
