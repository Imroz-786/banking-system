import sqlite3
import json
from datetime import datetime
from models.user import User
from models.account import Account
from models.transaction import Transaction, TransactionType

class DatabaseManager:
    """Database manager for banking system"""
    
    def __init__(self, db_name='banking_system.db'):
        self.db_name = db_name
        self.connection = None
        self.cursor = None
        self.initialize_database()
        
    def initialize_database(self):
        """Initialize database with required tables"""
        self.connect()
        self.create_tables()
        
    def connect(self):
        """Connect to database"""
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        
    def create_tables(self):
        """Create all required tables"""
        # Users table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                full_name TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Accounts table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS accounts (
                account_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                account_type TEXT NOT NULL,
                balance REAL DEFAULT 0.0,
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        # Transactions table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_id INTEGER NOT NULL,
                transaction_type TEXT NOT NULL,
                amount REAL NOT NULL,
                description TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'Completed',
                FOREIGN KEY (account_id) REFERENCES accounts (account_id)
            )
        ''')
        
        self.connection.commit()
        
    def add_user(self, user):
        """Add a new user to database"""
        try:
            self.cursor.execute('''
                INSERT INTO users (username, email, password, full_name)
                VALUES (?, ?, ?, ?)
            ''', (user.username, user.email, user.password, user.full_name))
            self.connection.commit()
            return self.cursor.lastrowid
        except sqlite3.IntegrityError as e:
            raise ValueError(f"User already exists: {str(e)}")
        
    def get_user_by_username(self, username):
        """Get user by username"""
        self.cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        row = self.cursor.fetchone()
        if row:
            return User(row[0], row[1], row[2], row[3], row[4])
        return None
    
    def add_account(self, account):
        """Add a new account"""
        self.cursor.execute('''
            INSERT INTO accounts (user_id, account_type, balance)
            VALUES (?, ?, ?)
        ''', (account.user_id, account.account_type, account.balance))
        self.connection.commit()
        return self.cursor.lastrowid
    
    def get_accounts_by_user(self, user_id):
        """Get all accounts for a user"""
        self.cursor.execute(
            'SELECT * FROM accounts WHERE user_id = ? AND is_active = 1',
            (user_id,)
        )
        accounts = []
        for row in self.cursor.fetchall():
            account = Account(row[0], row[1], row[2], row[3])
            account.is_active = row[4]
            accounts.append(account)
        return accounts
    
    def get_account_by_id(self, account_id):
        """Get a single account by account_id, returns a list"""
        self.cursor.execute(
            'SELECT * FROM accounts WHERE account_id = ? AND is_active = 1',
            (account_id,)
        )
        accounts = []
        for row in self.cursor.fetchall():
            account = Account(row[0], row[1], row[2], row[3])
            account.is_active = row[4]
            accounts.append(account)
        return accounts

    def update_account_balance(self, account_id, new_balance):
        """Update account balance"""
        self.cursor.execute(
            'UPDATE accounts SET balance = ? WHERE account_id = ?',
            (new_balance, account_id)
        )
        self.connection.commit()
    
    def add_transaction(self, transaction):
        """Add a new transaction"""
        self.cursor.execute('''
            INSERT INTO transactions 
            (account_id, transaction_type, amount, description, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (transaction.account_id, transaction.transaction_type.value, 
              transaction.amount, transaction.description, transaction.status))
        self.connection.commit()
        return self.cursor.lastrowid
    
    def get_transactions(self, account_id, limit=10):
        """Get transactions for an account"""
        self.cursor.execute('''
            SELECT * FROM transactions 
            WHERE account_id = ? 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (account_id, limit))
        
        transactions = []
        for row in self.cursor.fetchall():
            transaction_type = TransactionType(row[2])
            transaction = Transaction(row[0], row[1], transaction_type, row[3], row[4])
            transaction.status = row[6]
            transactions.append(transaction)
        return transactions
    
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()