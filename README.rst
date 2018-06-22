==========
scimschema
System for Cross-domain Identity Management

==========

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
    AssertError: 'Invalid' is not of type 'number'

Features
--------

* Full support for
  `SCIM 2.0 <http://www.simplecloud.info/#Specification>`_,


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


Contributing
------------

I'm Gordon So.

``scimschema`` is on `GitHub <https://github.com/GordonSo/scimschema>`_.

Get in touch, via GitHub or otherwise, if contributors are most welcome!
