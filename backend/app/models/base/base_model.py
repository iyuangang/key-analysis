from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.ext.declarative import declared_attr
from ...core.db import Base
import datetime


class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(
        DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower() + "s"
