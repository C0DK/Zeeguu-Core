# -*- coding: utf8 -*-
import re

import zeeguu
import datetime

from sqlalchemy import MetaData
from zeeguu.model.ranked_word import RankedWord
from zeeguu.model.url import Url
from zeeguu.model.text import Text
from zeeguu.model.exercise_outcome import ExerciseOutcome
from zeeguu.model.exercise_source import ExerciseSource
from zeeguu.model.user_word import UserWord
from zeeguu.model.bookmark import Bookmark
from zeeguu.model.language import Language
from zeeguu.model.user import User

WORD_PATTERN = re.compile("\[?([^{\[]+)\]?( {[^}]+})?( \[[^\]]\])?")

TEST_PASS='test'
TEST_EMAIL='i@mir.lu'

TEST_BOOKMARKS_COUNT = 2


def drop_current_tables(db):
    # We have to do a commit() before the drop_all()
    # Otherwise the system just freezes sometimes!
    db.session.commit()
    db.session.close_all()
    # Initial cleanup
    db.reflect()
    db.drop_all()
    # Creating the tables again
    db.create_all()


def add_bookmark(db, user, original_language, original_word, translation_language, translation_word,  date, the_context, the_url, the_url_title):

    url = Url.find (the_url)
    text = Text.find_or_create(the_context, translation_language, url)
    origin = UserWord.find(original_word.lower(), original_language)
    translation = UserWord.find(translation_word.lower(), translation_language)

    b1 = Bookmark(origin, translation, user, text, date)
    db.session.add_all([url,text,origin,translation,b1])
    db.session.commit()

    add_probability_to_existing_words_of_user(user,b1,original_language)


#
def create_minimal_test_db(db):

    drop_current_tables(db)

    # Some common test fixtures
    de = Language("de", "German")
    en = Language("en", "English")
    nl = Language("nl", "Dutch")
    ro = Language("ro", "Romanian")

    db.session.add_all([en, de, nl]);

    mir = User(TEST_EMAIL, "Mircea", TEST_PASS, de, en)

    db.session.add(mir)

    show_solution = ExerciseOutcome("Show solution")
    retry = ExerciseOutcome("Retry")
    correct = ExerciseOutcome("Correct")
    wrong = ExerciseOutcome("Wrong")
    typo = ExerciseOutcome("Typo")
    too_easy = ExerciseOutcome("Too easy")

    db.session.add_all([show_solution, retry,
                        correct, wrong, typo,
                        too_easy]);

    recognize = ExerciseSource("Recognize")
    translate = ExerciseSource("Translate")

    db.session.add_all([recognize, translate])

    add_bookmark(db, mir, de, "Schaf", en, "sheep",
                    datetime.datetime(2011, 01, 01, 01, 01, 01),
                    "Bitte... zeichne mir ein Schaf!",
                    "http://www.derkleineprinz-online.de/text/2-kapitel/",
                    "Der Kleine Prinz - Kapitel 2")

    add_bookmark(db, mir, de, "sprang", en, "jumped",
                    datetime.datetime(2011, 01, 01, 01, 01, 01),
                    "Ich sprang auf die Fusse.",
                    "http://www.derkleineprinz-online.de/text/2-kapitel/",
                    "Der Kleine Prinz - Kapitel 2")

    global TEST_BOOKMARKS_COUNT
    TEST_BOOKMARKS_COUNT = 2
    db.session.commit()

    add_ranked_word_to_db(db, 'de')



class WordCache(object):
    def __init__(self):
        self.cache = {}

    def __getitem__(self, args):
        word = self.cache.get(args, None)
        if word is None:
            word = UserWord(*args)
            zeeguu.db.session.add(word)
            self.cache[args] = word
        return word


def populate(from_, to, dict_file):
    cache = WordCache()
    with open(dict_file, "r") as f:
        for line in f:
            if line.startswith("#") or line.strip() == "":
                continue
            parts = line.split("\t")
            if len(parts) < 2:
                return
            orig = cache[clean_word(parts[0]), from_]
            trans = cache[clean_word(parts[1]), to]
            if trans not in orig.translations:
                orig.translations.append(trans)


def filter_word_list(word_list):
    filtered_word_list = []
    lowercase_word_list = []
    for word in word_list:
         if word.lower() not in lowercase_word_list:
            lowercase_word_list.append(word.lower())
    for lc_word in lowercase_word_list:
        for word in word_list:
            if word.lower()  == lc_word:
                filtered_word_list.append(word)
                break
    return filtered_word_list


def path_of_language_resources():
    """
    the easiest way to make sure that the langauge dictionary files
    are found when running the test cases, either from IDE or from the
    command line is to
    - compute the path relative to this file
    :return:
    """
    import os
    path = os.path.dirname(__file__)
    return path+"/../languages/"


def test_word_list(lang_code):

    words_file = open(path_of_language_resources()+lang_code+"-test.txt")
    words_list = words_file.read().splitlines()
    return words_list


def add_ranked_word_to_db(db, lang_code):
    # zeeguu.app.test_request_context().push()
    db.session.commit()
    from_lang = Language.find(lang_code)
    initial_line_number = 1

    for word in filter_word_list(test_word_list(lang_code)):
        r = RankedWord(word.lower(), from_lang,initial_line_number)
        db.session.add(r)
        initial_line_number+=1
        # print "added " + str(r.word)
    db.session.commit()


def clean_word(word):
    match = re.match(WORD_PATTERN, word)
    if match is None:
        return word.decode("utf8")
    return match.group(1).decode("utf8")





def add_probability_to_existing_words_of_user(user,bookmark,language):
    bookmark.calculate_probabilities_after_adding_a_bookmark(user,language)


