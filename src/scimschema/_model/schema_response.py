from .._model.scim_exceptions import AggregatedScimMultValueAttributeValidationExceptions


class ScimResponse(dict):

    def __init__(self, data, core_schema_definitions, extension_schema_definitions):

        super().__init__()
        for key in data.keys():
            self[key] = data[key]

        self._core_meta_schemas, self._extension_schema_definitions = self._get_meta_schemas(core_schema_definitions, extension_schema_definitions)
        if len(self._core_meta_schemas) != 1:
            raise AssertionError(
                "Response must specify exactly one core schema - {}".format(", ".join([s.id for s in self._core_meta_schemas]))
            )

    def _get_meta_schemas(self, core_schema_definitions, extension_schema_definitions):
        schema_names = self.get("schemas")

        if schema_names is None or len(schema_names) == 0:
            raise AssertionError("Response has no specified schema")

        core_schema_names = list(core_schema_definitions.keys())
        core_meta_schemas = [
            core_schema_definitions[schema_name] for schema_name in schema_names if schema_name in core_schema_names
        ]

        extension_meta_schemas = [
            extension_schema_definitions[schema_name] for schema_name in schema_names if schema_name not in core_schema_names
        ]
        return core_meta_schemas, extension_meta_schemas

    def validate(self):
        data = self.copy()
        exceptions = []
        for extension_schema_model in self._extension_schema_definitions:
            tmp_data = data.pop(extension_schema_model.id, {})
            try:
                extension_schema_model.validate(tmp_data)
            except AssertionError as ae:
                exceptions.append(ae)

        for core_schema_model in self._core_meta_schemas:
            try:
                core_schema_model.validate(data)
            except AssertionError as ae:
                exceptions.append(ae)

        if len(exceptions) > 0:
            raise AggregatedScimMultValueAttributeValidationExceptions(
                location="Scim response",
                exceptions=exceptions
            )
