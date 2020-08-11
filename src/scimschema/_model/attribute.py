import collections
import re
from copy import deepcopy
from datetime import datetime
from . import scim_exceptions


class Attribute:
    _accepted_case_exact_value = {True, False}
    _accepted_uniqueness_value = {"none", "server", "global"}

    def __init__(
        self, d, locator_path, is_parent_multi_valued=False, is_parent_complex=False
    ):
        # default values see - https://tools.ietf.org/html/rfc7643#section-2.2
        # Characteristics # https://tools.ietf.org/html/rfc7643#section-7
        self.__d = d.copy() if not hasattr(self, "__d") is None else self.__d
        self._is_parent_multi_valued = is_parent_multi_valued
        self._is_parent_complex = is_parent_complex

        self.name = d.pop("name", None)
        self._locator_path = locator_path
        self._locator_path.append(self.name)

        self.id = d.pop("id", None)
        # self.name = d.pop("name", self.name)
        self.type = d.pop("type", "string")
        self.description = d.pop("description", None)
        self.required = d.pop("required", False)
        self.canonicalValues = d.pop("canonicalValues", None)
        self.caseExact = d.pop("caseExact", False)
        self.mutability = d.pop("mutability", "readWrite")
        self.returned = d.pop("returned", "default")
        self.uniqueness = d.pop("uniqueness", "none")
        self.multiValued = d.pop("multiValued", False)  # todo confirm default is False?
        self._d = d

    # https://tools.ietf.org/html/rfc7643#section-7
    # <editor-fold desc="validate meta attribute methods">
    def _validate_schema_id(self):
        if self.id is None:
            # todo - improve the message in this error
            raise scim_exceptions.ModelInvalidPropertyException(
                id="unknown",
                property_name="id",
                expected="Not None",
                actual="None",
                reference="https://tools.ietf.org/html/rfc7643#section-7",
            )

    def _validate_schema_name(self):
        msg = 'valid name e.g. must be ALPHA * {{nameChar}} where nameChar   = "$" / "-" / "_" / DIGIT / ALPHA'
        # ^[a-zA-Z] - starts with ALPHA 0...many
        # (\$|\-|_|\w)$ - ends with $ - _ alphanumeric
        if self.name is None or not bool(re.match("^[a-zA-Z](\$|-|_|\w)*$", self.name)):
            raise scim_exceptions.ModelAttributeCharacteristicNotAllowedException(
                locator_path=self._locator_path,
                attribute_name="name",
                expected=msg,
                actual=self.name,
            )

    def _validate_schema_required(self):
        if not isinstance(self.required, bool):
            raise scim_exceptions.ModelAttributeCharacteristicNotAllowedException(
                locator_path=self._locator_path,
                attribute_name="required",
                expected="boolean",
                actual=self.required,
            )

    def _validate_schema_canonical_values(self):
        if self.canonicalValues is not None and not isinstance(
            self.canonicalValues, list
        ):
            raise scim_exceptions.ModelAttributeCharacteristicNotAllowedException(
                locator_path=self._locator_path,
                attribute_name="canonicalValues",
                expected="none or valid list",
                actual=self.canonicalValues,
            )

    def _validate_schema_case_exact(self):
        if self.caseExact not in self._accepted_case_exact_value:
            raise scim_exceptions.ModelAttributeCharacteristicNotAllowedException(
                locator_path=self._locator_path,
                attribute_name="caseExact",
                expected=self._accepted_case_exact_value,
                actual=self.caseExact,
            )

    def _validate_schema_mutability(self):
        # https://tools.ietf.org/html/rfc7643#section-7
        expected_values = {"readWrite", "readOnly", "immutable", "writeOnly"}
        if self.mutability not in expected_values:
            raise scim_exceptions.ModelAttributeCharacteristicNotAllowedException(
                locator_path=self._locator_path,
                attribute_name="mutability",
                expected=expected_values,
                actual=self.mutability,
            )

    def _validate_schema_returned(self):
        expected_values = {"default", "always", "never", "request"}
        if self.returned not in expected_values:
            raise scim_exceptions.ModelAttributeCharacteristicNotAllowedException(
                locator_path=self._locator_path,
                attribute_name="returned",
                expected=expected_values,
                actual=self.returned,
            )

    def _validate_schema_uniqueness(self):
        if self.uniqueness not in self._accepted_uniqueness_value:
            raise scim_exceptions.ModelAttributeCharacteristicNotAllowedException(
                locator_path=self._locator_path,
                attribute_name="uniqueness_value",
                expected=self._accepted_uniqueness_value,
                actual=self.uniqueness,
            )

    def _validate_schema_type(self):
        if not isinstance(self.type, str):
            raise scim_exceptions.ModelAttributeCharacteristicNotAllowedException(
                locator_path=self._locator_path,
                attribute_name="type",
                expected="a string",
                actual=type(self.type),
            )

    # </editor-fold>

    def validate_schema(self):
        """
        :param raise_error:
        default True - scim_exceptions stored in global until delay_assert.assert_expections() is called
        :return:
        """
        exceptions = []

        def execute(f):
            try:
                f()
            except AssertionError as ae:
                exceptions.append(ae)

        execute(self._validate_schema_name)
        execute(self._validate_schema_required)
        execute(self._validate_schema_canonical_values)
        execute(self._validate_schema_case_exact)
        execute(self._validate_schema_mutability)
        execute(self._validate_schema_returned)
        execute(self._validate_schema_uniqueness)
        execute(self._validate_schema_type)

        if self._d != {}:
            exceptions.append(
                scim_exceptions.ModelAttributeUnknownPropertyException(
                    attribute_name=self.name,
                    locator=self._locator_path,
                    info="SCIM Schema parser does not recognise keys: '{}'".format(
                        self._d.keys()
                    ),
                )
            )

        if len(exceptions) > 0:
            raise scim_exceptions.AggregatedScimSchemaExceptions(
                location=self._locator_path, exceptions=exceptions
            )

    @staticmethod
    def _get_significant_value(d):
        return d

    def _get_value(self, d):
        try:
            return d.pop(self.name)
        except KeyError:
            raise scim_exceptions.ScimAttributeValueNotFoundException(
                d, self._locator_path, self.name, self.multiValued
            )

    def _validate(self, value):
        raise NotImplementedError(
            "Abstract class Attribute does not have validate method - use a concrete Class"
        )

    def validate(self, d):
        try:
            value = self._get_value(deepcopy(d))
            self._validate(value)

        except scim_exceptions.ScimAttributeValueNotFoundException:
            if self.required:
                raise
            else:
                pass
        except scim_exceptions.ScimAttributeInvalidTypeException:
            raise


