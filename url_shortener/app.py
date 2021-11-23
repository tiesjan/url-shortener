import os

from flask import Flask
from werkzeug.exceptions import HTTPException

from url_shortener.database import db, migrate
from url_shortener.template_filters import pluralize
from url_shortener.web import blueprint as web_blueprint
from url_shortener.web.views import handle_http_exception


def get_configuration():
    return {
        'SQLALCHEMY_DATABASE_URI': (
            # Defaults to an in-memory SQLite3 database
            os.environ.get('SQLALCHEMY_DATABASE_URI', 'sqlite://')
        ),
        'SQLALCHEMY_ECHO': (
            os.environ.get('SQLALCHEMY_ECHO', 'False') == 'True'
        ),
        'TESTING': (
            os.environ.get('FLASK_TESTING', 'False') == 'True'
        ),
        'WTF_CSRF_ENABLED': (
            os.environ.get('WTF_CSRF_ENABLED', 'True') == 'True'
        ),
    }


def handle_routing_http_exception(exception):
    """
    Handles HTTP exceptions for "404 Not Found" and "405 Method Not Allowed"
    occurring while routing requests to corresponding views
    """
    return handle_http_exception(exception)


def create_app():
    # Create and configure the app
    app = Flask('url_shortener')
    app.config.from_mapping(
        get_configuration(),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,  # for Flask-Alchemy pre-3.x
    )

    # Initialize database
    with app.app_context():
        db.init_app(app)
        migrate.init_app(app, db)

    # Register custom template filters
    app.add_template_filter(pluralize)

    # Register web interface
    app.register_blueprint(web_blueprint, url_prefix='/')

    # Register HTTP exception handler for routing
    app.register_error_handler(HTTPException, handle_routing_http_exception)

    return app
