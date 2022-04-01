from flask import g, Flask, session as flask_session
from sqlalchemy import create_engine, and_
from .models import Base, User, Permission, Group, GroupUserMap, GUMRoleMap, Resources, Role, ResourceMapping
from sqlalchemy.orm import sessionmaker, scoped_session
from werkzeug.exceptions import BadRequest, Forbidden, NotFound
from polar.data.adapter.sqlalchemy_adapter import SqlAlchemyAdapter
from oso import Oso, OsoError
from app.insert_data import load_data


def create_app():
    engine = create_engine("sqlite:///newdatabase.db", connect_args={"check_same_thread":False})

    app = Flask(__name__)
    app.secret_key = "VccorpIAM"

    from app import routes

    app.register_blueprint(routes.user.bp)
    app.register_blueprint(routes.permission.bp)
    app.register_blueprint(routes.resource.bp)
    app.register_blueprint(routes.session.bp)
    app.register_blueprint(routes.group.bp)
    app.register_blueprint(routes.role.bp)


    @app.errorhandler(BadRequest)
    def handle_bad_request(*_):
        return {"message": "Bad Request"}, 400

    @app.errorhandler(Forbidden)
    def handle_forbidden(*_):
        return {"message": "Forbidden"}, 403

    @app.errorhandler(NotFound)
    def handle_not_found(*_):
        return {"message": "Access deny"}, 404

    Session = sessionmaker(bind=engine)

    init_oso(app, Session)
    Base.metadata.create_all(engine)

    db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
    Base.query = db_session.query_property()

    with open("permission.txt", "r") as t:
        if t.read() == "okay":
            load_data(Session())
    
    with open("permission.txt", "w") as t:
        t.write("deny")

    
    @app.before_request
    def set_current_user_and_session():
        flask_session.permanent = True

        g.session = Session()
        if "current_user" not in g:
            if "current_user_id" in flask_session:
                user_id = flask_session.get("current_user_id")
                user = g.session.query(User).filter_by(id=user_id).one_or_none()
                if user is None:
                    flask_session.pop("current_user_id")
                g.current_user = user
            else:
                g.current_user = None

    @app.after_request
    def add_cors_headers(res):
        res.headers.add("Access-Control-Allow-Origin", "http://192.168.18.117:8888")
        res.headers.add("Access-Control-Allow-Headers", "Accept,Content-Type")
        res.headers.add("Access-Control-Allow-Methods", "DELETE,GET,OPTIONS,PATCH,POST")
        res.headers.add("Access-Control-Allow-Credentials", "true")
        return res

    @app.after_request
    def close_session(res):
        if "session" in g:
            g.session.close()
        return res
    return app

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
        Resources,
        build_query=query_builder(Resources),
        fields={
            "id": int,
            "uuid": str,
            "type": str,
            "service_type": str,
            "service_name": str,
            "endpoint": str,
        },
    )

    oso.register_class(
        User,
        build_query=query_builder(User),
        fields={
            "id": int,
            "uuid": str,
            "email": str,
        },
    )

    oso.register_class(
        Permission,
        build_query=query_builder(Permission),
        fields={
            "id": int,
            "uuid": str,
            "role_uuid": str,
            "resource_uuid": str,
            "action": str,
        },
    )

    oso.register_class(
        Group,
        build_query=query_builder(Group),
        fields={
            "id": int,
            "uuid": str,
            "name": str,
        }
    )

    oso.register_class(
        GroupUserMap,
        build_query=query_builder(GroupUserMap),
        fields={
            "id": int,
            "uuid": str,
            "group_uuid": str,
            "user_uuid": str,
        }
    )

    oso.register_class(
        Role,
        build_query=query_builder(Role),
        fields={
            "id": int,
            "uuid": str,
            "name": str,
            "is_custom": bool,
        }
    )

    oso.register_class(
        GUMRoleMap,
        build_query=query_builder(GUMRoleMap),
        fields={
            "id": int,
            "uuid": str,
            "gum_uuid": str,
            "role_uuid": str,
        }
    )

    oso.register_class(
        ResourceMapping,
        build_query=query_builder(ResourceMapping),
        fields={
            "id": int,
            "uuid": str,
            "resource_uuid": str,
            "url": str,
        }
    )

    # Load authorization policy.
    oso.load_files(["app/main.polar"])

    # Attach Oso instance to Flask application.
    app.oso = oso