class BinaryAttribute(Attribute):
    _link_reference = "https://tools.ietf.org/html/rfc7643#section-2.3.6"
    _accepted_case_exact_value = {False}
    _accepted_uniqueness_value = {"none"}

    def _validate(self, value):
        # todo - there is no proper way to know the different between a string and a binary
        if not (isinstance(value, str)):
            raise scim_exceptions.ScimAttributeInvalidTypeException(
                expected=self._d,
                locator=self._locator_path,
                value=value,
                multi_value=self.multiValued,
                attribute_type="binary",
            )


class BooleanAttribute(Attribute):

    _link_reference = "https://tools.ietf.org/html/rfc7643#section-2.3.2"
    _accepted_case_exact_value = {False}
    _accepted_uniqueness_value = {"none"}

    def _validate(self, value):
        if not isinstance(value, bool):
            raise scim_exceptions.ScimAttributeInvalidTypeException(
                expected=self._d,
                locator=self._locator_path,
                value=value,
                multi_value=self.multiValued,
                attribute_type="boolean",
            )
            # raise ValueError("{}-{} value: {} must be type boolean".format(self.id, self._locator_path, value))


class DatetimeAttribute(Attribute):

    _link_reference = "https://tools.ietf.org/html/rfc7643#section-2.3.5"
    _accepted_case_exact_value = {False}
    _accepted_uniqueness_value = {"none"}

    def _validate(self, value):
        try:
            datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            raise scim_exceptions.ScimAttributeInvalidTypeException(
                expected=self._d,
                locator=self._locator_path,
                value=value,
                multi_value=self.multiValued,
                attribute_type="datetime with format 2008-01-23T04:56:22Z",
                reference=self._link_reference,
            )


