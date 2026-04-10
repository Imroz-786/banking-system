# Banking System

A full-stack banking system built with Python, featuring a Flask REST API backend and a Tkinter GUI frontend backed by an SQLite database.

## Features

- User registration and login with SHA-256 password hashing
- Multiple account types: Savings, Checking, Money Market
- Deposit and withdrawal operations
- Transaction history tracking
- RESTful API with proper error handling and CORS support
- Responsive Tkinter GUI

## Project Structure

```
banking-system/
├── backend/
│   ├── models/
│   │   ├── user.py           # User class with authentication
│   │   ├── account.py        # Account class with deposit/withdraw
│   │   ├── transaction.py    # Transaction and TransactionType classes
│   │   └── __init__.py
│   ├── database/
│   │   ├── db_manager.py     # SQLite database manager
│   │   └── __init__.py
│   ├── api/
│   │   ├── app.py            # Flask application setup
│   │   ├── routes.py         # API endpoints
│   │   └── __init__.py
│   ├── requirements.txt
│   └── run.py                # Backend entry point
└── frontend/
    ├── gui/
    │   ├── login_window.py   # Login & Registration windows
    │   ├── dashboard_window.py # Dashboard with account management
    │   ├── main_window.py    # Main application window
    │   └── __init__.py
    ├── client.py             # API client
    ├── requirements.txt
    └── run.py                # Frontend entry point
```

## Quick Start

**Terminal 1 – Backend:**
```bash
cd backend
pip install -r requirements.txt
python run.py
```

**Terminal 2 – Frontend:**
```bash
cd frontend
pip install -r requirements.txt
python run.py
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register a new user |
| POST | `/api/auth/login` | Authenticate a user |
| POST | `/api/accounts` | Create a new account |
| GET | `/api/accounts/<user_id>` | Get accounts for a user |
| POST | `/api/accounts/<id>/deposit` | Deposit funds |
| POST | `/api/accounts/<id>/withdraw` | Withdraw funds |
| GET | `/api/accounts/<id>/transactions` | Get transaction history |

## Technologies

- **Backend:** Python, Flask, Flask-CORS, SQLite, Werkzeug
- **Frontend:** Python, Tkinter, requests
