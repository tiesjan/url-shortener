from werkzeug.exceptions import NotFound

from url_shortener.app import get_configuration


def test_get_configuration(monkeypatch):
    # No environment variables set
    monkeypatch.delenv('SQLALCHEMY_DATABASE_URI', raising=False)
    monkeypatch.delenv('SQLALCHEMY_ECHO', raising=False)
    monkeypatch.delenv('FLASK_TESTING', raising=False)
    monkeypatch.delenv('WTF_CSRF_ENABLED', raising=False)
    assert get_configuration() == {
        'SQLALCHEMY_DATABASE_URI': 'sqlite://',
        'SQLALCHEMY_ECHO': False,
        'TESTING': False,
        'WTF_CSRF_ENABLED': True,
    }

    # All environment variables set
    monkeypatch.setenv('SQLALCHEMY_DATABASE_URI', 'sqlite:////tmp/app.db')
    monkeypatch.setenv('SQLALCHEMY_ECHO', 'True')
    monkeypatch.setenv('FLASK_TESTING', 'True')
    monkeypatch.setenv('WTF_CSRF_ENABLED', 'False')
    assert get_configuration() == {
        'SQLALCHEMY_DATABASE_URI': 'sqlite:////tmp/app.db',
        'SQLALCHEMY_ECHO': True,
        'TESTING': True,
        'WTF_CSRF_ENABLED': False,
    }


def test_handle_routing_http_exception(app, client, rendered_templates):
    response = client.get('/route/not/found/')
    assert response.status_code == 404
    assert response.mimetype == 'text/html'
    assert len(rendered_templates) == 1
    template, context = rendered_templates[0]
    assert template.name == 'web/exception.html'
    assert 'exception' in context
    assert isinstance(context['exception'], NotFound)
