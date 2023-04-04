from fastapi import FastAPI, HTTPException
from dataaccess.crud import db_funcs
from dataaccess.crud.utils import Constants, USER_PROFILES, USER_ROLES
from api.models.user import UserSchema, UserProfiles, get_user_role_str
from api.models.case import CaseSchema
from api.models.document import DocumentSchema

app = FastAPI()


@app.get('/')
async def index():
    return "test"

@app.get('/user/')
async def get_user_by_email(email: str):
    result = db_funcs.get_user_by_email(email)
    if result == None:
        raise HTTPException(status_code = 404, detail = Constants.no_user)
    
    return result.to_json()

@app.get('/cases/')
async def get_cases_list(profile: int):
    if profile == UserProfiles.figurant:
        raise HTTPException(status_code = 403, detail = Constants.wrong_profile)
    
    return db_funcs.get_all_cases()

@app.get('/cases/')
async def get_cases_by_user(profile: int, email: str):
    user = db_funcs.get_user_by_email(email)
    if user is None:
        raise HTTPException(status_code = 404, detail = Constants.no_user)

    return db_funcs.get_cases_by_user_id(user.user_id)

@app.post('/user/')
async def add_user(user: UserSchema, password: str):
    try:
        returned_user = db_funcs.add_user(user.to_dict())
        db_funcs.link_user_and_pswd(returned_user.user_id, password)
        return returned_user.to_json()
    except Exception as e:
        raise HTTPException(status_code = 401, detail = repr(e))

@app.post('/cases/')
async def add_case(profile: int, user_id: int, user_role: int, case: CaseSchema):
    if profile == UserProfiles.investor:
        raise HTTPException(status_code = 403, detail = Constants.wrong_profile)
    
    try:
        returned_case = db_funcs.add_case(case.to_dict())
        db_funcs.link_user_and_case(
            user_id,
            returned_case.case_id,
            get_user_role_str(user_role)
        )
        return returned_case.to_json()
    except Exception as e:
        raise HTTPException(status_code = 401, detail = repr(e))

@app.delete('/cases/')
async def delete_case(profile: int, user_id: int, case_id: int):
    if profile == UserProfiles.investor:
        raise HTTPException(status_code = 403, detail = Constants.wrong_profile)
    if db_funcs.user_owns_case(user_id, case_id) is False:
        raise HTTPException(status_code = 403, detail = Constants.wrong_profile)
    
    db_funcs.unlink_user_and_case(user_id, case_id)
    db_funcs.delete_case_by_id(case_id)

@app.post('/doc/')
async def add_document(profile: int, doc: DocumentSchema):
    if profile == UserProfiles.investor:
        raise HTTPException(status_code = 403, detail = Constants.wrong_profile)
    try:
        returned_doc = db_funcs.add_document(doc.to_dict())
        return returned_doc.to_json()
    except Exception as e:
        raise HTTPException(status_code = 401, detail = repr(e))
