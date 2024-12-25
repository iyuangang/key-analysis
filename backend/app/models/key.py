from sqlalchemy import Column, String, Float, Integer
from .base.base_model import BaseModel


class KeyInfo(BaseModel):
    fingerprint = Column(String)
    repeat_letter_score = Column(Float)
    increasing_letter_score = Column(Float)
    decreasing_letter_score = Column(Float)
    magic_letter_score = Column(Float)
    score = Column(Float)
    unique_letters_count = Column(Integer)
