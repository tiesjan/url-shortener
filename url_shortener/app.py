import os

from flask import Flask, render_template
from werkzeug.exceptions import HTTPException

from url_shortener.database import db, migrate
from url_shortener.short_urls import blueprint as short_urls_blueprint
from url_shortener.template_filters import pluralize


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


def handle_http_exception(exception):
    return (
        render_template('exception.html', exception=exception),
        exception.code
    )


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

    # Register blueprints
    app.register_blueprint(short_urls_blueprint, url_prefix='/')

    # Register HTTP exception handler
    app.register_error_handler(HTTPException, handle_http_exception)

    return app
