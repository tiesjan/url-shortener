from url_shortener.short_urls.slugs import generate_slug


def test_generate_slug(monkeypatch):
    return_values = ['A', 'b', '1', '1', 'C', 'd', '2', '2']

    def generate_value(*args):
        return return_values.pop(0)
    monkeypatch.setattr('random.SystemRandom.choice', generate_value)

    assert generate_slug() == 'Ab1Cd2'
