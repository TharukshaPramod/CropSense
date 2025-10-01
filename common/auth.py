# common/auth.py
import sqlite3, os, time
from passlib.context import CryptContext
from jose import jwt, JWTError
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
SECRET = os.environ.get("CROPSENSE_JWT_SECRET", "dev-secret-change-me")
ALGO = "HS256"
ACCESS_EXPIRE = 60 * 60 * 4  # 4 hours

# Password hashing context
pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

# SQLite setup
DB_PATH = os.path.join("common", "auth.db")
os.makedirs("common", exist_ok=True)
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY, 
    username TEXT UNIQUE, 
    hashed_pw TEXT
)""")
conn.commit()

# User functions
def create_user(username: str, password: str):
    hashed = pwd_ctx.hash(password)
    try:
        c.execute("INSERT INTO users (username, hashed_pw) VALUES (?,?)", (username, hashed))
        conn.commit()
    except Exception as e:
        raise e

def get_user(username: str):
    c.execute("SELECT id, username, hashed_pw FROM users WHERE username = ?", (username,))
    return c.fetchone()

def verify_password(plain, hashed):
    return pwd_ctx.verify(plain, hashed)

def authenticate_user(username: str, password: str):
    row = get_user(username)
    if not row:
        return False
    if not verify_password(password, row[2]):
        return False
    return True

def create_access_token(subject: str):
    exp = int(time.time()) + ACCESS_EXPIRE
    token = jwt.encode({"sub": subject, "exp": exp}, SECRET, algorithm=ALGO)
    return token

# FastAPI dependency
security = HTTPBearer()

def get_current_user(creds: HTTPAuthorizationCredentials = Depends(security)):
    token = creds.credentials
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGO])
        return payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
