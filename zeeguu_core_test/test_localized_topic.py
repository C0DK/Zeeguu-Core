from unittest import TestCase

from zeeguu_core.model import LocalizedTopic, Topic, Url
from zeeguu_core.server import db

from zeeguu_core_test.model_test_mixin import ModelTestMixIn
from zeeguu_core_test.rules.article_rule import ArticleRule
from zeeguu_core_test.rules.user_rule import UserRule



class LocalizedTopicTest(ModelTestMixIn, TestCase):

    def setUp(self):
        super().setUp()
        self.user = UserRule().user

    def test_topic_matching(self):
        self._localized_topic_keyword_in_url(
            "World", "World", "theguardian.com/world",
            "https://www.theguardian.com/world/2020/jun/06/new-zealand-readers"
        )

    def test_topic_matching_is_case_sensitive(self):
        self._localized_topic_keyword_in_url(
            "Music", "Muziek", "the-Voice",
            "https://www.nu.nl/media/6056161/winnaar-negende-seizoen-van-the-Voice-kids-bekend.html"
        )

    def _localized_topic_keyword_in_url(self, topic: str, localized: str, keyword: str, url: str):
        topic = Topic(topic)
        localized_topic = LocalizedTopic(topic, self.user.learned_language, localized)
        localized_topic.keywords = keyword

        article = ArticleRule().article
        url = Url.find_or_create(db.session, url)
        article.url = url

        assert localized_topic.matches_article(article)