def create_test_db(db):

    drop_current_tables(db)

    de = Language("de", "German")
    da = Language("da", "Danish")
    en = Language("en", "English")
    es = Language("es", "Spanish")
    fr = Language("fr", "French")
    it = Language("it", "Italian")
    no = Language("no", "Norwegian")
    nl = Language("nl", "Dutch")
    pt = Language("pt", "Portughese")
    ro = Language("ro", "Romanian")

    db.session.add(de)
    db.session.add(da)
    db.session.add(en)
    db.session.add(es)
    db.session.add(fr)
    db.session.add(it)
    db.session.add(no)
    db.session.add(nl)
    db.session.add(pt)
    db.session.add(ro)
    db.session.commit()

    show_solution = ExerciseOutcome("Show solution")
    retry = ExerciseOutcome("Retry")
    correct = ExerciseOutcome("Correct")
    wrong = ExerciseOutcome("Wrong")
    typo = ExerciseOutcome("Typo")
    too_easy = ExerciseOutcome("Too easy")

    recognize = ExerciseSource("Recognize")
    translate = ExerciseSource("Translate")
    zeekoe = ExerciseSource("ZeeKoe")

    db.session.add(show_solution)
    db.session.add(retry)
    db.session.add(correct)
    db.session.add(wrong)
    db.session.add(typo)
    db.session.add(too_easy)

    db.session.add(recognize)
    db.session.add(translate)
    db.session.add(zeekoe)

    user = User(TEST_EMAIL, "Mircea", TEST_PASS, de, ro)
    user2 = User("i@ada.lu", "Ada", "pass", fr)

    db.session.add(user)
    db.session.add(user2)

    jan111 = datetime.datetime(2011,01,01,01,01,01)
    ian101 = datetime.datetime(2001,01,01,01,01,01)
    jan14 = datetime.datetime(2014,1,14,01,01,01)

    today_dict = {
        'sogar':'actually',
        'sperren':'to lock, to close',
        'Gitter':'grates',
        'erfahren':'to experience',
        'treffen':'hit',
        'jeweils':'always',
        'Darstellung':'presentation',
        'Vertreter':'representative',
        'Knecht':'servant',
        'der':'the'
    }

    dict = {
            u'Spaß': 'fun',
            'solche': 'suchlike',
            'ehemaliger': 'ex',
            'betroffen': 'affected',
            'Ufer':'shore',
            u'höchstens':'at most'
            }

    french_dict = {
        'jambes':'legs',
        'de':'of',
        'et':'and'
            }

    story_url = 'http://www.gutenberg.org/files/23393/23393-h/23393-h.htm'
    japanese_story = [
            # ['recht', 'right', 'Du hast recht', story_url],
            ['Holzhauer', 'wood choppers', 'Da waren einmal zwei Holzhauer können', story_url],
            ['Da', 'there', 'Da waren einmal zwei Holzhauer können', story_url],
            ['zwei', 'two', 'Da waren einmal zwei Holzhauer können', story_url],
            [u'Wald','to arrive', u'Um in den Walden zu gelangen, mußten sie einen großen Fluß passieren. Um in den Walden zu gelangen, mußten sie einen großen Fluß passieren. Um in den Walden zu gelangen, mußten sie einen großen Fluß passieren. Um in den Walden zu gelangen, mußten sie einen großen Fluß passieren', story_url],
            ['eingerichtet','established',u'Um in den Wald zu gelangen, mußten sie einen großen Fluß passieren, über den eine Fähre eingerichtet war', story_url],
            [u'vorläufig','temporary',u'von der er des rasenden Sturmes wegen vorläufig nicht zurück konnte', story_url],
            [u'werfen', 'to throw',u'Im Hause angekommen, warfen sie sich zur Erde,', story_url],
            ['Tosen','roar',u'sie Tür und Fenster wohl verwahrt hatten und lauschten dem Tosen des Sturmes.sie Tür und Fenster wohl verwahrt hatten und lauschten dem Tosen des Sturmes.sie Tür und Fenster wohl verwahrt hatten und lauschten dem Tosen des Sturmes',story_url],
            ['Entsetzen','horror','Entsetzt starrte Teramichi auf die Wolke',story_url]
        ]

    add_ranked_word_to_db(db, 'de')

    for key in today_dict:
        add_bookmark(db, user, de, key, en, today_dict[key], jan111, "Keine bank durfe auf immunitat pochen, nur weil sie eine besonders herausgehobene bedeutung fur das finanzsystem habe, sagte holder, ohne namen von banken zu nennen",
                         "http://url2", "title of url2")

    for key in dict:
        add_bookmark(db, user, de, key, en, dict[key], ian101, "Deutlich uber dem medianlohn liegen beispielsweise forschung und entwicklung, tabakverarbeitung, pharma oder bankenwesen, am unteren ende der skala liegen die tieflohnbranchen detailhandel, gastronomie oder personliche dienstleistungen. ",
                         "http://url1", "title of url1")

    for key in french_dict:
        add_bookmark(db, user, de, key, en, french_dict[key], ian101, "Deutlich uber dem medianlohn liegen beispielsweise forschung und entwicklung, tabakverarbeitung, pharma oder bankenwesen, am unteren ende der skala liegen die tieflohnbranchen detailhandel, gastronomie oder personliche dienstleistungen. ",
                         "http://url1", "title of url1")
    for w in japanese_story:
        add_bookmark(db, user, de, w[0], en, w[1],jan14, w[2],w[3], "japanese story")

    db.session.commit()


if __name__ == "__main__":

    "in populate..."
    zeeguu.app.test_request_context().push()
    create_test_db(zeeguu.db)
