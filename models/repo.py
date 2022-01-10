from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Boolean
from base import Base
from base import BaseModel


class Repo(Base, BaseModel):
    __tablename__ = "repos"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)