from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# load environment variables from .env file
load_dotenv()
db_user = os.environ['DB_USER']
db_password = os.environ['DB_PASSWORD']
db_host = os.environ['DB_HOST']
db_port = os.environ['DB_PORT']
db_name = os.environ['DB_NAME']

# postgresql://user:password@postgresserver/db
SQLALCHEMY_DATABASE_URL = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()