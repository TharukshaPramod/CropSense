import sqlite3
import os
import time
from passlib.context import CryptContext
from jose import jwt, JWTError
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Config
SECRET = os.environ.get("CROPSENSE_JWT_SECRET", "dev-secret-change-me")
ALGO = "HS256"
ACCESS_EXPIRE = int(os.environ.get("CROPSENSE_JWT_EXPIRE_SECONDS", 60 * 60 * 4))

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

# SQLite DB
DB_DIR = os.path.join(os.getcwd(), "common")
os.makedirs(DB_DIR, exist_ok=True)
DB_PATH = os.path.join(DB_DIR, "auth.db")
_conn = sqlite3.connect(DB_PATH, check_same_thread=False)
_cursor = _conn.cursor()
_cursor.execute(
    """CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE,
        hashed_pw TEXT
    )"""
)
_conn.commit()


def create_user(username: str, password: str):
    """Create a new user in the DB."""
    hashed = pwd_ctx.hash(password)
    try:
        _cursor.execute("INSERT INTO users (username, hashed_pw) VALUES (?,?)", (username, hashed))
        _conn.commit()
        return True
    except sqlite3.IntegrityError:
        raise ValueError("User already exists")


def get_user_row(username: str):
    """Fetch user row from DB."""
    _cursor.execute("SELECT id, username, hashed_pw FROM users WHERE username = ?", (username,))
    return _cursor.fetchone()


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_ctx.verify(plain, hashed)


def authenticate_user(username: str, password: str) -> bool:
    row = get_user_row(username)
    if not row:
        return False
    return verify_password(password, row[2])


def create_access_token(subject: str) -> str:
    exp = int(time.time()) + ACCESS_EXPIRE
    token = jwt.encode({"sub": subject, "exp": exp}, SECRET, algorithm=ALGO)
    return token


# FastAPI dependencies
security = HTTPBearer()
security_optional = HTTPBearer(auto_error=False)

def get_current_user(creds: HTTPAuthorizationCredentials = Depends(security)):
    """Strict auth: raises 401 if invalid or missing."""
    token = creds.credentials
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGO])
        return payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


def get_current_user_optional(creds: HTTPAuthorizationCredentials = Depends(security_optional)):
    """Optional auth: returns None if missing/invalid token."""
    if creds is None:
        return None
    token = creds.credentials
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGO])
        return payload.get("sub")
    except JWTError:
        return None


def init_admin_user():
    """Create default admin if not present (for demo)."""
    try:
        create_user("admin", "admin123")
    except ValueError:
        pass
