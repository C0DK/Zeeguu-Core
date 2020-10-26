# the core model
from .language import Language
from .url import Url
from .domain_name import DomainName
from .article import Article
from .bookmark import Bookmark
from .text import Text
from .user import User
from .user_word import UserWord
from .user_preference import UserPreference
from .session import Session
from .unique_code import UniqueCode
from .word_knowledge.word_interaction_history import WordInteractionHistory

from .user_language import UserLanguage

from .topic import Topic
from .user_article import UserArticle
from .article_word import ArticleWord
from .articles_cache import ArticlesCache

from .feed import RSSFeed
from .feed_registrations import RSSFeedRegistration

from .topic import Topic
from .topic_subscription import TopicSubscription
from .topic_filter import TopicFilter
from .localized_topic import LocalizedTopic

from .search import Search
from .search_filter import SearchFilter
from .search_subscription import SearchSubscription

# exercises
from .exercise import Exercise
from .exercise_outcome import ExerciseOutcome
from .exercise_source import ExerciseSource

# user logging
from .user_activitiy_data import UserActivityData
from .smartwatch.watch_event_type import WatchEventType
from .smartwatch.watch_interaction_event import WatchInteractionEvent

# teachers and cohorts
from .cohort import Cohort
from .teacher_cohort_map import TeacherCohortMap
from .teacher import Teacher
from .cohort_article_map import CohortArticleMap

from .user_reading_session import UserReadingSession
from .user_exercise_session import UserExerciseSession

# bookmark scheduling
from zeeguu_core.model.bookmark_priority_arts import BookmarkPriorityARTS



# TODO create a `__all__` dictionary
