import os

from scimschema import core_schemas
from scimschema._model import attribute
from scimschema._model.schema_response import ScimResponse
from scimschema.core_schemas import load_dict as _load_dict

__author__ = "Gordon So"
__author_email__ = "gordonkwso@gmail.com"
__classifiers__ = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]
__description__ = "A validator for System for Cross domain Identity Management (SCIM) responses given predefine schemas"
__name__ = "scimschema"
build_number = os.getenv("GITHUB_RUN_NUMBER", "")
__version__ = f"0.2.{build_number}" if build_number else "develop"
__url__ = "https://github.com/GordonSo/scimschema"


print(f"Build_number: {__version__}")


def validate(data, extension_schema_definitions):
    ScimResponse(
        data=data,
        core_schema_definitions=core_schemas.schema,
        extension_schema_definitions=extension_schema_definitions,
    ).validate()


def load_dict_to_schema(path):
    return _load_dict(path=path)
