from fastapi import Depends, FastAPI, HTTPException, Form, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from jose import JWTError

from . import crud, models, schemas, util
from .database import SessionLocal, engine
models.Base.metadata.create_all(bind=engine)

ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def Auth_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = util.get_token_data(token)   # Decode the JWT token returned by "/login" endpoint
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    return token_data.username

# Login
@app.post("/login", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Authenticate
    user = crud.authenticate_user(db=db, username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Update time of last login
    crud.user_login(db=db, user_name=user.name)

    # Generate access token for JWT authorization
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = util.create_access_token(
        data={"sub": user.name}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}

# Get user data
@app.get("/user/", response_model=schemas.User, status_code=200)
def read_user(name: str = Form(), cur_uname: str = Depends(Auth_current_user), db: Session = Depends(get_db)):
    db_user = crud.get_user(db=db, user_name=name)
    if db_user is None:
        raise HTTPException(status_code=400, detail="User not found")
        
    return db_user

# Create user
@app.post("/user/", status_code=200)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db=db, user_name=user.name)
    if db_user:
        raise HTTPException(status_code=400, detail="User name already registered")
    
    crud.create_user(db=db, user=user)

# Delete user
@app.delete("/user/", status_code=200)
def delete_user(name: str = Form(), cur_uname: str = Depends(Auth_current_user), db: Session = Depends(get_db)):
    db_user = crud.get_user(db=db, user_name=name)
    if db_user is None:
        raise HTTPException(status_code=400, detail="User not found")

    crud.delete_user(db=db, user_name=name)

# Update password & birthday
# @app.patch("/user/")