class DecimalAttribute(Attribute):

    _link_reference = "https://tools.ietf.org/html/rfc7643#section-2.3.3"
    _accepted_case_exact_value = {False}

    def _validate(self, value):
        pos_period = str(value).index(".")
        if not (
            value
            and isinstance(value, float)
            and pos_period >= 1
            and len(str(value)) - pos_period >= 1
        ):
            type_description = "must be a real number with at least one digit to the left and right of the period"
            raise scim_exceptions.ScimAttributeInvalidTypeException(
                expected=self._d,
                locator=self._locator_path,
                value=value,
                multi_value=self.multiValued,
                attribute_type=type_description,
                reference=self._link_reference,
            )


class IntegerAttribute(Attribute):

    _link_reference = "https://tools.ietf.org/html/rfc7643#section-2.3.4"
    _accepted_case_exact_value = {True, False}

    def _validate(self, value):
        if not (not isinstance(value, bool) and isinstance(value, int)):
            raise scim_exceptions.ScimAttributeInvalidTypeException(
                expected=self._d,
                locator=self._locator_path,
                value=value,
                multi_value=self.multiValued,
                attribute_type="integer",
            )
            # raise ValueError("{}-{} value: {} must be an integer".format(self.id, self._locator_path, value))


class ReferenceAttribute(Attribute):

    _link_reference = "https://tools.ietf.org/html/rfc7643#section-2.3.7"
    # todo - confirm case exact rule on reference type attribute
    # according to https://tools.ietf.org/html/rfc7643#section-2.3.7 this must be True
    # however we saw that for core:2.0:user "profileUrl" is type reference with caseextract False
    _accepted_case_exact_value = {True, False}
    referenceTypes = None

    def _validate_schema_name(self):
        if self.name == "$ref":
            return

        super()._validate_schema_name()

    def __init__(
        self, d, locator_path, is_parent_multi_valued=False, is_parent_complex=False
    ):
        self.referenceTypes = d.pop("referenceTypes", None)
        super().__init__(
            d=d,
            locator_path=locator_path,
            is_parent_multi_valued=is_parent_multi_valued,
            is_parent_complex=is_parent_complex,
        )

    def _validate(self, value):
        if not (isinstance(value, str)):
            raise scim_exceptions.ScimAttributeInvalidTypeException(
                expected=self._d,
                locator=self._locator_path,
                value=value,
                multi_value=self.multiValued,
                attribute_type="type reference",
            )


class StringAttribute(Attribute):

    _link_reference = "https://tools.ietf.org/html/rfc7643#section-2.3.1"

    def _validate(self, value):
        if not isinstance(value, str):
            raise scim_exceptions.ScimAttributeInvalidTypeException(
                expected=self._d,
                locator=self._locator_path,
                value="({}){}".format(type(value).__name__, value),
                multi_value=self.multiValued,
                attribute_type="type string",
            )

        if self.canonicalValues:
            adjusted_value = value if self.caseExact else value.lower()
            adjusted_canonical_value = (
                self.canonicalValues
                if self.caseExact
                else [cv.lower() for cv in self.canonicalValues]
            )
            if not (adjusted_value in adjusted_canonical_value):
                raise scim_exceptions.ScimAttributeInvalidTypeException(
                    expected=self._d,
                    locator=self._locator_path,
                    value=value,
                    multi_value=self.multiValued,
                    attribute_type="one of {}".format(
                        " ,".join([v for v in adjusted_canonical_value])
                    ),
                )


