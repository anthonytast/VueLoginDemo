from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from jose import jwt, JWTError
from database.user_storage import users, UserDB

router = APIRouter(
    prefix = '/users',
    tags = ['users']
)

SECRET_KEY = "my-secret-jwt-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")

# can add password hashing later

class User(BaseModel):
    username: str
    first_name: str
    last_name: str
    phone_number: str

class UserCreate(BaseModel):
    username: str
    first_name: str
    last_name: str
    phone_number: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None or username not in users:
            return None
        return users[username]
    except JWTError:
        return None


@router.get("/")
def get_all_users(limit: int = 25): # Using the BaseModel class so password doesn't show
    filtered_users = [
        {
            "username": user.username,
            "first_name": user.first_name
        }
        for _, user in list(users.items())[:limit]
    ]
    return filtered_users


@router.post("/login")
def is_user_login_successful(username: str, password: str):
    user = users[username]
    if (user != None) and (password == user.password):
        return {"login": True}
    else:
        return {"login": False}


@router.post("/token", response_model=Token)
def jwt_token_from_successful_login(username: str, password: str):
    user = users.get(username)
    if not user or user.password != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": username})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/verify", response_model=User)
def verify_user(token: str = Depends(oauth2_scheme)):
    user = verify_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return User(**user.__dict__)


@router.post("/")
def create_user(user: UserCreate):
    if user.username not in users:
        new_user = UserDB(
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
                phone_number=user.phone_number,
                password=user.password
            )
        users[user.username] = new_user
        return {user.username: new_user}
    else:
        raise HTTPException(status_code=400, detail=f"Username {user.username} is taken")


@router.patch("/{username}", response_model=User)
def patch_user_by_username(updatedUser: User) -> User:
    user = users[updatedUser.username]
    if user != None:
        user.first_name = updatedUser.first_name
        user.last_name = updatedUser.last_name
        user.phone_number = updatedUser.phone_number
        return user
    else:
        raise HTTPException(status_code=404, detail=f"User {updatedUser.username} not found")


@router.delete("/{username}", response_model=User)
def delete_user_by_username(username: str) -> User:
    user = users[username]
    if (user != None):# and (user.password == password):
        del_user = users.pop(username)
        return del_user
    else:
        raise HTTPException(status_code=401, detail=f"Incorrect username and password")


