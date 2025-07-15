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

    # def __init__(self, user: UserDB, public=False):
    #     self.username = user.username
    #     self.first_name = user.first_name
    #     if public:
    #         self.last_name = user.last_name
    #         self.phone_number = user.phone_number



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
    # raise HTTPException(status_code=404, detail=f"User {username} not found")

@router.post("/")
def create_user(username: str, first_name: str, last_name: str, phone_number: str, password: str):
    new_user = UserDB(
            username=username,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            password=password
        )
    users[username] =  new_user
    return {username: new_user}

@router.get("/{username}")
def get_user_info_by_username(username: str):
    user = users[username]
    if user != None:
        return User(**user.__dict__)
    else:
        raise HTTPException(status_code=404, detail=f"User {username} not found")

@router.patch("/{username}")
def patch_user_by_username(username: str, first_name: str, last_name: str, phone_number: str) -> User:
    user = users[username]
    if user != None:
        user.first_name = first_name
        user.last_name = last_name
        user.phone_number = phone_number
        return user
    else:
        raise HTTPException(status_code=404, detail=f"User {username} not found")

@router.patch("/{username}") # COULD MAKE THIS FUNCTION MORE EFFICIENT LATER (CONSIDER CASE WITH MORE USERS)
def update_username_password(username: str, password: str, new_password: str):
    user = users[username]
    if (user != None) and (user.password == password):
        user.password = new_password
    else:
        raise HTTPException(status_code=401, detail=f"Incorrect username and password")


@router.delete("/{username}")
def delete_user_by_username(username: str, password: str) -> User:
    user = users[username]
    if (user != None) and (user.password == password):
        del_user = users.pop(username)
        return del_user
    else:
        raise HTTPException(status_code=401, detail=f"Incorrect username and password")


