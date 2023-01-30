from sqlalchemy.orm import Session
from . import models, schemas

def get_user(db: Session, user_name: str):
    return db.query(models.User).filter(models.User.name == user_name).first()

def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(name=user.name, birthday=user.birthday,  passwd=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user