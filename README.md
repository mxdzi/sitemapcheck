# sitemapcheck

A simple Python script for checking urls in sitemap.xml file.

## How to use

To check urls in sitemap pass url to sitemap.xml as first argument:

    sitemapcheck.py https://example.com/sitemap.xml

Options:
`--help` - show help message
`--method` - use GET or HEAD method for checkking urls (defaults to GET)  
`--login`, `--password`, `--auth` - use for password protected sites  
`--verbose` - use to show results realtime

## Tests

Run tests with:

    pytest --cov=sitemapcheck --cov-report html
