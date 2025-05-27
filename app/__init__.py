# app/__init__.py

from flask import Flask

# db connection
from app.util.db_connection import Connection


def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.json.sort_keys = False

    # Import and register Blueprints
    from .main import main_bp
    from .api import task_bp
    from .api import family_bp
    from .api import person_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(task_bp)
    app.register_blueprint(family_bp)
    app.register_blueprint(person_bp)

    app.teardown_appcontext(Connection.close_db)

    return app
