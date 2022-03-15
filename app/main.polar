actor User {}

resource Repository {}

allow(actor, action, resource) if
  has_permission(actor, action, resource);

# custom permission for role member
# member only have permission get and list without service billing
has_permission(actor: User, "allow", resource: Repository) if
  (actor.role == "member" and
  resource.type != "update" and
  resource.type != "delete" and
  resource.service != "billing");


# custom permission for role admin
# admin has full permission ignore delele
has_permission(actor: User, "allow", resource: Repository) if
  actor.role == "admin" and
  resource.type != "delete" and
  resource.service != "billing";

# custom permission for role owner
# owner can access any service
has_permission(actor: User, "allow", _resource: Repository) if
  actor.role == "owner";


# custom permission for role billing
# biller only access to biliing service
has_permission(actor: User, "allow", resource: Repository) if
  actor.role == "billing" and
  resource.service != "k8s" and
  resource.service != "cloud-server" and
  resource.service != "cloud-driver";


allow(actor, action, resource) if
  has_permission(actor, action, resource);

