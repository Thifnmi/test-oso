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

# This rule tells Oso how to fetch roles for a repository
has_role(actor: User, role_name: String, repository: Repository) if
  role in actor.roles and
  role_name = role.name and
  repository = role.repository;

has_permission(_actor: User, "read", repository: Repository) if
  repository.is_public;

# has_permission(user: User, "delete", repository: Repository) if
#   # User has the "admin" role.
#   has_role(user, "admin", repository);


# has_permission(user: User, "push", repository: Repository) if
#   # User has the "maintainer" role.
#   has_role(user, "maintainer", repository);


allow(actor, action, resource) if
  has_permission(actor, action, resource);
