import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Blueprint, request, jsonify
from models.user import User
from models.account import Account
from models.transaction import Transaction, TransactionType
from database.db_manager import DatabaseManager

api_bp = Blueprint('api', __name__)
db = DatabaseManager()


# ── Authentication routes ────────────────────────────────────────────────────

@api_bp.route('/auth/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json()
    required = ['username', 'email', 'password', 'full_name']
    if not data or not all(k in data for k in required):
        return jsonify({'error': 'Missing required fields'}), 400

    user = User(
        username=data['username'],
        email=data['email'],
        full_name=data['full_name'],
    )
    user.set_password(data['password'])

    try:
        user_id = db.add_user(user)
        user.user_id = user_id
        return jsonify({'message': 'User registered successfully',
                        'user': user.to_dict()}), 201
    except ValueError:
        return jsonify({'error': 'Username or email already exists'}), 409


@api_bp.route('/auth/login', methods=['POST'])
def login():
    """Authenticate a user"""
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Missing username or password'}), 400

    user = db.get_user_by_username(data['username'])
    if not user or not user.verify_password(data['password']):
        return jsonify({'error': 'Invalid credentials'}), 401

    return jsonify({'message': 'Login successful', 'user': user.to_dict()}), 200


# ── Account routes ───────────────────────────────────────────────────────────

@api_bp.route('/accounts', methods=['POST'])
def create_account():
    """Create a new bank account"""
    data = request.get_json()
    if not data or 'user_id' not in data or 'account_type' not in data:
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        account = Account(
            user_id=data['user_id'],
            account_type=data['account_type'],
            balance=data.get('initial_deposit', 0.0),
        )
        account_id = db.add_account(account)
        account.account_id = account_id

        if account.balance > 0:
            transaction = Transaction(
                account_id=account_id,
                transaction_type=TransactionType.DEPOSIT,
                amount=account.balance,
                description='Initial deposit',
            )
            db.add_transaction(transaction)

        return jsonify({'message': 'Account created successfully',
                        'account': account.to_dict()}), 201
    except ValueError:
        return jsonify({'error': 'Invalid account type or deposit amount'}), 400


@api_bp.route('/accounts/<int:user_id>', methods=['GET'])
def get_accounts(user_id):
    """Get all accounts for a user"""
    accounts = db.get_accounts_by_user(user_id)
    return jsonify({'accounts': [a.to_dict() for a in accounts]}), 200


# ── Transaction routes ───────────────────────────────────────────────────────

@api_bp.route('/accounts/<int:account_id>/deposit', methods=['POST'])
def deposit(account_id):
    """Deposit funds into an account"""
    data = request.get_json()
    if not data or 'amount' not in data:
        return jsonify({'error': 'Missing amount'}), 400

    accounts = db.get_account_by_id(account_id)
    if not accounts:
        return jsonify({'error': 'Account not found'}), 404

    account = accounts[0]
    try:
        new_balance = account.deposit(float(data['amount']))
        db.update_account_balance(account_id, new_balance)

        transaction = Transaction(
            account_id=account_id,
            transaction_type=TransactionType.DEPOSIT,
            amount=float(data['amount']),
            description=data.get('description', 'Deposit'),
        )
        db.add_transaction(transaction)

        return jsonify({'message': 'Deposit successful',
                        'new_balance': new_balance}), 200
    except ValueError:
        return jsonify({'error': 'Invalid deposit amount'}), 400


@api_bp.route('/accounts/<int:account_id>/withdraw', methods=['POST'])
def withdraw(account_id):
    """Withdraw funds from an account"""
    data = request.get_json()
    if not data or 'amount' not in data:
        return jsonify({'error': 'Missing amount'}), 400

    accounts = db.get_account_by_id(account_id)
    if not accounts:
        return jsonify({'error': 'Account not found'}), 404

    account = accounts[0]
    try:
        new_balance = account.withdraw(float(data['amount']))
        db.update_account_balance(account_id, new_balance)

        transaction = Transaction(
            account_id=account_id,
            transaction_type=TransactionType.WITHDRAWAL,
            amount=float(data['amount']),
            description=data.get('description', 'Withdrawal'),
        )
        db.add_transaction(transaction)

        return jsonify({'message': 'Withdrawal successful',
                        'new_balance': new_balance}), 200
    except ValueError:
        return jsonify({'error': 'Invalid amount or insufficient funds'}), 400


@api_bp.route('/accounts/<int:account_id>/transactions', methods=['GET'])
def get_transactions(account_id):
    """Get transaction history for an account"""
    limit = request.args.get('limit', 20, type=int)
    transactions = db.get_transactions(account_id, limit)
    return jsonify(
        {'transactions': [t.to_dict() for t in transactions]}
    ), 200
