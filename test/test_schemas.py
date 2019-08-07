import pytest

from file_processing_pipeline.schema import load_raw_schema_dict


@pytest.mark.run(order=100)
def test_load_raw_schema_dict():
    simple_schema = load_raw_schema_dict('simple')
    print(simple_schema)
