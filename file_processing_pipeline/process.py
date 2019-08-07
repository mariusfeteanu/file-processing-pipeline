"""End to end processing of data files, starting from input paths."""
from file_processing_pipeline.transform import transform_end_of_day
from file_processing_pipeline.io import load_csv, save_parquet, save_csv, load_excel


EOD_FILE_NAME = 'end_of_day'
CSV = 'csv'
EXCEL = 'excel'


def handle_input(file_type, path_root):
    """
    path root is
        - a folder name for csv files
        - an excel workbook for excel file
    """
    def handle_csv_input(data_set_name):
        return load_csv(f'{path_root}/{data_set_name}.{file_type}')

    def handle_excel_input(data_set_name):
        return load_excel(path_root, data_set_name)

    if file_type == CSV:
        return handle_csv_input
    elif file_type == EXCEL:
        return handle_excel_input


def process_end_of_day(input_path_root,
                       ref_path_root,
                       output_path_root,
                       file_type):
    ds_input = handle_input(file_type, input_path_root)
    ref_input = handle_input(file_type, ref_path_root)

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
    save_csv(errors_eod, f'{output_path_root}/errors/{EOD_FILE_NAME}.csv')
