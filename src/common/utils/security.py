import secrets
import hashlib
from pwdlib import PasswordHash

# Initialize PasswordHash (Argon2 is recommended and installed)
password_hash = PasswordHash.recommended()

def hash_password(password: str) -> str:
    """Hash a password using pwdlib."""
    return password_hash.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    """Verify a password against a hash using pwdlib."""
    return password_hash.verify(password, hashed_password)

def generate_reset_token() -> tuple[str, str]:
    """Generate a random token and its SHA-256 hash.
    
    Returns:
        tuple[str, str]: (raw_token, hash_token)
    """
    raw_token = secrets.token_hex(32)
    hash_token = hashlib.sha256(raw_token.encode("utf-8")).hexdigest()
    return raw_token, hash_token
