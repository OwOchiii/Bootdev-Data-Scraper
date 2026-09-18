import sys
import asyncio
from crawl import crawl_site_async


async def main():
    if len(sys.argv) < 2:
        print("no website provided")
        sys.exit(1)
    if len(sys.argv) > 4:
        print("too many arguments provided")
        sys.exit(1)
    url = sys.argv[1]
    max_concurrency = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    max_pages = int(sys.argv[3]) if len(sys.argv) > 3 else 100
    print(f"starting crawl of:{url} (max_concurrency={max_concurrency}, max_pages={max_pages})")
    page_data = await crawl_site_async(url, max_concurrency, max_pages)
    for data in page_data.values():
        print(f"URL: {data['url']}, Heading: {data['heading']}, First Paragraph: {data['first_paragraph']}")


if __name__ == "__main__":
    asyncio.run(main())
