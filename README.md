# PyGNews :: Overview

![PyGNews](./docs/static/img/logoColored.png)

_Python Library for Scrapping Google News Feeds._

Source Code: [https://github.com/Law101/pygnews/](**https://github.com/Law101/pygnews/**)

## Requirements

Python 3.6+ and ```pip```

PyGNews rest fully on:

* [Feedparser](https://pypi.org/project/feedparser/)
* [Requests](https://pypi.org/project/requests/)
* [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/)

You don't need to install these separately, running the pip install below handles everything for you.

## Installation

```shell
pip install pygnews
```

## Example

```python
# Import the Fetching Module
from pygnews import fetcher

# Create Fetching instance
news = fetcher.PyGNews()

# Get stop stories from Google News
print(news.top_stories())
```

## License

This project is licensed under the terms of the MIT license.
