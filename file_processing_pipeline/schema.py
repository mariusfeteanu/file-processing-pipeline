"""Definitions of data types and other validations to apply to each data set."""
import importlib.resources as pkg_resources
import decimal as D
from argparse import Namespace

import yaml
from pandas_schema import Column, Schema
from pandas_schema.validation import \
    InRangeValidation, \
    CustomSeriesValidation, \
    CanConvertValidation

from file_processing_pipeline import schemas


def load_raw_fields_schema(schema_name):
    query_template = pkg_resources.read_text(schemas, f'{schema_name}.yml')
    return yaml.safe_load(query_template)['schema']['fields']


def parse_validation(validation, reference_sets):
    def validate_reference_set(reference_name):
        def validate(series):
            reference_set = reference_sets[reference_name]
            return series.isin(reference_set)
        return CustomSeriesValidation(validate, f'is not a valid {reference_name}')

    if isinstance(validation, dict):
        name, config = list(validation.items())[0]
        if name == 'InRangeValidation':
            return InRangeValidation(**config)
        elif name == 'reference':
            return validate_reference_set(config)
    elif isinstance(validation, str):  # pragma: nocover
        if validation == 'not_null':
            return not_null()


def get_all_validations(field_schema, reference_sets):
    for validation in field_schema.get('validations', []):
        yield parse_validation(validation, reference_sets)

    if not field_schema.get('nullable', True):
        yield not_null()

    if field_schema['type'] == 'decimal':
        yield CanConvertValidation(D.Decimal)
    else:
        type_map = {'str': str, 'int64': int, 'float64': float, 'bool': bool}
        yield CanConvertValidation(type_map[field_schema['type']])


def load_schema_whatev(schema_name, reference_sets):
    raw_fields_schema = load_raw_fields_schema(schema_name)
    schema = Namespace()

    schema.pandas_data_types = {
        field_schema['name']: field_schema['type']
        for field_schema
        in raw_fields_schema
    }

    schema.validations = Schema([
        Column(field_schema['name'],
               get_all_validations(field_schema, reference_sets))
        for field_schema
        in raw_fields_schema
    ])
    return schema


def not_null():
    return CustomSeriesValidation(lambda series: ~series.isnull(), 'is null')


def load_schema(schema_name, reference_sets):
    _schemas = {
        'simple': {
            'validation': load_schema_whatev('simple', reference_sets).validations,
            'pandas_data_types': load_schema_whatev('simple', reference_sets).pandas_data_types
        },
        'end_of_day': {
            'validation': load_schema_whatev('end_of_day', reference_sets).validations,
            'pandas_data_types': load_schema_whatev('end_of_day', reference_sets).pandas_data_types
        }
    }
    return _schemas[schema_name]
