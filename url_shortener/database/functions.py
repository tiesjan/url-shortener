from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql import expression

from url_shortener.database import db


class utc_now(expression.FunctionElement):
    type = db.DateTime()


@compiles(utc_now, 'postgresql')
def utc_now_postgresql(element, compiler, **kwargs):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"
