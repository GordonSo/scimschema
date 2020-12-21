import os

from scimschema import core_schemas
from scimschema._model import attribute
from scimschema._model.schema_response import ScimResponse
from scimschema.core_schemas import load_dict as _load_dict


def read_version() -> str:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(dir_path, "VERSION")) as version_file:
        return version_file.read().strip()


__version__ = read_version()


def validate(data, extension_schema_definitions):
    ScimResponse(
        data=data,
        core_schema_definitions=core_schemas.schema,
        extension_schema_definitions=extension_schema_definitions,
    ).validate()


def load_dict_to_schema(path):
    return _load_dict(path=path)
