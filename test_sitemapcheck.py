from unittest.mock import MagicMock, patch

from sitemapcheck import main, SitemapCheck, HTTPBasicAuth, HTTPDigestAuth


@patch('sitemapcheck.requests.Session.request')
def test_main(mock_session, capsys):
    mock_response_xml = MagicMock()
    mock_response_xml.status_code = 200
    mock_response_xml.text = """<?xml version="1.0" encoding="UTF-8"?>
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
        <url>
            <loc>https://example.com/</loc>
            <lastmod>2019-01-01</lastmod>
        </url>
        <url>
            <loc>https://example.com/site.html</loc>
            <lastmod>2019-01-02</lastmod>
        </url>
    </urlset>
    """
    mock_session.side_effect = [mock_response_xml, MagicMock(status_code=200), MagicMock(status_code=200)]

    args = MagicMock()
    args.URL = "https://example.com/sitemap.xml"

    main(args)
    captured = capsys.readouterr()
    output = ("Found: 2 urls\n"
              "200 https://example.com/\n"
              "200 https://example.com/site.html\n"
              "Tested 2 of 2, 100.0% correct.\n")
    assert captured.out == output


@patch('sitemapcheck.requests.Session.request')
def test_main_not_verbose(mock_session, capsys):
    mock_response_xml = MagicMock()
    mock_response_xml.status_code = 200
    mock_response_xml.text = """<?xml version="1.0" encoding="UTF-8"?>
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
        <url>
            <loc>https://example.com/</loc>
            <lastmod>2019-01-01</lastmod>
        </url>
        <url>
            <loc>https://example.com/site.html</loc>
            <lastmod>2019-01-02</lastmod>
        </url>
    </urlset>
    """
    mock_session.side_effect = [mock_response_xml, MagicMock(status_code=200), MagicMock(status_code=404)]

    args = MagicMock()
    args.URL = "https://example.com/sitemap.xml"
    args.verbose = False

    main(args)
    captured = capsys.readouterr()
    output = ("Found: 2 urls\n"
              "200 https://example.com/\n"
              "404 https://example.com/site.html\n"
              "Tested 2 of 2, 50.0% correct.\n")
    assert captured.out == output


def test_main_basic_auth():
    checker = SitemapCheck(url="", login="user", password="password", auth="basic")
    assert isinstance(checker._get_auth(), HTTPBasicAuth)
    assert checker._get_auth() == HTTPBasicAuth("user", "password")


def test_main_digest_auth():
    checker = SitemapCheck(url="", login="user", password="password", auth="digest")
    assert isinstance(checker._get_auth(), HTTPDigestAuth)
    assert checker._get_auth() == HTTPDigestAuth("user", "password")
