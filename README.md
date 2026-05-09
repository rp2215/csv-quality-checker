# CSV Data Quality Checker

## Overview

CSV Data Quality Checker is a basic Python command-line project that analyses CSV files and produces a simple data quality report.

## Features

Implemented:

- Load a CSV file
- Count rows and columns
- Display column names
- Count missing values per column
- Detect duplicate rows
- Show data types
- Generate a basic report
- support for batch upload/ every csv file in folder
- allow user to choose between termina report output, markdown report download, or both
- optional user can choose report name
- calculate column level quality scores
- calculate overall file quality score 
- display overall file quality rating
- cli input path
- summaries for numeric columns

To Do:

- charts to visually display num of errors
- export report as .txt
- export reports as .json
- web interface 
- num unque values per column
   
- warning messages with severity levels e.g. Datasets contains duplicate rows (Medium), Age column has more than 50% missing values (HIGH)
- configurable rules, user loads rules and csv file -> returns pass/fail for each column based on rules
- schema validation
- recursive option for folders within folders
- progress messages/ percentage during batch uploads
- for batch uploads can output into a desired folder





