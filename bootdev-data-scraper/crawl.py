from urllib import request
from urllib.parse import urlparse
from bs4 import BeautifulSoup, Tag
import requests


def get_html(url):
    r = requests.get(url, headers={"User-Agent": "BootCrawler/1.0"})
    if r.status_code == 400 or r.status_code == 404:
        raise Exception("Bad request")
    if r.headers['Content-Type'] != 'text/html':
        raise Exception("Not HTML")
    return r.text

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

def get_urls_from_html(html, base_url):
    soup = BeautifulSoup(html, 'html.parser')
    urls = []
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if href.startswith('http'):
            urls.append(href)
        else:
            # Handle relative URLs
            parsed_base_url = urlparse(base_url)
            normalized_base_url = parsed_base_url.scheme + "://" + parsed_base_url.netloc
            full_url = normalized_base_url + href if href.startswith('/') else normalized_base_url + '/' + href
            urls.append(full_url)
    return urls

def get_img_urls_from_html(html,input_url):
    soup = BeautifulSoup(html, 'html.parser')
    img_urls = []
    for img_tag in soup.find_all('img', src=True):
        img_urls.append(input_url + img_tag['src'])
    return img_urls

def extract_page_data(input_body, input_url):
    return dict(
        url=input_url,
        heading=get_heading_from_html(input_body),
        first_paragraph=get_first_paragraph_from_html(input_body),
        outgoing_links=get_urls_from_html(input_body, input_url),
        image_urls=get_img_urls_from_html(input_body,input_url),
    )