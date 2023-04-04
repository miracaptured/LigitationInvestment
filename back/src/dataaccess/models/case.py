from dataaccess.models.base import Base
from sqlalchemy import Column, String, Integer, Text, Sequence, PrimaryKeyConstraint
from sqlalchemy.engine.result import Row

CASE_ID = Sequence('case_id_seq')

class Case(Base):
    __tablename__ = 'cases'

    def __init__(self, name, status, claim, description = ''):
        self.name = name
        self.status = status
        self.claim = claim
        self.description = description

    case_id     =   Column(Integer, CASE_ID, primary_key=True)
    name        =   Column(String)
    status      =   Column(String)
    claim       =   Column(Integer)
    description =   Column(Text)

    def to_json(self):
        return {
        'case_id':      self.case_id,
        'name':         self.name,
        'status':       self.status,
        'claim':        self.claim,
        'description':  self.description
    }

    def to_case(self, row: Row) -> object:
        return Case(
            case_id = row['case_id'],
            name = row['name'],
            status = row['status'],
            claim = row['claim'],
            description = row['description']
        )


class UserCaseRelation(Base):
    __tablename__ = 'cases_by_users'

    def __init__(self, user_id, case_id, user_role):
        self.user_id = user_id
        self.case_id = case_id
        self.user_role = user_role
    
    case_id = Column(Integer)
    user_id = Column(Integer)
    user_role = Column(String)

    __table_args__ = (
        PrimaryKeyConstraint(case_id, user_id),
        {},
    )

    def to_dict(self) -> dict:
        return {
            'user_id': self.user_id,
            'case_id': self.case_id,
            'user_role': self.user_role
        }
