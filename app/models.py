
from dataclasses import dataclass
from typing import List


@dataclass
class Repository:
    name: str
    is_public: bool = False

    @staticmethod
    def get_by_name(name):
        return repos_db.get(name)

    @staticmethod
    def get_all():
        return repos_db


@dataclass
class Role:
    name: str
    repository: Repository


@dataclass
class User:
    roles: List[Role]

    @staticmethod
    def get_current_user(name):
        return users_db[name]
    
    def has_admin(user):
        if user.roles[0].name.upper() == 'ADMIN':
            return True
        return False


repos_db = {
    "gmail": Repository("gmail"),
    "react": Repository("react", is_public=True),
    "oso": Repository("oso"),
}

users_db = {
    "user1": User([Role(name="admin", repository=repos_db["gmail"])]),
    "user2": User([Role(name="maintainer", repository=repos_db["react"])]),
    "user3": User([Role(name="contributor", repository=repos_db["oso"])]),
}