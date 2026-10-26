import bcrypt
import jwt
from datetime import datetime, timedelta, timezone

def get_password_hash(password: str) -> str:
    """Takes a plain text password and returns a secure hash."""
    # bcrypt requires bytes, not strings, so we encode it first
    password_bytes = password.encode('utf-8')
    # Generate a random salt and hash the password
    hashed_bytes = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    # Decode back to a string so it can be saved in the database
    return hashed_bytes.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Checks if the provided password matches the saved hash."""
    password_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)

SECRET_KEY = "my-super-secret-key-do-not-use-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict) -> str:
    """Generates a signed JWT valid for 30 minutes."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    # Create the cryptographically signed token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt