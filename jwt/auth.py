from datetime import datetime, timedelta
from typing import Annotated
from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import BaseModel, ValidationError
from starlette import status
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from models import User
from database import SessionLocal
from sqlalchemy.orm import Session

def get_db():
    db = SessionLocal()
    try:
        yield db # give the db session to request
    finally:
        db.close() # after request completed, control comes here and closes session

db_dependency = Annotated[Session, Depends(get_db)]

auth_router = APIRouter(prefix="/auth", tags=["Auth"])

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 20
REFRESH_TOKEN_EXPIRE_MINUTES = 120

oaut2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token") # localhost:8000/token
bcrypt_context = CryptContext(schemes=["bcrypt"])

refresh_tokens = []

class UserBase(BaseModel):
    username: str
    email: str
    role: str

class CreateUserRequest(UserBase):
    password: str

class UserDetail(UserBase):
    disabled: bool

class Token(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str

@auth_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    create_user_model = User(
        username=create_user_request.username,
        email=create_user_request.email,
        role=create_user_request.role,
        hashed_password=bcrypt_context.hash(create_user_request.password),
    )
    db.add(create_user_model)
    db.commit()

@auth_router.post("/token", response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    db_user = authenticate_user(form_data.username, form_data.password, db)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="incorrect username or password")
    access_token = create_access_token(db_user.username, db_user.id, db_user.role, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh_token = create_access_token(db_user.username, db_user.id, db_user.role, timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES))
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

def get_user(user_id: int, db: db_dependency):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user
    

def authenticate_user(username: str, password: str, db):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta):
    encode = {"sub": username, "id": user_id, "role": role}
    expires = datetime.utcnow() + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

# get current user from token
async def get_current_user(token: Annotated[str,Depends(oaut2_bearer)], db: db_dependency):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        expires: datetime = payload.get("exp")
        if user is None or id is None or datetime.fromtimestamp(expires) < datetime.utcnow():
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="could not valiate user")
        db_user = get_user(user_id, db)
        return {'username': username, 'id': user_id, 'role': db_user.role, 'disabled': db_user.disabled}
    except JWTError as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="could not valiate user")
    
async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user["disabled"]:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

async def validate_refresh_token(token: Annotated[str, Depends(oaut2_bearer)], db: db_dependency):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    try:
        if token in refresh_tokens:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            role: str = payload.get("role")
            user_id: int = payload.get("id")
            if username is None or role is None:
                raise credentials_exception
        else:
            raise credentials_exception

    except (JWTError, ValidationError):
        raise credentials_exception

    user = get_user(user_id, db)

    if user is None:
        raise credentials_exception

    return user, token
    
user_dependency = Annotated[dict, Depends(get_current_user)]

@auth_router.get("/")
async def user(user: user_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    return {"User": user}

class RoleChecker:
  def __init__(self, allowed_roles):
    self.allowed_roles = allowed_roles

  def __call__(self, user: Annotated[User, Depends(get_current_active_user)]):
    if user["role"] in self.allowed_roles:
      return True
    raise HTTPException(
status_code=status.HTTP_401_UNAUTHORIZED, 
detail="You don't have enough permissions")
  
@auth_router.get("/data")
def get_data(_: Annotated[bool, Depends(RoleChecker(allowed_roles=["admin"]))]):
  return {"data": "This is important data"}