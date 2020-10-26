from zeeguu_core.server import db
from zeeguu_core.model import RSSFeed

if __name__ == "__main__":
    session = db.session

    feeds = RSSFeed.query.all()

    for each in feeds:
        each.icon_name = each.image_url.path.split('/')[-1]
        session.add(each)
        session.commit()
        print(each.icon_name)
