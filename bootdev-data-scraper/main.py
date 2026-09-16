import sys
import asyncio
from crawl import crawl_site_async


async def main():
    if len(sys.argv) > 2:
        print("too many arguments provided")
        sys.exit(1)
    if len(sys.argv) < 2:
        print("no website provided")
        sys.exit(1)
    url = sys.argv[1]
    print("starting crawl of:" + url)
    page_data = await crawl_site_async(url)
    for data in page_data.values():
        print(f"URL: {data['url']}, Heading: {data['heading']}, First Paragraph: {data['first_paragraph']}")


if __name__ == "__main__":
    asyncio.run(main())
