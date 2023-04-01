from dataaccess.dbsession import session_scope
from dataaccess.models.user import User
from dataaccess.models.case import Case, to_case
from dataaccess.models.document import Document
import sqlalchemy as sa

'''
USER TABLE
'''

def get_user_by_id(id: int) -> User:
    with session_scope() as session:
        return session.query(User).where(User.user_id == id).first()

def add_user(user: User) -> None:
    with session_scope() as session:
        session.add(user)

def delete_user_by_id(id: int) -> None:
    with session_scope() as session:
        session.delete(session.query(User).where(User.user_id == id).first())

'''
CASES TABLE
'''

def get_case_by_id(id: int) -> Case:
    with session_scope() as session:
        return session.query(Case).where(Case.case_id == id).first()

def add_case(case: Case) -> None:
    with session_scope() as session:
        session.add(case)

def delete_case_by_id(id: int) -> None:
    with session_scope() as session:
        session.delete(session.query(Case).where(Case.case_id == id).first())


'''
DOCUMENTS TABLE
'''

def get_document_by_id(id: int) -> Document:
    with session_scope() as session:
        return session.query(Document).where(Document.doc_id == id).first()

def add_document(doc: Document) -> None:
    with session_scope() as session:
        session.add(doc)

def delete_document_by_id(id: int) -> None:
    with session_scope() as session:
        session.delete(session.query(Document).where(Document.doc_id == id).first())


'''
RELATIONS
'''

def link_user_and_case(user_id: int, case_id: int):
    with session_scope() as session:
        session.execute(sa.text(f'CALL link_user_and_case({user_id}, {case_id})'))

def unlink_user_and_case(user_id: int, case_id: int):
    with session_scope() as session:
        session.execute(sa.text(f'CALL unlink_user_and_case({user_id}, {case_id})'))

def get_documents_by_case_id(id: int) -> list[Document]:
    with session_scope() as session:
        return session.query(Document).where(Document.case_id == id).all()
    
def get_cases_by_user_id(user_id: int) -> list[Case]:
    with session_scope() as session:
        return list(map(lambda r: to_case(r),
                        session.execute(sa.text(f'SELECT * FROM get_cases_by_user({user_id})')).mappings().all()))
    
def get_documents_by_case_id(case_id: int) -> list[Document]:
    with session_scope() as session:
        return session.query(Document).where(Document.case_id == case_id).all()
