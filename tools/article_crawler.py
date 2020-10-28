from datetime import datetime


from zeeguu_core.logs import log
from feed_retrieval import retrieve_articles_from_all_feeds
from recompute_recommender_cache import clean_the_cache, recompute_for_users

import logging
if __name__ == "__main__":
    logging.getLogger("elasticsearch").setLevel(logging.CRITICAL)

    logging.getLogger("zeeguu_core").setLevel(logging.INFO)


    start = datetime.now()
    log(f"started at: {datetime.now()}")

    retrieve_articles_from_all_feeds()
    clean_the_cache()
    recompute_for_users()

    end = datetime.now()
    log(f"done at: {end}")
    log(f"total duration: {end - start}")
