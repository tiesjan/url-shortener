from url_shortener.database import db
from url_shortener.database.functions import utc_now


class ShortURL(db.Model):
    __tablename__ = 'short_url'

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(50), nullable=False, unique=True)
    target_url = db.Column(db.String(500), nullable=False)
    public = db.Column(db.Boolean, nullable=False)
    visit_count = db.Column(db.Integer, nullable=False, server_default=db.text('0'))
    created_at = db.Column(db.DateTime, nullable=False, server_default=utc_now())

    def __repr__(self):
        return '<ShortURL %r>' % self.slug
