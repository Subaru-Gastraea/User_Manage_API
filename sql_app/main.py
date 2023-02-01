from fastapi import Depends, FastAPI, HTTPException, Form
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from . import crud, models, schemas
from .database import SessionLocal, engine
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Login
@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_name=form_data.username)
    if db_user is None:
        raise HTTPException(status_code=400, detail="User not found")

    hashed_password = crud.fake_hash_password(form_data.password)
    if not hashed_password == db_user.passwd:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    crud.user_login(db, user_name=db_user.name)

    return {"access_token": db_user.name, "token_type": "bearer"}

# Get user data
@app.get("/user/", response_model=schemas.User, status_code=200)
def read_user(name: str = Form(), db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_name=name)
    if db_user is None:
        raise HTTPException(status_code=400, detail="User not found")
        
    return db_user

# Create user
@app.post("/user/", status_code=200)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_name=user.name)
    if db_user:
        raise HTTPException(status_code=400, detail="User name already registered")
    
    crud.create_user(db=db, user=user)

# Delete user
# @app.delete("/user/")

# Update password & birthday
# @app.patch("/user/")
