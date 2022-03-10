actor User {}

resource Repository {
  permissions = ["read", "push", "delete"];
  roles = ["contributor", "maintainer", "admin"];
  
  "read" if "contributor";
  "push" if "maintainer";
  "delete" if "admin";
  
  "contributor" if "maintainer";
  "maintainer" if "admin";
}

has_role(actor: User, role_name: String, repository: Repository) if
  role in actor.roles and
  role_name = role.name and
  repository = role.repository;
  
has_permission(_actor: User, "read", repository: Repository) if
  # (role in actor.roles and
  # role.name == "admin") or
  # (role in actor.roles and
  # role.name = "maintainer") or
  repository.is_public;

allow(actor, action, resource) if
  has_permission(actor, action, resource);

has_permission(actor: User, "delete", repository: Repository) if
  (role in actor.roles and
  role.name == "admin") or
  (role in actor.roles and
  repository = role.repository);

has_permission(actor: User, "push", repository: Repository) if
  (role in actor.roles and
  role.name == "admin") or
  (role in actor.roles and
  repository = role.repository) or
  (role in actor.roles and
  role.name = "maintainer");

allow(actor, action, resource) if
  has_permission(actor, action, resource);
