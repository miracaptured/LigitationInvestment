from dataaccess.dbsession import session_scope
from dataaccess.models.user import User
from dataaccess.models.case import Case
from dataaccess.models.document import Document
from dataaccess.models.application import Application
from dataaccess.crud.utils import Constants, USER_PROFILES
import sqlalchemy as sa
from sqlalchemy import exists
from multipledispatch import dispatch


'''
USER TABLE
'''

def check_user_profile(profile: str) -> bool:
    return profile.lower() in USER_PROFILES

def user_exists(email: str) -> bool:
    with session_scope() as session:
        return session.query(exists().where(User.email == email)).scalar()

def get_user_by_id(id: int) -> User:
    with session_scope() as session:
        result = session.query(User).where(User.user_id == id).first()
    return result

def get_user_by_email(email: str) -> User:
    with session_scope() as session:
        result = session.query(User).where(User.email == email).first()
    return result

@dispatch(User)
def add_user(user: User) -> User:
    if check_user_profile(user.profile) is False:
        raise Exception(Constants.wrong_profile)
    
    with session_scope() as session:
            session.add(user)
    return user

@dispatch(str, bool, str, str, str, str, str, str)
def add_user(profile, is_company, email, name, birthdate, city, phone, job) -> User:
    if check_user_profile(profile) is False:
        raise Exception(Constants.wrong_profile)
    with session_scope() as session:
            inserted_user = User(profile, is_company, email, name, birthdate, city, phone, job)
            session.add(inserted_user)
    return inserted_user
        

@dispatch(dict)
def add_user(user: dict) -> User:
    if check_user_profile(user['profile']) is False:
        raise Exception(Constants.wrong_profile)
    with session_scope() as session:
            inserted_user = User(
                user['profile'],
                user['is_company'],
                user['email'],
                user['name'],
                user['birthdate'],
                user['city'],
                user['phone'],
                user['job']
            )
            session.add(inserted_user)
    return inserted_user

def delete_user_by_id(id: int) -> None:
    with session_scope() as session:
        to_delete = session.query(User).where(User.user_id == id).first()

        if to_delete is None:
            raise Exception(Constants.no_user)
        
        session.delete(to_delete)

def delete_user_by_email(email: str) -> None:
    with session_scope() as session:
        to_delete = session.query(User).where(User.email == email).first()

        if to_delete is None:
            raise Exception(Constants.no_user)
        
        session.delete(to_delete)

'''
APPLICATIONS TABLE
'''
def get_application_by_id(id: int) -> Application:
    with session_scope() as session:
        result = session.query(Application).where(Application.application_id == id).first()
    return result

def add_application(application: dict) -> Application:
    with session_scope() as session:
        inserted_application = Application(
                application['name'],
                application['status'],
                application['claim'],
                application['description']
        )
        session.add(inserted_application)
    return inserted_application

def delete_application_by_id(id: int) -> None:
    with session_scope() as session:
        to_delete = session.query(Application).where(Application.application_id == id).first()

        if to_delete is None:
            raise Exception('No such case!')
        
        session.delete(to_delete)

'''
CASES TABLE
'''

def get_case_by_id(id: int) -> Case:
    with session_scope() as session:
        result = session.query(Case).where(Case.case_id == id).first()
    return result

def get_case_by_name(name: str) -> Case:
    with session_scope() as session:
        result = session.query(Case).where(Case.name == name).first()
    return result

@dispatch(Case)
def add_case(case: Case) -> Case:
    with session_scope() as session:
        session.add(case)
    return case

@dispatch(dict)
def add_case(case: dict) -> Case:
    with session_scope() as session:
        inserted_case = Case(
            case['name'],
            case['status'],
            case['claim'],
            case['description']
            )
        
        session.add(inserted_case)
    return inserted_case


def delete_case_by_id(id: int) -> None:
    with session_scope() as session:
        to_delete = session.query(Case).where(Case.case_id == id).first()

        if to_delete is None:
            raise Exception('No such case!')
        
        delete_documents_by_case_id(to_delete.case_id)
        session.delete(to_delete)

def delete_case_by_name(name: str) -> None:
    with session_scope() as session:
        to_delete = session.query(Case).where(Case.name == name).first()

        if to_delete is None:
            raise Exception('No such case!')
        
        delete_documents_by_case_id(to_delete.case_id)
        session.delete(to_delete)


'''
DOCUMENTS TABLE
'''

def get_document_by_id(id: int) -> Document:
    with session_scope() as session:
        result = session.query(Document).where(Document.doc_id == id).first()
    
    return result

@dispatch(Document)
def add_document(doc: Document) -> Document:
    with session_scope() as session:
        session.add(doc)

    return doc

@dispatch(dict)
def add_document(doc: dict) -> Document:
    with session_scope() as session:
        inserted_doc = Document(doc['case_id'], doc['name'], doc['link'])
        session.add(inserted_doc)

    return inserted_doc

def delete_documents_by_case_id(case_id: int) -> None:
    with session_scope() as session:
        session.query(Document).filter(Document.case_id == case_id).delete(synchronize_session=False)

def delete_document_by_id(id: int) -> None:
    with session_scope() as session:
        to_delete = session.query(Document).where(Document.doc_id == id).first()

        if to_delete is None:
            raise Exception(Constants.no_document)
        
        session.delete(to_delete)


'''
RELATIONS
'''

def link_user_and_pswd(user_id: int, pswd: str):
    with session_scope() as session:
        session.execute(sa.text(f"CALL link_user_pswd({user_id}, '{pswd}')"))

def invest(user_id: int, case_id: int, investment: int):
    with session_scope() as session:
        session.execute(sa.text(f"CALL link_user_and_case({user_id}, {case_id}, 'инвестор', {investment})"))

def link_user_and_case(user_id: int, case_id: int, user_role: str):
    with session_scope() as session:
        session.execute(sa.text(f"CALL link_user_and_case({user_id}, {case_id}, '{user_role}', 0)"))

def unlink_user_and_case(user_id: int, case_id: int):
    with session_scope() as session:
        session.execute(sa.text(f"CALL unlink_user_and_case({user_id}, {case_id})"))

def get_documents_by_case_id(id: int) -> list[Document]:
    with session_scope() as session:
        result = session.query(Document).where(Document.case_id == id).all()
        return result

def user_owns_case(user_id: int, case_id: int) -> bool:
    with session_scope() as session:
        return session.execute(sa.text(f'SELECT user_owns_case({user_id}, {case_id})')).scalar()

def get_cases_by_user_id(user_id: int) -> list[dict]:
    with session_scope() as session:
        return list(session.execute(sa.text(f'SELECT * FROM get_cases_by_user({user_id})')).mappings().all())

def get_all_cases() -> list[Case]:
    with session_scope() as session:
        result = session.query(Case).all()
        return result
