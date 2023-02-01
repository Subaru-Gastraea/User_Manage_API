from sqlalchemy.orm import Session
from . import models, schemas, util
from datetime import datetime

def authenticate_user(db: Session, username: str, password: str):
    db_user = get_user(db, user_name=username)
    if not db_user:
        return False
    if not util.verify_password(password, db_user.passwd):
        return False

    return db_user

def get_user(db: Session, user_name: str):
    return db.query(models.User).filter(models.User.name == user_name).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = util.get_password_hash(user.password)
    db_user = models.User(name=user.name, birthday=user.birthday,  passwd=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

def user_login(db: Session, user_name: str):
    db.query(models.User).filter(models.User.name == user_name).update(
        {"last_login": datetime.utcnow()}, synchronize_session="fetch"
    )
    db.commit()