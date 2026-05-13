# CSV Data Quality Checker

A Python command-line tool for checking the quality of CSV files and generating clear reports for review

The project supports both a CLI and a flask web interface

---

## Overview

CSV Data Quality Checker helps identify common data quality issues in CSV datasets

The tool can display generated reports in following formats:

- In terminal
- As a saved Markdown file
- On the web interface

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

### Custom Rules Validation 

The tool supports loading a custom JSON rules file that validates CSV files against custom column expectations

Current Supported Rules:

- Required columns
- Maximum allowed missing value percentage
- Data type checking

Rules validation returns pass/fail results for:

- The overall dataset
- Each configured column
- Each rule check applied to those columns

Example JSON rules file:

```
{
    "columns": {
        "id": {
            "required": true,
            "type": "integer",
            "max_missing_percent": 0
        },
        "age": {
            "required": true,
            "type": "integer",
            "max_missing_percent": 0
        },
        "joined": {
            "required": true,
            "type": "date",
            "max_missing_percent": 0
        }
    }
}
```

Planned custom rule improvements:

- Minimum and Maxmimum numeric value validation
- Allowed values validation
- More data types validation support

---

### Report Output Options

The command line interface allows the user to choose how reports are produced:

- Display report in the terminal
- Save report as a Markdown file
- Display and save the report at the same time
- Choose a custom report name
- Automatically generate unique report names for batch outputs
- Include custom rules validation results in terminal and Markdown reports

---

### Web Interface

The project includes a Flask web interface that allows users to upload CSV files trhough their browser and view a generated data quality report.

Current web features

- Upload CSV files through an HTML form
- Validate that uploaded files are CSV files
- Save uploaded files into a web uploads folder
- Use timestamped filenames for saved uploads
- Support multiple CSV file uploads
- Save each batch upload into a timestamped batch folder
- Reuse existing CLI batch processing logic
- Display batch report results in the browser
- Display successful and failed file counts
- Display per-file report summaries
- Display warning messages for each uploaded file
- Basic CSS styling for the upload and report pages
- add custom rule file upload/creation support

Planned web improvements

- Add charts to display quality issues
- add .md report downloads
- improve styling and responsive layout


---

## Tech Stack

- Python 
- pandas
- Flask
- HTML
- CSS
- JavaScript


---

## Usage CLI

Run commands from the project root folder

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

#### Analyse a single CSV file with a rules file

- `PYTHONPATH=src python src/main.py --input <folder_name>/example.csv --rules <folder_name>/example.json`

#### Analyse a folder with rules

- `PYTHONPATH=src python src/main.py --input <folder_name> --rules <folder_name>/example.json`

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
- imporve web interface
- add testing suite
- add sample CSV files
