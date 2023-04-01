from dataaccess.models.base import Base
from sqlalchemy import Column, String, Integer, Text
from sqlalchemy.engine.result import Row


class Document(Base):
    __tablename__ = 'documents'

    def __init__(self, doc_id, case_id, name, link):
        self.doc_id = doc_id
        self.case_id = case_id
        self.name = name
        self.link = link

    doc_id      =   Column(Integer, primary_key=True)
    case_id     =   Column(Integer)
    name        =   Column(String)
    link        =   Column(Text)

def to_document(row: Row) -> Document:
    return Document(
        doc_id = row['doc_id'],
        case_id = row['case_id'],
        name = row['name'],
        link = row['link']
    ) 