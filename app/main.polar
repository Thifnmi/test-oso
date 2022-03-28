actor User {}

resource Resources {}

allow(actor, action, resource) if
  has_permission(actor, action, resource);

has_permission(actor: User, action: String, resource: Resources) if
  actor.is_custom() and
  per in actor.get_permission() and
  per.resource_uuid == resource.uuid and
  action == per.action;

# custom permission for role member
# member only have permission get and list without service billing
has_permission(actor: User, _action: String, resource: Resources) if
  (actor.is_custom() and
  actor.get_role() == "member" and
  resource.type != "update" and
  resource.type != "delete" and
  resource.service_name != "billing");


# custom permission for role admin
# admin has full permission ignore delele
# has_permission(actor: User, _action: String, resource: Resources) if
#   actor.get_role() == "admin" and
#   resource.type != "delete" and
#   resource.service_name != "billing";

# custom permission for role owner
# owner can access any service
has_permission(actor: User, _action: String, _resource: Resources) if
  actor.get_role() == "owner";


# custom permission for role billing
# biller only access to biliing service
# has_permission(actor: User, _action: String, resource: Resources) if
#   actor.get_role() == "billing" and
#   resource.service_name != "k8s" and
#   resource.service_name != "cloud-server" and
#   resource.service_name != "cloud-driver";


allow(actor, action, resource) if
  has_permission(actor, action, resource);

