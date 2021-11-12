from werkzeug.datastructures import MultiDict
from wtforms.fields import URLField

from url_shortener.web.forms import BaseFlaskForm, ShortURLForm
from url_shortener.web.form_filters import prepend_http, strip_value


def test_base_flask_form_bind_field(app):
    class TestForm(BaseFlaskForm):
        url = URLField('URL', filters=[prepend_http])

    # Create instance once
    form_data = MultiDict({'url': 'http://www.example.com/  '})
    form = TestForm(form_data, meta={'csrf': False})
    assert form.url.filters == [strip_value, prepend_http]
    assert form.data == {'url': 'http://www.example.com/'}

    # Create instance twice
    form_data = MultiDict({'url': '  http://www.example.com/'})
    form = TestForm(form_data, meta={'csrf': False})
    assert form.url.filters == [strip_value, prepend_http]
    assert form.data == {'url': 'http://www.example.com/'}


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
