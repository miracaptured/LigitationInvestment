from dataaccess.models.base import Base
from sqlalchemy import Column, String, Integer, Boolean, Date

class User(Base):
    __tablename__ = 'users'

    def __init__(self, user_id, profile, is_company, email, name, birthdate, city, phone, job):
        self.user_id = user_id
        self.profile = profile
        self.is_company = is_company
        self.email = email
        self.name = name
        self.birthdate = birthdate
        self.city = city
        self.phone = phone
        self.job = job

    user_id     =   Column(Integer, primary_key=True)
    profile     =   Column(Integer)
    is_company  =   Column(Boolean)
    email       =   Column(String)
    name        =   Column(String)
    birthdate   =   Column(Date)
    city        =   Column(String)
    phone       =   Column(String)
    job         =   Column(String)

