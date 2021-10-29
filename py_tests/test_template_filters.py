from url_shortener.template_filters import pluralize


def test_pluralize():
    assert pluralize(0) == 's'
    assert pluralize(1) == ''
    assert pluralize(2) == 's'
    assert pluralize(3) == 's'