class ComplexAttribute(Attribute):

    _link_reference = "https://tools.ietf.org/html/rfc7643#section-2.3.8"

    def __init__(
        self, d, locator_path, is_parent_multi_valued=False, is_parent_complex=False
    ):
        self.__d = d.copy()
        super().__init__(
            d=d,
            locator_path=locator_path,
            is_parent_multi_valued=is_parent_multi_valued,
            is_parent_complex=is_parent_complex,
        )
        self.subAttributes = [
            AttributeFactory().create(
                d=d,
                locator_path=self._locator_path,
                is_parent_multi_valued=is_parent_multi_valued,
                is_parent_complex=True,
            )
            for d in d.pop("subAttributes", [])
        ]

    def _get_significant_value(self, d):
        try:
            return d.get("value")
        except KeyError:
            raise scim_exceptions.ScimAttributeValueNotFoundException(
                d, self._locator_path, self.name, self.multiValued
            )

    def validate_schema(self):
        if self._is_parent_complex:
            # sub attribute of complex cannot be complex
            raise scim_exceptions.ModelAttributeCharacteristicNotAllowedException(
                locator_path=self._locator_path,
                attribute_name=self.name,
                expected="simple type sub-attribute",
                actual="complex type sub-attribute on a complex parent",
            )

        super().validate_schema()
        exceptions = []
        for sa in self.subAttributes:
            try:
                sa.validate_schema()
            except AssertionError as ae:
                exceptions.append(ae)

        if len(exceptions) > 0:
            scim_exceptions.AggregatedScimSchemaExceptions(
                self._locator_path, exceptions=exceptions
            )

    def _validate(self, value):
        exceptions = []

        for sa in self.subAttributes:
            try:
                sa.validate(value)
            except scim_exceptions.ScimAttributeInvalidTypeException as iat:
                exceptions.append(iat)
            except Exception as e:
                exceptions.append(e)

        if len(exceptions) > 0:
            raise scim_exceptions.AggregatedScimMultValueAttributeValidationExceptions(
                self._locator_path, exceptions=exceptions
            )


