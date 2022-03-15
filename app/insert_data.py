from app.models import Base, User, Permission, Repository

def load_data(session):
    def user(role):
        user = User(role=role)
        session.add(user)

    def permission(action):
        permission = Permission(action=action)
        session.add(permission)

    def repository(type, service, endpoint):
        repository = Repository(type=type, service=service, endpoint=endpoint)
        session.add(repository)


    per_allow = Permission(action="allow")
    per_deny = Permission(action="deny")
    pers = [per_allow, per_deny]

    for per in pers:
        session.add(per)

    repo1 = Repository(type="list", service="cloud-server", endpoint="iaas/api/list-server")
    repo2 = Repository(type="get", service="cloud-server", endpoint="iaas/api/servers")
    repo3 = Repository(type="create", service="cloud-server", endpoint="iaas/api/create-server")
    repo4 = Repository(type="update", service="cloud-server",endpoint="iaas/api/update-server")
    repo5 = Repository(type="delete", service="cloud-server",endpoint="iaas/api/delete-server")
    repo6 = Repository(type="list", service="billing", endpoint="billing/api/list-invoice")
    repo7 = Repository(type="get", service="billing", endpoint="billing/api/invoices")
    repo8 = Repository(type="create", service="billing", endpoint="billing/api/create-invoice")
    repo9 = Repository(type="update", service="billing", endpoint="billing/api/update-invoice")
    repo10 = Repository(type="delete", service="billing", endpoint="billing/api/delete-invoice")
    repo11 = Repository(type="list", service="cloud-driver", endpoint="cloud-storage/api/list-driver")
    repo12 = Repository(type="get", service="cloud-driver", endpoint="cloud-storage/api/driver")
    repo13 = Repository(type="create", service="cloud-driver", endpoint="cloud-storage/api/create-driver")
    repo14 = Repository(type="update", service="cloud-driver",endpoint="cloud-storage/api/update-driver")
    repo15 = Repository(type="delete", service="cloud-driver",endpoint="cloud-storage/api/delete-driver")
    repo16 = Repository(type="list", service="k8s", endpoint="kubernetes-engine/api/list-kubernetes-engine")
    repo17 = Repository(type="get", service="k8s", endpoint="kubernetes-engine/api/kubernetes-engine")
    repo18 = Repository(type="create", service="k8s", endpoint="kubernetes-engine/api/create-kubernetes-engine")
    repo19 = Repository(type="update", service="k8s", endpoint="kubernetes-engine/api/update-kubernetes-engine")
    repo20 = Repository(type="delete", service="k8s", endpoint="kubernetes-engine/api/delete-kubernetes-engine")

    repos = [repo1, repo2, repo3, repo4, repo5, repo6, repo7, repo8, repo9, repo10,
        repo11, repo12, repo13, repo14, repo15, repo16, repo17, repo18, repo19, repo20]
    for repo in repos:
        session.add(repo)
    
    user1 = User(role="owner")
    user2 = User(role="billing")
    user3 = User(role="admin")
    user4 = User(role="member")
    users = [user1, user2, user3, user4]

    for usr in users:
        session.add(usr)

    session.flush()
    session.commit()
    session.close()