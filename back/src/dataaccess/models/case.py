from dataaccess.models.base import Base
from sqlalchemy import Column, String, Integer, Text, Sequence, PrimaryKeyConstraint
from sqlalchemy.engine.result import Row

CASE_ID = Sequence('case_id_seq')

class Case(Base):
    __tablename__ = 'cases'

    def __init__(self, name, initiator_id, status, claim, initiator_role, description = ''):
        self.name = name
        self.initiator_id = initiator_id
        self.status = status
        self.claim = claim
        initiator_role = initiator_role
        self.description = description

    case_id     =   Column(Integer, CASE_ID, primary_key=True)
    name        =   Column(String)
    initiator_id = Column(Integer)
    status      =   Column(String)
    claim       =   Column(Integer)
    initiator_role = Column(String)
    description =   Column(Text)

    def to_json(self):
        return {
        'case_id':      self.case_id,
        'name':         self.name,
        'initiator_id': self.initiator_id,
        'status':       self.status,
        'claim':        self.claim,
        'initiator_role': self.initiator_role,
        'description':  self.description
    }

    def to_case(self, row: Row) -> object:
        return Case(
            case_id = row['case_id'],
            name = row['name'],
            initiator_id = row['initiator_id'],
            status = row['status'],
            claim = row['claim'],
            initiator_role = row['initiator_role'],
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
