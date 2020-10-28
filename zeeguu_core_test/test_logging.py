from unittest import TestCase

from zeeguu_core.logs import log


class LanguageTest(TestCase):

    def test_languages_exists(self):
        log("tüst")
