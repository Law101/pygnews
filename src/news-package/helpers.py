import requests
import urllib
import feedparser
from bs4 import BeautifulSoup
# import dateparser
# import json


def set_ceid(country="US", language="en"):
    """Set Country and Language parameters"""
    ceid = "?ceid={country}:{language}&hl={language}&gl={country}".format(
        country=country, language=language
    )
    return ceid


def feed_parser(feedURL):
    """Use Feedparser to Extract Feeds"""

    # Check if it's a supported URL
    request_feed = requests.get(feedURL)
    if "https://news.google.com/rss/unsupported" in request_feed.url:
        raise Exception("Feed not Available")

    parser = feedparser.parse(request_feed.text)

    # Return Only Feed and Entries from the parse dictionary
    return dict((k, parser[k]) for k in ("feed", "entries"))


def topStories_parser(text_dict):
    """Return subarticles from the main and topic feeds"""

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

    entries_dict = dict()
    for i, val in enumerate(entries):
        if "summary" in entries[i].keys():
            entries_dict[i] = topStories_parser(entries[i])
        else:
            print("News Summary Not Available")

    return entries_dict


def search_parser(search_query):
    parsed_url = urllib.parse.quote_plus(search_query)
    return parsed_url


def date_parser(date=None):
    try:
        valid_date = dateparser.parse(date).strftime("%Y-%m-%d")
        return str(valid_date)
    except:
        raise Exception("Could not parse date")
