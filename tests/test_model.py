import re
from scimschema._model import model

# </editor-fold># <editor-fold desc="test meta schema">


def test_meta_schema_name():
    mock_schema = {
        "id": "urn:ietf:params:scim:schemas:core2:2.0:User",
        "name": "User"
    }
    model.Model(mock_schema)._validate_schema_name()


def test_meta_schema_invalid_name():
    schema_id = "urn:ietf:params:scim:schemas:core2:2.0:User"
    mock_schema = {
        "id": schema_id,
        "name": "_User"
    }
    assert_error = None
    try:
        model.Model(mock_schema)
    except AssertionError as ae:
        assert_error = ae

    pattern_invalid_str = re.compile(
        "Model schema id {} has property name which is expected to be a valid name".format(schema_id)
    )
    assert re.search(pattern_invalid_str, str(assert_error))


def test_meta_schema_invalid_sub_attributes():
    schema_id = "urn:ietf:params:scim:schemas:core2:2.0:User"
    mock_schema = {
        "id": schema_id,
        "name": "User",
        "attributes": [
            {
                "name": "employeeNumber",
                "type": "string",
                "multiValued": False,
                "description":
                    "Numeric or alphanumeric identifier assigned to a person, "
                    "typically based on order of hire or association with an organization.",
                "required": False,
                "caseExact": False,
                "mutability": "readWrite",
                "returned": "invalid",
                "uniqueness": "none"
            },
            {
                "name": "costCenter",
                "type": "invalid",
                "multiValued": False,
                "description": "Identifies the name of a cost center.",
                "required": False,
                "caseExact": False,
                "mutability": "readWrite",
                "returned": "default",
                "uniqueness": "none"
            }
        ]
    }
    assert_error = None
    try:
        model.Model(mock_schema)
    except AssertionError as ae:
        assert_error = ae

    pattern_invalid_str = re.compile("Attribute type 'invalid' .* is not a valid type")
    assert re.search(pattern_invalid_str, str(assert_error))


def test_meta_schema_invalid_description():
    mock_schema = {
        "id": "urn:ietf:params:scim:schemas:core2:2.0:User",
        "name": "User",
        "description": 404
    }
    assert_error = None
    try:
        model.Model(mock_schema)
    except AssertionError as ae:
        assert_error = ae
    assert assert_error is not None

# </editor-fold>
