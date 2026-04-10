import requests


BASE_URL = 'http://127.0.0.1:5000/api'


class APIClient:
    """Client for communicating with the banking system backend API"""

    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()

    def _get(self, endpoint, params=None):
        try:
            response = self.session.get(
                f"{self.base_url}{endpoint}", params=params, timeout=10
            )
            return response.json(), response.status_code
        except requests.exceptions.ConnectionError:
            return {'error': 'Cannot connect to server'}, 0

    def _post(self, endpoint, data):
        try:
            response = self.session.post(
                f"{self.base_url}{endpoint}", json=data, timeout=10
            )
            return response.json(), response.status_code
        except requests.exceptions.ConnectionError:
            return {'error': 'Cannot connect to server'}, 0

    # ── Auth ─────────────────────────────────────────────────────────────────

    def register(self, username, email, password, full_name):
        return self._post('/auth/register', {
            'username': username,
            'email': email,
            'password': password,
            'full_name': full_name,
        })

    def login(self, username, password):
        return self._post('/auth/login', {
            'username': username,
            'password': password,
        })

    # ── Accounts ─────────────────────────────────────────────────────────────

    def get_accounts(self, user_id):
        return self._get(f'/accounts/{user_id}')

    def create_account(self, user_id, account_type, initial_deposit=0.0):
        return self._post('/accounts', {
            'user_id': user_id,
            'account_type': account_type,
            'initial_deposit': initial_deposit,
        })

    # ── Transactions ─────────────────────────────────────────────────────────

    def deposit(self, account_id, amount, description='Deposit'):
        return self._post(f'/accounts/{account_id}/deposit', {
            'amount': amount,
            'description': description,
        })

    def withdraw(self, account_id, amount, description='Withdrawal'):
        return self._post(f'/accounts/{account_id}/withdraw', {
            'amount': amount,
            'description': description,
        })

    def get_transactions(self, account_id, limit=20):
        return self._get(
            f'/accounts/{account_id}/transactions', {'limit': limit}
        )
