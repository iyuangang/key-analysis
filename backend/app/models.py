from sqlalchemy import Column, Integer, String, DateTime, Float
from .database import Base


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
