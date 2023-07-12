from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    username = Column(String, unique=True)
    mobile_no = Column(String, default="9988776655")
    role = Column(String)
    job = relationship("Job", back_populates="owner")
    
class job_type(Base):
    __tablename__ = "jobtype"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String,index=True)
    job = relationship("Job", back_populates="jobtype")

class Job(Base):
    __tablename__ = "Job"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    Job_description = Column(String, index=True)

    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="job")

    job_type_id = Column(Integer, ForeignKey("jobtype.id"))
    jobtype = relationship("job_type", back_populates="job")

