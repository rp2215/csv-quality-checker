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

To Do:

- assign each column a quality score based on (missing values etc)
- overall file quality score
- charts to visually display num of errors
- export report as .txt
- web interface 
- num unque values per column
- summaries for numeric columns:
    - min
    - max
    - mean
    - median
- let user choose report name
- configurable rules, user loads rules and csv file -> returns pass/fail for each column based on rules
- schema validation



