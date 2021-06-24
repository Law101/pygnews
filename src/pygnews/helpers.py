# Import Neccessary Libraries
import requests
import urllib
import feedparser
from bs4 import BeautifulSoup
import dateparser

# import json


def set_ceid(country="US", language="en"):

    """Set the base country and language for the RSS Feed

    Args:
        country (str, optional): Country abbreviation. Defaults to "US".
        language (str, optional): Country Language abbreviation. Defaults to "en".

    Returns:
        ceid (str): acceptable RSS feed query string.
    """

    ceid = "?ceid={country}:{language}&hl={language}&gl={country}".format(
        country=country, language=language
    )
    return ceid


def feed_parser(feedURL):
    """Use Feedparser to Extract Feeds from the specified URL.

    Args:
        feedURL (str): URL to extract feeds from

    Raises:
        Exception: when feed is not available.

    Returns:
        dict: a dictionary object with feed and entries as keys.
    """

    # Check if it's a supported URL
    request_feed = requests.get(feedURL)
    if "https://news.google.com/rss/unsupported" in request_feed.url:
        raise Exception("Feed not Available")

    parser = feedparser.parse(request_feed.text)

    # Return Only Feed and Entries from the parse dictionary
    return dict((k, parser[k]) for k in ("feed", "entries"))


def topStories_parser(text_dict):
    """Extracts relevant infomation from feed Entries

    Args:
        text_dict (dict): feed Entity to extract information from.

    Returns:
        coverage (dict): a dictionary containing extracted information.
    """

    summary = text_dict["summary"]
    bs4_html = BeautifulSoup(summary, "html.parser")
    lis = bs4_html.find_all("li")

    # Create an empty list to collect news cluster
    coverage = list()

    if len(lis) == 0:
        try:
            coverage.append(
                {
                    "url": bs4_html.a["href"],
                    "title": bs4_html.a.text,
                    "publisher": bs4_html.font.text,
                    "published_date": text_dict["published"],
                }
            )

        except:
            pass
    else:
        for li in lis:
            try:
                coverage.append(
                    {
                        "url": li.a["href"],
                        "title": li.a.text,
                        "publisher": li.font.text,
                        "published_date": text_dict["published"],
                    }
                )
            except:
                pass

    return coverage


def collect_coverage(entries):
    """Extract sub news and collate them together.

    Args:
        entries (dict): feed entries

    Returns:
        entries_dict (dict): news coverage collection
    """

    entries_dict = dict()
    for i, _ in enumerate(entries):
        if "summary" in entries[i].keys():
            # Use topStories_parser to extract information from entries
            entries_dict[i] = topStories_parser(entries[i])
        else:
            print("News Summary Not Available")

    return entries_dict


def search_parser(search_query):
    """Construct URL from search query

    Args:
        search_query (str): Search Querry supplied by user.

    Returns:
        parsed_url (str): Passed URL
    """
    parsed_url = urllib.parse.quote_plus(search_query)
    return parsed_url


def date_parser(date=None):
    """Validate date and extract Year, Month and Day

    Args:
        date (str, optional): Date to be parsed. Defaults to None.

    Raises:
        Exception: When invalid date pattern is parsed

    Returns:
        valid_date (str): Extracted Date
    """
    try:
        valid_date = dateparser.parse(date).strftime("%Y-%m-%d")
        return str(valid_date)
    except:
        raise Exception("Could not parse date")
