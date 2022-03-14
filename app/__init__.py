from flask import g, Flask, session as fl_session
from sqlalchemy import create_engine, and_, inspect, event, text
from .models import User, Permission, Resource
from sqlalchemy.orm import sessionmaker
from werkzeug.exceptions import BadRequest, Forbidden, NotFound
from polar.data_filtering import Relation
from polar.data.adapter.sqlalchemy_adapter import SqlAlchemyAdapter
from oso import Oso, OsoError


def create_app():
    engine = create_engine("sqlite:///test.db", connect_args={"check_same_thread":False})

    app = Flask(__name__)
    app.secret_key = "VccorpIAM"

    from app import routes

    app.register_blueprint(routes.users.bp)
    app.register_blueprint(routes.permissions.bp)
    app.register_blueprint(routes.resources.bp)

    @app.errorhandler(BadRequest)
    def handle_bad_request(*_):
        return {"message": "Bad Request"}, 400

    @app.errorhandler(Forbidden)
    def handle_forbidden(*_):
        return {"message": "Forbidden"}, 403

    @app.errorhandler(NotFound)
    def handle_not_found(*_):
        return {"message": "Not Found"}, 404

    Session = sessionmaker(bind=engine)

    init_oso(app, Session)

def init_oso(app, Session: sessionmaker):
    # Initialize SQLAlchemyOso instance.
    oso = Oso(forbidden_error=Forbidden, not_found_error=NotFound)

    def query_builder(model):
        # A "filter" is an object returned from Oso that describes
        # a condition that must hold on an object. This turns an
        # Oso filter into one that can be applied to an SQLAlchemy
        # query.
        def to_sqlalchemy_filter(filter):
            if filter.field is not None:
                field = getattr(model, filter.field)
                value = filter.value
            else:
                field = model.id
                value = filter.value.id

            if filter.kind == "Eq":
                return field == value
            elif filter.kind == "In":
                return field.in_(value)
            else:
                raise OsoError(f"Unsupported filter kind: {filter.kind}")

        # Turn a collection of Oso filters into one SQLAlchemy filter.
        def combine_filters(filters):
            filter = and_(*[to_sqlalchemy_filter(f) for f in filters])
            return Session().query(model).filter(filter)

        return combine_filters

    oso.set_data_filtering_adapter(SqlAlchemyAdapter(Session()))

    oso.register_class(
        Repo,
        build_query=query_builder(Repo),
        fields={
            "id": int,
            "name": str,
            "org": Relation(
                kind="one", other_type="Org", my_field="org_id", other_field="id"
            ),
            "issues": Relation(
                kind="many", other_type="Issue", my_field="id", other_field="repo_id"
            ),
        },
    )

    oso.register_class(
        OrgRole,
        build_query=query_builder(OrgRole),
        fields={
            "name": str,
            "user": Relation(
                kind="one", other_type="User", my_field="user_id", other_field="id"
            ),
            "org": Relation(
                kind="one", other_type="Org", my_field="org_id", other_field="id"
            ),
        },
    )

    oso.register_class(
        RepoRole,
        build_query=query_builder(RepoRole),
        fields={
            "name": str,
            "user": Relation(
                kind="one", other_type="User", my_field="user_id", other_field="id"
            ),
            "repo": Relation(
                kind="one", other_type="Repo", my_field="repo_id", other_field="id"
            ),
        },
    )

    oso.register_class(
        Issue,
        build_query=query_builder(Issue),
        fields={
            "title": str,
            "repo": Relation(
                kind="one", other_type="Repo", my_field="repo_id", other_field="id"
            ),
        },
    )

    oso.register_class(
        Org,
        build_query=query_builder(Org),
        fields={
            "id": int,
            "name": str,
            "base_repo_role": str,
            "billing_address": str,
            "repos": Relation(
                kind="many", other_type="Repo", my_field="id", other_field="org_id"
            ),
        },
    )

    oso.register_class(
        User,
        build_query=query_builder(User),
        fields={
            "email": str,
            "org_roles": Relation(
                kind="many", other_type="OrgRole", my_field="id", other_field="user_id"
            ),
            "repo_roles": Relation(
                kind="many", other_type="RepoRole", my_field="id", other_field="user_id"
            ),
        },
    )

    # Load authorization policy.
    oso.load_files(["app/authorization.polar"])

    # Attach Oso instance to Flask application.
    app.oso = oso
