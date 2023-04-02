from pydantic import BaseModel, Field, EmailStr


class UserSchema(BaseModel):
    user_id:    int     =   Field(default=None)
    profile:    str     =   Field(...)
    is_company: bool    =   Field(...)
    email:      str     =   EmailStr(...)
    name:       str     =   Field(...)
    birthdate:  str     =   Field(...)
    city:       str     =   Field(...)
    phone:      str     =   Field(...)
    job:        str     =   Field(...)

    class Config:
        schema_extra = {
            "example": {
                "profile":  1,
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
            'profile': self.profile,
            'is_company': self.is_company,
            'email': self.email,
            'name': self.name,
            'birthdate': self.birthdate,
            'city': self.city,
            'phone': self.phone,
            'job': self.job
        }