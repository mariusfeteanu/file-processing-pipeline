"""A command line interface to processes files."""
import click

from file_processing_pipeline.process import process_end_of_day, CSV


@click.command()
@click.option("-d", "--data-set",
              help="The data set to import, e.g. end_of_day.",
              default='end_of_day',
              required=True)
@click.option("-i", "--input-root",
              help="The directory containing the dataset, or the excel workbook (not just dir).",
              required=True)
@click.option("-r", "--reference-root",
              help="The directory containing the reference data,"
                   " or the excel workbook (not just dir).",
              required=True)
@click.option("-o", "--output-root",
              help="The directory where to output the data.",
              required=True)
@click.option("-t", "--file-type",
              help="The input file type (csv or excel).",
              default=CSV,
              required=True)
def cli(data_set,
        input_root,
        reference_root,
        output_root,
        file_type):
    if data_set == 'end_of_day':
        process_end_of_day(input_path_root=input_root,
                           ref_path_root=reference_root,
                           output_path_root=output_root,
                           file_type=file_type)


def main():  # pragma: nocover
    cli(auto_envvar_prefix='FPP')  # pylint: disable=unexpected-keyword-arg,no-value-for-parameter
