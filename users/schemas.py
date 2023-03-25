from pydantic import BaseModel, EmailStr

#properties required during user creation
class UserCreate(BaseModel):
    username: str
    email : EmailStr
    password : str


class UserUpdate(BaseModel):
    username: str
    new_username: str

class PasswordUpdate(BaseModel):
    username: str
    new_password: str

class SuperUser(BaseModel):
    username: str


class ShowUser(BaseModel):
    id: int
    username : str 
    email : EmailStr
    api_key: str

    class Config():  #to convert non dict obj to json
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str