import pytest

from file_processing_pipeline.schema import load_raw_fields_schema


@pytest.mark.run(order=100)
def test_load_raw_fields_schema():
    simple_schema = load_raw_fields_schema('simple')
    assert simple_schema == [
        {
        'name': 'a',
        'type': 'int64',
        'validations': [{'InRangeValidation': {'min': 0, 'max': 14}}]
        },
        {
        'name': 'b',
        'type': 'str',
        'validations': [{'reference': 'singular'}]
        },
        {
        'name': 'c',
        'type': 'decimal'
        }
    ]
