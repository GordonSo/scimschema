import re
from copy import deepcopy

import pytest
from scimschema._model import model
from scimschema._model import attribute


def test_default_meta_attribute():
    d = {
        "name": "_userName",
        "type": "string",
        "multiValued": False,
        "description": "Unique identifier for the User, typically used by the user to directly authenticate to the "
        "service provider. Each User MUST include a non-empty userName value.  This identifier MUST be "
        "unique across the service provider's entire set of Users. REQUIRED.",
        "required": True,
        "caseExact": False,
        "mutability": "invalid",
    }
    maf = model.AttributeFactory.create(
        d=d, locator_path="urn:ietf:params:scim:schemas:test:default_attribute"
    )
    expected_exception = None
    try:
        maf.validate_schema()
    except AssertionError as ae:
        expected_exception = ae

    def grep_exception_counts(msg):
        try:
            prog = re.compile("\d aggregated exceptions found")
            return next(i for i in prog.findall(msg))
        except TypeError:
            return None

    exception_msg = str(expected_exception)
    count_msg = grep_exception_counts(exception_msg)
    assert re.search(
        re.compile("2 aggregated exceptions found"), exception_msg
    ), "Expected 2 aggregated exceptions found but got '{}'".format(count_msg)
    assert re.search(
        re.compile("'_userName'] and has 'name' property which must be valid name"),
        exception_msg,
    )
    assert re.search(
        re.compile(
            "'_userName'] and has 'mutability' property which must be .* but got 'invalid'"
        ),
        exception_msg,
    )


def test_binary_attribute_validate():
    schema = {
        "name": "data",
        "type": "binary",
        "required": True,
    }
    data = {"data": "kjj"}

    maf = model.AttributeFactory.create(
        d=schema, locator_path="urn:ietf:params:scim:schemas:test:binary_attribute"
    )
    maf.validate_schema()
    maf.validate(data)


def test_complex_meta_attribute():
    d = {
        "name": "name",
        "type": "complex",
        "multiValued": False,
        "description": "The components of the user's real name. Providers MAY return just the full name as a single string in the formatted sub-attribute, or they MAY return just the individual component attributes using the other sub-attributes, or they MAY return both.  If both variants are returned, they SHOULD be describing the same name, with the formatted name indicating how the component attributes should be combined.",
        "required": False,
        "subAttributes": [
            {
                "name": "formatted",
                "type": "string",
                "multiValued": False,
                "description": "The full name, including all middle names, titles, and suffixes as appropriate, formatted for display (e.g., 'Ms. Barbara J Jensen, III').",
                "required": False,
                "caseExact": False,
                "mutability": "readWrite",
                "returned": "default",
                "uniqueness": "none",
            },
            {
                "name": "familyName",
                "type": "string",
                "multiValued": False,
                "description": "The family name of the User, or last name in most Western languages (e.g., 'Jensen' given the full name 'Ms. Barbara J Jensen, III').",
                "required": False,
                "caseExact": False,
                "mutability": "readWrite",
                "returned": "default",
                "uniqueness": "none",
            },
            {
                "name": "givenName",
                "type": "string",
                "multiValued": False,
                "description": "The given name of the User, or first name in most Western languages (e.g., 'Barbara' given the full name 'Ms. Barbara J Jensen, III').",
                "required": False,
                "caseExact": False,
                "mutability": "readWrite",
                "returned": "default",
                "uniqueness": "none",
            },
            {
                "name": "middleName",
                "type": "string",
                "multiValued": False,
                "description": "The middle name(s) of the User (e.g., 'Jane' given the full name 'Ms. Barbara J Jensen, III').",
                "required": False,
                "caseExact": False,
                "mutability": "readWrite",
                "returned": "default",
                "uniqueness": "none",
            },
            {
                "name": "honorificPrefix",
                "type": "string",
                "multiValued": False,
                "description": "The honorific prefix(es) of the User, or title in most Western languages (e.g., 'Ms.' given the full name 'Ms. Barbara J Jensen, III').",
                "required": False,
                "caseExact": False,
                "mutability": "readWrite",
                "returned": "default",
                "uniqueness": "none",
            },
            {
                "name": "honorificSuffix",
                "type": "string",
                "multiValued": False,
                "description": "The honorific suffix(es) of the User, or suffix in most Western languages (e.g., 'III' given the full name 'Ms. Barbara J Jensen, III').",
                "required": False,
                "caseExact": False,
                "mutability": "readWrite",
                "returned": "default",
                "uniqueness": "none",
            },
        ],
        "mutability": "readWrite",
        "returned": "default",
        "uniqueness": "none",
    }
    maf = model.AttributeFactory.create(
        d=d, locator_path="urn:ietf:params:scim:schemas:test:complex_attribute"
    )
    maf.validate_schema()


