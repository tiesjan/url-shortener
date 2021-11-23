from url_shortener.form_filters import prepend_http, strip_value


def test_prepend_http():
    assert prepend_http('example.com/') == 'http://example.com/'
    assert prepend_http('http://example.com/') == 'http://example.com/'
    assert prepend_http('https://example.com/') == 'https://example.com/'
    assert prepend_http('') == ''
    assert prepend_http(None) is None


def test_strip_value():
    assert strip_value('   example ') == 'example'
    assert strip_value('example') == 'example'
    assert strip_value('') == ''
    assert strip_value(None) is None
