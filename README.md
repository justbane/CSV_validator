# CSV Validator CLI Tool

A command-line interface tool for analyzing and validating CSV files. This tool performs comprehensive checks on CSV files and generates detailed reports about their content and structure.

## Features

- Validates CSV file format
- Checks file encoding (UTF-8 validation)
- Validates column alignment and consistency
- Counts duplicate records
- Analyzes null values in each column
- Reports column data types
- Counts unique values per column
- Provides basic file statistics
- Generates detailed validation reports in text files

## Prerequisites

- Python 3.6 or higher
- Git (for cloning the repository)
- pip (Python package installer)

## Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd csv-validator
   ```

2. Create and activate a virtual environment:

   On macOS/Linux:
   ```bash
   # Create virtual environment
   python3 -m venv venv
   
   # Activate virtual environment
   source venv/bin/activate
   ```

   On Windows:
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   .\venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Verify installation:
   ```bash
   python csv_validator.py --help
   ```

### Deactivating the Virtual Environment

When you're done using the tool, you can deactivate the virtual environment:

```bash
deactivate
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
   - Validates UTF-8 encoding
   - Checks column alignment and consistency

2. Column Alignment Details
   - Number of columns in header
   - Column count consistency across data rows
   - Detailed information about any mismatched rows

3. Basic Statistics
   - Total number of rows
   - Total number of columns
   - Number of duplicate rows

4. Null Value Analysis
   - Count of null values in each column

5. Column Statistics
   - Data type of each column
   - Number of unique values in each column

### Report Files

The tool automatically generates a detailed report file in the current directory with a name format:
```
<original_filename>_validation_report_YYYYMMDD_HHMMSS.txt
```

For example:
```
data_validation_report_20240321_143022.txt
```

## Error Handling

The tool will:
- Verify that the provided file exists and has a .csv extension
- Check for proper CSV formatting
- Validate UTF-8 encoding
- Check column alignment and consistency
- Exit with a status code of 1 if any errors are encountered
- Display appropriate error messages to stderr

## Development

To contribute to the project:

1. Install the required dependencies as described above
2. Make your changes
3. Test thoroughly with various CSV files
4. Submit a pull request 