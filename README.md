# CSV Data Quality Checker

A Python command-line tool for checking the quality of CSV files and generating clear reports for review

---

## Overview

CSV Data Quality Checker helps identify common data quality issues in CSV datasets

The tool can display reports in the terminal, save reports as Markdown files, or both. It also supports batch processing, recursive folder scanning, custom report names, and progress messages during larger batch runs.

---

## Features

### CSV Analysis

- Load and validate CSV files
- Count rows and columns
- Display column names
- Count missing values per column
- Calculate missing value percentages
- Detect duplicate rows
- Calculate duplicate row percentages
- Detect empty rows
- Detect duplicate column names
- Show data types for each column
- Count unique values per column
- Generate numeric summaries of columns:
    - Minimum
    - Maximum
    - Mean
    - Median

---

### Quality Scoring

- Calculate column level quality scores
- Calculate an overall file quality score
- Display an overall file quality rating:
    - Excellent
    - Good
    - Needs Review
    - Poor

---

### Warning System

The tool generates warning messages with the following severity levels:
- CRITICAL
- HIGH
- MEDIUM
- LOW

Warnings are generated for issues such as:
- Columns with high missing value percentages
- Completely empty columns/rows
- Duplicate rows
- Duplicate column names
- Low value variation in columns
- Poor overall file quality scores

---

### Batch Processing

- Process every CSV file inside a selected folder with option for recursive scanning for subfolders
- Displays progress messages during batch proecessing showing file count and completion percentage
- Will continue to process remaining files even if one file fails
- Save separate reports for each successfully processed files

---

### Report Output Options

The command line interface allows the user to choose how reports are produced:

- Display report in the terminal
- Save report as a Markdown file
- Display and save the report at the same time
- Choose a custom report name
- Automatically generate unique report names for batch outputs

---

### Web Interface

The project includes an early Flask web interface that allows users to upload a CSV file trhough their browser and view a generated data quality report.

Current web features

- Upload a CSV file through an HTML form
- Validate that the uploaded file is a CSV
- Save uploaded files into a web uploads folder
- Run existing CLI quality check logic
- Display report results in browser

Planned web improvements

- Add styling with CSS
- Add charts to display quality issues
- support multiple file uploads
- timestamp for saved uploads
- add .md report downloads

---

## Tech Stack

- Python 
- pandas
- Flask
- HTML


---

## Usage CLI

#### Analyse a single CSV file

- `python main.py --input <folder_name>/example.csv`

#### Analyse a folder of CSV files

- `python main.py --input <folder_name>`

#### Analyse folders recursively

- `python main.py --input <folder_name> --recursive`

#### Show report in terminal

- `python main.py --input <folder_name>/example.csv --mode terminal`

#### Save report as a Markdown file

- `python main.py --input <folder_name>/example.csv --mode download`

#### Show report in terminal and download it

- `python main.py --input <folder_name>/example.csv --mode both`

#### Choose custom report name

- `python main.py --input <folder_name>/example.csv --mode download --report-name <custom_report_name>`

## Usage Web App

#### Run the Flask Web App

- From project root folder run `PYTHONPATH=src python -m web_app.app` then open `http://127.0.0.1:5000` in browser

---

## Roadmap

Planned improvements:

- Add charts to visually display data quality issues
- Export reports as `.txt`
- Export reports as `.json`
- Allow users to choose the output folder for saved reports
- Add schema validation
- Add configurable quality rules
- Allow users to load a rules file and validate CSV files against it
- Return pass/fail results for each column based on custom rules
- imporve web interface
- add testing suite
- add sample CSV files
