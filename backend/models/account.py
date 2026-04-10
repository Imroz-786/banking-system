class Account:
    """Account class with deposit and withdraw methods"""

    ACCOUNT_TYPES = ['Savings', 'Checking', 'Money Market']

    def __init__(self, account_id=None, user_id=None,
                 account_type='Savings', balance=0.0):
        self.account_id = account_id
        self.user_id = user_id
        if account_type not in self.ACCOUNT_TYPES:
            raise ValueError(
                f"Invalid account type. Choose from: {self.ACCOUNT_TYPES}"
            )
        self.account_type = account_type
        self.balance = float(balance)
        self.is_active = True

    def deposit(self, amount):
        """Deposit funds into the account"""
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.balance += amount
        return self.balance

    def withdraw(self, amount):
        """Withdraw funds from the account"""
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount
        return self.balance

    def to_dict(self):
        """Return a dictionary representation"""
        return {
            'account_id': self.account_id,
            'user_id': self.user_id,
            'account_type': self.account_type,
            'balance': self.balance,
            'is_active': self.is_active,
        }

    def __repr__(self):
        return (
            f"Account(id={self.account_id}, type={self.account_type}, "
            f"balance={self.balance:.2f})"
        )
