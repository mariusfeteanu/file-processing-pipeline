import decimal as D

from file_processing_pipeline.validation import validate
from file_processing_pipeline.io import load_csv


def test_apply():
    df = load_csv('test/resources/simple.csv')
    valid_df, errors_df = validate(df, 'simple', {'singular': ('word', 'Éclair')})
    assert list(valid_df.columns) == ['a', 'b', 'c']

    # make sure the correct type were set
    assert valid_df['a'].dtype.name == 'int64'
    assert valid_df['b'].dtype.name == 'object'  # means str
    assert valid_df['c'].dtype.name == 'object'
    assert type(valid_df.at[0, 'c']) is D.Decimal

    # make sure we only load valid rows
    assert valid_df.shape[0] == 1

    # and we flag errors
    assert errors_df.shape[0] == 2

    # range errors
    assert errors_df.at[1, 'row'] == 2
    assert errors_df.at[1, 'field'] == 'a'
    assert errors_df.at[1, 'reason'] == 'was not in the range [0, 14)'
    assert errors_df.at[1, 'value'] == '15'

    # lookup errors
    assert errors_df.at[0, 'row'] == 1
    assert errors_df.at[0, 'field'] == 'b'
    assert errors_df.at[0, 'reason'] == 'is not a valid singular'
    assert errors_df.at[0, 'value'] == 'words'
