from fastapi import FastAPI, HTTPException
from dataaccess.crud import db_funcs
from dataaccess.models.user import User
from api.models.user import UserSchema
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
        raise HTTPException(status_code = 404, detail = "User not found")
    
    return result.to_json()

@app.get('/cases/')
async def get_cases_by_user(email: str):
    user = db_funcs.get_user_by_email(email)
    if user is None:
        raise HTTPException(status_code = 404, detail = "User not found")

    return db_funcs.get_cases_by_user_id(user.user_id)

@app.post('/user/')
async def add_user(user: UserSchema):
    try:
        db_funcs.add_user(user.to_dict())        
        return user.to_dict()
    except Exception as e:
        raise HTTPException(status_code = 401, detail = repr(e))

@app.post('/case/')
async def add_case(case: CaseSchema):
    try:
        db_funcs.add_case(case.to_dict())
        return case.to_dict()
    except Exception as e:
        raise HTTPException(status_code = 401, detail = repr(e))

@app.post('/doc/')
async def add_document(doc: DocumentSchema):
    try:
        db_funcs.add_document(doc.to_dict())
        return doc.to_dict()
    except Exception as e:
        raise HTTPException(status_code = 401, detail = repr(e))
