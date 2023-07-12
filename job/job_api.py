from sqlalchemy.orm import Session
import models, schemas
from accounts.api import get_current_user
from fastapi import APIRouter,Depends



def Jobtype_create(db: Session, jobtypeschema: schemas.Jobtype_Schema):
    db_user = models.job_type(name=jobtypeschema.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_jobtype(db: Session):
    return db.query(models.job_type).all()


def get_job(db: Session):
    return db.query(models.Job).all()

def get_job_current_user(db: Session, payload: str = Depends(get_current_user)):
    print("payload", payload)
    return db.query(models.Job).filter(models.Job.owner_id == payload.get("id")).all()

def Job_create(db: Session, jobschema: schemas.Job_Schema, payload: str = Depends(get_current_user)):
    print("payload $$$$$$$$$$$", payload)
    db_user = models.Job(name=jobschema.name, Job_description=jobschema.Job_description, owner_id=payload.get("id"), job_type_id=jobschema.job_type_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_jobtype_by_id(db: Session, id: int):
    return db.query(models.job_type).filter(models.job_type.id == id).first()


