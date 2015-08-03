#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from flask_script import Manager, Shell, Server
from flask_migrate import MigrateCommand

from colorsearchtest.app import create_app
from colorsearchtest.settings import DevConfig, ProdConfig
from colorsearchtest.database import db

if os.environ.get("COLORSEARCHTEST_ENV") == 'prod':
    app = create_app(ProdConfig)
else:
    app = create_app(DevConfig)

HERE = os.path.abspath(os.path.dirname(__file__))
TEST_PATH = os.path.join(HERE, 'tests')

manager = Manager(app)


def _make_context():
    """Return context dict for a shell session so you can access
    app and db by default.
    """
    return {'app': app, 'db': db}


@manager.command
def test():
    """Run the tests."""
    import pytest
    exit_code = pytest.main([TEST_PATH, '--verbose'])
    return exit_code


manager.add_command('server', Server())
manager.add_command('shell', Shell(make_context=_make_context))
manager.add_command('db', MigrateCommand)

@manager.command
def createcolors(min_colors, max_colors):
    from colorsearchtest.models import Color

    cc_func_args = dict(min_colors=int(min_colors), max_colors=int(max_colors))

    color_count = Color.query.count()
    if color_count:
        Color.query.delete()
        print('Deleted {0} existing colors'.format(color_count))

    from colorsearchtest.commands import createcolors as createcolors_func

    color_count = createcolors_func(**cc_func_args)

    print('Created {0} new colors'.format(color_count))


if __name__ == '__main__':
    manager.run()
