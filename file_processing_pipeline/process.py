"""End to end processing of data files, starting from input paths."""
from file_processing_pipeline.transform import transform_end_of_day
from file_processing_pipeline.io import save_parquet, save_csv, make_input_handler


EOD_FILE_NAME = 'end_of_day'


def process_end_of_day(input_path_root,
                       ref_path_root,
                       output_path_root,
                       file_type):
    ds_input = make_input_handler(file_type, input_path_root)
    ref_input = make_input_handler(file_type, ref_path_root)

    end_of_day_raw = ds_input(EOD_FILE_NAME)
    currency_code_raw = ref_input('currencies')
    country_code_raw = ref_input('countries')
    company_source_id_raw = ref_input('companies')

    valid_eod, errors_eod = transform_end_of_day(
        end_of_day_raw,
        currency_code_raw,
        country_code_raw,
        company_source_id_raw)

    save_parquet(valid_eod, f'{output_path_root}/valid/{EOD_FILE_NAME}.parquet.snappy')
    save_csv(valid_eod, f'{output_path_root}/debug/{EOD_FILE_NAME}.csv')
    if errors_eod.shape[0] > 0:
        save_csv(errors_eod, f'{output_path_root}/errors/{EOD_FILE_NAME}.csv')
