from werkzeug.security import generate_password_hash, check_password_hash


class User:
    """User class with authentication support"""

    def __init__(self, user_id=None, username=None, email=None,
                 password=None, full_name=None):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password = password
        self.full_name = full_name

    @staticmethod
    def hash_password(password):
        """Hash a plaintext password using PBKDF2-HMAC-SHA256 with a random salt"""
        return generate_password_hash(password)

    def set_password(self, plaintext_password):
        """Set hashed password from plaintext"""
        self.password = self.hash_password(plaintext_password)

    def verify_password(self, plaintext_password):
        """Verify a plaintext password against the stored hash"""
        return check_password_hash(self.password, plaintext_password)

    def to_dict(self):
        """Return a dictionary representation (excluding password)"""
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
        }

    def __repr__(self):
        return f"User(id={self.user_id}, username={self.username})"

