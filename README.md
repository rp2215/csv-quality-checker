# CSV Data Quality Checker

![CI](https://github.com/rp2215/csv-quality-checker/actions/workflows/ci.yml/badge.svg)

A Python based tool for analysing CSV files, identifying data quality issues, and generating clear reports with insightful information through both a command-line interface and a Flask web interface

---

## Overview

CSV Data Quality Checker helps users review CSV datasets and identify common data quality issues 

This project supports:

- CLI-based CSV analysis
- Flask web uploads
- Batch CSV processing
- Custom JSON rule creation and validation
- Markdown report downloads
- Automated testing with pytest
- CI checks with GitHub Actions and Ruff

---

## Key Features

### CSV Analysis

The tool analyses CSV files and generate a structured quality report covering the main indicators of dataset quality

Reports include:

- Dataset summary information
- Missing value analysis
- Duplicate row and column checks
- Data type overview
- Numeric column summaries
- Column level quality scores
- Overall file quality score
- Quality rating:
    - Excellent
    - Good
    - Needs Review
    - Poor
- Warning messages grouped by severity

---

### Custom Rules Validation 

Users can validate CSV files against custom column expectations using a JSON rules file.

They can either:

- Upload an existing JSON rules file
- Create a new rules file through the web interface using the built in rules builder and download the generated `.json` file

Rules validation returns pass/fail for:

- The overall dataset
- Each configured column
- Each individual rule check with reason for failure

Supported rule types include:

- Required and optional columns
- Maximum missing value percentages
- Type Checks:
    - Integer
    - Date
    - Boolean
- Minimum and Maximum numeric values
- A list of allowed values

Example rules file:

```json
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

---

### Batch Processing

The CLI and web interface both support batch CSV processing.

Batch Processing allows:

- Processing of all CSV files in selected folder or upload batch
- Scanning of folders recursively to find all CSV files
- Per file success or failure reports
- Continuation of processing if a file in batch fails


---

### Flask Web Interface

The Flask web app allows user to analyse their CSV files through a browser reusing the same core processing logic as the CLI.

Current web features:

- Upload one or more CSV files
- Upload an optional JSON rules file
- Create a custom rules JSON file through the browser
- View batch results in the browser
- Download Markdown reports
- Choose custom report names
- Use timestamped upload and report folders to avoid filename collisions

---

## Tech Stack

- Python 
- pandas
- pytest
- Flask
- HTML
- CSS
- JavaScript
- Ruff
- GitHub Actions


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

#### Save a Markdown report

- `python main.py --input <folder_name>/example.csv --mode download`

#### Display and save a report

- `python main.py --input <folder_name>/example.csv --mode both`

#### Choose custom report name

- `python main.py --input <folder_name>/example.csv --mode download --report-name <custom_report_name>`

#### Analyse with a custom rules file

- `PYTHONPATH=src python src/main.py --input <folder_name>/example.csv --rules <folder_name>/example.json`

---

## Web App Usage

Run the Flask app from the project root:

`PYTHONPATH=src python -m web_app.app`

Then open:

`http://127.0.0.1:5000`

---

## Testing

The project uses pytest for automated testing.

Run tests with:

`PYTHONPATH=src pytest`

---

## CI Pipeline

The project includes a GitHub Actions CI workflow

The pipeline runs on push and pull requests to `main` branch

It checks:

- Ruff linting
- pytest tests
- CLI startup via `--help`


## Roadmap

Planned improvements:

- add cleanup logic for old uploads and reports
- add configurable warning thresholds
- add screenshots/ short demo
- add Docker support for easier setup
- regex pattern validation
- data preview in report (first 5 lines)
- .xlsx support
- add unique rule
- add date range rule
- colour coded terminal output
- drag and drop upload on web interface
- dark mode toggle for interface
