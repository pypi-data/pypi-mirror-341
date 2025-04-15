from __future__ import annotations

from collections.abc import Sequence
from typing import Optional, TypedDict, Union

import pandas as pd
import pyarrow as pa

from dbnl.errors import DBNLInputValidationError

from .models import (
    ListTypeDict,
    Run,
    RunConfigColumnSchemaDict,
    RunConfigScalarSchemaDict,
    RunQuery,
    RunSchemaColumnSchema,
    RunSchemaColumnSchemaDict,
    RunSchemaScalarSchema,
    RunSchemaScalarSchemaDict,
    TestSessionInput,
    _RunConfigContainerFieldSchemaDict,
    _RunConfigFieldSchemaValueTypeDict,
    _RunConfigPrimitiveFieldSchemaDict,
    _RunSchemaFieldSchemaDict,
)


def _get_schemas_from_dataframe(
    df: pd.DataFrame,
) -> list[_RunSchemaFieldSchemaDict]:
    """
    Get the column schemas for the columns in the provided dataframe.

    :param df: Dataframe from which to extract columns.
    :return: List of field schemas.
    """
    fields: list[RunSchemaColumnSchemaDict] = []
    schema = pa.Schema.from_pandas(df)
    for f in schema:
        if pa.types.is_integer(f.type):
            fields.append({
                "name": f.name,
                "type": "int",
            })
        elif pa.types.is_floating(f.type):
            fields.append(
                _RunSchemaFieldSchemaDict(
                    name=f.name,
                    type="float",
                )
            )
        elif pa.types.is_boolean(f.type):
            fields.append(
                _RunSchemaFieldSchemaDict(
                    name=f.name,
                    type="boolean",
                )
            )
        elif pa.types.is_string(f.type):
            fields.append(
                _RunSchemaFieldSchemaDict(
                    name=f.name,
                    type="string",
                )
            )
        elif pa.types.is_list(f.type):
            value_type = f.type.value_type
            if not pa.types.is_string(value_type):
                raise ValueError(
                    f"Column '{f.name}' has unsupported list value type: {value_type}. Only string is supported."
                )
            fields.append(
                _RunSchemaFieldSchemaDict(
                    name=f.name,
                    type=ListTypeDict(
                        type="list",
                        value_type="string",
                    ),
                )
            )
        elif pa.types.is_dictionary(f.type):
            fields.append(
                _RunSchemaFieldSchemaDict(
                    name=f.name,
                    type="category",
                )
            )
        else:
            raise ValueError(f"Field '{f.name}' has unsupported data type: {f.type}")
    return fields


def get_column_schemas_from_dataframe(df: pd.DataFrame) -> list[RunSchemaColumnSchemaDict]:
    return _get_schemas_from_dataframe(df)


def get_scalar_schemas_from_dataframe(df: pd.DataFrame) -> list[RunSchemaScalarSchemaDict]:
    return _get_schemas_from_dataframe(df)


def get_run_schema_columns_from_dataframe(df: pd.DataFrame) -> list[RunSchemaColumnSchema]:
    column_schema_dict = get_column_schemas_from_dataframe(df)
    return [RunSchemaColumnSchema.from_dict(d) for d in column_schema_dict]


def get_run_schema_scalars_from_dataframe(df: pd.DataFrame) -> list[RunSchemaScalarSchema]:
    scalar_schema_dict = get_scalar_schemas_from_dataframe(df)
    return [RunSchemaScalarSchema.from_dict(d) for d in scalar_schema_dict]


def _populate_optional_field_attributes(
    source: _RunSchemaFieldSchemaDict,
    target: Union[_RunConfigContainerFieldSchemaDict, _RunConfigPrimitiveFieldSchemaDict],
) -> None:
    if "description" in source:
        target["description"] = source["description"]
    if "component" in source:
        target["component"] = source["component"]
    if "greater_is_better" in source:
        target["greater_is_better"] = source["greater_is_better"]
    if "metric" in source:
        target["metric"] = source["metric"]
    if "app_context" in source:
        target["app_context"] = source["app_context"]


def _convert_run_schema_field_to_legacy_run_config_field(
    field: _RunSchemaFieldSchemaDict,
) -> Union[_RunConfigContainerFieldSchemaDict, _RunConfigPrimitiveFieldSchemaDict]:
    result: Union[_RunConfigContainerFieldSchemaDict, _RunConfigPrimitiveFieldSchemaDict]
    if isinstance(field["type"], str):
        result = _RunConfigPrimitiveFieldSchemaDict(
            name=field["name"],
            type=field["type"],
        )
    else:
        assert isinstance(field["type"], dict)
        type_ = field["type"]
        if type_["type"] == "list":
            list_type: ListTypeDict = type_
            result = _RunConfigContainerFieldSchemaDict(
                name=field["name"],
                type=list_type["type"],
                value_type=_RunConfigFieldSchemaValueTypeDict(
                    type=list_type["value_type"],
                ),
            )
        else:
            raise ValueError(f"Field '{field['name']}' has unsupported data type: {field['type']}")
    _populate_optional_field_attributes(field, result)
    return result


def get_run_config_column_schemas_from_dataframe(df: pd.DataFrame) -> list[RunConfigColumnSchemaDict]:
    run_schema_fields = _get_schemas_from_dataframe(df)
    return [_convert_run_schema_field_to_legacy_run_config_field(f) for f in run_schema_fields]


def get_run_config_scalar_schemas_from_dataframe(df: pd.DataFrame) -> list[RunConfigScalarSchemaDict]:
    run_schema_fields = _get_schemas_from_dataframe(df)
    return [_convert_run_schema_field_to_legacy_run_config_field(f) for f in run_schema_fields]


def make_test_session_input(
    *,
    run: Optional[Run] = None,
    run_query: Optional[RunQuery] = None,
    run_alias: str = "EXPERIMENT",
) -> TestSessionInput:
    """
    Create a TestSessionInput object from a Run or a RunQuery. Useful for creating TestSessions right after closing a Run.

    :param run: The Run to create the TestSessionInput from
    :param run_query: The RunQuery to create the TestSessionInput from
    :param run_alias: Alias for the Run, must be 'EXPERIMENT' or 'BASELINE', defaults to "EXPERIMENT"

    :raises DBNLInputValidationError: If both run and run_query are None

    :return: TestSessionInput object
    """
    if run_alias not in ["EXPERIMENT", "BASELINE"]:
        raise DBNLInputValidationError("run_alias must be 'EXPERIMENT' or 'BASELINE'")
    if bool(run) == bool(run_query):
        raise DBNLInputValidationError("Exactly one of `run` or `run_query` must be provided")
    if run:
        return TestSessionInput(run_alias=run_alias, run_id=run.id)
    assert run_query
    return TestSessionInput(run_alias=run_alias, run_query_id=run_query.id)


class ColumnSchemaDict(TypedDict, total=False):
    component: Optional[str]


def get_default_components_dag_from_column_schemas(
    column_schemas: Sequence[ColumnSchemaDict],
) -> Optional[dict[str, list[str]]]:
    """
    Gets the unconnected components DAG from a list of column schemas. If there are no components, returns None.
    The default components dag is of the form
    {
        "component1": [],
        "component2": [],
        ...}

    :param column_schemas: list of column schemas

    :return: dictionary of components DAG or None
    """
    components_dag: dict[str, list[str]] = {
        c["component"]: [] for c in column_schemas if "component" in c and c["component"] is not None
    }
    if not components_dag:
        return None
    return components_dag
