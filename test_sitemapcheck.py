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

    main([""])
    captured = capsys.readouterr()
    output = ("Found: 2 urls\n"
              "200 https://example.com/\n"
              "200 https://example.com/site.html\n")
    assert captured.out == output