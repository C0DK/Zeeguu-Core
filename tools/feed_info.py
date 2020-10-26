#!/usr/bin/env python

from zeeguu_core.model import RSSFeed, RSSFeedRegistration
from zeeguu_core.server import db

if __name__ == "__main__":
    session = db.session

    name = input("Feed name: ")

    all_feeds = RSSFeed.query.all()
    for feed in all_feeds:
        if feed.title == name:

            print(feed.title)
            print(feed.description)
            print(feed.language.code)
            print(feed.url.as_string())
            print(feed.image_url.as_string())

            for reg in RSSFeedRegistration.query.all():
                if reg.rss_feed_id == feed.id:
                    print("... registraion by user " + reg.user.name)
