# CSV Validator CLI Tool

A command-line interface tool for analyzing and validating CSV files. This tool performs comprehensive checks on CSV files and generates detailed reports about their content and structure.

## Features

- Validates CSV file format
- Counts duplicate records
- Analyzes null values in each column
- Reports column data types
- Counts unique values per column
- Provides basic file statistics

## Prerequisites

- Python 3.6 or higher
- Git (for cloning the repository)

## Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd csv-validator
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the validator by providing a path to your CSV file:
```bash
python csv_validator.py /path/to/your/file.csv
```

### Arguments

- `file_path`: Path to the CSV file you want to analyze (required)

### Example

```bash
python csv_validator.py data.csv
```

### Sample Output

The tool will generate a report with the following sections:

1. CSV Format Validation
   - Confirms if the file is properly formatted
   - Reports any formatting issues

2. Basic Statistics
   - Total number of rows
   - Total number of columns
   - Number of duplicate rows

3. Null Value Analysis
   - Count of null values in each column

4. Column Statistics
   - Data type of each column
   - Number of unique values in each column

## Error Handling

The tool will:
- Verify that the provided file exists and has a .csv extension
- Check for proper CSV formatting
- Exit with a status code of 1 if any errors are encountered
- Display appropriate error messages to stderr

## Development

To contribute to the project:

1. Install the required dependencies as described above
2. Make your changes
3. Test thoroughly with various CSV files
4. Submit a pull request 