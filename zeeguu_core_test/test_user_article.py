from unittest import TestCase

from zeeguu_core import server
from zeeguu_core.model.user_article import UserArticle

from zeeguu_core_test.model_test_mixin import ModelTestMixIn
from zeeguu_core_test.rules.user_article_rule import UserArticleRule

session = server.db.session


class UserArticleTest(ModelTestMixIn, TestCase):
    def setUp(self):
        super().setUp()

        self.user_article = UserArticleRule().user_article
        self.user = self.user_article.user
        self.article = self.user_article.article

    def test_article_is_not_starred_initially(self):
        assert not self.user_article.starred

    def test_all_starred_articles(self):
        self.article.star_for_user(session, self.user)
        assert 1 == len(UserArticle.all_starred_articles_of_user(self.user))

    def test_all_starred_or_liked_articles(self):
        self.article.star_for_user(session, self.user)
        assert 1 == len(
            UserArticle.all_starred_or_liked_articles_of_user(self.user))
