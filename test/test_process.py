import pytest
import pandas as pd
import decimal as D

from file_processing_pipeline.process import process_end_of_day, CSV, EXCEL


INPUT_ROOT = 'test/resources/input_root'
OUTPUT_ROOT = 'test/resources/output_root'
REFERENCE_ROOT = 'test/resources/reference'


@pytest.mark.run(order=400)
def test_process_end_of_day_simple_csv():
    process_end_of_day(f'{INPUT_ROOT}/simple',
                       REFERENCE_ROOT,
                       f'{OUTPUT_ROOT}/simple',
                       file_type=CSV)


    errors = pd.read_csv(f'{OUTPUT_ROOT}/simple/errors/end_of_day.csv')
    valid = pd.read_parquet(f'{OUTPUT_ROOT}/simple/valid/end_of_day.parquet.snappy')

    assert errors.shape[0] == 3
    assert valid.shape[0] == 7

    assert list(valid.columns) == ['open',
                                   'high',
                                   'low',
                                   'close',
                                   'volume',
                                   'P/E',
                                   'EPS',
                                   'currency_code',
                                   'country_code',
                                   'company_source_id',
                                   'central_company_id']
    type(valid.at[0, 'high']) == D.Decimal


@pytest.mark.run(order=400)
def test_process_end_of_day_simple_excel():
    process_end_of_day(f'{INPUT_ROOT}/excel/end_of_day.xlsx',
                       f'{INPUT_ROOT}/excel/end_of_day.xlsx',
                       f'{OUTPUT_ROOT}/excel',
                       file_type=EXCEL)


    errors = pd.read_csv(f'{OUTPUT_ROOT}/excel/errors/end_of_day.csv')
    valid = pd.read_parquet(f'{OUTPUT_ROOT}/excel/valid/end_of_day.parquet.snappy')

    assert errors.shape[0] == 2
    assert valid.shape[0] == 8

    assert list(valid.columns) == ['open',
                                   'high',
                                   'low',
                                   'close',
                                   'volume',
                                   'P/E',
                                   'EPS',
                                   'currency_code',
                                   'country_code',
                                   'company_source_id',
                                   'central_company_id']
    type(valid.at[0, 'high']) == D.Decimal


@pytest.mark.skip(reason="slow (20sec), enable if curious")
@pytest.mark.run(order=400)
def test_process_end_of_day_big_csv():
    process_end_of_day(f'{INPUT_ROOT}/big',
                       REFERENCE_ROOT,
                       f'{OUTPUT_ROOT}/big',
                       file_type=CSV)


    errors = pd.read_csv(f'{OUTPUT_ROOT}/big/errors/end_of_day.csv')
    valid = pd.read_parquet(f'{OUTPUT_ROOT}/big/valid/end_of_day.parquet.snappy')

    assert errors.shape[0] < 50000
    assert valid.shape[0] > 500000

    assert list(valid.columns) == ['open',
                                   'high',
                                   'low',
                                   'close',
                                   'volume',
                                   'P/E',
                                   'EPS',
                                   'currency_code',
                                   'country_code',
                                   'company_source_id',
                                   'central_company_id']
    type(valid.at[0, 'high']) == D.Decimal
