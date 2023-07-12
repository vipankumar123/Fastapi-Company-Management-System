from fastapi import FastAPI
import models
from database import SessionLocal, engine
from accounts import auth
from job import job_router

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(auth.auth_router)
app.include_router(job_router.Job_router)

@app.get("/hello")
def hello_world():
    return ("hello, welcome back.")




