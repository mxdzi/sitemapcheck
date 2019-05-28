# sitemapcheck

A simple Python script for checking urls in sitemap.xml file.

## How to use

To check URLs in the sitemap, pass the URL to sitemap.xml as the first argument:

    sitemapcheck.py https://example.com/sitemap.xml

Options:

`--help` - show help message

`--method` - use GET or HEAD method for checking urls (defaults to GET)

`--login`, `--password`, `--auth` - use for password protected sites

`--verbose` - show results in realtime

## Tests

Run tests with:

    pytest --cov=sitemapcheck --cov-report html
