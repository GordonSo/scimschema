.. image:: https://raw.githubusercontent.com/GordonSo/scimschema/master/scimschema-logo.png
   :target: https://github.com/GordonSo/scimschema
   :align: center
   :alt: scimschema-logo

------

ScimSchema
==========
.. image:: https://travis-ci.org/GordonSo/scimschema.svg?branch=master
    :target: https://travis-ci.org/GordonSo/scimschema

Validate JSon content given a predefined set of SCIM Schemas (in JSON representation format) as specified in `SCIM <http://www.simplecloud.info/>`_ (supporting Python 3+).

Example use case
----------------

1) Install the library via pip:

.. code-block:: python


    pip install scimschema


2) Specify any custom schemas in json format as per the rfc requirement: https://tools.ietf.org/html/rfc7643#section-2

3) Put the json files under a Python package as per our examples here: https://github.com/GordonSo/scimschema/tree/master/tests/extension (also checkout our __init__() file which is handy for loading the json)

4) Import the ```validate``` method from scimschema and pass in json response/request content and the extension schemas to assert its validness

To step through the above in working code, check out this test: `test_scim_schema.py <https://github.com/GordonSo/scimschema/blob/master/tests/test_scim_schema.py>`_.

.. code-block:: python

    from scimschema import validate
    from . import extension # <- this is the custom schemas define by your: see https://github.com/GordonSo/scimschema/tree/master/tests/extension for example

    # A sample schema, like what we'd get from response.get(<scim entity url>).json()
    content = {
        "schemas": ["urn:ietf:params:scim:schemas:core2:2.0:Group", "urn:huddle:params:scim:schemas:extension:2.0:SimpleAccount"],
        "id": "2819c223-7f76-453a-919d-413861904646",
        "externalId": 9,
        "meta": {
            "resourceType": "User",
            "created": "2011-08-01T18:29:49.793Z",
            "lastModified": "Invalid date",
            "location": "https://example.com/v2/Users/2819c223...",
            "version": "W\/\"f250dd84f0671c3\""
        }
    }
    validate(
        data=content,
        extension_schema_definitions=extension.schema
    )

    >>>    E   _scimschema._model.scim_exceptions.AggregatedScimMultValueAttributeValidationExceptions: Found 1 aggregated exceptions at Scim response:
    >>>    E    ScimAttributeValueNotFoundException:
    >>>    E    	 'Single-value attribute:ipRestrictionsEnabled' is required at the following location '['urn:huddle:params:scim:schemas:extension:2.0:Account', 'ipRestrictionsEnabled']' but found '{}'
    >>>    !!!!!!!!!!!!!!!!!!! Interrupted: 1 errors during collection !!!!!!!!!!!!!!!!!!!


Features
--------

Support for `SCIM 2.0 <http://www.simplecloud.info/#Specification>`_,
  - Validate SCIM Schema definition
     - Validate Model (schema) Id, Name, description, attributes
     - Validate Attribute (schema) Name, Type, Required, Canonical Values, Mutability, Returned, Uniqueness

  - Validate JSON Content against SCIM Schema
     - Validate significant value against Type (Binary, Boolean, Datetime, Decimal, Integer, Reference, String, Complex, MultiValued)
     - Characteristics Required, Canonical Values, Uniqueness


Upcoming features
-----------------

  - Validate JSON Content for characteristics below:
     - Mutability, Returned



Running the Test Suite
----------------------

The project requires `pytest` to discover tests, and it integrates with `travis <https://github.com/GordonSo/scimschema/blob/master/.travis.yml>`_ to run on commit.
If you use a Windows machine, there are helpful commands in the `go.bat <https://github.com/GordonSo/scimschema/blob/master/go.bat>`_ to get you started...


Contributing
------------

This project is powered by the QA department at `Huddle <https://twitter.com/HuddleEng>`_

The source code is available on `GitHub <https://github.com/GordonSo/scimschema>`_.

Get in touch, via GitHub or otherwise, contributors are also welcome!
