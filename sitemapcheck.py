import argparse
from xml.etree import ElementTree

import requests

version = 1.0

class SitemapCheck:
    def __init__(self, url):
        self.url = url

    def check(self):
        result = requests.request('GET', self.url)
        if result.status_code == 200:
            self._parse_xml(result.text)
            self._check_urls()

    def _parse_xml(self, sitemap):
        sitemap_xml = ElementTree.fromstring(sitemap)
        self.urls = []
        for loc in sitemap_xml:
            self.urls.append(loc[0].text)
        print("Found: {} urls".format(len(self.urls)))

    def _check_urls(self):
        for url in self.urls:
            result = requests.request('GET', url)
            print(result.status_code, url)


def main(args):
    if args.URL:
        sitemapcheck = SitemapCheck(args.URL)
        sitemapcheck.check()


if __name__ == "__main__":  # pragma: nocover
    parser = argparse.ArgumentParser(prog="SitemapCheck")
    parser.add_argument('URL', help='Full URL to sitemap file ex: "https://example.com/sitemap.xml"')
    parser.add_argument('--version', '-v', action='version', version=f"%(prog)s {version}")
    args = parser.parse_args()
    main(args)
