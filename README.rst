==========
scimschema
System for Cross-domain Identity Management

==========

|PyPI| |Pythons| |Travis| |AppVeyor|

.. |PyPI| image:: https://img.shields.io/pypi/v/jsonschema.svg
   :alt: PyPI version
   :target: https://pypi.python.org/pypi/jsonschema

.. |Pythons| image:: https://img.shields.io/pypi/pyversions/jsonschema.svg
   :alt: Supported Python versions
   :target: https://pypi.python.org/pypi/jsonschema

.. |Travis| image:: https://travis-ci.org/Julian/jsonschema.svg?branch=master
   :alt: Travis build status
   :target: https://travis-ci.org/Julian/jsonschema

.. |AppVeyor| image:: https://ci.appveyor.com/api/projects/status/adtt0aiaihy6muyn?svg=true
   :alt: AppVeyor build status
   :target: https://ci.appveyor.com/project/Julian/jsonschema


``scimschema`` is an implementation of `SCIM Schema <http://www.simplecloud.info/>` for Python (supporting Python 3+).

.. code-block:: python

    >>> from scimschema import validate

    >>> # A sample schema, like what we'd get from json.load()
    >>> schema = {
    ...    "schemas": ["urn:ietf:params:scim:schemas:core2:2.0:User"],
    ...    "id": "2819c223-7f76-453a-919d-413861904646",
    ...    "externalId": 9,
    ...    "meta": {
    ...        "resourceType": "User",
    ...        "created": "2011-08-01T18:29:49.793Z",
    ...        "lastModified": "Invalid date",
    ...        "location": "https://example.com/v2/Users/2819c223...",
    ...        "version": "W\/\"f250dd84f0671c3\""
    ...    }
    ...}

    >>> # If no exception is raised by validate(), the instance is valid.
    >>> validate({"name" : "Eggs", "price" : 34.99}, schema)

    >>> validate(
    ...     {"name" : "Eggs", "price" : "Invalid"}, schema
    ... )                                   # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    ValidationError: 'Invalid' is not of type 'number'

Features
--------

* Full support for
  `Draft 6 <https://python-jsonschema.readthedocs.io/en/latest/validate/#jsonschema.Draft6Validator>`_,
  `Draft 4 <https://python-jsonschema.readthedocs.io/en/latest/validate/#jsonschema.Draft4Validator>`_
  and
  `Draft 3 <https://python-jsonschema.readthedocs.io/en/latest/validate/#jsonschema.Draft3Validator>`_

* `Lazy validation <https://python-jsonschema.readthedocs.io/en/latest/validate/#jsonschema.IValidator.iter_errors>`_
  that can iteratively report *all* validation errors.

* Small and extensible

* `Programmatic querying <https://python-jsonschema.readthedocs.io/en/latest/errors/#module-jsonschema>`_
  of which properties or items failed validation.


Release Notes
-------------

Version 2.6.0 drops support for Python 2.6.X (ha ha) and contains a
number of small improvements in error messages, as well as a bug fix for
``ErrorTree``.


Running the Test Suite
----------------------

If you have ``tox`` installed (perhaps via ``pip install tox`` or your
package manager), running ``tox`` in the directory of your source checkout will
run ``jsonschema``'s test suite on all of the versions of Python ``jsonschema``
supports. Note that you'll need to have all of those versions installed in
order to run the tests on each of them, otherwise ``tox`` will skip (and fail)
the tests on that version.

Of course you're also free to just run the tests on a single version with your
favorite test runner. The tests live in the ``jsonschema.tests`` package.


Benchmarks
----------

``jsonschema``'s benchmarks make use of `perf <https://perf.readthedocs.io>`_.

Running them can be done via ``tox -e perf``, or by invoking the ``perf``
commands externally (after ensuring that both it and ``jsonschema`` itself are
installed)::

    $ python -m perf jsonschema/benchmarks/test_suite.py --hist --output results.json

To compare to a previous run, use::

    $ python -m perf compare_to --table reference.json results.json

See the ``perf`` documentation for more details.


Community
---------

There's a `mailing list <https://groups.google.com/forum/#!forum/jsonschema>`_
for this implementation on Google Groups.

Please join, and feel free to send questions there.


Contributing
------------

I'm Gordon So.

``scimschema`` is on `GitHub <http://github.com/Julian/jsonschema>`_.

Get in touch, via GitHub or otherwise, if you've got something to contribute,
it'd be most welcome!

You can also generally find me on Freenode (nick: ``tos9``) in various
channels, including ``#python``.
