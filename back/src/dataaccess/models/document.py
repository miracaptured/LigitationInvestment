from dataaccess.models.base import Base
from sqlalchemy import Column, String, Integer, Text, Sequence
from sqlalchemy.engine.result import Row

DOC_ID = Sequence('doc_id_seq')

class Document(Base):
    __tablename__ = 'documents'

    def __init__(self, case_id, name, link):
        self.case_id = case_id
        self.name = name
        self.link = link

    doc_id      =   Column(Integer, DOC_ID, primary_key=True)
    case_id     =   Column(Integer)
    name        =   Column(String)
    link        =   Column(Text)

    def to_json(self) -> dict:
        return {
            'doc_id': self.doc_id,
            'case_id': self.case_id,
            'name': self.name,
            'link': self.link
        }

def to_document(row: Row) -> Document:
    return Document(
        doc_id = row['doc_id'],
        case_id = row['case_id'],
        name = row['name'],
        link = row['link']
    )