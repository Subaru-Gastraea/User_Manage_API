from fastapi import Depends, FastAPI, HTTPException, Form
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Login
# @app.post("/login")

# Get user data
@app.get("/user/", response_model=schemas.User, status_code=200)
def read_user(name: str = Form(), db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_name=name)
    if db_user is None:
        raise HTTPException(status_code=400, detail="Bad request")
        
    return db_user

# Create user
@app.post("/user/", status_code=200)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_name=user.name)
    if db_user:
        raise HTTPException(status_code=400, detail="Bad request")
    
    crud.create_user(db=db, user=user)

# Delete user
# @app.delete("/user/")

# Update password & birthday
# @app.patch("/user/")
