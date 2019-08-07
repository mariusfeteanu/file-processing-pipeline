## File Processing Pipeline-

We would like you to create a python process to pick up two flat files (excel and csv), validate them and to produce output files.

Original File
Parquet File
(Error file – if applicable)

You will need to produce a series of input files which will test the logic in your python package. For example, a file containing character codes within a decimal field will produce an error file. The error file is to contain the reason for failure and the field and row on which it occurred.

### For the CSV File

Create a file having 10 fields each with the following types:-

- 7 Decimal fields (28,8) – any value is allowed (negative and positive)
- 1 Country field (ISO standard) – create a lookup file
- 1 Currency field (ISO standard) – create a lookup file
- 1 Company field (make up a list of dummy companies – must have grave accent codes ).
  You will need to create a lookup file. Containing source id, central company id and company name
- Make the company, currency, country and one decimal field mandatory.

### For Excel

Create two worksheets one containing the 10 fields specified above and the other the list of lookup codes (company, currency and country)


Provide processing files that cover a small number of records for both the csv and excel.
In addition for the csv a file containing a large number of records (up to ½ million)

Validation & Check which needs to be done

- Validate data types
- Validate Country against a list
- Validate currency against a list
- Validate company against your lookup file using the company source id from you dummy data. Append the central company id to the output file.
