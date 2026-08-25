from urllib.parse import urlparse

def normalize_url(url):
    """
    Normalize a URL by removing the scheme and trailing slash.
    """
    parsed_url = urlparse(url)
    normalized_url = parsed_url.netloc + parsed_url.path.rstrip('/')
    return normalized_url