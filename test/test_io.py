import pytest

from file_processing_pipeline.io import load_csv, load_excel


INPUT_ROOT = 'test/resources/input_root'


@pytest.mark.run(order=100)
def test_load_csv():
    df = load_csv('test/resources/simple.csv')
    assert list(df.columns) == ['a', 'b', 'c']

    # don't assume types, we'll do that later
    assert df['a'].dtype.name == 'object'

    # make sure we load all rows
    assert df.shape[0] == 4

    # make df we handle unicode
    assert df.at[2, 'b'] == 'Éclair'


@pytest.mark.run(order=100)
def test_load_excel():
    df = load_excel(f'{INPUT_ROOT}/excel/end_of_day.xlsx', 'end_of_day')

    df.shape[0] == 10
    df.shape[1] == 10
    list(df.columns) == ['open',
                         'high',
                         'low',
                         'close',
                         'volume',
                         'P/E',
                         'EPS',
                         'currency_code',
                         'country_code',
                         'company_source_id']
