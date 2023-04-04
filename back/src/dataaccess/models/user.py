from dataaccess.models.base import Base
from sqlalchemy import Column, String, Integer, Boolean, Date, Sequence

USER_ID = Sequence('user_id_seq')

class User(Base):
    __tablename__ = 'users'

    def __init__(self, profile, is_company, email, name, birthdate, city, phone, job):
        self.profile = profile
        self.is_company = is_company
        self.email = email
        self.name = name
        self.birthdate = birthdate
        self.city = city
        self.phone = phone
        self.job = job
    
    def to_json(self) -> dict:
        return {
            'user_id': self.user_id,
            'profile': self.profile,
            'is_company': self.is_company,
            'email': self.email,
            'name': self.name,
            'birthdate': self.birthdate,
            'city': self.city,
            'phone': self.phone,
            'job': self.job
        }

    user_id     =   Column(Integer, USER_ID, primary_key=True)
    profile     =   Column(String)
    is_company  =   Column(Boolean)
    email       =   Column(String)
    name        =   Column(String)
    birthdate   =   Column(Date)
    city        =   Column(String)
    phone       =   Column(String)
    job         =   Column(String)

