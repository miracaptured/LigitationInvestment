from dataaccess.models.base import Base
from sqlalchemy import Column, String, Integer, Text
from sqlalchemy.engine.result import Row

class Case(Base):
    __tablename__ = 'cases'

    def __init__(self, case_id, name, status, claim, description = ''):
        self.case_id = case_id
        self.name = name
        self.status = status
        self.claim = claim
        self.description = description

    case_id     =   Column(Integer, primary_key=True)
    name        =   Column(String)
    status      =   Column(Integer)
    claim       =   Column(Integer)
    description =   Column(Text)


def to_case(row: Row) -> Case:
    return Case(
        case_id = row['case_id'],
        name = row['name'],
        status = row['status'],
        claim = row['claim'],
        description = row['description']
    )
