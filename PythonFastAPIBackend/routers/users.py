from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
from database.user_storage import users
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

'''
Can add get database here
'''

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


### HELPER FUNCTIONS

def create_access_token(username: str, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    to_encode = {'sub': username}
    expire = datetime.utcnow() + (expires_delta)
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

def authenticate_user(username: str, password: str):
    user = users.get(username)
    if not user: # user is None
        return False
    if not bcrypt_context.verify(password, user.password):
        return False
    return user


### ENDPOINTS

@router.get("/")
def get_all_users(limit: int = 25):
    return list(users.values())[:limit]


@router.post("/token", response_model=Token)
def jwt_from_login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(user.username)
    return {"access_token": token, "token_type": "bearer"}


@router.get("/verify", response_model=User)
def verify_user(token: str = Depends(oauth2_scheme)):
    user = verify_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user


@router.post("/")
def create_user(new_user: User):
    if new_user.username not in users:
        new_user.password = bcrypt_context.hash(new_user.password)
        users[new_user.username] = new_user
        return new_user
    else:
        raise HTTPException(status_code=400, detail=f"Username {new_user.username} is taken")


@router.patch("/{username}", response_model=User)
def patch_user_by_username(updatedUser: UserUpdate, token: str = Depends(oauth2_scheme)) -> User:
    user = verify_token(token)
    if user != None:
        user.first_name = updatedUser.first_name
        user.last_name = updatedUser.last_name
        user.phone_number = updatedUser.phone_number
        return user
    else:
        raise HTTPException(status_code=404, detail=f"User {updatedUser.username} not found")


@router.delete("/{username}", response_model=User)
def delete_user_by_username(username: str, token: str = Depends(oauth2_scheme)) -> User:
    user = verify_token(token)
    if (user != None) and (user == users[username]):
        del_user = users.pop(username)
        return del_user
    else:
        raise HTTPException(status_code=401, detail=f"Incorrect username and password")


