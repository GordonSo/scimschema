import re

from scimschema import validate

from . import extension


# A sample schema, like what we'd get from response.get(<scim entity url>).json()
def test_validate_invalid_repsonse():
    content = {
        "schemas": [
            "urn:ietf:params:scim:schemas:core:2.0:Group",
            "urn:huddle:params:scim:schemas:extension:2.0:SimpleAccount",
        ],
        "id": "2819c223-7f76-453a-919d-413861904646",
        "externalId": 9,
        "meta": {
            "resourceType": "User",
            "created": "2011-08-01T18:29:49.793Z",
            "lastModified": "Invalid date",
            "location": "https://example.com/v2/Users/2819c223...",
            "version": r"W\/(\")f250dd84f0671c3(\")",
        },
    }
    try:
        validate(data=content, extension_schema_definitions=extension.schema)
    except AssertionError as ae:
        expected_error = (
            "attribute:ipRestrictionsEnabled' is required at the following location"
        )
        pattern = re.compile(expected_error)
        assert pattern.findall(str(ae))


# >>>    E   scimschema._model.scim_exceptions.AggregatedScimMultValueAttributeValidationExceptions: Found 1 aggregated exceptions at Scim response:
# >>>    E    ScimAttributeValueNotFoundException:
# >>>    E    	 'Single-value attribute:ipRestrictionsEnabled' is required at the following location '['urn:huddle:params:scim:schemas:extension:2.0:Account', 'ipRestrictionsEnabled']' but found '{}'
# >>>    !!!!!!!!!!!!!!!!!!! Interrupted: 1 errors during collection !!!!!!!!!!!!!!!!!!!
