import json
from flask import Flask
from oso import Oso, NotFoundError, ForbiddenError
from .models import User, Resources


# Initialize the Oso object. This object is usually used globally throughout
# an application.
oso = Oso()

# Tell Oso about the data you will authorize. These types can be referenced
# in the policy.
oso.register_class(User)
oso.register_class(Resources)
oso.load_files(["app/main.polar"])
# policy1 = 'allow(actor, action, resource) if has_permission(actor, action, resource); actor User {} resource Repository { permissions = ["read", "push", "delete"]; roles = ["contributor", "maintainer", "admin"]; "read" if "contributor"; "push" if "maintainer"; "delete" if "admin"; "contributor" if "maintainer"; "maintainer" if "admin"; } has_role(actor: User, role_name: String, repository: Repository) if role in actor.roles and role_name = role.name and repository = role.repository;'
# policy2 = 'allow(actor, action, resource) if has_permission(actor, action, resource); actor User {} resource Repository { permissions = ["read", "push", "delete"]; roles = ["contributor", "maintainer", "admin"]; "read" if "contributor"; "push" if "maintainer"; "delete" if "admin"; "contributor" if "maintainer"; "maintainer" if "admin"; } has_role(actor: User, role_name: String, repository: Repository) if role in actor.roles and role_name = role.name and repository = role.repository; has_permission(_actor: User, "read", repository: Repository) if repository.is_public; allow(actor, action, resource) if has_permission(actor, action, resource);'

# Load your policy from string.
# def change_rule(rule):
#     oso.clear_rules()
#     oso.load_str(rule)


# change_rule(policy1)

app = Flask(__name__)


@app.route("/resource/<id_resource>/<id_user>")
def repo_show(id_resource, id_user):
    repo = Resources.get_by_id(id_resource)
    print(repo)
    if repo:
        print(User.get_current_user(id_user))
        if oso.is_allowed(User.get_current_user(id_user), repo):
            res = {}
            res["_username"] = id_user
            res["status"] = "OK"
            res["status"] = 200
            # res["permission"] = permission
            data = {}
            data["type"] = repo.type
            data["service"] = repo.service
            data["endpoint"] = repo.endpoint
            res["resource"] = data
            return res, 200
        else:
            return {"message": "permission deny"}
    return {"message": "repo not found"}


@app.route("/all-resource")
def allResource():
    repos = json.dumps(Resources.get_all(), sort_keys=False)
    print(type(repos))
    if repos is None:
        res = {}
        res["message"] = "List resource is none"
        res["status"] = 404
        return res, 404
    return repos, 200


# @app.route("/repos/<username>/<permission>")
# def list_repos(username, permission):
#     # change_rule(policy1)
#     repos = Resources.get_all()
#     if repos is None:
#         res = {}
#         res["message"] = "List repo is none"
#         res["status"] = 404
#         return res, 404
#     repo = []
#     for item in repos:
#         item = Resources.get_by_name(item)
#         if oso.is_allowed(User.get_current_user(username), permission, item):
#             repo.append(item)
#     repo = json.dumps(repo, default=str)
#     return repo, 200
