# Schema / Model exceptions


class AggregatedScimSchemaExceptions(AssertionError):
    def __init__(self, location, exceptions):
        msg = "Invalid SCIM schema {}: {} aggregated exceptions found: \n {}".format(
            location, len(exceptions), "\n\t".join(["{}: \n \t {}".format(e.__class__.__name__, str(e)) for e in exceptions])
        )
        super().__init__(msg)


class AggregatedScimMultValueAttributeValidationExceptions(AssertionError):
    def __init__(self, location, exceptions):
        msg = "Found {} aggregated exceptions at {}: \n {}".format(
            len(exceptions), location, "\n\t".join(["{}: \n \t {}".format(e.__class__.__name__, str(e)) for e in exceptions])
        )
        super().__init__(msg)


class ModelInvalidPropertyException(AssertionError):

    def __init__(
            self, id, property_name, expected, actual, reference="https://tools.ietf.org/html/rfc7643#section-2.1"
    ):
        msg =\
            "Model schema id {} has property {}" \
            " which is expected to be {} but got ""{}"" ({})".format(
                id, property_name, expected, actual, reference
            )
        super().__init__(msg)


class ModelAttributeUnknownPropertyException(AssertionError):
    def __init__(self, attribute_name, locator, info):
        super().__init__("Unknown properties {} on attribute '{} (path: '{}''".format(info, attribute_name, locator))


class ModelAttributeCharacteristicNotAllowedException(AssertionError):
    def __init__(self, locator_path, attribute_name, expected, actual):
        msg = \
            "Attribute ""{}"" and " \
            "has '{}' property which must be {} but got '{}' (https://tools.ietf.org/html/rfc7643#section-2.1)".format(
                locator_path, attribute_name, expected, actual
            )
        super().__init__(msg)


# Value exceptions


class ScimAttributeValueNotFoundException(AssertionError):
    def __init__(self, d, locator, attribute_name, multi_value):
        mv_attribute = "Single-value attribute" if not multi_value else "Multi-value attribute"
        super().__init__(
            "'{}:{}' is required at the following location '{}' but found '{}'".format(mv_attribute, attribute_name, locator, d)
        )


class ScimAttributeInvalidTypeException(AssertionError):
    def __init__(self, expected, locator, value, multi_value, attribute_type, sub_attributes_exceptions=None, reference=None):
        path = "/".join(locator)
        mv_attribute = "Single-value attribute" if not multi_value else "Multi-value attribute"
        error_msg = "'{}: '{}' (at path: {}) is expected to be '{}' (see: {})"\
            .format(mv_attribute, value, path, attribute_type, expected, reference)
        if not sub_attributes_exceptions:
            super().__init__(sub_attributes_exceptions, error_msg)
        else:
            super().__init__(error_msg)


class ScimAttributeDuplicateValueException(AssertionError):
    def __init__(self, locator, value):
        path = "/".join(locator)
        error_msg = "'Multi-value attribute: '{}' (at path: {}) is not unique as required".format(value, path)
        super().__init__(error_msg)


class ScimAttributeInvalidPrimaryPropertyException(AssertionError):
    def __init__(self, locator, value):
        path = "/".join(locator)
        error_msg = "'Multi-value attribute: '{}' (at path: {}) has more than one values with 'primary' property"\
            .format(value, path)
        super().__init__(error_msg)