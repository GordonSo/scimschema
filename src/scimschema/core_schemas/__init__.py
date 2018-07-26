import os
import glob
import json
from pathlib import Path
from .._model.model import Model
import logging
scim_logger = logging.getLogger("pyscim")


""" 
    Dynamically load all the json files at the root of this module into a dictionary attribute "schema") 
    The Key is the name of the json file (without extension)
    The Value is the json object 
    E.g. 
    from core_schemas import core2
    user_schema = core2.schema["user"]
"""


def load_dict(path):
    """
        Dynamically load all the json files at the root of this module into a dictionary attribute "schema")
        The Key is the name of the json file (without extension)
        The Value is the json object
        E.g.
        from core_schemas import core2
        user_schema = core2.schema["user"]
    """
    def load(_path):
        try:
            with open(_path) as f:
                module_name = Path(_path).stem
                scim_logger.debug("Loading {} by {}.{}".format(module_name, Model.load.__module__, Model.load.__name__))
                return Model.load(f)
        except json.JSONDecodeError as jde:
            assert jde is None, "Failed to load example: {} from {}".format(_path, __package__)

    return {schema.id: schema for schema in (load(path) for path in glob.glob(os.path.join(path, "*.json")))}


scim_logger.debug("Logging scim core schema")
schema = load_dict(path=os.path.dirname(__file__))