class MultiValuedAttribute(Attribute):

    _link_reference = "https://tools.ietf.org/html/rfc7643#section-2.4"

    def __init__(
        self, d, locator_path, is_parent_multi_valued=False, is_parent_complex=False
    ):
        self.__d = d.copy()
        self.type = d.get("type", None)  # shared attribute name to core
        self.primary = d.pop("primary", None)
        self.display = d.pop("display", None)
        self.value = d.pop("value", None)
        self.ref = d.pop("ref", None)
        self.element_attribute = AttributeFactory().create(
            d=d,
            locator_path=locator_path,
            attribute_type=self.type,
            is_parent_multi_valued=True,
            is_parent_complex=self.type == "Complex",
        )

        super().__init__(
            d=d,
            locator_path=locator_path,
            is_parent_multi_valued=is_parent_multi_valued,
            is_parent_complex=is_parent_complex,
        )

        self.name = self.element_attribute.name
        self.multiValued = self.element_attribute.multiValued
        self.id = self.element_attribute.id
        self.description = self.element_attribute.description
        self.required = self.element_attribute.required
        self.canonicalValues = self.element_attribute.canonicalValues
        self.caseExact = self.element_attribute.caseExact
        self.mutability = self.element_attribute.mutability
        self.returned = self.element_attribute.returned
        self.uniqueness = self.element_attribute.uniqueness

    def _get_value(self, d):
        return self.element_attribute._get_value(d)

    def _validate_schema_type(self):
        if not isinstance(self.type, str):
            raise scim_exceptions.ModelAttributeCharacteristicNotAllowedException(
                locator_path=self._locator_path,
                attribute_name="type",
                expected="a string",
                actual=self.value,
            )

    def _validate_schema_primary(self):
        if not isinstance(self.primary, bool):
            raise scim_exceptions.ModelAttributeCharacteristicNotAllowedException(
                locator_path=self._locator_path,
                attribute_name="primary",
                expected="a boolean",
                actual=self.primary,
            )

    def _validate_schema_display(self):
        if not isinstance(self.display, str):
            raise scim_exceptions.ModelAttributeCharacteristicNotAllowedException(
                locator_path=self.display,
                attribute_name="ref",
                expected="a human-readable name (string)",
                actual=self.display,
            )

    def _validate_schema_ref(self):
        if not isinstance(self.ref, str):
            raise scim_exceptions.ModelAttributeCharacteristicNotAllowedException(
                locator_path=self.display,
                attribute_name="ref",
                expected="a human-readable name (string)",
                actual=self.ref,
            )

    def validate_schema(self):
        self.element_attribute.validate_schema()

    def _validate_uniqueness(self, list_values):
        if self.uniqueness:
            difference_values = [
                item
                for item, count in collections.Counter(list_values).items()
                if count > 1
            ]
            if len(set(difference_values)) > 0:
                raise scim_exceptions.ScimAttributeDuplicateValueException(
                    locator=self._locator_path, value=difference_values
                )

    def _validate(self, value):
        if not isinstance(value, list):
            raise scim_exceptions.ScimAttributeInvalidTypeException(
                self._d, self._locator_path, value, self.multiValued, "list"
            )

        adjusted_values = [
            self.element_attribute._get_significant_value(v)
            for v in value
            if (not v == {} and v is not None)
        ]
        if len(adjusted_values) == 0:
            raise scim_exceptions.ScimAttributeValueNotFoundException(
                value, self._locator_path, self.name, self.multiValued
            )

        exceptions = []
        try:
            self._validate_uniqueness(list_values=adjusted_values)
        except AssertionError as dpp:
            exceptions.append(dpp)

        for v in value:
            if not v == {} and v is not None:
                try:
                    self.element_attribute._validate(v)
                except AssertionError as iat:
                    exceptions.append(iat)

        if len(exceptions) > 0:
            raise scim_exceptions.AggregatedScimMultValueAttributeValidationExceptions(
                location="{} at path ('{}')".format(self.name, self._locator_path),
                exceptions=exceptions,
            )


attribute_factory = {
    "binary": BinaryAttribute,
    "boolean": BooleanAttribute,
    "datetime": DatetimeAttribute,
    "decimal": DecimalAttribute,
    "complex": ComplexAttribute,
    "integer": IntegerAttribute,
    "reference": ReferenceAttribute,
    "string": StringAttribute,
}


class AttributeFactory:
    @staticmethod
    def create(
        d,
        locator_path,
        attribute_type=None,
        is_parent_multi_valued=False,
        is_parent_complex=False,
    ):
        locator_path = (
            locator_path.copy() if isinstance(locator_path, list) else [locator_path]
        )
        multi_valued = d.get("multiValued", False)
        if multi_valued and attribute_type is None:
            return MultiValuedAttribute(
                d=d,
                locator_path=locator_path,
                is_parent_multi_valued=is_parent_multi_valued,
                is_parent_complex=is_parent_complex,
            )
        attribute_type = (
            d.get("type", "string") if attribute_type is None else attribute_type
        )

        if attribute_type not in attribute_factory.keys():
            raise AssertionError(
                "Attribute type '{}' (path: {}) is not a valid type - expected on of these: ({})".format(
                    attribute_type, locator_path, ", ".join(attribute_factory.keys())
                )
            )
        attribute_class = attribute_factory[attribute_type]
        return attribute_class(
            d=d,
            locator_path=locator_path,
            is_parent_multi_valued=is_parent_multi_valued,
            is_parent_complex=is_parent_complex,
        )
