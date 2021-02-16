import re

from scimschema import validate

from . import extension

content = {
    "id": "2819c223-7f76-453a-919d-413861904646",
    "name": "2819c223-7f76-453a-919d-413861904646",
    "schemas": [ "urn:ietf:params:scim:schemas:core:2.0:Schema" ],
    "attributes": [
        {
            "name": "name",
            "type": "complex",
            "multiValued": False,
            "description": "The components of the user's real name. Providers MAY return just the full name as a single string in the formatted sub-attribute, or they MAY return just the individual component attributes using the other sub-attributes, or they MAY return both. If both variants are returned, they SHOULD be describing the same name, with the formatted name indicating how the component attributes should be combined.",
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
    ]
}


# A sample schema, like what we'd get from response.get(<scim entity url>).json()
def test_validate_response():
    validate(data=content, extension_schema_definitions=extension.schema)
