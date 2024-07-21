from typing import List
from sqlmodel import Relationship, SQLModel, Field
from pydantic import EmailStr

#=======================================================================================================

class AdminLoginModel(SQLModel):
    admin_email:str
    admin_password:str

#=======================================================================================================

class AdminSignUpModel(AdminLoginModel):
    admin_name:str
    phone_number: int = Field()
    admin_address:str = Field(max_length=70)
    # admin_email:str
    # admin_password:str
    
#=======================================================================================================
class AdminModel(AdminSignUpModel):
    pass

#=======================================================================================================

class Admin(AdminSignUpModel, table = True):
    admin_id : int | None = Field(default=None, primary_key=True)
    tokens: List["AdminToken"] = Relationship(back_populates="admin")

#=======================================================================================================

class AdminToken(SQLModel, table=True):
    token_id: int = Field(default=None, primary_key=True)
    admin_id: int = Field(foreign_key="admin.admin_id")
    refresh_token: str
    admin: "Admin" = Relationship(back_populates="tokens")