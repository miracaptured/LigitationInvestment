from pydantic import BaseModel, Field, EmailStr
from enum import Enum

class UserProfiles(Enum):
    investor = 1
    figurant = 2

class UserRoles(Enum):
    plaintiff = 1
    defendant = 2
    investor = 3

def get_user_role_str(role_id: int):
    val = UserRoles(role_id)
    if val == UserRoles.investor:
        return "инвестор"
    elif val == UserRoles.defendant:
        return "ответчик"
    elif val == UserRoles.plaintiff:
        return "истец"

class UserSchema(BaseModel):
    user_id:    int     =   Field(default=None)
    profile:    str     =   Field(...)
    is_company: bool    =   Field(...)
    email:      str     =   EmailStr(...)
    password:   str     =   Field(...)
    name:       str     =   Field(...)
    birthdate:  str     =   Field(...)
    city:       str     =   Field(...)
    phone:      str     =   Field(...)
    job:        str     =   Field(...)

    class Config:
        schema_extra = {
            "example": {
                "profile":  "инвестор",
                "is_company": False,
                "email": "test@email.com",
                "name": "testname",
                "birthdate": "2002-07-10",
                "city": "Москва",
                "phone": "testphone",
                "job": "testjob"
            }
        }
    
    def to_dict(self) -> dict:
        return {
            'profile': self.profile.lower(),
            'is_company': self.is_company,
            'email': self.email,
            'name': self.name,
            'birthdate': self.birthdate,
            'city': self.city,
            'phone': self.phone,
            'job': self.job
        }