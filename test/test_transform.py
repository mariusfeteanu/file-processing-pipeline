import pytest

from file_processing_pipeline.io import load_csv
from file_processing_pipeline.transform import transform_end_of_day


RESOURCE_ROOT = 'test/resources/'
REFERENCE_ROOT = RESOURCE_ROOT + 'reference/'
COMPANIES_PATH = REFERENCE_ROOT + 'companies.csv'
COUNTRIES_PATH = REFERENCE_ROOT + 'countries.csv'
CURRENCIES_PATH = REFERENCE_ROOT + 'currencies.csv'


@pytest.mark.run(order=300)
def test_transform_end_of_day_simple():
    end_of_day_raw = load_csv(RESOURCE_ROOT + 'end_of_day_simple.csv')
    company_source_id_raw = load_csv(COMPANIES_PATH)
    country_code_raw = load_csv(COUNTRIES_PATH)
    currency_code_raw = load_csv(CURRENCIES_PATH)

    valid_end_of_day, errors_end_of_day = \
        transform_end_of_day(
            end_of_day_raw,
            currency_code_raw,
            country_code_raw,
            company_source_id_raw)

    assert valid_end_of_day.shape[0] == 2
    assert errors_end_of_day.shape[0] == 0


@pytest.mark.run(order=300)
def test_transform_end_of_day_error_country():
    end_of_day_raw = load_csv(RESOURCE_ROOT + 'end_of_day_error_country.csv')
    company_source_id_raw = load_csv(COMPANIES_PATH)
    country_code_raw = load_csv(COUNTRIES_PATH)
    currency_code_raw = load_csv(CURRENCIES_PATH)

    valid_end_of_day, errors_end_of_day = \
        transform_end_of_day(
            end_of_day_raw,
            currency_code_raw,
            country_code_raw,
            company_source_id_raw)

    assert valid_end_of_day.shape[0] == 0

    assert list(valid_end_of_day.columns) == ['open',
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

    assert errors_end_of_day.shape[0] == 3

    assert errors_end_of_day.at[0, 'reason'] == 'is not a valid country_code'
    assert errors_end_of_day.at[1, 'reason'] == 'is not a valid country_code'
    assert errors_end_of_day.at[2, 'reason'] == 'is null'
