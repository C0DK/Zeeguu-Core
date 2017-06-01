
from tests_core_zeeguu.rules.base_rule import BaseRule
from zeeguu.model.url import Url


class UrlRule(BaseRule):

    def __init__(self):
        super().__init__()

        self.url = self._create_model_object()

        self.save(self.url)

    def _create_model_object(self):
        random_url = self.faker.uri()
        random_title = self.faker.sentence()

        url = Url(random_url, random_title)

        if self._exists_in_db(url):
            return self._create_model_object()

        return url

    @staticmethod
    def _exists_in_db(obj):
        """Checks the existence of an object in the database

        In this case, an existence check is not necessary since no unique
        constraints can be violated.

        :param obj: BaseRule object, whose existence needs to be checked
        :return: True, if object exists, False otherwise
        """
        return False
