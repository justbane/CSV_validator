#!/usr/bin/env python3

import argparse
import sys
from pathlib import Path
import pandas as pd
from tabulate import tabulate
import csv
from typing import Dict, Any, Tuple
import chardet
from datetime import datetime

def validate_file_path(file_path: str) -> Path:
    """
    Validate that the provided file path exists and has a .csv extension.
    
    Args:
        file_path (str): Path to the file to validate
        
    Returns:
        Path: Path object of the validated file
        
    Raises:
        FileNotFoundError: If the file does not exist
        ValueError: If the file is not a CSV file
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"The file {file_path} does not exist")
    if path.suffix.lower() != '.csv':
        raise ValueError(f"The file {file_path} is not a CSV file")
    return path

def check_csv_format(file_path: Path) -> Tuple[bool, str, Dict[str, Any]]:
    """
    Check if the CSV file is properly formatted.
    
    Args:
        file_path (Path): Path to the CSV file
        
    Returns:
        Tuple[bool, str, Dict[str, Any]]: (is_valid, error_message, details)
    """
    details = {
        'header_columns': 0,
        'data_columns': [],
        'mismatched_rows': []
    }
    
    try:
        with open(file_path, 'r', newline='') as csvfile:
            # Try to read first few lines to check format
            reader = csv.reader(csvfile)
            header = next(reader)
            if not header:
                return False, "Empty CSV file", details
            
            details['header_columns'] = len(header)
            
            # Check if all rows have the same number of columns
            for i, row in enumerate(reader, start=2):
                details['data_columns'].append(len(row))
                if len(row) != len(header):
                    details['mismatched_rows'].append({
                        'row_number': i,
                        'expected_columns': len(header),
                        'actual_columns': len(row)
                    })
            
            if details['mismatched_rows']:
                error_msg = "Column count mismatch found in the following rows:\n"
                for mismatch in details['mismatched_rows']:
                    error_msg += f"Row {mismatch['row_number']}: Expected {mismatch['expected_columns']} columns, found {mismatch['actual_columns']}\n"
                return False, error_msg.strip(), details
                
        return True, "CSV format is valid", details
    except csv.Error as e:
        return False, f"CSV format error: {str(e)}", details
    except Exception as e:
        return False, f"Error reading CSV: {str(e)}", details

def analyze_csv(file_path: Path) -> Dict[str, Any]:
    """
    Analyze the CSV file and generate a report.
    
    Args:
        file_path (Path): Path to the CSV file
        
    Returns:
        Dict[str, Any]: Analysis results
    """
    # Read the CSV file
    df = pd.read_csv(file_path)
    
    # Initialize results dictionary
    results = {
        'total_rows': len(df),
        'total_columns': len(df.columns),
        'columns': list(df.columns),
        'null_counts': df.isnull().sum().to_dict(),
        'duplicate_rows': len(df) - len(df.drop_duplicates()),
        'column_stats': {}
    }
    
    # Get statistics for each column
    for column in df.columns:
        results['column_stats'][column] = {
            'unique_values': df[column].nunique(),
            'dtype': str(df[column].dtype)
        }
    
    return results

def format_report(results: Dict[str, Any], format_check: Tuple[bool, str, Dict[str, Any]]) -> str:
    """
    Format the analysis results into a readable report.
    
    Args:
        results (Dict[str, Any]): Analysis results
        format_check (Tuple[bool, str, Dict[str, Any]]): CSV format check results
        
    Returns:
        str: Formatted report
    """
    report = []
    
    # Format check results
    report.append("CSV Format Validation")
    report.append("=" * 20)
    report.append(f"Status: {'✓ Valid' if format_check[0] else '✗ Invalid'}")
    report.append(f"Details: {format_check[1]}")
    
    # Add column alignment details if available
    if format_check[2]['header_columns'] > 0:
        report.append("\nColumn Alignment Details")
        report.append("-" * 20)
        report.append(f"Header columns: {format_check[2]['header_columns']}")
        if format_check[2]['data_columns']:
            unique_column_counts = set(format_check[2]['data_columns'])
            if len(unique_column_counts) > 1:
                report.append("Warning: Multiple column counts found in data rows")
                report.append("Column counts found: " + ", ".join(map(str, sorted(unique_column_counts))))
            else:
                report.append(f"All data rows have {format_check[2]['data_columns'][0]} columns")
    
    report.append("")
    
    # Basic statistics
    report.append("Basic Statistics")
    report.append("=" * 20)
    report.append(f"Total Rows: {results['total_rows']}")
    report.append(f"Total Columns: {results['total_columns']}")
    report.append(f"Duplicate Rows: {results['duplicate_rows']}")
    report.append("")
    
    # Null value counts
    report.append("Null Value Analysis")
    report.append("=" * 20)
    null_table = [[col, count] for col, count in results['null_counts'].items()]
    report.append(tabulate(null_table, headers=['Column', 'Null Count'], tablefmt='grid'))
    report.append("")
    
    # Column statistics
    report.append("Column Statistics")
    report.append("=" * 20)
    stats_table = [
        [
            col,
            stats['dtype'],
            stats['unique_values']
        ]
        for col, stats in results['column_stats'].items()
    ]
    report.append(tabulate(stats_table, 
                         headers=['Column', 'Data Type', 'Unique Values'],
                         tablefmt='grid'))
    
    return "\n".join(report)

def check_file_encoding(file_path: Path) -> Tuple[bool, str]:
    """
    Check if the file is UTF-8 encoded.
    
    Args:
        file_path (Path): Path to the file to check
        
    Returns:
        Tuple[bool, str]: (is_utf8, encoding_info)
    """
    try:
        # Read a chunk of the file to detect encoding
        with open(file_path, 'rb') as f:
            raw_data = f.read(10000)  # Read first 10KB for encoding detection
            result = chardet.detect(raw_data)
            
            if result['encoding'].lower() == 'utf-8':
                return True, "File is UTF-8 encoded"
            else:
                return False, f"File is {result['encoding']} encoded, not UTF-8"
    except Exception as e:
        return False, f"Error checking file encoding: {str(e)}"

def write_report_to_file(report: str, input_file: Path) -> Path:
    """
    Write the report to a file in the current directory.
    
    Args:
        report (str): The report content to write
        input_file (Path): The input CSV file path
        
    Returns:
        Path: Path to the created report file
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    input_filename = input_file.stem
    report_filename = f"{input_filename}_validation_report_{timestamp}.txt"
    report_path = Path(report_filename)
    
    try:
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        return report_path
    except Exception as e:
        print(f"Warning: Could not write report to file: {e}", file=sys.stderr)
        return None

def main():
    parser = argparse.ArgumentParser(
        description="CSV Validator - Analyzes and validates CSV files",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        "file_path",
        type=str,
        help="Path to the CSV file to analyze"
    )
    
    args = parser.parse_args()
    
    try:
        # Validate file path
        file_path = validate_file_path(args.file_path)
        
        # Check file encoding
        encoding_check = check_file_encoding(file_path)
        if not encoding_check[0]:
            print(f"Error: {encoding_check[1]}", file=sys.stderr)
            sys.exit(1)
        
        # Check CSV format
        format_check = check_csv_format(file_path)
        
        # Analyze CSV if format is valid
        if format_check[0]:
            results = analyze_csv(file_path)
            report = format_report(results, format_check)
            print(report)
            
            # Write report to file
            report_path = write_report_to_file(report, file_path)
            if report_path:
                print(f"\nReport has been written to: {report_path}")
        else:
            print(f"Error: {format_check[1]}", file=sys.stderr)
            sys.exit(1)
            
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main() 