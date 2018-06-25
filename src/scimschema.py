from _scimschema.core_schemas import load_dict as _load_dict
from _scimschema import core_schemas
from _scimschema._model.schema_response import ScimResponse
from _scimschema._model import scim_exceptions, model, attribute


__all__ = [
    "core_schemas",
    "validate",
    "load_dict_to_schema",
    "scim_exceptions",
    "model",
    "attribute"
]


def validate(data, extension_schema_definitions):
    ScimResponse(
        data=data,
        core_schema_definitions=core_schemas.schema,
        extension_schema_definitions=extension_schema_definitions
    )


def load_dict_to_schema(path):
    return _load_dict(path=path)
