import os
import glob
import json
from pathlib import Path
import logging

scim_logger = logging.getLogger("pyscim")
scim_logger.setLevel(logging.DEBUG)


def load_json_dict(path):
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
                scim_logger.error("Loading {} by {}.{}".format(module_name, json.load.__module__, json.load.__name__))
                globals()[module_name] = json.load(f)
        except json.JSONDecodeError as jde:
            assert jde is None, "Failed to load example: {} from {}".format(_path, __package__)

    return [load(path) for path in glob.glob(os.path.join(path, "*.json"))]

load_json_dict(path=os.path.dirname(__file__))
