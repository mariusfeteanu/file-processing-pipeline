"""Uses provided schemas to validate raw data sets."""
import decimal as D

import pandas as pd

from file_processing_pipeline.schema import load_schema


def validate(df, schema_name, reference_sets):
    """
    Applies a schema to a data frame. Returns two data frames:
        - one with valid rows
        - one with errors
    """
    schema = load_schema(schema_name, reference_sets)

    if df.shape[0] > 0:
        # Remove invalid rows
        errors = schema.validations.validate(df)
        error_index_labels = [error.row for error in errors]
        # Create a data frame containing the errors, reasons etc.
        errors_df = get_errors_df(errors)
        valid_df = df.drop(df.index[error_index_labels])
    else:
        errors_df = get_errors_df([])
        valid_df = df

    # apply pandas data types to valid ones
    valid_df = apply_pandas_data_types(valid_df, schema.pandas_data_types)

    return valid_df, errors_df


def apply_pandas_data_types(df, pandas_data_types):
    # apply pandas native data type
    native_data_types = {field_name: (data_type if data_type != 'decimal' else 'object')
                         for field_name, data_type
                         in pandas_data_types.items()}
    df = df.astype(native_data_types)

    # Decimals are not handled natively by pandas so we manually convert them
    decimal_col_names = [field_name
                         for field_name, data_type
                         in pandas_data_types.items()
                         if data_type == 'decimal']

    for decimal_col_name in decimal_col_names:
        df[decimal_col_name] = df[decimal_col_name].apply(D.Decimal)

    return df


def get_errors_df(errors):
    error_header = ['row', 'field', 'value', 'reason']
    if not errors:
        return pd.DataFrame(columns=error_header)

    errors_list = ([error.row, error.column, error.value, error.message]
                   for error
                   in errors)
    errors_df = pd.DataFrame(errors_list)
    errors_df.columns = error_header
    return errors_df
