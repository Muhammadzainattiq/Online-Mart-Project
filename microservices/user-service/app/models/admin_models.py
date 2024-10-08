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
    phone_number: str = Field(max_length=15)
    admin_address:str = Field(max_length=70)
    # admin_email:str
    # admin_password:str
    
#=======================================================================================================
class AdminModel(AdminSignUpModel):
    pass

#=======================================================================================================

class Admin(AdminSignUpModel, table = True):
    admin_id : int | None = Field(default=None, primary_key=True)

#=======================================================================================================