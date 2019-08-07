from click.testing import CliRunner
import pytest

import pandas as pd

from file_processing_pipeline.cli import cli


INPUT_ROOT = 'test/resources/input_root'
OUTPUT_ROOT = 'test/resources/output_root'
REFERENCE_ROOT = 'test/resources/reference'


@pytest.mark.run(order=500)
def test_cli_csv():
  runner = CliRunner()
  result = runner.invoke(cli,
                         ['--input-root', f'{INPUT_ROOT}/cli',
                          '--reference-root', REFERENCE_ROOT,
                          '--output-root', f'{OUTPUT_ROOT}/cli'])

  assert result.exit_code == 0, result.output

  errors = pd.read_csv(f'{OUTPUT_ROOT}/cli/errors/end_of_day.csv')
  valid = pd.read_parquet(f'{OUTPUT_ROOT}/cli/valid/end_of_day.parquet.snappy')

  assert errors.shape[0] == 3
  assert valid.shape[0] == 7


@pytest.mark.run(order=500)
def test_cli_excel():
  runner = CliRunner()
  result = runner.invoke(cli,
                         ['--input-root', f'{INPUT_ROOT}/excel/end_of_day.xlsx',
                          '--reference-root', f'{INPUT_ROOT}/excel/end_of_day.xlsx',
                          '--output-root', f'{OUTPUT_ROOT}/cli_excel',
                          '--file-type', 'excel'])

  assert result.exit_code == 0, result.output

  errors = pd.read_csv(f'{OUTPUT_ROOT}/cli_excel/errors/end_of_day.csv')
  valid = pd.read_parquet(f'{OUTPUT_ROOT}/cli_excel/valid/end_of_day.parquet.snappy')

  assert errors.shape[0] == 2
  assert valid.shape[0] == 8


@pytest.mark.run(order=500)
def test_cli_no_args():
  runner = CliRunner()
  result = runner.invoke(cli, [])

  assert result.exit_code > 0
  assert result.output.startswith('Usage:')
