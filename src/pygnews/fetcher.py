from . import helpers
from . import constants


class PyGNews:
    def __init__(self, baseURL=constants.baseURL, country="US", language="en"):
        """Set default parameters for PyGNews objects.
        Args:
            baseURL (str, optional): Google News Feed URL.
                                    Defaults to constants.baseURL.
            country (str, optional): Base country for the Feed URL.
                                    Defaults to "US".
            language (str, optional): Base language for the Feed URL.
                                      Defaults to "en".
        """
        self.baseURL = baseURL
        self.country = country
        self.language = language

    def top_stories(self):
        """Return a dictionaries of top news on Google.

        Returns:
            dict: Google news top stories.
        """
        feeder = helpers.feed_parser(
            self.baseURL
            + helpers.set_ceid(country=self.country, language=self.language)
        )

        entries_dict = helpers.collect_coverage(feeder["entries"])
        return entries_dict

    def topic_headlines(self, topic: str = "WORLD"):
        """ Return a list of all articles from the topic page of Google News
            given a country and a language

        Args:
            topic (str, optional): topic of interest. Defaults to "WORLD".
                                    Available Topics include
                                    WORLD,
                                    NATION,
                                    BUSINESS,
                                    TECHNOLOGY,
                                    ENTERTAINMENT,
                                    SCIENCE,
                                    SPORTS,
                                    HEALTH.

        Raises:
            Exception: When Topic is not in the listed Topics

        Returns:
            dict: Topic headlines
        """
        if topic.upper() in constants.TOPICS:
            passed_feed = helpers.feed_parser(
                self.baseURL
                + "/headlines/section/topic/{}".format(topic.upper())
                + helpers.set_ceid(country=self.country, language=self.language)
            )
        else:
            passed_feed = helpers.feed_parser(
                self.baseURL
                + "/topics/{}".format(topic)
                + helpers.set_ceid(country=self.country, language=self.language)
            )

        headlines = helpers.collect_coverage(passed_feed["entries"])
        if len(headlines) > 0:
            return headlines
        else:
            raise Exception(
                "Unsupported Topic, Only the following Topics are allowed {}".format(
                    constants.TOPICS
                )
            )

    def location_headlines(self, location: str = "US"):
        """Gives a list of all articles about a specific geolocation
            given a country and a language

        Args:
            location (str, optional): Abbreviation of the Country name to search. Defaults to "US".

        Returns:
            dict: News headlines from country
        """
        loacation_parsed = helpers.feed_parser(
            self.baseURL
            + "/headlines/section/geo/{}".format(location)
            + helpers.set_ceid(country=self.country, language=self.language)
        )

        location_news = helpers.collect_coverage(loacation_parsed["entries"])
        return location_news

    def search(
        self,
        search_query: str = None,
        since_when=None,
        after_date=None,
        before_date=None,
    ):
        """Gives all articles based on search querry and specified date.

        Args:
            search_query (str, optional): Search Querry. Defaults to None.
            since_when ([type], optional): Time since when news was published.
                                           2m Corresponds to 2 minutes,
                                           2h Corresponds to 2 hours,
                                           2d Corresponds to 2 days.
                        Defaults to None.
            after_date ([type], optional): News puclished after this date.
                        Defaults to None.
            before_date ([type], optional): News puclished before this date.
                        Defaults to None.

        Raises:
            TypeError: Raise error when search queryis not given.

        Returns:
            dict: News based on search query.
        """

        if search_query is None:
            raise TypeError("Input a Search Querry")

        if since_when:
            search_query += " when:" + since_when

        if after_date and not since_when:
            after_date = helpers.date_parser(date=after_date)
            search_query += " after:" + after_date

        if before_date and not since_when:
            before_date = helpers.date_parser(date=before_date)
            search_query += " before:" + before_date

        search_query = helpers.search_parser(search_query)

        search_ceid = helpers.set_ceid(
            country=self.country, language=self.language
        ).replace("?", "&")

        news_feed = helpers.feed_parser(
            self.baseURL + "/search?q={}".format(search_query) + search_ceid
        )

        searched_news = helpers.collect_coverage(news_feed["entries"])
        return searched_news
