from fastapi import APIRouter, Depends, HTTPException
from .job_api import *
import schemas
from database import SessionLocal
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from accounts.api import check_active, get_current_user
Job_router = APIRouter()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Job typecreate  API
@Job_router.post("/jobtype/uscreateer/",response_model=schemas.Jobtype_Schema, tags=["Job Type"])
def JobtypeCreate(jobtypeschema: schemas.Jobtype_Schema, db: Session = Depends(get_db)):
    data =  Jobtype_create(db=db, jobtypeschema=jobtypeschema)
    return data

# Job type get API
@Job_router.get("/get/jobtype/",tags=["Job Type"])
def Get_Jobtype(db: Session = Depends(get_db)):
    data = get_jobtype(db)
    return data


# Job typecreate  API
@Job_router.post("/job/create/",response_model=schemas.Job_Schema,dependencies=[Depends(check_active)], tags=["Job"])
def JobCreate(jobschema: schemas.Job_Schema, db: Session = Depends(get_db), payload: str = Depends(get_current_user)):
    jobtype = get_jobtype_by_id(db, jobschema.job_type_id)
    if not jobtype:
        raise HTTPException(status_code=400, detail="jobtype id does not exists!!")
    data =  Job_create(db=db, jobschema=jobschema, payload=payload)
    return data


# Job get API
@Job_router.get("/get/jobe/",tags=["Job"])
def Get_Job(db: Session = Depends(get_db)):
    data = get_job(db)
    return data


# Job get API
@Job_router.get("/get/current/user/jobs/",tags=["Job"])
def Get_Current_user_Jobs(db: Session = Depends(get_db), payload: str = Depends(get_current_user)):
    data = get_job_current_user(db, payload)
    return data








