"""Transforms raw data sets into validated and enriched data sets."""
import pandas as pd

from file_processing_pipeline.validation import validate


def transform_end_of_day(end_of_day_raw,
                         currency_code_raw,
                         country_code_raw,
                         company_source_id_raw):
    valid_eod, errors_eod = validate(
        end_of_day_raw,
        schema_name='end_of_day',
        reference_sets={
            'currency_code': set(currency_code_raw['AlphabeticCode']),
            'country_code': set(country_code_raw['alpha-2']),
            'company_source_id': set(company_source_id_raw['source_id'])
        })

    companies = company_source_id_raw[['source_id', 'central_company_id']]
    companies = companies.rename(columns={'source_id': 'company_source_id'})

    enriched_eod = pd.merge(valid_eod,
                            companies)

    return enriched_eod, errors_eod
