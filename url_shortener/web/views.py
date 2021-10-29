from flask import redirect, render_template, url_for

from url_shortener.core import generate_slug
from url_shortener.models import ShortURL, db
from url_shortener.web.forms import ShortURLForm


def handle_http_exception(exception):
    return (
        render_template('web/exception.html', exception=exception),
        exception.code
    )


def index():
    form = ShortURLForm()
    if form.validate_on_submit():
        # Generate unique slug and store in database
        while True:
            slug = generate_slug(length=6)
            if db.session.query(ShortURL.id).filter_by(slug=slug).first() is None:
                short_url = ShortURL(slug=slug)
                form.populate_obj(short_url)
                db.session.add(short_url)
                db.session.commit()
                break

        # Redirect to url preview view
        return redirect(url_for('web.url_preview', slug=slug))

    # Render form with a list of all short URLs
    short_urls = db.session.query(
        ShortURL.slug, ShortURL.target_url, ShortURL.visit_count
    ).filter_by(public=True).order_by(ShortURL.created_at.desc()).limit(10).all()
    return render_template('web/index.html', form=form, short_urls=short_urls)


def url_preview(slug):
    short_url = db.session.query(ShortURL).filter_by(slug=slug).first_or_404()
    return render_template('web/url_preview.html', short_url=short_url)


def url_redirect(slug):
    short_url = db.session.query(ShortURL).filter_by(slug=slug).first_or_404()

    # Grab target URL
    target_url = short_url.target_url

    # Increment visit count
    short_url.visit_count = ShortURL.visit_count + 1
    db.session.commit()

    # Redirect to target URL
    return redirect(target_url)
