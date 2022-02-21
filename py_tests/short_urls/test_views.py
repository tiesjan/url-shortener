from datetime import datetime, timedelta

from flask import request, url_for
from werkzeug.datastructures import MultiDict

from url_shortener.database import db
from url_shortener.database.models import ShortURL
from url_shortener.short_urls.forms import ShortURLForm
from url_shortener.short_urls.slugs import generate_slug


def test_index_retrieve(client, rendered_templates):
    # Create 2 public and 1 private ShortURL instances
    short_url1 = ShortURL(
        slug=generate_slug(), target_url='http://www1.example.com/',
        public=True, created_at=datetime.utcnow() - timedelta(days=3)
    )
    db.session.add(short_url1)
    short_url2 = ShortURL(
        slug=generate_slug(), target_url='http://www2.example.com/',
        public=True, created_at=datetime.utcnow() - timedelta(days=2)
    )
    db.session.add(short_url2)
    short_url3 = ShortURL(
        slug=generate_slug(), target_url='http://www3.example.com/',
        public=False, created_at=datetime.utcnow() - timedelta(days=1)
    )
    db.session.add(short_url3)
    db.session.commit()

    # Perform request and assert response
    response = client.get(url_for('short_urls.index'))
    assert response.status_code == 200
    assert response.mimetype == 'text/html'
    assert len(rendered_templates) == 1
    template, context = rendered_templates[0]
    assert template.name == 'short_urls/index.html'
    assert 'form' in context
    assert isinstance(context['form'], ShortURLForm)
    assert 'latest_short_urls' in context
    assert context['latest_short_urls'] == [
        (short_url2.slug, short_url2.target_url, short_url2.visit_count),
        (short_url1.slug, short_url1.target_url, short_url1.visit_count),
    ]


def test_index_create(client, monkeypatch, rendered_templates):
    # Create a ShortURL instance
    short_url = ShortURL(
        slug='Ab1Cd2', target_url='http://www1.example.com/',
        public=True, created_at=datetime.utcnow() - timedelta(days=1)
    )
    db.session.add(short_url)
    db.session.commit()

    # Monkey patch slug generator
    return_values = [
        'A', 'b', '1', 'C', 'd', '2',  # Same as ShortURL instance above
        'E', 'f', '3', 'G', 'h', '4',
    ]

    def generate_value(*args):
        return return_values.pop(0)
    monkeypatch.setattr('random.SystemRandom.choice', generate_value)

    # Perform request and assert response/state
    request_data = MultiDict({
        'target_url': 'http://www2.example.com/', 'public': ''
    })
    response = client.post(url_for('short_urls.index'), data=request_data)
    assert response.status_code == 302
    assert response.location == '{}://{}{}'.format(
        request.scheme, request.host, url_for('short_urls.url_preview', slug='Ef3Gh4')
    )
    short_urls = db.session.query(ShortURL).order_by('id').all()
    assert len(short_urls) == 2
    assert short_urls[0].slug == 'Ab1Cd2'
    assert short_urls[0].target_url == 'http://www1.example.com/'
    assert short_urls[0].public is True
    assert short_urls[1].slug == 'Ef3Gh4'
    assert short_urls[1].target_url == 'http://www2.example.com/'
    assert short_urls[1].public is False


def test_url_preview(client, rendered_templates):
    # Create ShortURL instance
    short_url = ShortURL(
            slug=generate_slug(), target_url='http://example.com/', public=True)
    db.session.add(short_url)
    db.session.commit()

    # Perform request and assert response
    response = client.get(url_for('short_urls.url_preview', slug=short_url.slug))
    assert response.status_code == 200
    assert response.mimetype == 'text/html'
    assert len(rendered_templates) == 1
    template, context = rendered_templates[0]
    assert template.name == 'short_urls/url_preview.html'
    assert 'short_url' in context
    assert context['short_url'] == short_url


def test_url_redirect(client):
    # Create ShortURL instance
    short_url = ShortURL(
            slug=generate_slug(), target_url='http://example.com/', public=True)
    db.session.add(short_url)
    db.session.commit()

    # Perform request and assert response/state
    response = client.get(url_for('short_urls.url_redirect', slug=short_url.slug))
    assert response.status_code == 302
    assert response.location == short_url.target_url
    assert short_url.visit_count == 1

    # Perform request again and assert response/state
    response = client.get(url_for('short_urls.url_redirect', slug=short_url.slug))
    assert response.status_code == 302
    assert response.location == short_url.target_url
    assert short_url.visit_count == 2
