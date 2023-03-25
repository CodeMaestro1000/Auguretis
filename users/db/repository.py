from sqlalchemy.orm import Session
import uuid
from schemas import UserCreate
from .models import Users
from core.hashing import Hasher

# repository design pattern - abstracts away db interaction from routes
def create_new_user(user: UserCreate, db: Session):
    key = uuid.uuid4().hex
    user = Users(username=user.username,
        email = user.email,
        hashed_password=Hasher.get_password_hash(user.password),
        is_superuser=False,
        api_key = key
        )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_all_users(db: Session):
    return db.query(Users).all()

def get_user_by_id(db: Session, user_id: int):
    return db.query(Users).filter(Users.id == user_id).first()

def get_user_by_email(db: Session, email:str):
    return db.query(Users).filter(Users.email == email).first()

def get_user_by_username(db: Session, username: str):
    return db.query(Users).filter(Users.username == username).first()

def get_user_by_api_key(db: Session, api_key: str):
    return db.query(Users).filter(Users.api_key == api_key).first()

def get_user(db: Session, username: str):
    # gets user by email or username
    user = get_user_by_username(db, username)
    if not user:
        user = get_user_by_email(db, username)
    return user

def update_username(db: Session, username: str, new_username: str):
    db_user = get_user_by_username(db, username)
    db_user.username = new_username
    db.commit()
    return db_user

def update_password(db: Session, username: str, new_password: str):
    db_user = get_user_by_username(db, username)
    db_user.hashed_password = Hasher.get_password_hash(new_password)
    db.commit()
    return db_user

def update_superuser(db: Session, username: str, value: bool = True): # pass value = false to deactivate superuser
    db_user = get_user_by_username(db, username)
    db_user.is_superuser = value
    db.commit()
    return db_user


def delete_user(db: Session, username: str):
    db_user = get_user_by_username(db, username)
    db.delete(db_user)
    db.commit()
    return db_user