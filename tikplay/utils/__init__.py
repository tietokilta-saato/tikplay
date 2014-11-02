def is_uri(uri):
    return uri.find(":") != -1 and len(uri) > 3


def is_url(uri):
    return uri.startswith(("http://", "https://"))