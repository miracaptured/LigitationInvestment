from dataaccess.models.base import Base
from sqlalchemy import Column, String, Integer, Text, Sequence
from sqlalchemy.engine.result import Row

CASE_ID = Sequence('case_id_seq')

class Case(Base):
    __tablename__ = 'cases'

    def __init__(self, name, status, claim, description = ''):
        self.name = name
        self.status = status
        self.claim = claim
        self.description = description

    case_id     =   Column(Integer, primary_key=True, default=CASE_ID.next_value())
    name        =   Column(String)
    status      =   Column(Integer)
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

def to_case(row: Row) -> Case:
    return Case(
        case_id = row['case_id'],
        name = row['name'],
        status = row['status'],
        claim = row['claim'],
        description = row['description']
    )
