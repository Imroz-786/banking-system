from enum import Enum
from datetime import datetime


class TransactionType(Enum):
    DEPOSIT = 'Deposit'
    WITHDRAWAL = 'Withdrawal'
    TRANSFER = 'Transfer'


class Transaction:
    """Transaction class representing a single banking transaction"""

    def __init__(self, transaction_id=None, account_id=None,
                 transaction_type=None, amount=0.0, description=''):
        self.transaction_id = transaction_id
        self.account_id = account_id
        self.transaction_type = transaction_type
        self.amount = float(amount)
        self.description = description
        self.timestamp = datetime.now()
        self.status = 'Completed'

    def to_dict(self):
        """Return a dictionary representation"""
        return {
            'transaction_id': self.transaction_id,
            'account_id': self.account_id,
            'transaction_type': (
                self.transaction_type.value
                if self.transaction_type else None
            ),
            'amount': self.amount,
            'description': self.description,
            'timestamp': str(self.timestamp),
            'status': self.status,
        }

    def __repr__(self):
        return (
            f"Transaction(id={self.transaction_id}, "
            f"type={self.transaction_type}, amount={self.amount:.2f})"
        )
