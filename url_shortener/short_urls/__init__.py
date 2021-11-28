from flask import Blueprint

from .views import index, url_preview, url_redirect


blueprint = Blueprint('short_urls', __name__)

blueprint.add_url_rule('/', view_func=index, methods=('GET', 'POST'))
blueprint.add_url_rule('/<slug>+', view_func=url_preview, methods=('GET',))
blueprint.add_url_rule('/<slug>', view_func=url_redirect, methods=('GET',))
