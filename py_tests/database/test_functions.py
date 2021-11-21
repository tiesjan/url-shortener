from url_shortener.database.functions import utc_now_postgresql


def test_utc_now_postgresql():
    assert utc_now_postgresql(None, None) == "TIMEZONE('utc', CURRENT_TIMESTAMP)"
