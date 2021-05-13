import json
import re
from copy import deepcopy
from typing import Dict, List, Optional, TextIO

from . import scim_exceptions
from .attribute import Attribute, AttributeFactory


class Model(object):
    id: str = ""
    name: Optional[str] = None
    description: Optional[str] = None
    attributes: List[Attribute] = []

    def __init__(self, schema_data: Dict):

        self.id = schema_data.pop("id", "")
        self.external_id = schema_data.pop("externalId", None)
        self.meta = schema_data.pop("meta", None)

        self.name = schema_data.pop("name", None)
        self.description = schema_data.pop("description", None)
        attributes = schema_data.pop("attributes", None)

        if attributes:
            self.attributes = [
                AttributeFactory().create(
                    d=d,
                    locator_path=[self.id] if self.id else [],
                    is_parent_multi_valued=False,
                )
                for d in attributes
            ]

        exceptions = []
        try:
            self.validate_schema()
        except AssertionError as ae:
            exceptions.append(ae)

        if schema_data != {}:
            e = AssertionError(
                "Unexpected properties found: {}".format(schema_data.keys())
            )
            exceptions.append(e)

        if len(exceptions) > 0:
            raise scim_exceptions.AggregatedScimMultValueAttributeValidationExceptions(
                location=self.id, exceptions=exceptions
            )

    def validate(self, d):
        for attribute in self.attributes:
            attribute.validate(d=deepcopy(d))

    def validate_schema(self):
        exceptions = []
        try:
            self._validate_schema_id()
        except AssertionError as ae:
            exceptions.append(ae)
        try:
            self._validate_schema_name()
        except AssertionError as ae:
            exceptions.append(ae)
        try:
            self._validate_schema_description()
        except AssertionError as ae:
            exceptions.append(ae)
        try:
            self._validate_schema_attributes()
        except AssertionError as ae:
            exceptions.append(ae)

        if len(exceptions) > 0:
            raise scim_exceptions.AggregatedScimSchemaExceptions(self.id, exceptions)

    def _validate_schema_id(self):
        if not self.id:
            raise scim_exceptions.ModelInvalidPropertyException(
                id=self.id,
                property_name="id",
                expected="not None",
                actual="None",
                reference="https://tools.ietf.org/html/rfc7643#section-7",
            )

    def _validate_schema_name(self):
        if self.name is None:
            # OPTIONAL for scim schema - mandatory for service providers overriden via inheritance
            return

        if not bool(re.match(r"^[a-zA-Z]*([a-zA-Z]|\s)*(\$|-|_|\w)$", self.name)):
            raise scim_exceptions.ModelInvalidPropertyException(
                id=self.id,
                property_name="name",
                expected="a valid name - "
                'must be ALPHA * {{nameChar}} where nameChar   = "$" / "-" / "_" / DIGIT / ALPHA',
                actual=self.name,
            )

    def _validate_schema_description(self):
        if self.description is None:
            return

        if not isinstance(self.description, str):
            raise scim_exceptions.ModelInvalidPropertyException(
                id=self.id,
                property_name="description",
                expected="a non-string description",
                actual=self.description,
            )

    def _validate_schema_attributes(self):
        exceptions = []
        for attribute in self.attributes:
            try:
                attribute.validate_schema()
            except AssertionError as ae:
                exceptions.append(ae)
        if len(exceptions) > 0:
            raise scim_exceptions.AggregatedScimMultValueAttributeValidationExceptions(
                location=self.id, exceptions=exceptions
            )

    @staticmethod
    def load(file: TextIO) -> "Model":
        data = json.load(file)
        return Model(data)


class MetaServiceProviderSchema(Model):
    def _validate_schema_name(self):
        if self.name is None or not bool(
            re.match(self.name, r"^[\w]*(\$|\-|_|\d|\w)$")
        ):
            raise scim_exceptions.ModelInvalidPropertyException(
                id=self.id,
                property_name="name",
                expected="meta schema: {}-{}- name must be "
                'LPHA * {nameChar} where nameChar   = "$" / "-" / "_" / DIGIT / ALPHA',
                actual=self.name,
            )

    def _validate_schema_description(self):
        if self.description is None or not isinstance(self.description, str):
            raise scim_exceptions.ModelInvalidPropertyException(
                id=self.id,
                property_name="description",
                expected="service providers MUST specify the description",
                actual=self.description,
                reference="https://tools.ietf.org/html/rfc7643#section-6",
            )
