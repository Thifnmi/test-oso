actor User {}

resource Resources {}

allow(actor, action, resource) if
  has_permission(actor, action, resource);


# permission for custom role
has_permission(actor: User, action: String, resource: Resources) if
  (actor.is_custom() and
  per in actor.get_permission() and
  per.resource_uuid == resource.uuid and
  action == per.action);

# custom permission for role member
# member only have permission get, list and create  without service billing
# has_permission(actor: User, "allow", resource: Resources) if
#   (gum in actor.get_gum_role_map() and
#   gum.role_uuid == "f25a679f-60b1-42cd-8ff7-df7145023f9b" and #replace with member uuid
#   resource.type != "update" and
#   resource.type != "delete" and
#   resource.service_name != "billing");


# custom permission for role reader
# reader only have permission get and list without service billing
# has_permission(actor: User, "allow", resource: Resources) if
#   (gum in actor.get_gum_role_map() and
#   gum.role_uuid == "896d667b-f4cc-4559-8ff4-ba719afb7376" and #replace with reader uuid
#   resource.type != "create" and
#   resource.type != "update" and
#   resource.type != "delete" and
#   resource.service_name != "billing");


# custom permission for role admin
# admin has full permission ignore delele
# has_permission(actor: User, _action: String, resource: Resources) if
#   (gum in actor.get_gum_role_map() and
#   gum.role_uuid == "13517f1e-0bbe-49fc-87cc-0de6716fe8cb" and #replace with admin uuid
#   resource.type != "delete" and
#   resource.service_name != "billing");


# custom permission for role owner
# owner can access any service
# has_permission(actor: User, _action: String, _resource: Resources) if
#   (gum in actor.get_gum_role_map() and
#   gum.role_uuid == "1c1f0495-b7af-43a7-abfc-2bc76ff2f3be"); #replace with owner uuid


# custom permission for role billing
# biller only access to biliing service
# has_permission(actor: User, _action: String, resource: Resources) if
#   (gum in actor.get_gum_role_map() and
#   gum.role_uuid == "e5ae830b-ba22-466b-b4cf-b16f56102b1f" and #replace with billing uuid
#   resource.service_name != "k8s" and
#   resource.service_name != "cloud-server" and
#   resource.service_name != "cloud-driver");


allow(actor, action, resource) if
  has_permission(actor, action, resource);

