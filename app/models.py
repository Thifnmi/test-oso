
from dataclasses import dataclass
from typing import List


@dataclass
class Resources:
    id: int
    type: str
    service: str
    endpoint: str

    @staticmethod
    def get_by_id(id):
        for item in resource_db:
            # if item['id'] == id:
            #     return item
            print(item)
        return "resource_db[id]"

    @staticmethod
    def get_by_type(type):
        return resource_db.get(type)

    @staticmethod
    def get_by_service(service):
        return resource_db.get(service)

    @staticmethod
    def get_all():
        return resource_db


@dataclass
class Permission:
    id: int
    action: str

    @staticmethod
    def get_permission(id):
        return permission_db.get(id)

    @staticmethod
    def get_all_permission():
        return permission_db

@dataclass
class User:
    id: int
    role: str

    @staticmethod
    def get_current_user(id):
        return users_db[0]


users_db = {
    (1, "owner"),
    (2, "billing"),
    (3, "admin"),
    (4, "member"),
}

resource_db = {
    (1, "list", "cloud-server", "iaas/api/list-server"),
    (2, "get", "cloud-server", "iaas/api/servers"),
    (3, "create", "cloud-server", "iaas/api/create-server"),
    (4, "update", "cloud-server", "iaas/api/update-server"),
    (5, "delete", "cloud-server", "iaas/api/delete-server"),
    (6, "list", "billing", "billing/api/list-invoice"),
    (7, "get", "billing", "billing/api/invoices"),
    (8, "create", "billing", "billing/api/create-invoice"),
    (9, "update", "billing", "billing/api/update-invoice"),
    (10, "delete", "billing", "billing/api/delete-invoice"),
}

permission_db = {
    (1, "allow"),
    (2, "deny"),
}