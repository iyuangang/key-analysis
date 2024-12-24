from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean
from .database import Base
import datetime


class KeyInfo(Base):
    __tablename__ = "key_infos"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime)
    fingerprint = Column(String)
    repeat_letter_score = Column(Float)
    increasing_letter_score = Column(Float)
    decreasing_letter_score = Column(Float)
    magic_letter_score = Column(Float)
    score = Column(Float)
    unique_letters_count = Column(Integer)


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    disabled = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(
        DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )
