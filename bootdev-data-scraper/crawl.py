from urllib.parse import urlparse
from bs4 import BeautifulSoup, Tag

def normalize_url(url):
    """
    Normalize a URL by removing the scheme and trailing slash.
    """
    parsed_url = urlparse(url)
    normalized_url = parsed_url.netloc + parsed_url.path.rstrip('/')
    return normalized_url

def get_heading_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    heading = soup.find('h1')
    if heading:
        return heading.get_text()
    return None

def get_first_paragraph_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    main = soup.find('main')
    paragraph = main.find('p') if main else None
    if not paragraph:
        paragraph = soup.find('p')
    if paragraph:
        return paragraph.get_text()
    return None