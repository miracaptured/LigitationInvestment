from dataaccess.crud import db_funcs
from dataaccess.crud.utils import Constants

def register_user(user: dict):
    if (db_funcs.user_exists(user["email"])):
        raise Exception(Constants.email_exists)
    
    returned_user = db_funcs.add_user(user)
    db_funcs.link_user_and_pswd(returned_user.user_id, user['password'])
    return returned_user.to_json()

def get_cases_list():
    return list(map(lambda case: {
            "case_id": case.case_id, 
            "name": case.name,
            "claim": case.claim,
            "status": case.status,
            "description": case.description,
            "investment": get_investment_by_case(case.case_id),
            "initiator_role": case.initiator_role
            },
            db_funcs.get_all_cases()))

def get_cases_by_user(user_id: int):
    return list(map(lambda case: {
        "case_id": case.case_id, 
        "name": case.name,
        "claim": case.claim,
        "status": case.status,
        "description": case.description,
        "investment": get_investment_by_case(case.case_id),
        "initiator_role": case.user_role
    },
    db_funcs.get_cases_by_user_id(user_id)))

def get_user_by_id(id: int):
    return db_funcs.get_user_by_id(id)

def get_user_by_email(email: str):
    return db_funcs.get_user_by_email(email)

def get_case_by_id(id: int):
    return db_funcs.get_case_by_id(id)

def get_document_by_id(id: int):
    return db_funcs.get_document_by_id(id)

def get_all_documents(case_id: int):
    return db_funcs.get_documents_by_case_id(case_id)

def add_application(application: dict):
    returned_application = db_funcs.add_application(application)
    return returned_application.to_json()

def get_applications_by_user(user_id: int):
    return db_funcs.get_applications_by_user(user_id)

def get_application_by_id(id: int):
    return db_funcs.get_application_by_id(id)

def invest(user_id: int, case_id: int, money: int):
    db_funcs.invest(user_id, case_id, money)

def delete_user(id: int):
    returned_user = db_funcs.get_user_by_id(id)
    db_funcs.delete_user_by_id(id)
    return returned_user.to_json()

def delete_application(id: int):
    returned_application = db_funcs.get_application_by_id(id)
    db_funcs.delete_application_by_id(id)
    return returned_application.to_json()

def delete_case(user_id: int, case_id: int):
    if db_funcs.user_owns_case(user_id, case_id) is False:
        raise Exception(status_code = 403, detail = Constants.wrong_profile)
    
    db_funcs.unlink_user_and_case(user_id, case_id)
    db_funcs.delete_case_by_id(case_id)

def add_document(doc: dict):
    returned_doc = db_funcs.add_document(doc)
    return returned_doc.to_json()

def delete_document(id: int):
    returned_doc = db_funcs.get_document_by_id(id)
    db_funcs.delete_document_by_id(id)
    return returned_doc

def check_password(email: str, pswd: str):
    return db_funcs.check_password(email, pswd)

def get_investment_by_case(case_id: int):
    investment = db_funcs.get_investment_by_case(case_id)
    if investment is None:
        return 0
    return investment

def link_investor(user_id: int, case_id: int):
    db_funcs.link_user_and_case(user_id, case_id, 'инвестор')