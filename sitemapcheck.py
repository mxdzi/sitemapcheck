import argparse
from xml.etree import ElementTree

import requests
from requests.auth import HTTPBasicAuth, HTTPDigestAuth

version = 1.7


class SitemapCheck:
    def __init__(self, url, *, login=None, password=None, auth=None, method='GET', verbose=False):
        self.url = url
        self.login = login
        self.password = password
        self.auth = auth
        self.method = method
        self.verbose = verbose
        self.urls = []
        self.results = []
        self.errors = 0

    def check(self):
        auth = self._get_auth()
        result = requests.request('GET', self.url, auth=auth)
        if result.status_code == 200:
            self._parse_xml(result.text)
            self._check_urls()

    def _parse_xml(self, sitemap):
        sitemap_xml = ElementTree.fromstring(sitemap)
        for loc in sitemap_xml:
            self.urls.append(loc[0].text)
        if self.verbose:
            print(f"Found: {len(self.urls)} urls")

    def _check_urls(self):
        auth = self._get_auth()
        session = requests.Session()
        session.auth = auth
        for url in self.urls:
            result = session.request(self.method, url, auth=auth)
            self.results.append((result.status_code, url))
            if result.status_code >= 400:
                self.errors += 1
            if self.verbose:
                print(result.status_code, url)

    def _get_auth(self):
        if self.auth == 'basic':
            auth = HTTPBasicAuth(self.login, self.password)
        elif self.auth == 'digest':
            auth = HTTPDigestAuth(self.login, self.password)
        else:
            auth = None
        return auth


def main(args):
    sitemapcheck = SitemapCheck(url=args.url, login=args.login, password=args.password, auth=args.auth,
                                method=args.method, verbose=args.verbose)
    sitemapcheck.check()

    if not args.verbose:
        print(f"Found: {len(sitemapcheck.urls)} urls")
        for status_code, url in sitemapcheck.results:
            print(status_code, url)

    all = len(sitemapcheck.urls)
    tested = len(sitemapcheck.results)
    percent = ((tested - sitemapcheck.errors) / all) * 100 if all else 0
    print(f"Tested {tested} of {all}, {percent}% correct.")


if __name__ == "__main__":  # pragma: nocover
    parser = argparse.ArgumentParser(prog="SitemapCheck")
    parser.add_argument('url', metavar='URL', help='Full URL to sitemap file ex: "https://example.com/sitemap.xml"')
    parser.add_argument('--login', '-l', nargs='?', help='login')
    parser.add_argument('--password', '-p', nargs='?', help='password')
    parser.add_argument('--auth', '-a', choices=['basic', 'digest'], help='Auth method')
    parser.add_argument('--method', '-m', choices=['GET', 'HEAD'], default='GET', help='HTTP method for checking urls')
    parser.add_argument('--verbose', '-v', action="store_true", help="Show results in realtime")
    parser.add_argument('--version', '-V', action='version', version=f"%(prog)s {version}")
    args = parser.parse_args()
    main(args)
