from fastapi import APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from fastapi import Depends
from typing import List
from schemas import UserCreate, ShowUser, UserUpdate, PasswordUpdate, SuperUser
from db.models import Users
from db.session import get_db
from db.repository import (
    create_new_user, get_all_users, get_user_by_id, get_user_by_email, 
    update_username, get_user_by_username, get_user_by_api_key, delete_user, update_password,
    update_superuser
)
from routes.login import get_current_user_from_token

user_router = APIRouter()

@user_router.post("/new/", response_model = ShowUser)
def create_user(user : UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with email already exists")
    
    db_user = get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with username already exists")
    return create_new_user(user=user,db=db)

######### For admin purposes only #########################
@user_router.post("/new-superuser", response_model = ShowUser)
def create_user(user : UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with email already exists")
    
    db_user = get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with username already exists")
    create_new_user(user=user,db=db)
    return update_superuser(db, user.username)

@user_router.patch("/add-superuser/", response_model= ShowUser)
def add_super_user(user: SuperUser, db: Session = Depends(get_db), current_user: Users = Depends(get_current_user_from_token)):
    if not current_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not permitted to access this endpoint")
    
    db_user = get_user_by_username(db, user.username)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User does not exist")
    return update_superuser(db, user.username)

@user_router.patch("/remove-superuser/", response_model= ShowUser)
def remove_super_user(user: SuperUser, db: Session = Depends(get_db), current_user: Users = Depends(get_current_user_from_token)):
    if not current_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not permitted to access this endpoint")

    db_user = get_user_by_username(db, user.username)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User does not exist")
    return update_superuser(db, user.username, False)


@user_router.get("/all/", response_model= List[ShowUser])
def get_users(db: Session = Depends(get_db), current_user: Users = Depends(get_current_user_from_token)):
    if not current_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not permitted to access this endpoint")
    
    return get_all_users(db)

@user_router.get("/{user_id}/", response_model = ShowUser)
def get_user(user_id: int, db: Session = Depends(get_db), current_user: Users = Depends(get_current_user_from_token)):
    if  current_user.id != user_id and current_user.is_superuser != True:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not permitted to access this endpoint")
    
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User does not exist")
    return user

@user_router.get("", response_model = ShowUser)
def get_user_key(api_key: str, db: Session = Depends(get_db)):
    user = get_user_by_api_key(db, api_key=api_key)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with API key does not exist")
    return user

@user_router.post("/user-update/", response_model = ShowUser)
def update_details(user: UserUpdate,  db: Session = Depends(get_db), current_user: Users = Depends(get_current_user_from_token)):
    if current_user.username != user.username and current_user.is_superuser != True:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not permitted to access this endpoint")
    
    db_user = get_user_by_username(db, user.username)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User does not exist")
    return update_username(db, user.username, user.new_username)

###### Fix this to require existing and new password ##################
@user_router.post("/password-update/", response_model = ShowUser)
def update_details(user: PasswordUpdate,  db: Session = Depends(get_db), current_user: Users = Depends(get_current_user_from_token)):
    if current_user.username != user.username and current_user.is_superuser != True:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not permitted to access this endpoint")
    
    db_user = get_user_by_username(db, user.username)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User does not exist")
    return update_password(db, user.username, user.new_password)

@user_router.post("/delete/{username}", response_model = ShowUser)
def remove_user(username: str, db: Session = Depends(get_db), current_user: Users = Depends(get_current_user_from_token)):
    if current_user.username != username and current_user.is_superuser != True:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not permitted to access this endpoint")
    
    db_user = get_user_by_username(db, username)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User does not exist")
    return delete_user(db, username)

################ The two routes below are used to verify that the username and email doesn't already exist
@user_router.get("/user-exists/{username}/") # for verifying username exists
def verify_username_exists(username: str, db: Session = Depends(get_db)):
    user = get_user_by_username(db, username)
    if user: 
        return {"exists": "True"}
    return {"exists": "False"}

@user_router.get("/email-exists/{email}/") # for verifying email exists
def verify_email_exists(email: str, db: Session = Depends(get_db)):
    user = get_user_by_email(db, email)
    if user: 
        return {"exists": "True"}
    return {"exists": "False"}