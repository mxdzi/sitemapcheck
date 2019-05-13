from unittest.mock import MagicMock, patch

from sitemapcheck import main


@patch('sitemapcheck.requests')
def test_main(mock_requests, capsys):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = """<?xml version="1.0" encoding="UTF-8"?>
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
    mock_requests.request.return_value = mock_response

    args = MagicMock()
    args.URL = "https://example.com/sitemap.xml"

    main(args)
    captured = capsys.readouterr()
    output = ("Found: 2 urls\n"
              "200 https://example.com/\n"
              "200 https://example.com/site.html\n"
              "Tested 2 of 2, 100.0% correct.\n")
    assert captured.out == output


@patch('sitemapcheck.requests')
def test_main_not_verbose(mock_requests, capsys):
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
    mock_requests.request.side_effect = [mock_response_xml, MagicMock(status_code=200), MagicMock(status_code=404)]

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


@patch('sitemapcheck.requests')
def test_main_basic_auth(mock_requests, capsys):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = """<?xml version="1.0" encoding="UTF-8"?>
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
    mock_requests.request.return_value = mock_response

    args = MagicMock()
    args.URL = "https://example.com/sitemap.xml"
    args.login = "user"
    args.password = "password"
    args.auth = "basic"

    main(args)
    captured = capsys.readouterr()
    output = ("Found: 2 urls\n"
              "200 https://example.com/\n"
              "200 https://example.com/site.html\n"
              "Tested 2 of 2, 100.0% correct.\n")
    assert captured.out == output


@patch('sitemapcheck.requests')
def test_main_digest_auth(mock_requests, capsys):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = """<?xml version="1.0" encoding="UTF-8"?>
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
    mock_requests.request.return_value = mock_response

    args = MagicMock()
    args.URL = "https://example.com/sitemap.xml"
    args.login = "user"
    args.password = "password"
    args.auth = "digest"

    main(args)
    captured = capsys.readouterr()
    output = ("Found: 2 urls\n"
              "200 https://example.com/\n"
              "200 https://example.com/site.html\n"
              "Tested 2 of 2, 100.0% correct.\n")
    assert captured.out == output
