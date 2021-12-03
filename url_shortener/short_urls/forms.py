from ipaddress import ip_address
from urllib.parse import urlsplit

from flask_wtf import FlaskForm
from wtforms.fields import BooleanField, URLField
from wtforms.validators import InputRequired, Optional, URL, ValidationError

from url_shortener.form_filters import prepend_http, strip_value


class ShortURLForm(FlaskForm):
    target_url = URLField(
        'Target URL',
        filters=[strip_value, prepend_http],
        validators=[InputRequired(), URL()],
    )
    public = BooleanField(
        'Make short URL public',
        default=True,
        filters=[],
        validators=[Optional()],
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
