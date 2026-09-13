import unittest
from crawl import normalize_url, get_heading_from_html, get_first_paragraph_from_html, get_urls_from_html, \
    extract_page_data


class TestCrawl(unittest.TestCase):
    def test_normalize_url(self):
        input_url = "https://www.boot.dev/blog/path"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_get_heading_from_html_basic(self):
        input_body = "<html><body><h1>Test Title</h1></body></html>"
        actual = get_heading_from_html(input_body)
        expected = "Test Title"
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_main_priority(self):
        input_body = """<html><body>
            <p>Outside paragraph.</p>
            <main>
                <p>Main paragraph.</p>
            </main>
        </body></html>"""
        actual = get_first_paragraph_from_html(input_body)
        expected = "Main paragraph."
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_absolute(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="https://crawler-test.com"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_relative(self):
        input_url = "https://crawler-test.com/path"
        input_body = '<html><body><a href="/path/to/page"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/path/to/page"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_multiple(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="https://crawler-test.com/path"><span>Boot.dev</span></a><a href="/path/to/page"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/path", "https://crawler-test.com/path/to/page"]
        self.assertEqual(actual, expected)

    def test_extract_page_data_legacy(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><h1>Test Title</h1><p>Test paragraph.</p><a href="https://crawler-test.com/path"><span>Boot.dev</span></a></body></html>'
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "Test Title",
            "first_paragraph": "Test paragraph.",
            "outgoing_links": ["https://crawler-test.com/path"],
            "image_urls": [],
        }
        self.assertEqual(actual, expected)

    def test_extract_page_data_basic(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
            <h1>Test Title</h1>
            <p>This is the first paragraph.</p>
            <a href="/link1">Link 1</a>
            <img src="/image1.jpg" alt="Image 1">
        </body></html>"""
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "Test Title",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": ["https://crawler-test.com/link1"],
            "image_urls": ["https://crawler-test.com/image1.jpg"],
        }
        self.assertEqual(actual, expected)

    # normalize_url
    def test_normalize_url_trailing_slash(self):
        self.assertEqual(normalize_url("https://boot.dev/path/"), "boot.dev/path")

    def test_normalize_url_no_path(self):
        self.assertEqual(normalize_url("https://boot.dev"), "boot.dev")

    def test_normalize_url_http(self):
        self.assertEqual(normalize_url("http://boot.dev/page"), "boot.dev/page")

    # get_heading_from_html
    def test_get_heading_from_html_no_h1(self):
        self.assertIsNone(get_heading_from_html("<html><body><p>No heading</p></body></html>"))

    def test_get_heading_from_html_multiple_h1(self):
        self.assertEqual(
            get_heading_from_html("<html><body><h1>First</h1><h1>Second</h1></body></html>"),
            "First"
        )

    # get_first_paragraph_from_html
    def test_get_first_paragraph_no_main(self):
        self.assertEqual(
            get_first_paragraph_from_html("<html><body><p>Only paragraph.</p></body></html>"),
            "Only paragraph."
        )

    def test_get_first_paragraph_no_paragraph(self):
        self.assertIsNone(get_first_paragraph_from_html("<html><body><h1>Title</h1></body></html>"))

    def test_get_first_paragraph_main_no_p(self):
        self.assertEqual(
            get_first_paragraph_from_html("<html><body><p>Outside.</p><main><span>No p here.</span></main></body></html>"),
            "Outside."
        )

    # get_urls_from_html
    def test_get_urls_from_html_no_links(self):
        self.assertEqual(get_urls_from_html("<html><body><p>No links.</p></body></html>", "https://boot.dev"), [])

    def test_get_urls_from_html_relative_no_leading_slash(self):
        actual = get_urls_from_html('<a href="page">x</a>', "https://boot.dev")
        self.assertEqual(actual, ["https://boot.dev/page"])

    # extract_page_data
    def test_extract_page_data_no_heading(self):
        actual = extract_page_data("<html><body><p>Para.</p></body></html>", "https://boot.dev")
        self.assertIsNone(actual["heading"])

    def test_extract_page_data_url_preserved(self):
        actual = extract_page_data("<html><body></body></html>", "https://boot.dev/page")
        self.assertEqual(actual["url"], "https://boot.dev/page")

    def test_extract_page_data_no_links(self):
        actual = extract_page_data("<html><body><p>Para.</p></body></html>", "https://boot.dev")
        self.assertEqual(actual["outgoing_links"], [])

    def test_extract_page_data_with_links(self):
        actual = extract_page_data('<html><body><a href="page">Link</a></body></html>', "https://boot.dev")
        self.assertEqual(actual["outgoing_links"], ["https://boot.dev/page"])


if __name__ == "__main__":
    unittest.main()