@pytest.mark.parametrize("value", [1, 0, 99, -1])
def test_int_meta_attribute(value):
    schema = {"name": "amount", "type": "integer", "required": True}
    maf = model.AttributeFactory.create(
        d=schema, locator_path="urn:ietf:params:scim:schemas:test:integer_attribute"
    )
    maf.validate_schema()

    data = {"amount": value}
    maf.validate(data)


def test_reference_meta_attribute():
    d = {
        "name": "profileUrl",
        "type": "reference",
        "referenceTypes": ["external"],
        "multiValued": False,
        "description": "A fully qualified URL pointing to a page representing the User's online profile.",
        "required": False,
        "caseExact": True,
        "mutability": "readWrite",
        "returned": "default",
        "uniqueness": "none",
    }
    maf = model.AttributeFactory.create(
        d=d,
        locator_path="urn:ietf:params:scim:schemas:test:ref_attribute",
        is_parent_multi_valued=True,
    )
    maf.validate_schema()


def test_datetime_meta_attribute():
    schema = {"name": "birthday", "type": "datetime", "required": True}
    maf = model.AttributeFactory.create(
        d=schema, locator_path="urn:ietf:params:scim:schemas:test:datetime_attribute"
    )
    maf.validate_schema()

    data = {"birthday": "2008-01-23T04:56:22Z"}
    maf.validate(data)


def test_invalid_datetime_meta_attribute():
    schema = {
        "name": "created",
        "type": "datetime",
        "description": "The 'DateTime' that the resource was added to the service provider.  This attribute MUST be a DateTime.",
        "required": False,
    }
    maf = model.AttributeFactory.create(
        d=schema, locator_path="urn:ietf:params:scim:schemas:test:datetime_attribute"
    )
    maf.validate_schema()

    data = {"created": "xyz1-01-23T04:56:22"}
    assert_exceptions = None
    try:
        maf.validate(data)
    except AssertionError as ae:
        assert_exceptions = ae

    pattern = re.compile(
        "'Single-value attribute: 'xyz1-01-23T04:56:22' \(at path.*\) is expected to be 'datetime with format 2008-01-23T04:56:22Z'"
    )
    assert re.search(pattern=pattern, string=str(assert_exceptions)) is not None


def test_decimal_meta_attribute():
    schema = {"name": "open_price", "type": "decimal", "required": True}
    maf = model.AttributeFactory.create(
        d=schema, locator_path="urn:ietf:params:scim:schemas:test:decimal_attribute"
    )
    maf.validate_schema()

    data = {"open_price": 0.1}
    maf.validate(data)


def test_invalid_decimal_meta_attribute():
    schema = {"name": "open_price", "type": "decimal", "required": True}
    maf = model.AttributeFactory.create(
        d=schema, locator_path="urn:ietf:params:scim:schemas:test:decimal_attribute"
    )
    maf.validate_schema()

    data = {"open_price": ".1"}
    assert_exceptions = None
    try:
        maf.validate(data)
    except AssertionError as ae:
        assert_exceptions = ae

    pattern = re.compile(
        "'Single-value attribute: '.1' \(at path:.*\) is expected to be 'must be a real number with at least one digit to the left and right of the period'"
    )
    assert re.search(pattern=pattern, string=str(assert_exceptions)) is not None


def test_string_meta_attribute():
    schema = {"name": "userName", "type": "string", "required": True}
    maf = model.AttributeFactory.create(
        d=schema, locator_path="urn:ietf:params:scim:schemas:test:string_attribute"
    )
    maf.validate_schema()

    data = {"userName": "Superuser"}
    maf.validate(data)


