from dataaccess.dbsession import session_scope
from dataaccess.models.user import User
from dataaccess.models.case import Case, to_case
from dataaccess.models.document import Document
import sqlalchemy as sa
from multipledispatch import dispatch


'''
USER TABLE
'''

def exists(email: str) -> bool:
    with session_scope() as session:
        return session.query(exists().where(User.email == email)).scalar()

def get_user_by_id(id: int) -> User:
    with session_scope() as session:
        result = session.query(User).where(User.user_id == id).first()
        session.expunge_all()
        return result

def get_user_by_email(email: str) -> User:
    with session_scope() as session:
        result = session.query(User).where(User.email == email).first()
        session.expunge_all()
        return result

@dispatch(User)
def add_user(user: User) -> None:
    with session_scope() as session:
        session.add(user)

@dispatch(int, bool, str, str, str, str, str, str)
def add_user(profile, is_company, email, namfe, birthdate, city, phone, job) -> None:
    with session_scope() as session:
        session.add(User(profile, is_company, email, name, birthdate, city, phone, job))

@dispatch(dict)
def add_user(user) -> None:
    with session_scope() as session:
        session.add(User(
            user['profile'],
            user['is_company'],
            user['email'],
            user['name'],
            user['birthdate'],
            user['city'],
            user['phone'],
            user['job'])
            )

def delete_user_by_id(id: int) -> None:
    with session_scope() as session:
        session.delete(session.query(User).where(User.user_id == id).first())

def delete_user_by_email(email: str) -> None:
    with session_scope() as session:
        session.delete(session.query(User).where(User.email == email).first())

'''
CASES TABLE
'''

def get_case_by_id(id: int) -> Case:
    with session_scope() as session:
        result = session.query(Case).where(Case.case_id == id).first()
        session.expunge_all()
        return result

@dispatch(Case)
def add_case(case: Case) -> None:
    with session_scope() as session:
        session.add(case)

@dispatch(dict)
def add_case(case: dict) -> None:
    with session_scope() as session:
        session.add(Case(case['name'], case['status'], case['claim'], case['description']))

def delete_case_by_id(id: int) -> None:
    with session_scope() as session:
        session.delete(session.query(Case).where(Case.case_id == id).first())


'''
DOCUMENTS TABLE
'''

def get_document_by_id(id: int) -> Document:
    with session_scope() as session:
        result = session.query(Document).where(Document.doc_id == id).first()
        session.expunge_all()
        return result

@dispatch(Document)
def add_document(doc: Document) -> None:
    with session_scope() as session:
        session.add(doc)

@dispatch(dict)
def add_document(doc: dict) -> None:
    with session_scope() as session:
        session.add(Document(doc['case_id'], doc['name'], doc['link']))

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
        result = session.query(Document).where(Document.case_id == id).all()
        session.expunge_all()
        return result
    
def get_cases_by_user_id(user_id: int) -> list[Case]:
    with session_scope() as session:
        return list(map(lambda r: to_case(r),
                        session.execute(sa.text(f'SELECT * FROM get_cases_by_user({user_id})')).mappings().all()))
