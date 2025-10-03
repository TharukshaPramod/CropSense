# common/auth.py - COMPLETE VERSION WITH ALL REQUIRED FUNCTIONS
import sqlite3
import os
import time
import bcrypt
import threading
from jose import jwt, JWTError
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import logging
from contextlib import contextmanager

# Set up logging
logger = logging.getLogger(__name__)

# Config
SECRET = os.environ.get("CROPSENSE_JWT_SECRET", "dev-secret-change-me")
ALGO = "HS256"
ACCESS_EXPIRE = int(os.environ.get("CROPSENSE_JWT_EXPIRE_SECONDS", 60 * 60 * 4))

# SQLite DB - Use container path
DB_DIR = "/app/common"
DB_PATH = os.path.join(DB_DIR, "auth.db")

# Ensure directory exists
os.makedirs(DB_DIR, exist_ok=True)
logger.info(f"Database path: {DB_PATH}")

# Thread-local storage for database connections
_thread_local = threading.local()

def get_db_connection():
    """Get a database connection for the current thread"""
    if not hasattr(_thread_local, "db_connection") or _thread_local.db_connection is None:
        _thread_local.db_connection = sqlite3.connect(DB_PATH, check_same_thread=False, timeout=30.0)
        # Enable WAL mode for better concurrency
        _thread_local.db_connection.execute("PRAGMA journal_mode=WAL")
        _thread_local.db_connection.execute("PRAGMA busy_timeout=5000")
    return _thread_local.db_connection

@contextmanager
def db_transaction():
    """Context manager for database transactions"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        yield cursor
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e

def init_db():
    """Initialize database tables"""
    with db_transaction() as cursor:
        # Don't drop tables if they exist - preserve existing data
        # cursor.execute("DROP TABLE IF EXISTS profiles")
        # cursor.execute("DROP TABLE IF EXISTS users")
        
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE,
                hashed_pw TEXT,
                role TEXT DEFAULT 'user'
            )"""
        )
        
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS profiles (
                user_id INTEGER PRIMARY KEY,
                full_name TEXT,
                organization TEXT,
                default_region TEXT,
                default_crop TEXT,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )"""
        )
    logger.info("Database tables created")

def create_user(username: str, password: str, role: str = "user"):
    """Create a new user"""
    if role not in ("user", "admin"):
        role = "user"
    
    if not username or not password:
        raise ValueError("Username and password are required")
    
    if len(username) < 3:
        raise ValueError("Username must be at least 3 characters")
    
    if len(password) < 6:
        raise ValueError("Password must be at least 6 characters")
    
    try:
        # Hash password
        password_bytes = password.encode('utf-8')
        if len(password_bytes) > 72:
            password_bytes = password_bytes[:72]
        hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode('utf-8')
        
        with db_transaction() as cursor:
            cursor.execute("INSERT INTO users (username, hashed_pw, role) VALUES (?,?,?)", 
                         (username, hashed, role))
        
        logger.info(f"User '{username}' created")
        return True
        
    except sqlite3.IntegrityError:
        raise ValueError("User already exists")
    except Exception as e:
        raise ValueError(f"Registration failed: {str(e)}")

def get_user_row(username: str):
    """Get user from database"""
    with db_transaction() as cursor:
        cursor.execute("SELECT id, username, hashed_pw, role FROM users WHERE username = ?", (username,))
        return cursor.fetchone()

def authenticate_user(username: str, password: str) -> bool:
    """Authenticate user"""
    row = get_user_row(username)
    if not row:
        return False
    
    try:
        password_bytes = password.encode('utf-8')
        if len(password_bytes) > 72:
            password_bytes = password_bytes[:72]
        hashed_bytes = row[2].encode('utf-8')
        return bcrypt.checkpw(password_bytes, hashed_bytes)
    except Exception:
        return False

def create_access_token(subject: str) -> str:
    """Create JWT token"""
    exp = int(time.time()) + ACCESS_EXPIRE
    row = get_user_row(subject)
    role = row[3] if row else "user"
    token = jwt.encode({"sub": subject, "role": role, "exp": exp}, SECRET, algorithm=ALGO)
    return token

# FastAPI dependencies
security = HTTPBearer()
security_optional = HTTPBearer(auto_error=False)

def get_current_user(creds: HTTPAuthorizationCredentials = Depends(security)):
    """Get current user from token"""
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
    """Create admin user"""
    try:
        create_user("admin", "admin123", "admin")
        logger.info("Admin user created")
    except ValueError:
        logger.info("Admin user already exists")

# Profile functions - ADDED BACK
def upsert_profile(username: str, full_name: str | None = None, organization: str | None = None, 
                  default_region: str | None = None, default_crop: str | None = None):
    """Create or update user profile"""
    row = get_user_row(username)
    if not row:
        raise ValueError("User not found")
    
    user_id = row[0]
    
    with db_transaction() as cursor:
        cursor.execute("SELECT user_id FROM profiles WHERE user_id = ?", (user_id,))
        exists = cursor.fetchone() is not None
        
        if exists:
            cursor.execute(
                "UPDATE profiles SET full_name=?, organization=?, default_region=?, default_crop=? WHERE user_id=?",
                (full_name, organization, default_region, default_crop, user_id),
            )
        else:
            cursor.execute(
                "INSERT INTO profiles (user_id, full_name, organization, default_region, default_crop) VALUES (?,?,?,?,?)",
                (user_id, full_name, organization, default_region, default_crop),
            )
    
    logger.info(f"Profile updated for user '{username}'")

def get_profile(username: str):
    """Get user profile"""
    row = get_user_row(username)
    if not row:
        return None
    
    user_id = row[0]
    
    with db_transaction() as cursor:
        cursor.execute("SELECT user_id, full_name, organization, default_region, default_crop FROM profiles WHERE user_id = ?", (user_id,))
        p = cursor.fetchone()
        
        if not p:
            return None
        
        return {
            "user_id": p[0],
            "full_name": p[1],
            "organization": p[2],
            "default_region": p[3],
            "default_crop": p[4],
        }

# Test function
def test_auth():
    """Test authentication"""
    print("=== Testing Auth ===")
    
    test_cases = [
        ("tharu123", "Normal password"),
        ("a" * 100, "Long password"),
        ("test@123", "Special chars"),
    ]
    
    for pwd, desc in test_cases:
        try:
            # Test hashing
            pwd_bytes = pwd.encode('utf-8')
            if len(pwd_bytes) > 72:
                pwd_bytes = pwd_bytes[:72]
            hashed = bcrypt.hashpw(pwd_bytes, bcrypt.gensalt())
            verified = bcrypt.checkpw(pwd_bytes, hashed)
            print(f"✓ {desc}: Verified: {verified}")
        except Exception as e:
            print(f"✗ {desc}: Error: {e}")

# Initialize database and admin
try:
    init_db()
    init_admin_user()
except Exception as e:
    logger.error(f"Initialization failed: {e}")