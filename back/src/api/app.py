from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dataaccess.crud import db_funcs
from dataaccess.crud.utils import Constants, USER_PROFILES, USER_ROLES
from api.models.user import UserSchema, UserProfiles, get_user_role_str
from api.models.case import CaseSchema
from api.models.application import ApplicationSchema
from api.models.document import DocumentSchema

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
async def index():
    return "test"

@app.post('/user/')
async def register_user(user: UserSchema):
    try:
        returned_user = db_funcs.add_user(user.to_dict())
        db_funcs.link_user_and_pswd(returned_user.user_id, user.password)
        return returned_user.to_json()
    except Exception as e:
        print(repr(e))
        raise HTTPException(status_code = 401, detail = repr(e))
    
@app.get('/cases/all/')
async def get_cases_list():
    return db_funcs.get_all_cases()

@app.get('/cases/')
async def get_cases_by_user(id: int):
    return db_funcs.get_cases_by_user_id(id)

@app.get('/userid/')
async def get_user_by_id(id: int):
    result = db_funcs.get_user_by_id(id)
    if result == None:
        raise HTTPException(status_code=404, detail=Constants.no_user)
    
    return result.to_json()

@app.get('/user/')
async def get_user_by_email(email: str):
    result = db_funcs.get_user_by_email(email)
    if result == None:
        raise HTTPException(status_code=404, detail=Constants.no_user)
    
    return result.to_json()

@app.get('/cases/')
async def get_user_by_id(id: int):
    result = db_funcs.get_case_by_id(id)
    if result == None:
        raise HTTPException(status_code=404, detail=Constants.no_case)
    
    return result.to_json()

@app.get('/documents/')
async def get_document_by_id(id: int):
    result = db_funcs.get_document_by_id(id)
    if result == None:
        raise HTTPException(status_code=404, detail=Constants.no_document)
    
    return result.to_json()

@app.get('/documents/all')
async def get_all_documents(case_id: int):
    result = db_funcs.get_documents_by_case_id(case_id)

    return result

@app.post('/application/')
async def add_application(application: ApplicationSchema):
    try:
        returned_application = db_funcs.add_application(application.to_dict())
        return returned_application.to_json()
    except Exception as e:
        print(repr(e))
        raise HTTPException(status_code = 401, detail = repr(e))

@app.get('/application/')
async def get_application_by_id(id: int):
    result = db_funcs.get_application_by_id(id)
    if result == None:
        raise HTTPException(status_code=404)
    
    return result.to_json()

@app.post('/invest/')
async def invest(user_id: int, case_id: int, money: int):
    db_funcs.invest(user_id, case_id, money)

@app.delete('/user/')
async def delete_user(id: int):
    try:
        returned_user = db_funcs.get_user_by_id(id)
        db_funcs.delete_user_by_id(id)
        return returned_user.to_json()
    except Exception as e:
        print(repr(e))
        raise HTTPException(status_code = 401, detail = repr(e))
    
@app.delete('/application/')
async def delete_application_by_id(id: int):
    try:
        returned_application = db_funcs.get_application_by_id(id)
        db_funcs.delete_application_by_id(id)
        return returned_application.to_json()
    except Exception as e:
        print(repr(e))
        raise HTTPException(status_code = 401, detail = repr(e))

@app.delete('/cases/')
async def delete_case(user_id: int, case_id: int):
    if db_funcs.user_owns_case(user_id, case_id) is False:
        raise HTTPException(status_code = 403, detail = Constants.wrong_profile)
    
    db_funcs.unlink_user_and_case(user_id, case_id)
    db_funcs.delete_case_by_id(case_id)

@app.post('/doc/')
async def add_document(doc: DocumentSchema):
    try:
        returned_doc = db_funcs.add_document(doc.to_dict())
        return returned_doc.to_json()
    except Exception as e:
        raise HTTPException(status_code = 401, detail = repr(e))

@app.delete('/doc/')
async def delete_document(id: int):
    try:
        returned_doc = db_funcs.get_document_by_id(id)
        db_funcs.delete_document_by_id(id)
        return returned_doc
    except Exception as e:
        print(repr(e))
        raise HTTPException(status_code = 401, detail = repr(e))
