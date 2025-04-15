"""
NASA Parser Library - A tool for parsing NASA PDF files and extracting structured data.

This library can:
- Process NASA PDFs and extract structured information
- Convert the data to JSON
- Convert the data to pandas DataFrames
- Save data in various formats
"""

import os
import logging
from pathlib import Path

# Configure logging
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Import the main functionality from nasa_parser.py
from .nasa_parser import (
    group_pdfs_by_customer,
    process_pdf_01,
    process_pdf_02,
    process_pdf_09,
    combine_json_outputs
)

# Import DataFrame utilities
from .dataframe_utils import json_to_df

def process_folder(folder_path, save_json=False, output_dir=None):
    """
    Process all PDF files in the specified folder and return the combined JSON results.

    Args:
        folder_path (str): Path to the folder containing PDF files
        save_json (bool): Whether to save JSON output files
        output_dir (str, optional): Directory to save output files (defaults to folder_path/output)

    Returns:
        dict: Dictionary with customer IDs as keys and combined JSON data as values
    """
    folder_path = os.path.abspath(folder_path)
    if not os.path.exists(folder_path):
        logger.error(f"Folder not found: {folder_path}")
        return {}

    if output_dir is None:
        output_dir = os.path.join(folder_path, "output")

    if save_json:
        os.makedirs(output_dir, exist_ok=True)

    pdf_groups = group_pdfs_by_customer(folder_path)
    results = {}

    for cust_id, pdfs in pdf_groups.items():
        logger.info(f"Processing customer: {cust_id}")
        json_01 = process_pdf_01(pdfs["01"]) if "01" in pdfs else None
        json_02 = process_pdf_02(pdfs["02"]) if "02" in pdfs else None
        json_09 = process_pdf_09(pdfs["09"]) if "09" in pdfs else None

        combined_json = combine_json_outputs(json_01, json_02, json_09, cust_id)
        results[cust_id] = combined_json

        if save_json:
            output_path = os.path.join(output_dir, f"{cust_id}_combined.json")
            try:
                with open(output_path, "w", encoding="utf-8") as f:
                    import json
                    json.dump(combined_json, f, indent=2)
                logger.info(f"Saved combined JSON for {cust_id} to {output_path}")
            except Exception as e:
                logger.error(f"Error saving JSON for {cust_id}: {e}")

    return results

def get_dataframe(folder_path):
    """
    Process PDF files and return the data as a pandas DataFrame.

    Args:
        folder_path (str): Path to the folder containing PDF files

    Returns:
        pandas.DataFrame: DataFrame with the extracted data
    """
    results = process_folder(folder_path)
    return json_to_df(results)

def save_dataframe(folder_path, output_file, format='csv'):
    """
    Process PDF files and save the data as a DataFrame in the specified format.

    Args:
        folder_path (str): Path to the folder containing PDF files
        output_file (str): Path to save the output file
        format (str): Format to save ('csv', 'excel', 'parquet', etc.)

    Returns:
        bool: True if successful, False otherwise
    """
    df = get_dataframe(folder_path)

    try:
        if format.lower() == 'csv':
            df.to_csv(output_file, index=False)
        elif format.lower() in ['excel', 'xlsx', 'xls']:
            df.to_excel(output_file, index=False)
        elif format.lower() == 'parquet':
            df.to_parquet(output_file, index=False)
        elif format.lower() == 'json':
            df.to_json(output_file, orient='records', lines=True)
        else:
            logger.error(f"Unsupported format: {format}")
            return False

        logger.info(f"DataFrame saved to {output_file} in {format} format")
        return True
    except Exception as e:
        logger.error(f"Error saving DataFrame: {e}")
        return False
