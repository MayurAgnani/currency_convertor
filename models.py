from sqlalchemy import Column, Integer, String, Float, DateTime, TEXT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import datetime

DATABASE_URL = "sqlite:///./user.db"

Base = declarative_base()

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class UserRequest(Base):
    __tablename__ = "user_requests"
    id = Column(Integer, primary_key=True, index=True)
    api_key = Column(String, index=True)
    from_currency = Column(String, index=True)
    to_currency = Column(String, index=True)
    amount = Column(Float)
    converted_amount = Column(Float)
    timestamp = Column(DateTime, default=datetime.datetime.now())
    response_body = Column(TEXT)  # Store the response body as JSON


class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    api_key = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now())


def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()