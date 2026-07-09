from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from fastapi import HTTPException, status
from src.common.config.env_config import (
    JWT_ACCESS_SECRET,
    JWT_REFRESH_SECRET,
    JWT_RESET_SECRET,
    JWT_VERIFICATION_SECRET,
    JWT_ALGORITHM,
)

# Token configuration (durations)
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7
RESET_TOKEN_EXPIRE_MINUTES = 15

def generate_token(payload: dict, secret: str, expires_in: timedelta) -> str:
    """Helper function to generate a JWT token."""
    to_encode = payload.copy()
    now = datetime.now(timezone.utc)
    expire = now + expires_in
    to_encode.update({
        "exp": int(expire.timestamp()),
        "iat": int(now.timestamp())
    })
    return jwt.encode(to_encode, secret, algorithm=JWT_ALGORITHM)

def verify_token(token: str, secret: str) -> dict:
    """Helper function to decode and verify a JWT token.
    Raises HTTPException (401) on invalid or expired tokens.
    """
    try:
        payload = jwt.decode(token, secret, algorithms=[JWT_ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Access Token Functions
def generate_access_token(payload: dict) -> str:
    return generate_token(payload, JWT_ACCESS_SECRET, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

def verify_access_token(token: str) -> dict:
    return verify_token(token, JWT_ACCESS_SECRET)

# Refresh Token Functions
def generate_refresh_token(payload: dict) -> str:
    return generate_token(payload, JWT_REFRESH_SECRET, timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))

def verify_refresh_token(token: str) -> dict:
    return verify_token(token, JWT_REFRESH_SECRET)

# Reset Token Functions
def generate_reset_token(payload: dict) -> str:
    return generate_token(payload, JWT_RESET_SECRET, timedelta(minutes=RESET_TOKEN_EXPIRE_MINUTES))

def verify_reset_token(token: str) -> dict:
    return verify_token(token, JWT_RESET_SECRET)

# Verification Token Functions
def generate_verification_token(payload: dict) -> str:
    return generate_token(payload, JWT_VERIFICATION_SECRET, timedelta(days=1))

def verify_verification_token(token: str) -> dict:
    return verify_token(token, JWT_VERIFICATION_SECRET)

# Compatibility aliases for camelCase and potential typo (genrateAccessToken/genrateRefreshToken)
generateAccessToken = generate_access_token
genrateAccessToken = generate_access_token

verifyAccessToken = verify_access_token

generateRefreshToken = generate_refresh_token
genrateRefreshToken = generate_refresh_token

verifyRefreshToken = verify_refresh_token

generateResetToken = generate_reset_token
verifyResetToken = verify_reset_token

generateVerificationToken = generate_verification_token
verifyVerificationToken = verify_verification_token

