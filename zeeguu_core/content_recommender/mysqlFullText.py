from sqlalchemy import or_, desc
from sqlalchemy_fulltext import FullText, FullTextMode, FullTextSearch
from zeeguu_core.model import UserLanguage, Article


def build_mysql_query(mysql, count, search_terms, topics, unwanted_topics, user_topics, unwanted_user_topics, language,
                      upper_bounds,
                      lower_bounds):
    class FulltextContext(FullText):
        __fulltext_columns__ = ('article.content', 'article.title')
    query = mysql.query(Article)
    # if no user topics wanted or un_wanted we can do natural language mode
    if not unwanted_user_topics and not user_topics:
        boolean_query = False
        if search_terms:
            search = search_terms
            query = mysql.query(Article).filter(FullTextSearch(search, FulltextContext, FullTextMode.NATURAL))
    else:  # build a boolean query instead'
        boolean_query = True
        unwanted_user_topics = add_symbol_in_front_of_words('-', unwanted_user_topics)
        user_topics = add_symbol_in_front_of_words('', user_topics)
        search_terms = add_symbol_in_front_of_words('', search_terms)
        search = search_terms + " " + user_topics.strip() + " " + unwanted_user_topics.strip()
        query = mysql.query(Article).filter(FullTextSearch(search, FulltextContext, FullTextMode.BOOLEAN))

    # Language
    query = query.filter(Article.language_id == language.id)

    # Topics
    # TODO for now we extraxt the id from a string given,
    # but it would be better to just use the topic object returned by the database in the future
    topic_IDs = split_numbers_in_string(topics)
    topic_conditions = []
    if topic_IDs:
        for ID in topic_IDs:
            topic_conditions.append(Article.Topic.id == ID)
        query = query.filter(or_(*topic_conditions))

    # Unwanted topics
    # TODO same as above, dont use a string we split
    unwanted_topic_IDs = split_numbers_in_string(unwanted_topics)
    untopic_conditions = []

    if unwanted_topic_IDs:
        for ID in unwanted_topic_IDs:
            untopic_conditions.append(Article.Topic.id != ID)
        query = query.filter(or_(*untopic_conditions))

    # difficulty, upper and lower
    query = query.filter(lower_bounds < Article.fk_difficulty)
    query = query.filter(upper_bounds > Article.fk_difficulty)
    # if boolean then order by relevance score
    if boolean_query:
        query = query.order_by(desc(FullTextSearch(search, FulltextContext, FullTextMode.BOOLEAN)))

    return query.limit(count)


def add_symbol_in_front_of_words(symbol, input_string):
    words = input_string.split()
    acc = ""
    for word in words:
        acc += symbol + word + " "
    return acc


def split_numbers_in_string(input_string):
    numbers = input_string.split()
    acc = []
    for number in numbers:
        acc.append(int(number))
    return acc