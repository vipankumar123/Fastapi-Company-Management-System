from sqlalchemy.orm import Session
import models, schemas
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from jose import jwt, JWTError
# import crud

JWT_SECRET = "vipan"
ALGORITHM = "HS256"
from datetime import datetime, timedelta

from passlib.context import CryptContext
from database import SessionLocal

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

from enum import Enum

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Role_name(str, Enum):
    admin = "admin"
    employee = "employee"
    employer = "employer"


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, user: schemas.UserCreate, role_name=Role_name):
    hash_pass = get_password_hash(user.hashed_password)
    # print("hash_pass", hash_pass)
    db_user = models.User(email=user.email, hashed_password=hash_pass, username=user.username, is_active=user.is_active, mobile_no=user.mobile_no, role=role_name)
    print("db_user", db_user)
    db.add(db_user)
    db.commit()
    # db.refresh(db_user)
    return db_user

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(user):
    try:
        claims = {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "role": user.role,
            "is_active": user.is_active,
            "password": user.hashed_password,
            "exp": datetime.utcnow() + timedelta(minutes=120),
        }
        return jwt.encode(claims=claims, key=JWT_SECRET, algorithm=ALGORITHM)
    except Exception as ex:
        print(str(ex))
        raise ex
    
def verify_token(token):
    try:
        payload = jwt.decode(token, key=JWT_SECRET)
        print("1----------")
        return payload
    except:
        print("2----------")
        raise Exception("Wrong token")
    


    
def get_current_user(db: Session = Depends(get_db),token: str = Depends(HTTPBearer())):
    try:
        payload = jwt.decode(token.credentials, JWT_SECRET, algorithms=[ALGORITHM])
        username = payload.get("username")
        if username is None:
            raise HTTPException(
                detail="Invalid authentication credentials",
            )
        token_data = {"username": username}
    except JWTError:
        raise HTTPException(
            detail="Invalid authentication credentials",
        )
    user = get_user_by_username(db, username=token_data["username"])
    print("user", user.username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return payload

def check_active(payloadd: str = Depends(get_current_user)):
    # print("data------------")
    print("payload----", payloadd)
    active = payloadd.get("is_active")
    if active != True:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Please activate your Account first",
            headers={"WWW-Authenticate": "Bearer"},
        )
    else:
        return active
