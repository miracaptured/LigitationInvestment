
from datetime import timedelta, datetime
from typing import Annotated, Union
from fastapi import FastAPI, HTTPException, status, Depends
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dataaccess.crud.utils import Constants
from api.models.user import UserSchema
from api.models.application import ApplicationSchema
from api.models.document import DocumentSchema
import api.task_processor as task_processor
from dataaccess.config import SSL_KEY

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

class Settings(BaseModel):
    authjwt_secret_key: str = SSL_KEY

@AuthJWT.load_config
def get_config():
    return Settings()

@app.post("/login")
async def login(creds: dict, Authorize: AuthJWT = Depends()):
    if task_processor.check_password(creds["email"], creds["password"]):
        access_token = Authorize.create_access_token(subject=creds["email"])
        return {
            "access_token": access_token,
            "user": task_processor.get_user_by_email(creds["email"])
        }
    else:
        raise HTTPException(401, "Not Authorized")

@app.get("/user")
async def user(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    user_email = Authorize.get_jwt_subject()
    return task_processor.get_user_by_email(user_email)

@app.post("/register")
async def register_user(user: UserSchema, Authorize: AuthJWT = Depends()):
    try:
        returned_user = task_processor.register_user(user.to_dict())
        access_token = Authorize.create_access_token(subject=user.email)
        return {
            "user": returned_user,
            "access_token": access_token
        }
    except Exception as e:
        raise HTTPException(403, e)

@app.post("/applications")
async def add_application(application: ApplicationSchema, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        return task_processor.add_application(application.to_dict())
    except:
        raise HTTPException(403)

@app.get("/applications")
async def get_application_list(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    user_email = Authorize.get_jwt_subject()
    user = task_processor.get_user_by_email(user_email)
    if user is None:
        raise HTTPException(404)
    return task_processor.get_applications_by_user(user.user_id)

@app.get("/cases/all")
async def get_all_cases(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    try:
        return task_processor.get_cases_list()
    except Exception as e:
        raise HTTPException(403, e)

@app.get("/cases")
async def get_cases_list(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        user_email = Authorize.get_jwt_subject()
        user = task_processor.get_user_by_email(user_email)
        return task_processor.get_cases_by_user(user.user_id)
    except:
        raise HTTPException(403)

@app.get("/cases/{case_id}/investment")
async def get_investment(case_id: int):
    try:
        return task_processor.get_investment_by_case(case_id)
    except:
        raise HTTPException(403)

@app.post("/invest")
async def invest(data: dict, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    user_email = Authorize.get_jwt_subject()
    user = task_processor.get_user_by_email(user_email)
    task_processor.link_investor(user.user_id, data['case_id'])
    #task_processor.invest(user_id=user.user_id, case_id=data['case_id'], money=data['money'])

@app.post("/doc")
async def add_document(doc: DocumentSchema, Authorize: AuthJWT = Depends()):
    try:
        task_processor.add_document(doc.to_dict())
    except:
        raise HTTPException(403)
    