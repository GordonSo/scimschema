import os

from scimschema import load_dict_to_schema

schema = load_dict_to_schema(path=os.path.dirname(__file__))
