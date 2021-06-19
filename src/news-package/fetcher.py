import helpers
import constants


class PyGNews:
    def __init__(self, baseURL, country="US", language="en"):
        self.baseURL = constants.baseURL
        self.country = country
        self.language = language

    def top_stories(self):
        """Top Stories from Google News"""
        feeder = helpers.feed_parser(
            self.baseURL
            + helpers.set_ceid(country=self.country, language=self.language)
        )

        entries_dict = helpers.collect_coverage(feeder["entries"])
        return entries_dict

    def topic_headlines(self, topic: str):
        """Return a list of all articles from the topic page of Google News
        given a country and a language"""
        if topic.upper() in constants.TOPICS:
            passed_feed = helpers.feed_parser(
                self.baseURL
                + "/headlines/section/topic/{}".format(topic.upper())
                + helpers.set_ceid(country=self.country,
                                   language=self.language)
            )
        else:
            passed_feed = helpers.feed_parser(
                self.baseURL
                + "/topics/{}".format(topic)
                + helpers.set_ceid(country=self.country,
                                   anguage=self.language)
            )

        headlines = helpers.collect_coverage(passed_feed["entries"])
        if len(headlines) > 0:
            return headlines
        else:
            raise Exception(
                "Unsupported Topic, Only the following Topics are allowed {}"
                .format(constants.TOPICS)
            )

    def location_headlines(self, location: str):
        """Return a list of all articles about a specific geolocation
        given a country and a language"""

        loacation_parsed = helpers.feed_parser(
            self.baseURL
            + "/headlines/section/geo/{}".format(location)
            + helpers.set_ceid(country=self.country, language=self.language)
        )

        location_news = helpers.collect_coverage(loacation_parsed["entries"])
        return location_news

    def search(
        self,
        search_query: str,
        since_when=None,
        after_date=None,
        before_date=None
    ):
        """
        Return a list of all articles given a full-text search parameter,
        a country and a language
        :param bool helper: When True helps with URL quoting
        :param str when: Sets a time range for the artiles that can be found
        """

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
