"""Definitions of data types and other validations to apply to each data set."""
import importlib.resources as pkg_resources
import decimal as D

import yaml
from pandas_schema import Column, Schema
from pandas_schema.validation import \
    CanConvertValidation, \
    InRangeValidation, \
    CustomSeriesValidation

from file_processing_pipeline import schemas


def load_raw_schema_dict(schema_name):
    query_template = pkg_resources.read_text(schemas, f'{schema_name}.yml')
    return yaml.safe_load(query_template)


def not_null():
    return CustomSeriesValidation(lambda series: ~series.isnull(), 'is null')


def load_schema(schema_name, reference_sets):

    def validate_reference_set(reference_name):
        def validate(series):
            reference_set = reference_sets[reference_name]
            return series.isin(reference_set)
        return CustomSeriesValidation(validate, f'is not a valid {reference_name}')

    _schemas = {
        'simple': {
            'validation': Schema([
                Column('a', [CanConvertValidation(int), InRangeValidation(0, 14)]),
                Column('b', [CanConvertValidation(str), validate_reference_set('singular')]),
                Column('c', [CanConvertValidation(D.Decimal)])
            ]),
            'pandas_data_types': {
                'a': 'int64',
                'b': 'str',
                'c': 'decimal'
            }
        },
        'end_of_day': {
            'validation': Schema([
                Column('open', [CanConvertValidation(D.Decimal), not_null()]),
                Column('high', [CanConvertValidation(D.Decimal)]),
                Column('low', [CanConvertValidation(D.Decimal)]),
                Column('close', [CanConvertValidation(D.Decimal)]),
                Column('volume', [CanConvertValidation(D.Decimal)]),
                Column('P/E', [CanConvertValidation(D.Decimal)]),
                Column('EPS', [CanConvertValidation(D.Decimal)]),
                Column('currency_code', [CanConvertValidation(str),
                                         validate_reference_set('currency_code'),
                                         not_null()]),
                Column('country_code', [CanConvertValidation(str),
                                        validate_reference_set('country_code'),
                                        not_null()]),
                Column('company_source_id', [CanConvertValidation(str),
                                             validate_reference_set('company_source_id'),
                                             not_null()]),
            ]),
            'pandas_data_types': {
                'open': 'decimal',
                'high': 'decimal',
                'low': 'decimal',
                'close': 'decimal',
                'volume': 'decimal',
                'P/E': 'decimal',
                'EPS': 'decimal',
                'currency_code': 'object',
                'country_code': 'object',
                'company_source_id': 'object'
            }
        }
    }
    return _schemas[schema_name]
