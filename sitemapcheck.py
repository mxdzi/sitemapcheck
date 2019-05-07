import sys
from xml.etree import ElementTree

import requests


class SitemapCheck:
    def __init__(self, url):
        self.url = url

    def check(self):
        result = requests.request('GET', self.url)
        if result.status_code == 200:
            sitemap_xml = ElementTree.fromstring(result.text)

            urls = []
            for loc in sitemap_xml:
                urls.append(loc[0].text)

            print("Found: {} urls".format(len(urls)))

            for url in urls:
                result = requests.request('GET', url)
                print(result.status_code, url)


def main(args):
    if len(args):
        sitemapcheck = SitemapCheck(args[0])
        sitemapcheck.check()


if __name__ == "__main__":  # pragma: nocover
    main(sys.argv[1:])