def test_invalid_string_meta_attribute():
    schema = {
        "name": "userName",
        "type": "string",
        "multiValued": False,
        "description": "Unique identifier for the User, typically used by the user to directly authenticate to the "
        "service provider. Each User MUST include a non-empty userName value.  "
        "This identifier MUST be unique across the service provider's entire set of Users. REQUIRED.",
        "required": True,
        "caseExact": False,
        "mutability": "readWrite",
        "returned": "default",
        "uniqueness": "server",
    }
    maf = model.AttributeFactory.create(
        d=schema, locator_path="urn:ietf:params:scim:schemas:test:string_attribute"
    )
    maf.validate_schema()

    data = {"userName": 123}
    assert_exceptions = None
    try:
        maf.validate(data)
    except AssertionError as ae:
        assert_exceptions = ae

    pattern = re.compile("'\(int\)123' \(at path.*\) is expected to be 'type string'")
    assert re.search(pattern=pattern, string=str(assert_exceptions)) is not None


def test_multi_valued_string_meta_attribute():
    schema = {
        "name": "userName",
        "type": "string",
        "multiValued": True,
        "required": True,
    }
    maf = model.AttributeFactory.create(
        d=schema,
        locator_path="urn:ietf:params:scim:schemas:test:multi_string_attribute",
    )
    maf.validate_schema()

    data = {"userName": ["Superuser"]}
    maf.validate(data)


def test_multi_valued_complex_meta_attribute():
    schema = {
        "name": "emails",
        "type": "complex",
        "multiValued": True,
        "description": "Email addresses for the user.  The value SHOULD be canonicalized by the service provider, e.g., 'bjensen@example.com' instead of 'bjensen@EXAMPLE.COM'. Canonical type values of 'work', 'home', and 'other'.",
        "required": False,
        "subAttributes": [
            {
                "name": "value",
                "type": "string",
                "multiValued": False,
                "description": "Email addresses for the user.  The value SHOULD be canonicalized by the service provider, e.g., 'bjensen@example.com' instead of 'bjensen@EXAMPLE.COM'. Canonical type values of 'work', 'home', and 'other'.",
                "required": False,
                "caseExact": False,
                "mutability": "readWrite",
                "returned": "default",
                "uniqueness": "none",
            },
            {
                "name": "display",
                "type": "string",
                "multiValued": False,
                "description": "A human-readable name, primarily used for display purposes.  READ-ONLY.",
                "required": False,
                "caseExact": False,
                "mutability": "readWrite",
                "returned": "default",
                "uniqueness": "none",
            },
            {
                "name": "type",
                "type": "string",
                "multiValued": False,
                "description": "A label indicating the attribute's function, e.g., 'work' or 'home'.",
                "required": False,
                "caseExact": False,
                "canonicalValues": ["work", "home", "other"],
                "mutability": "readWrite",
                "returned": "default",
                "uniqueness": "none",
            },
            {
                "name": "primary",
                "type": "boolean",
                "multiValued": False,
                "description": "A Boolean value indicating the 'primary' or preferred attribute value for this attribute, e.g., the preferred mailing address or primary email address.  The primary attribute value 'true' MUST appear no more than once.",
                "required": False,
                "mutability": "readWrite",
                "returned": "default",
            },
        ],
        "mutability": "readWrite",
        "returned": "default",
        "uniqueness": "none",
    }
    response = {
        "emails": [
            {"value": "bjensen@example.com", "type": "work", "primary": True},
            {"value": "babs@jensen.org", "type": "home"},
            {},
            {"primary": True},
        ]
    }
    maf = model.AttributeFactory.create(
        d=schema,
        locator_path="urn:ietf:params:scim:schemas:test:multi_complex_attribute",
    )
    assert maf.name == "emails"
    assert maf.element_attribute.name == "emails"
    maf.validate_schema()
    original = deepcopy(response)
    maf.validate(response)
    assert response == original


