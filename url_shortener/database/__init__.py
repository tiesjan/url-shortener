from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.model import BindMetaMixin, Model
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base


naming_convention = {
    'ix': 'ix_%(column_0_N_label)s',
    'uq': 'uq_%(table_name)s_%(column_0_N_name)s',
    'ck': 'ck_%(table_name)s_%(constraint_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'pk': 'pk_%(table_name)s'
}
metadata = MetaData(naming_convention=naming_convention)


class SimpleMeta(BindMetaMixin, DeclarativeMeta):
    pass


session_options = {
    'expire_on_commit': False
}


db = SQLAlchemy(
    metadata=metadata,
    model_class=declarative_base(cls=Model, metaclass=SimpleMeta, name='Model'),
    session_options=session_options
)


migrate = Migrate()
