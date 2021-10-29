from url_shortener.models import ShortURL


def test_shorturl_repr():
    instance = ShortURL(slug='Ab1Cd2')
    assert repr(instance) == '<ShortURL {}>'.format(repr(instance.slug))
