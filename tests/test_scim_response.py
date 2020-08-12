import pytest
import json
import re
from scimschema import core_schemas
from scimschema._model.schema_response import ScimResponse
from . import extension
# ------------------------------The Following are method tests ------------------------------ #


def _dict_to_json(d):
    return json.loads(json.dumps(d))


def test_validating_example_user():
    from . import examples
    ScimResponse(data=examples.user, core_schema_definitions=core_schemas.schema, extension_schema_definitions=extension.schema).validate()


def test_validating_example_group():
    from . import examples
    ScimResponse(data=examples.group, core_schema_definitions=core_schemas.schema, extension_schema_definitions=extension.schema).validate()


def test_validating_example_custom_user():
    from . import examples
    ScimResponse(data=examples.customUser, core_schema_definitions=core_schemas.schema, extension_schema_definitions=extension.schema).validate()


def test_validating_invalid_example_user():
    user_example_without_username_property = {
        "schemas": ["urn:ietf:params:scim:schemas:core:2.0:User"],
        "id": "2819c223-7f76-453a-919d-413861904646"
    }
    assert_error = None

    try:
        ScimResponse(data=user_example_without_username_property, core_schema_definitions=core_schemas.schema, extension_schema_definitions=extension.schema).validate()
    except AssertionError as ae:
        assert_error = ae
    assert assert_error is not None
    pattern_invalid_str = re.compile(
        "'Single-value attribute:userName' is required at the following location '\['urn:ietf:params:scim:schemas:core:2.0:User', 'userName'\]' but found '{'"
    )
    assert re.search(pattern_invalid_str, str(assert_error))


def test_validating_valid_example_account():
    account_examples = {
        "schemas": ["urn:ietf:params:scim:schemas:core:2.0:Group", "urn:huddle:params:scim:schemas:extension:2.0:Account"],
        "id": "2819c223-7f76-453a-919d-413861904646",
        "urn:huddle:params:scim:schemas:extension:2.0:Account": {
            "package": {}
        }
    }
    assert_error = None
    try:
        ScimResponse(data=account_examples, core_schema_definitions=core_schemas.schema, extension_schema_definitions=extension.schema).validate()
    except AssertionError as ae:
        assert_error = ae
    assert assert_error is not None
    pattern_invalid_str = re.compile(
        "'Single-value attribute:accountPackage' is required at the following location '\['urn:huddle:params:scim:schemas:extension:2.0:Account', 'package', 'accountPackage'\]' but found '{}'"
    )
    assert re.search(pattern_invalid_str, str(assert_error))


# <editor-fold desc="test Schema">
def test_get_invalid_meta_schema():

    # given a response with a validate schemas attribute - both user and group (for the sack of testing)
    example_with_schemas = _dict_to_json(
        {"schemas": ["urn:ietf:params:scim:schemas:core:2.0:User", "urn:ietf:params:scim:schemas:core:2.0:Group"]}
    )

    # when get schemas is called
    assert_exception = None
    try:
        ScimResponse(data=example_with_schemas, core_schema_definitions=core_schemas.schema, extension_schema_definitions=extension.schema)
    except AssertionError as ae:
        assert_exception = ae

    assert assert_exception is not None


def test_get_meta_schema():
    # given a response with a validate schemas attribute - both user and group (for the sack of testing)
    example_with_schemas = _dict_to_json(
        {"schemas": ["urn:ietf:params:scim:schemas:core:2.0:User"]}
    )
    # when get schemas is called
    scim_response = ScimResponse(data=example_with_schemas, core_schema_definitions=core_schemas.schema, extension_schema_definitions=extension.schema)
    # then it should return the matching modules
    expected_schemas = {core_schemas.schema["urn:ietf:params:scim:schemas:core:2.0:User"]}
    assert set(scim_response._core_meta_schemas) == expected_schemas, \
        "Get schema expected {} but got {}".format([schema["id"] for schema in expected_schemas], [schema["id"] for schema in scim_response])


@pytest.mark.parametrize(
    "schema_without_definition", [
        _dict_to_json({"schemas": []}),
        _dict_to_json({})
    ]
)
def test_get_meta_schema_without_definitions(schema_without_definition):
    # given a response without a validate schemas attribute is supplied from the row test

    # when get schemas is called
    exception = None
    try:
        ScimResponse(schema_without_definition, core_schema_definitions=core_schemas.schema, extension_schema_definitions=extension.schema)
    except AssertionError as ke:
        exception = ke

    # then exceptions should be raised
    assert isinstance(exception, AssertionError)
    assert 'Response has no specified schema' in str(exception)


