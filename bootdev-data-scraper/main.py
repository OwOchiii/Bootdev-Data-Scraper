import sys
from crawl import get_html, crawl_page


def main():
    if len(sys.argv) > 2:
        print("too many arguments provided")
        sys.exit(1)
    if len(sys.argv) < 2:
        print("no website provided")
        sys.exit(1)
    url = sys.argv[1]
    print("starting crawl of:" + url)
    page_data = crawl_page(url)
    for url, data in page_data.items():
        print(f"URL: {url}, Heading: {data['heading']}, First Paragraph: {data['first_paragraph']}")


if __name__ == "__main__":
    main()
