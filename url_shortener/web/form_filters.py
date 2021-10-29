def prepend_http(value):
    valid_schemas = ('http://', 'https://')
    if value is not None and len(value) and not value.startswith(valid_schemas):
        return 'http://{}'.format(value)
    else:
        return value


def strip_value(value):
    if value is not None and hasattr(value, 'strip'):
        return value.strip()
    else:
        return value
