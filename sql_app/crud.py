from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime

def fake_hash_password(password: str):
    return password + "notreallyhashed"

def get_user(db: Session, user_name: str):
    return db.query(models.User).filter(models.User.name == user_name).first()

def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = fake_hash_password(user.password)
    db_user = models.User(name=user.name, birthday=user.birthday,  passwd=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

def user_login(db: Session, user_name: str):
    db.query(models.User).filter(models.User.name == user_name).update(
        {"last_login": datetime.utcnow()}, synchronize_session="fetch"
    )
    db.commit()