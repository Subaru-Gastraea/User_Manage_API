from sqlalchemy import Column, String, Date, DateTime
from datetime import datetime

from database import Base

class User(Base):
    __tablename__ = "userinfo_tb"

    name = Column(String, primary_key=True)
    passwd = Column(String, nullable=False)
    birthday = Column(Date) # default: nullable=False
    createT = Column(DateTime, default = datetime.utcnow())
    last_login = Column(DateTime, nullable=True)