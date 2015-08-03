Color Search Test
=================

Test searching by closest color in Flask / Postgres.

Closest colors are calculated and sorted using the various `Delta E
<http://www.colorwiki.com/wiki/Delta_E:_The_Color_Difference>`_
(CIE Lab) `color difference
<https://en.wikipedia.org/wiki/Color_difference>`_ formulae.

By default, this app uses two Delta E formulae (the 1976 and the 2000
version) that are implemented as custom Postgres SQL functions. It
can also be switched to use the `python-colormath
<https://github.com/gtaylor/python-colormath>`_ implementations, for
baseline comparison of accuracy and performance.

Here's a `demo of the app in action
<https://colorsearchtest.herokuapp.com/>`_.


Quickstart
----------

First, set your app's secret key as an environment variable. For
example, add the following to ``.bashrc`` or ``.bash_profile``.

.. code-block:: bash

    export COLORSEARCHTEST_SECRET='something-really-secret'


Then run the following commands to bootstrap your environment.


::

    git clone https://github.com/Jaza/colorsearchtest
    cd colorsearchtest
    pip install -r requirements/dev.txt
    python manage.py server

You will see a pretty welcome screen.


Dynamic Secret Key
------------------

You can have a different random secret key each time the app starts,
if you want:

::

    export COLORSEARCHTEST_SECRET=`python -c "import os; from binascii import hexlify; print(hexlify(os.urandom(24)))"`; python manage.py server


Specifying DB config
--------------------

You can specify DB config when the app starts:

::

    export COLORSEARCHTEST_DATABASE_URI="postgresql://colorsearchtest:colorsearchtest@localhost:5432/colorsearchtest"; python manage.py server


Setting up schema
-----------------

Once you have installed your DBMS, run the following if necessary
(shouldn't be necessary), to set up the migrations:

::

    python manage.py db init
    python manage.py db migrate


Then, run the following to create your app's database tables and
perform the initial migration:

::

    python manage.py db upgrade
    python manage.py server


Creating random colors
----------------------

To actually use colorsearchtest, you need to create a set of random
colors in the database. To do this, run the following command,
specifying a minimum and maximum number of colors to generate (of
your choice), e.g:

::

    python manage.py createcolors 900 1000


You can re-run this whenever you like. Each time you re-run it, the
script will delete all existing colors and save new ones.


Switching between SQL-based and Python-based Delta E
----------------------------------------------------

By default, the Delta E formulae to use are configured as follows:

::

    IS_DELTA_E_COLORMATH_ENABLED = False
    IS_DELTA_E_DBQUERY_ENABLED = True


These can be toggled by editing the ``colorsearchtest/settings.py``
file.


Deployment
----------

In your production environment, make sure the ``COLORSEARCHTEST_ENV``
environment variable is set to ``"prod"``.


Shell
-----

To open the interactive shell, run ::

    python manage.py shell

By default, you will have access to ``app`` and ``db``.


Running Tests
-------------

To run all tests, run ::

    python manage.py test


Migrations
----------

Whenever a database migration needs to be made. Run the following commands:
::

    python manage.py db migrate

This will generate a new migration script. Then run:
::

    python manage.py db upgrade

To apply the migration.

For a full migration command reference, run ``python manage.py db --help``.
