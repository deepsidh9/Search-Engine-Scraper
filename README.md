[![Downloads](https://pepy.tech/badge/search-engine-scraper)](https://pepy.tech/project/search-engine-scraper) [![Downloads](https://pepy.tech/badge/search-engine-scraper/month)](https://pepy.tech/project/search-engine-scraper/month)
# Search-Engine-Scraper
A module to scrape popular search engines

## Capabilities

The very first version can do the following:
* Query and get results for google,bing and yahoo.
* Scrape 20 free proxies and randomly select one before querying the search engine.
  * This scraping will happen after 15 minutes since the last scraping was done.
* Randomize an user agent for the query run.

## Usage and Installation
Python 3.6+ is required

Install via pip:

`pip install search-engine-scraper`

Import the search engines as :

`from search_engine_scraper import google_search,bing_search,yahoo_search`

Run query as :

`google_search.search("your text here , search for whatever you wish")`
