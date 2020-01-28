def bad_quality_bookmark(bookmark):
    """
    reasons that disqualify a bookmark from beeing quality

    """

    return (

            origin_same_as_translation(bookmark) or

            is_subset_of_larger_bookmark(bookmark) or

            is_made_of_too_many_words(bookmark) or

            is_a_very_short_word(bookmark) or

            context_is_too_long(bookmark) or

            translation_already_in_context_bug(bookmark)

    )


def context_is_too_long(bookmark):
    return bookmark.context_word_count() > 42


def is_a_very_short_word(bookmark):
    return len(bookmark.origin.word) < 3


def is_made_of_too_many_words(bookmark):
    words_in_origin = bookmark.origin.word.split(" ")
    return len(words_in_origin) > 2


def is_subset_of_larger_bookmark(self):
    """
        if the user translates a superset of this sentence
    """
    from zeeguu_core.model.bookmark import Bookmark
    all_bookmarks_in_text = Bookmark.find_all_for_text_and_user(self.text, self.user)

    for each in all_bookmarks_in_text:
        if each != self:
            if self.origin.word in each.origin.word:
                return True
        return False


def origin_same_as_translation(self):
    try:
        return self.origin.word.lower() == self.translation.word.lower()
    except:
        print("missing word for bookmark with id {0}".format(self.id))
        return False


def translation_already_in_context_bug(self):
    # a superset of translation same as origin...
    # happens in the case of some bugs in translation
    # where the translation is inserted in the text
    # till we fix it, we should not show this

    if self.translation.word in self.text.content:
        return True
