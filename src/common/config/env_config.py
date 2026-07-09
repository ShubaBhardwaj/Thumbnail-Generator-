import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
IMAGEKIT_PRIVATE_KEY = os.getenv("IMAGEKIT_PRIVATE_KEY", "")
IMAGEKIT_PUBLIC_KEY = os.getenv("IMAGEKIT_PUBLIC_KEY", "")
IMAGEKIT_URL_ENDPOINT = os.getenv("IMAGEKIT_URL_ENDPOINT", "")

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./auth.db")

JWT_ACCESS_SECRET = os.getenv("JWT_ACCESS_SECRET", "access-secret-key-1234567890-xyz")
JWT_REFRESH_SECRET = os.getenv("JWT_REFRESH_SECRET", "refresh-secret-key-1234567890-xyz")
JWT_RESET_SECRET = os.getenv("JWT_RESET_SECRET", "reset-secret-key-1234567890-xyz")
JWT_VERIFICATION_SECRET = os.getenv("JWT_VERIFICATION_SECRET", "verification-secret-key-1234567890-xyz")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

RESEND_API_KEY = os.getenv("RESEND_API_KEY", "")
RESEND_FROM_EMAIL = os.getenv("RESEND_FROM_EMAIL", "Acme <onboarding@resend.dev>")
APP_URL = os.getenv("APP_URL", "http://localhost:8000")