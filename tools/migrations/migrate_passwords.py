# script used to convert

from zeeguu_core.server import db
from zeeguu_core.model import User

if __name__ == "__main__":
    session = db.session

    for user in User.query.all():
        print (f'updating user {user}')
        user.password = user.password.hex().encode('utf-8')
        user.password_salt = user.password_salt.hex().encode('utf-8')
        session.add(user)
        session.commit()

    # now make sure to change the column type of the
    # table to string.
