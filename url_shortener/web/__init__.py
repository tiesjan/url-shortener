from flask import Blueprint
from werkzeug.exceptions import HTTPException

from .views import handle_http_exception, index, url_preview, url_redirect


blueprint = Blueprint('web', __name__)

blueprint.add_url_rule('/', view_func=index, methods=('GET', 'POST'))
blueprint.add_url_rule('/<slug>+', view_func=url_preview, methods=('GET',))
blueprint.add_url_rule('/<slug>', view_func=url_redirect, methods=('GET',))

blueprint.register_error_handler(HTTPException, handle_http_exception)
