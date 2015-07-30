# -*- coding: utf-8 -*-
"""Extensions module. Each extension is initialized in the app factory located
in app.py
"""

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

import sqlalchemy_defaults
db.Column = sqlalchemy_defaults.Column
sqlalchemy_defaults.make_lazy_configured(db.mapper)

from flask_migrate import Migrate
migrate = Migrate()

from flask_cache import Cache
cache = Cache()

from flask_debugtoolbar import DebugToolbarExtension
debug_toolbar = DebugToolbarExtension()
