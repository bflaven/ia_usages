# grab from https://fastapi.tiangolo.com/tutorial/sql-databases/
# from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy import Column, Integer, String

from sqlalchemy.orm import relationship

from database import Base


class Films(Base):
    __tablename__ = "films"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True)
    director = Column(String)
