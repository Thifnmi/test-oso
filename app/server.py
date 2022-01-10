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

# Load your policy files.
oso.load_files(["app/main.polar"])

app = Flask(__name__)


@app.route("/repo/<name>/<username>/<permission>")
def repo_show(name, username, permission):
    repo = Repository.get_by_name(name)
    print(repo)
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
    # try:
    #     if oso.is_allowed(User.get_current_user(username), permission, repo):
    #         res = {}
    #         res["_username"] = username
    #         res["status"] = "OK"
    #         res["permission"] = permission
    #         res["repo"] = repo.name
    #         res["status"] = 200
    #         return res, 200
    #     else:
    #         return {"message": "permission deny"}
    #     oso.authorize(User.get_current_user(username), permission, repo)
    #     res = {}
    #     res["_username"] = username
    #     res["status"] = "OK"
    #     res["permission"] = permission
    #     res["repo"] = repo.name
    #     res["status"] = 200
    #     return res, 200

    # except NotFoundError:
    #     res = {}
    #     res["_username"] = username
    #     res["except"] = "NotFoundError"
    #     res["permission"] = permission
    #     res["repo"] = name
    #     res["status"] = 404
    #     return res, 404
    # except ForbiddenError:
    #     res = {}
    #     res["_username"] = username
    #     res["except"] = "ForbiddenError"
    #     res["permission"] = permission
    #     res["repo"] = name
    #     res["status"] = 403
    #     return res, 403


@app.route("/allrepo")
def all_repo():
    repos = Repository.get_all()
    if repos is None:
        res = {}
        res["message"] = "List repo is none"
        res["status"] = 404
        return res, 404
    return repos, 200


@app.route("/repo/<username>")
def list_repo(username):
    repos = Repository.get_all()
    if repos is None:
        res = {}
        res["message"] = "List repo is none"
        res["status"] = 404
        return res, 404
    repo = []
    for item in repos:
        item = Repository.get_by_name(item)
        if oso.is_allowed(User.get_current_user(username), "read", item):
            repo.append(item)
    repo = json.dumps(repo, default=str)
    return repo, 200


@app.route("/update/<repo_name>/<username>/<permission>")
def update_repo(repo_name, username, permission):
    repo = Repository.get_by_name(repo_name)
    if repo is None:
        res = {}
        res["status"] = 404
        return res, 404
    return repo, 200


# @app.route("/list/<username>")
# def list_repo_can_read(username):
#     repos = User.get_repo_by_user(username)
#     print(repos)
#     return repos
