from dataaccess.models.base import Base
from sqlalchemy import Column, String, Integer, Text, Sequence, PrimaryKeyConstraint
from sqlalchemy.engine.result import Row

APPLICATION_ID = Sequence('application_id_seq')

class Application(Base):
    __tablename__ = 'applications'

    def __init__(self, name, initiator_id, status, claim, initiator_role, description = ''):
        self.name = name
        self.initiator_id = initiator_id
        self.status = status
        self.claim = claim
        self.initiator_role = initiator_role
        self.description = description

    application_id     =   Column(Integer, APPLICATION_ID, primary_key=True)
    name               =   Column(String)
    initiator_id       =   Column(Integer)
    status             =   Column(String)
    claim              =   Column(Integer)
    initiator_role     =   Column(String)
    description        =   Column(Text)

    def to_json(self):
        return {
        'application_id':       self.application_id,
        'name':                 self.name,
        'initiator_id':         self.initiator_id,
        'status':               self.status,
        'claim':                self.claim,
        'initiator_role':       self.initiator_role,
        'description':          self.description
    }

    def to_application(self, row: Row) -> object:
        return Application(
            application_id = row['application_id'],
            name = row['name'],
            initiator_id = row['initiator_id'],
            status = row['status'],
            claim = row['claim'],
            initiator_role = row['initiator_role'],
            description = row['description']
        )


class UserApplicationRelation(Base):
    __tablename__ = 'applications_by_users'

    def __init__(self, user_id, application_id, user_role):
        self.user_id = user_id
        self.application_id = application_id
        self.user_role = user_role
    
    application_id = Column(Integer)
    user_id = Column(Integer)
    user_role = Column(String)

    __table_args__ = (
        PrimaryKeyConstraint(application_id, user_id),
        {},
    )

    def to_dict(self) -> dict:
        return {
            'user_id': self.user_id,
            'application_id': self.application_id,
            'user_role': self.user_role
        }
