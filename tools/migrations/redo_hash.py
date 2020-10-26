# script used to convert the old binary hashes
# to their hex counterparts. binary can not be
# insured UNIQUE by a mysql constraint
from zeeguu_core import util
from zeeguu_core.model import Text
from zeeguu_core.server import db

if __name__ == "__main__":
    session = db.session

    texts = session.query(Text).all()
    for t in texts:
        t.content_hash = util.text_hash(t.content)
        session.add(t)
        session.commit()
    # input ("next?/")
