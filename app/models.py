from sqlalchemy.sql.sqltypes import Boolean
from sqlalchemy.types import Integer, String
from sqlalchemy.schema import Column, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    role = Column(String)

    def repr(self):
        return {
            "id": self.id,
            "role": self.role,
        }

class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True)
    type = Column(String)
    service = Column(String)
    endpoint = Column(String)

    def repr(self):
        return {
            "id": self.id,
            "type": self.type,
            "service": self.service,
            "endpoint": self.endpoint
        }

class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True)
    action = Column(String)

    def repr(self):
        return {
            "id": self.id,
            "action": self.action
        }



# from dataclasses import dataclass
# from typing import List


# @dataclass
# class Resources:
#     id: int
#     type: str
#     service: str
#     endpoint: str

#     @staticmethod
#     def get_by_id(id):
#         print(id, resource_db.get(id), resource_db[id])
#         # for item in resource_db:
#             # if item['id'] == id:
#             #     return item
#             # print(item)
#         return resource_db[id]

#     # @staticmethod
#     # def get_by_type(type):
#     #     return resource_db.get(type)

#     # @staticmethod
#     # def get_by_service(service):
#     #     return resource_db.get(service)

#     @staticmethod
#     def get_all():
#         return resource_db


# @dataclass
# class Permission:
#     id: int
#     action: str

#     @staticmethod
#     def get_permission(id):
#         return permission_db.get(id)

#     @staticmethod
#     def get_all_permission():
#         return permission_db

# @dataclass
# class User:
#     id: int
#     role: str

#     @staticmethod
#     def get_current_user(id):
#         return users_db.get(id)


# users_db = {
#     1: (1, "owner"),
#     2: (2, "billing"),
#     3: (3, "admin"),
#     4: (4, "member"),
# }

# resource_db = {
#     1: (1, "list", "cloud-server", "iaas/api/list-server"),
#     2: (2, "get", "cloud-server", "iaas/api/servers"),
#     3: (3, "create", "cloud-server", "iaas/api/create-server"),
#     4: (4, "update", "cloud-server", "iaas/api/update-server"),
#     5: (5, "delete", "cloud-server", "iaas/api/delete-server"),
#     6: (6, "list", "billing", "billing/api/list-invoice"),
#     7: (7, "get", "billing", "billing/api/invoices"),
#     8: (8, "create", "billing", "billing/api/create-invoice"),
#     9: (9, "update", "billing", "billing/api/update-invoice"),
#     10: (10, "delete", "billing", "billing/api/delete-invoice"),
# }

# permission_db = {
#     1: (1, "allow"),
#     2: (2, "deny"),
# }