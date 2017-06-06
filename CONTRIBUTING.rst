============
Contributing
============

You are welcome to contribute to the development of django-tables2 in various ways:

* Discover and report bugs. Make sure to include a minimal example to show your problem.
* Propose features, add tests or fix bugs by opening a Pull Request.
* Fix documenation or translations.

When contributing code or making bug fixes, we appreciate to have unit tests to verify the expected
behaviour.

Running the tests
=================

To run the tests you need to install ``requirements_test.txt`` with pip ::

    pip install -r requirements/test.txt

Then you can run the test suite by typing ``pytest``.


Source code style
=================

This project is configured to run ``flake8`` as a test, if a file doesn't follow ``falke8``
rules in ``src/setup.cfg`` the test will fail. Also, try follow the rules defined in
``.editorconfig`` file.
