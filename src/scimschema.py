from _scimschema._core_schemas import load_dict as _load_dict
from _scimschema import _core_schemas
from _scimschema._model.schema_response import ScimResponse
from _scimschema._model import scim_exceptions


def validate(data, extension_schema_definitions):
    ScimResponse(
        data=data,
        core_schema_definitions=_core_schemas.schema,
        extension_schema_definitions=extension_schema_definitions
    )


def load_dict_to_schema(path):
    return _load_dict(path=path)
