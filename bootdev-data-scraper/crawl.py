from urllib.parse import urlparse
from bs4 import BeautifulSoup
import asyncio
import aiohttp


class AsyncCrawler:
    def __init__(self, base_url, max_concurrency=10):
        self.base_url = base_url
        self.base_domain = urlparse(base_url).netloc
        self.page_data = {}
        self.visited = set()
        self.lock = asyncio.Lock()
        self.max_concurrency = max_concurrency
        self.semaphore = asyncio.Semaphore(max_concurrency)
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def add_page_visit(self, normalized_url):
        async with self.lock:
            if normalized_url in self.visited:
                return False
            self.visited.add(normalized_url)
            return True

    async def get_html(self, url):
        async with self.semaphore:
            async with self.session.get(url, headers={"User-Agent": "BootCrawler/1.0"}) as r:
                if r.status in (400, 404):
                    raise Exception("Bad request")
                if not r.headers.get('Content-Type', '').startswith('text/html'):
                    raise Exception("Not HTML")
                return await r.text()

    async def crawl_page(self, current_url):
        if urlparse(current_url).netloc != self.base_domain:
            return
        normalized_current = normalize_url(current_url)
        if not await self.add_page_visit(normalized_current):
            return
        try:
            print(f"Crawling: {current_url}")
            html = await self.get_html(current_url)
            data = extract_page_data(html, current_url)
            async with self.lock:
                self.page_data[normalized_current] = data
            print(f"Heading: {data['heading']}, First Paragraph: {data['first_paragraph']}")
            tasks = [asyncio.create_task(self.crawl_page(link)) for link in data['outgoing_links']]
            await asyncio.gather(*tasks)
        except Exception as e:
            print(f"Error crawling {current_url}: {e}")

    async def crawl(self):
        await self.crawl_page(self.base_url)
        return self.page_data


async def crawl_site_async(base_url):
    async with AsyncCrawler(base_url) as crawler:
        return await crawler.crawl()

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