def test_multi_valued_invalid_complex_meta_attribute():
    schema = {
        "name": "emails",
        "type": "complex",
        "multiValued": True,
        "description": "Email addresses for the user.  The value SHOULD be canonicalized by the service provider, e.g., 'bjensen@example.com' instead of 'bjensen@EXAMPLE.COM'. Canonical type values of 'work', 'home', and 'other'.",
        "required": False,
        "subAttributes": [
            {
                "name": "value",
                "type": "string",
                "multiValued": False,
                "description": "Email addresses for the user.  The value SHOULD be canonicalized by the service provider, e.g., 'bjensen@example.com' instead of 'bjensen@EXAMPLE.COM'. Canonical type values of 'work', 'home', and 'other'.",
                "required": True,
                "caseExact": False,
                "mutability": "readWrite",
                "returned": "default",
                "uniqueness": "none",
            },
            {
                "name": "display",
                "type": "string",
                "multiValued": False,
                "description": "A human-readable name, primarily used for display purposes.  READ-ONLY.",
                "required": False,
                "caseExact": False,
                "mutability": "readWrite",
                "returned": "default",
                "uniqueness": "none",
            },
            {
                "name": "type",
                "type": "string",
                "multiValued": False,
                "description": "A label indicating the attribute's function, e.g., 'work' or 'home'.",
                "required": False,
                "caseExact": False,
                "canonicalValues": ["work", "home", "other"],
                "mutability": "readWrite",
                "returned": "default",
                "uniqueness": "none",
            },
            {
                "name": "primary",
                "type": "boolean",
                "multiValued": False,
                "description": "A Boolean value indicating the 'primary' or preferred attribute value for this attribute, e.g., the preferred mailing address or primary email address.  The primary attribute value 'true' MUST appear no more than once.",
                "required": False,
                "mutability": "readWrite",
                "returned": "default",
            },
        ],
        "mutability": "readWrite",
        "returned": "default",
        "uniqueness": "none",
    }
    response = {
        "emails": [
            {"value": "bjensen@example.com", "type": False, "primary": True},
            {"value": "babs@jensen.org", "type": 888},
            {},
        ]
    }
    maf = model.AttributeFactory.create(
        d=schema,
        locator_path="urn:ietf:params:scim:schemas:test:multi_complex_attribute",
    )

    assert isinstance(maf, attribute.MultiValuedAttribute)
    maf.validate_schema()
    exception = None
    try:
        maf.validate(response)
    except AssertionError as ae:
        exception = ae
    assert exception is not None, "Expected 2 assert exceptions"
    pattern_invalid_str = re.compile(
        "'\(bool\)False' \(at path: urn:ietf:params:scim:schemas:test:multi_complex_attribute/emails/type\) is expected to be 'type string'"
    )
    assert re.search(pattern_invalid_str, str(exception))
    pattern_int = re.compile(
        "'\(int\)888' \(at path: urn:ietf:params:scim:schemas:test:multi_complex_attribute/emails/type\) is expected to be 'type string'"
    )
    assert re.search(pattern_int, str(exception))


def test_multi_valued_invalid_string_meta_attribute():
    schema = {
        "name": "userName",
        "type": "string",
        "multiValued": True,
        "required": True,
    }
    maf = model.AttributeFactory.create(
        d=schema,
        locator_path="urn:ietf:params:scim:schemas:test:multi_string_attribute",
    )
    maf.validate_schema()

    data = {"userName": ["Superuser", 123, 567]}
    assert_exceptions = None
    try:
        maf.validate(data)
    except AssertionError as ae:
        assert_exceptions = ae

    pattern_123 = re.compile(
        "'\(int\)123' \(at path.*\) is expected to be 'type string'"
    )
    assert re.search(pattern=pattern_123, string=str(assert_exceptions)) is not None
    pattern_567 = re.compile(
        "'\(int\)567' \(at path.*\) is expected to be 'type string'"
    )
    assert re.search(pattern=pattern_567, string=str(assert_exceptions)) is not None


# <editor-fold desc="test meta-attribute">
@pytest.mark.parametrize("key, value", [("", "")])
def test_meta_attribute(key, value):

    example_schema_attribute_dict = {
        "name": "timezone",
        "type": "string",
        "multiValued": False,
        "description": "The User's time zone in the 'Olson' time zone database format, "
        "e.g., 'America/Los_Angeles'.",
        "required": False,
        "caseExact": False,
        "mutability": "readWrite",
        "returned": "default",
        "uniqueness": "none",
    }

    example_data = {"timezone": "25-05-2018 11:28:00.000Z"}
    meta_attribute = model.AttributeFactory.create(
        d=example_schema_attribute_dict, locator_path="root"
    )
    assert meta_attribute.name == "timezone"
    assert meta_attribute.type == "string"
    # assert meta_attribute.multi_valued == False
    meta_attribute.validate_schema()
    meta_attribute.validate(example_data)


# </editor-fold>
