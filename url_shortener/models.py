from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
migrate = Migrate()


class ShortURL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(50), unique=True, nullable=False)
    target_url = db.Column(db.String(500), nullable=False)
    public = db.Column(db.Boolean, nullable=False)
    visit_count = db.Column(db.Integer, nullable=False, server_default=db.text('0'))
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        return '<ShortURL %r>' % self.slug
