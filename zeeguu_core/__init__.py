import logging
from . import elastic
from . import emailer
from . import account_management
from . import bookmark_quality
from . import content_recommender
from . import model
from . import language
from . import configuration
from . import crowd_translations
from . import util
from . import definition_of_learned
from . import language
from . import word_scheduling
from . import logs


if __name__ == "__main__":
    logs.logp(f"zeeguu_core initialized logger with name: {logger.name}")
    logging.basicConfig(
        format="%(asctime)s %(levelname)s %(name)s %(message)s")
