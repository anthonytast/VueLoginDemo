from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
from database.users_db_init import get_db_connection
from typing import Annotated

router = APIRouter(
    prefix = '/users',
    tags = ['users']
)

#These would be moved to .env in production
SECRET_KEY = "my-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")

class User(BaseModel):
    username: str
    first_name: str
    last_name: str
    phone_number: str
    password: str

class UserUpdate(BaseModel):
    first_name: str
    last_name: str
    phone_number: str

class Token(BaseModel):
    access_token: str
    token_type: str


# # #  HELPER FUNCTIONS  # # #

def get_user_by_username(username: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    if user != None:
        return dict(user)
    else:
        return None

def create_access_token(username: str, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    to_encode = {'sub': username}
    expire = datetime.utcnow() + (expires_delta)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            return None
        return get_user_by_username(username)
    except JWTError:
        return None

def authenticate_user(username: str, password: str):
    user = get_user_by_username(username)
    if not user: # user is None
        return False
    if not bcrypt_context.verify(password, user['password']):
        return False
    return user

def get_all_usernames():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT username FROM users")
    rows = cursor.fetchall()
    conn.close()

    # Extract usernames from rows
    usernames = [row["username"] for row in rows]
    return list(usernames)

def insert_user(user: User):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM users WHERE username = ?", (user.username,))
    if cursor.fetchone():
        conn.close()
        return False

    hashed_password = bcrypt_context.hash(user.password)

    cursor.execute('''
        INSERT INTO users (username, first_name, last_name, phone_number, password)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        user.username,
        user.first_name,
        user.last_name,
        user.phone_number,
        hashed_password
    ))

    conn.commit()
    conn.close()
    return True

def patch_user(username: str, updates: UserUpdate):
    conn = get_db_connection()
    cursor = conn.cursor()

    sql = '''
        UPDATE users
        SET first_name = ?,
            last_name = ?,
            phone_number = ?
        WHERE username = ?
    '''

    cursor.execute(sql, (
        updates.first_name,
        updates.last_name,
        updates.phone_number,
        username
    ))

    conn.commit()
    conn.close()

def delete_user(username: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM users WHERE username = ?", (username,))

    conn.commit()
    conn.close()

# # #  ENDPOINTS  # # #

@router.get("/")
def get_all_users(limit: int = 25):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM users LIMIT ?', (limit,))
    rows = cursor.fetchall()
    conn.close()

    # Convert rows to dicts
    users = [dict(row) for row in rows]
    return users


@router.post("/token", response_model=Token)
def jwt_from_login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(user['username'])
    return {"access_token": token, "token_type": "bearer"}


@router.get("/verify", response_model=User)
def verify_user(token: str = Depends(oauth2_scheme)):
    user = verify_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user


@router.post("/", response_model=User)
def create_user(new_user: User):
    if new_user.username not in get_all_usernames():
        new_user.password = bcrypt_context.hash(new_user.password)
        if insert_user(new_user):
            return new_user
    
    raise HTTPException(status_code=400, detail=f"Username '{new_user.username}' is taken")


@router.patch("/{username}", response_model=User)
def patch_user_by_username(username: str, updatedUser: UserUpdate, token: str = Depends(oauth2_scheme)) -> User:
    user = verify_token(token)
    if username in get_all_usernames() and username == user.get('username'):
        patch_user(username, updatedUser)
        return get_user_by_username(username)
    else:
        raise HTTPException(status_code=404, detail=f"User {updatedUser.username} not found")


@router.delete("/{username}", response_model=User)
def delete_user_by_username(username: str, token: str = Depends(oauth2_scheme)) -> User:
    user = verify_token(token)
    if (user != None) and (username == user['username']):
        delete_user(username)
        return user
    else:
        raise HTTPException(status_code=401, detail=f"Incorrect username and password")


