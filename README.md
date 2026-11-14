# Excel & CSV Automation Tool

A simple Python command-line tool for merging CSV files, removing duplicate rows, and exporting cleaned data to Excel or CSV.

## Features

- Merge multiple CSV files into one dataset
- Remove duplicate rows
- Export results to `.xlsx` or `.csv`
- Automatically create output directories
- Display basic processing statistics
- Automated testing with pytest

## Technologies

- Python 3.14
- pandas
- openpyxl
- pytest

## Installation

Clone the repository:

```bash
git clone https://github.com/danilevskiiis/excel-csv-automation.git
cd excel-csv-automation
```

Create a virtual environment and install dependencies:

```bash
python -m venv .venv
python -m pip install -r requirements.txt
```

## Usage

Run the tool:

```bash
python src/main.py --input examples --output output/result.xlsx
```

Export to CSV instead:

```bash
python src/main.py --input examples --output output/result.csv
```

## Run Tests

```bash
python -m pytest -v
```

## Limitations

Input CSV files should use UTF-8 encoding, comma-separated fields, and compatible column structures.

## License

No license has been selected yet.
