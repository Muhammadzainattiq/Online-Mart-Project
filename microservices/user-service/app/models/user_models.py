from typing import List
from sqlmodel import Relationship, SQLModel, Field
from pydantic import EmailStr

#=======================================================================================================

class LoginModel(SQLModel):
    user_email:EmailStr
    user_password:str

#=======================================================================================================

class SignUpModel(LoginModel):
    user_name:str
    phone_number: int = Field()
    user_address:str = Field(max_length=70)
    # user_email:str
    # user_password:str

#=======================================================================================================
class UserModel(SignUpModel):
    pass
#=======================================================================================================

class User(UserModel, table = True):
    user_id : int | None = Field(default=None, primary_key=True)
    tokens: List["UserToken"] = Relationship(sa_relationship_kwargs={"cascade": "delete"}, back_populates="user")

#=======================================================================================================
class UserUpdate(SQLModel):
    user_name: str = None
    phone_number: int = None
    user_email: EmailStr = None
    user_password: str = None

#=======================================================================================================

class UserToken(SQLModel, table=True):
    token_id: int = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.user_id")
    refresh_token: str
    user: "User" = Relationship(back_populates="tokens")

#=======================================================================================================