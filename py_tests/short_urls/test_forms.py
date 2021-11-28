from werkzeug.datastructures import MultiDict

from url_shortener.short_urls.forms import ShortURLForm


def test_shorturl_form_validate_target_url(app):
    # URL with domain
    form_data = MultiDict({'target_url': 'http://example.com/'})
    form = ShortURLForm(form_data, meta={'csrf': False})
    form.validate()
    assert form.errors == {}

    # URL with public IP address
    form_data = MultiDict({'target_url': 'http://1.2.3.4/'})
    form = ShortURLForm(form_data, meta={'csrf': False})
    form.validate()
    assert form.errors == {}

    # URL with private IP address
    form_data = MultiDict({'target_url': 'http://10.0.0.1/'})
    form = ShortURLForm(form_data, meta={'csrf': False})
    form.validate()
    assert form.errors == {'target_url': ['Invalid URL.']}
