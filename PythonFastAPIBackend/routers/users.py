from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from database.user_storage import users, UserDB

router = APIRouter(
    prefix = '/users',
    tags = ['users']
)

class User(BaseModel):
    username: str
    first_name: str
    last_name: str
    phone_number: str

'''
For testing purposes, will keep users as list and keep the get all funciton.
For deployment, it would make more sense to have a dict for storing users and 
not allow a get all users endpoint (for security reasons)
'''
@router.get("/")
def get_all_users(limit: int = 25) -> list[User]: # Using the BaseModel class so password doesn't show
    return users[0:limit]

# COULD MAKE THIS FUNCTION MORE EFFICIENT LATER (CONSIDER CASE WITH MORE USERS)
# Could enhance this later for security
@router.get("/login")
def is_user_login_successful(username: str, password: str):
    for user in users:
        if user.username == username:
            if user.password == password:
                return {"login": True}
            return {"login": False}
    raise HTTPException(status_code=404, detail=f"User {username} not found")

@router.post("/")
def create_user(username: str, first_name: str, last_name: str, phone_number: str, password: str):
    new_user = UserDB(
            username=username,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            password=password
        )
    users.append(new_user)
    return new_user

@router.get("/{username}")
def get_user_by_username(username: str) -> User:
    for user in users:
        if user.username == username:
            return user
    raise HTTPException(status_code=404, detail=f"User {username} not found")

@router.patch("/{username}")
def patch_user_by_username(username: str, first_name: str, last_name: str, phone_number: str) -> User:
    for user in users:
        if user.username == username:
            user.first_name = first_name
            user.last_name = last_name
            user.phone_number = phone_number
            return user
    raise HTTPException(status_code=404, detail=f"User {username} not found")

@router.patch("/{username}") # COULD MAKE THIS FUNCTION MORE EFFICIENT LATER (CONSIDER CASE WITH MORE USERS)
def update_username_password(username: str, password: str, new_password: str):
    for user in users:
        if user.username == username:
            if user.password == password:
                user.password = new_password
            break
    raise HTTPException(status_code=401, detail=f"Incorrect username and password")


@router.delete("/{username}")
def delete_user_by_username(username: str, password: str) -> User:
    for user in users:
        if user.username == username:
            if user.password == password:
                users.remove(user)
            break
    raise HTTPException(status_code=401, detail=f"Incorrect username and password")


