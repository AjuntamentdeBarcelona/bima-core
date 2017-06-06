=========
BIMA CORE
=========

Example deploying a `djang-bima-core <https://github.com/AjuntamentdeBarcelona/django-bima-core>`_
based project.

Installation and run
--------------------

#. Clone project from the Git repository.

#. Setup virtualenv Python ::

    cd bima_core
    mkvirtualenv "bima_core" -p python3
    pip install -r requirements/local.txt

#. Create local configuration ::

    cd src
    cp app.ini.template app.ini
    # Review and edit app.ini

#. Check test ::

    pytest

#. Run local server ::

    python manage.py runserver

#. Load minimum data ::

    python manage.py import_groups
    # Create an `user`, `copyright` and `author` in the admin.

#. Run rq queues ::

    python manage.py rqworker upload haystack-photo-index

Contributing
------------

See `<CONTRIBUTING.rst>`_.
