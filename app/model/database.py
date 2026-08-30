import os

from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

load_dotenv(override=True)


engine = create_engine(os.getenv("DATABASE_URL"))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)





class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

