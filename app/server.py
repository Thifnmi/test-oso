import json
from flask import Flask
from oso import Oso, NotFoundError, ForbiddenError
from .models import User, Repository

# Initialize the Oso object. This object is usually used globally throughout
# an application.
oso = Oso()

# Tell Oso about the data you will authorize. These types can be referenced
# in the policy.
oso.register_class(User)
oso.register_class(Repository)
oso.load_files(["app/main.polar"])
# policy1 = 'allow(actor, action, resource) if has_permission(actor, action, resource); actor User {} resource Repository { permissions = ["read", "push", "delete"]; roles = ["contributor", "maintainer", "admin"]; "read" if "contributor"; "push" if "maintainer"; "delete" if "admin"; "contributor" if "maintainer"; "maintainer" if "admin"; } has_role(actor: User, role_name: String, repository: Repository) if role in actor.roles and role_name = role.name and repository = role.repository;'
# policy2 = 'allow(actor, action, resource) if has_permission(actor, action, resource); actor User {} resource Repository { permissions = ["read", "push", "delete"]; roles = ["contributor", "maintainer", "admin"]; "read" if "contributor"; "push" if "maintainer"; "delete" if "admin"; "contributor" if "maintainer"; "maintainer" if "admin"; } has_role(actor: User, role_name: String, repository: Repository) if role in actor.roles and role_name = role.name and repository = role.repository; has_permission(_actor: User, "read", repository: Repository) if repository.is_public; allow(actor, action, resource) if has_permission(actor, action, resource);'

# Load your policy from string.
# def change_rule(rule):
#     oso.clear_rules()
#     oso.load_str(rule)


# change_rule(policy1)

app = Flask(__name__)


@app.route("/repo/<name>/<username>/<permission>")
def repo_show(name, username, permission):
    repo = Repository.get_by_name(name)
    if repo:
        print(oso.get_allowed_actions(User.get_current_user(username), repo))
        if oso.is_allowed(User.get_current_user(username), permission, repo):
            res = {}
            res["_username"] = username
            res["status"] = "OK"
            res["permission"] = permission
            res["repo"] = repo.name
            res["status"] = 200
            return res, 200
        else:
            return {"message": "permission deny"}
    return {"message": "repo not found"}


@app.route("/allrepo")
def all_repo():
    repos = Repository.get_all()
    if repos is None:
        res = {}
        res["message"] = "List repo is none"
        res["status"] = 404
        return res, 404
    return repos, 200


@app.route("/repos/<username>/<permission>")
def list_repos(username, permission):
    # change_rule(policy1)
    repos = Repository.get_all()
    if repos is None:
        res = {}
        res["message"] = "List repo is none"
        res["status"] = 404
        return res, 404
    repo = []
    for item in repos:
        item = Repository.get_by_name(item)
        if oso.is_allowed(User.get_current_user(username), permission, item):
            repo.append(item)
    repo = json.dumps(repo, default=str)
    return repo, 200


# @app.route("/repo/<username>/<permission>")
# def list_repo(username, permission):
#     # change_rule(policy2)
#     print(User.get_current_user(username).has_admin())
#     repos = Repository.get_all()
#     if repos is None:
#         res = {}
#         res["message"] = "List repo is none"
#         res["status"] = 404
#         return res, 404
#     repo = []
#     for item in repos:
#         item = Repository.get_by_name(item)
#         if oso.is_allowed(User.get_current_user(username), permission, item):
#             repo.append(item)
#     repo = json.dumps(repo, default=str)
#     return repo, 200
