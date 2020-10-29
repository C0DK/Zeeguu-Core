#!/usr/bin/env python3
import re
import flask_sqlalchemy
from zeeguu_core.configuration.configuration import load_configuration_or_abort

from zeeguu_core.logs import warning
from flask import Flask


# we create the app here and load the corresponding configuration
#
# TODO check if `app` is created somehow
app = Flask("Zeeguu-Core")
load_configuration_or_abort(app, 'ZEEGUU_CORE_CONFIG',
                            ['MAX_SESSION',
                                 'SQLALCHEMY_DATABASE_URI',
                                 'SQLALCHEMY_TRACK_MODIFICATIONS'])

# Create the db object, which will be the superclass
# of all the model classes
db = flask_sqlalchemy.SQLAlchemy(app)

# Note that this must be called after all the model classes are loaded
db.init_app(app)
db.create_all(app=app)

# Log the DB connection string; after masking the password
db_connection_string = app.config["SQLALCHEMY_DATABASE_URI"]
anon_conn_string = re.sub(
    ":([a-zA-Z_][a-zA-Z_0-9]*)@", ":****@", db_connection_string)
warning('*** ==== ZEEGUU CORE: Linked model with: ' + anon_conn_string)
