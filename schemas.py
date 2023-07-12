# from typing import List, Union
from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    is_active: bool
    email: str
    mobile_no: str
    hashed_password: str

    class Config:
        orm_mode = True


class Jobtype_Schema(BaseModel):
    name: str

    class Config:
        orm_mode = True

class Job_Schema(BaseModel):
    name: str
    Job_description: str
    job_type_id: int

    class Config:
        orm_mode = True

