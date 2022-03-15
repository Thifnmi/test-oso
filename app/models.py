import uuid
from sqlalchemy.sql.sqltypes import Boolean
from sqlalchemy.types import Integer, String
from sqlalchemy.schema import Column, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from sqlalchemy.ext.declarative import declarative_base



Base = declarative_base()

def generate_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    uuid = Column(String(36), name="uuid", unique=True, default=generate_uuid)
    role = Column(String)
    is_active = Column(Boolean, default=True)

    def repr(self):
        return {
            "id": self.id,
            "uuid": self.uuid,
            "role": self.role,
            "is_active": self.is_active,
        }

class Repository(Base):
    __tablename__ = "repository"

    id = Column(Integer, primary_key=True)
    uuid = Column(String(36), name="uuid", unique=True, default=generate_uuid)
    type = Column(String)
    service = Column(String)
    endpoint = Column(String)
    is_active = Column(Boolean, default=True)

    def repr(self):
        return {
            "id": self.id,
            "uuid": self.uuid,
            "type": self.type,
            "service": self.service,
            "endpoint": self.endpoint,
            "is_active": self.is_active,
        }

class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True)
    uuid = Column(String(36), name="uuid", unique=True, default=generate_uuid)
    action = Column(String)

    def repr(self):
        return {
            "id": self.id,
            "uuid": self.uuid,
            "action": self.action,
        }
