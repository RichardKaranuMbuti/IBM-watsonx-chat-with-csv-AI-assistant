from sqlalchemy import Column, Integer, String
from .database import Base

class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, unique=False, index=True, nullable=False)
    description = Column(String, nullable=True)
