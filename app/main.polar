actor User {}
# action Permission {}
# resource Permission {}
resource Resources {}


  
has_permission(actor: User, "allow", resource: Resources) if
  (actor.role == "member" and
  resource.type == "get");

allow(actor, action, resource) if
  has_permission(actor, action, resource);

