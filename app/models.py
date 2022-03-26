import uuid
from sqlalchemy.sql.sqltypes import Boolean
from sqlalchemy.types import Integer, String
from sqlalchemy.schema import Column, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from sqlalchemy.ext.declarative import declarative_base



Base = declarative_base()

def generate_uuid():
    return str(uuid.uuid4())


class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True)
    uuid = Column(String(36), name="uuid", unique=True, default=generate_uuid)
    name = Column(String)

    def repr(self):
        return {
            "id": self.id,
            "uuid": self.uuid,
            "name": self.name
        }


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    uuid = Column(String(36), name="uuid", unique=True, default=generate_uuid)
    email = Column(String)

    def repr(self):
        return {
            "id": self.id,
            "uuid": self.uuid,
            "email": self.email,
        }


class GroupUserMap(Base):
    __tablename__ = "group_user_maps"

    id = Column(Integer, primary_key=True)
    uuid = Column(String(36), name="uuid", unique=True, default=generate_uuid)
    group_uuid = Column(String(36), name="group_uuid")
    user_uuid = Column(String(36), name="user_uuid")

    def repr(self):
        return {
            "id": self.id,
            "uuid": self.uuid,
            "gum_uid": self.group_uuid,
            "user_uuid": self.user_uuid,
        }


class Resources(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True)
    uuid = Column(String(36), name="uuid", unique=True, default=generate_uuid)
    type = Column(String)
    service_type = Column(String)
    service_name = Column(String)
    endpoint = Column(String)

    def repr(self):
        return {
            "id": self.id,
            "uuid": self.uuid,
            "type": self.type,
            "service type": self.service_type,
            "service name": self.service_name,
            "endpoint": self.endpoint,
        }


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    uuid = Column(String(36), name="uuid", unique=True, default=generate_uuid)
    pum_uuid = Column(String(36), name="pum_uuid", default=generate_uuid)
    name = Column(String)
    is_custom = Column(Boolean)

    def repr(self):
        return {
            "id": self.id,
            "uuid": self.uuid,
            "pum_uuid": self.uuid,
            "name": self.name,
        }


class GUMRoleMap(Base):
    __tablename__ = "gum_role_map"

    id = Column(Integer, primary_key=True)
    uuid = Column(String(36), name="uuid", unique=True, default=generate_uuid)
    gum_uuid = Column(String(36), name="gum_uuid", default=generate_uuid)
    role_uuid = Column(String(36), name="role_uuid", default=generate_uuid)

    def repr(self):
        return {
            "id": self.id,
            "uuid": self.uuid,
            "gum_uuid": self.gum_uuid,
            "name": self.role_uuid,
        }


class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True)
    uuid = Column(String(36), name="uuid", unique=True, default=generate_uuid)
    gum_role_map_uuid = Column(String(36), name="gum_role_map_uuid")
    resource_uuid = Column(String(36), name="resource_uuid")
    action = Column(String(10))

    def repr(self):
        return {
            "id": self.id,
            "uuid": self.uuid,
            "gum_role_map_uuid": self.gum_role_map_uuid,
            "resource_uuid": self.resource_uuid,
            "action": self.action
        }


class ResourceMapping(Base):
    __tablename__ = "resource_mapping"

    id = Column(Integer, primary_key=True)
    resource_uuid = Column(String(36), name="resource_uuid")
    url = Column(String)

    def repr(self):
        return {
            "id": self.id,
            "resource_uuid": self.resource_uuid,
            "url": self.url,
        }
