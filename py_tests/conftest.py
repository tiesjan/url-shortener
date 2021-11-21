from flask import template_rendered
from flask_migrate import upgrade
import pytest

from url_shortener.app import create_app
from url_shortener.database import db


@pytest.fixture(scope='session')
def app():
    yield create_app()


@pytest.fixture(scope='session', autouse=True)
def db_init_schema(app):
    # Apply database migrations before session starts
    with app.app_context():
        upgrade(directory='url_shortener/database/migrations/')

    yield


@pytest.fixture(scope='function', autouse=True)
def db_clear_tables():
    yield

    # Clear table data after each test
    for table in reversed(db.metadata.sorted_tables):
        db.session.execute(table.delete())
    db.session.commit()


@pytest.fixture
def rendered_templates(app):
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template, context))

    template_rendered.connect(record, app)

    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)
