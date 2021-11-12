from ipaddress import ip_address
from urllib.parse import urlsplit

from flask_wtf import FlaskForm
from wtforms.fields import BooleanField, URLField
from wtforms.validators import DataRequired, URL, ValidationError

from url_shortener.web.form_filters import prepend_http, strip_value


class BaseFlaskForm(FlaskForm):
    class Meta:
        def bind_field(self, form, unbound_field, options):
            filters = unbound_field.kwargs.get('filters', [])
            if strip_value not in filters:
                filters.insert(0, strip_value)
            return unbound_field.bind(form=form, filters=filters, **options)


class ShortURLForm(BaseFlaskForm):
    target_url = URLField(
        'Target URL',
        filters=[prepend_http],
        validators=[DataRequired(), URL()]
    )
    public = BooleanField(
        'Make short URL public',
        default=True,
    )

    def validate_target_url(self, field):
        url_parts = urlsplit(field.data)
        try:
            ip = ip_address(url_parts.netloc)
        except ValueError:
            pass
        else:
            if not ip.is_global:
                raise ValidationError('Invalid URL.')
