"""
Utilities for converting NASA parser JSON data to pandas DataFrames.
"""

import pandas as pd
import json
from collections import defaultdict

def json_to_df(json_data):
    """
    Convert the nested JSON data from the NASA parser to a pandas DataFrame.

    Args:
        json_data (dict): Dictionary with customer IDs as keys and combined JSON data as values

    Returns:
        pandas.DataFrame: DataFrame with the extracted data
    """
    # Make sure pandas is available
    try:
        import pandas as pd
    except ImportError:
        raise ImportError("Pandas is required for DataFrame functionality. Install it with 'pip install pandas'")

    # Extract data from the nested JSON structure
    rows = []

    for cust_id, data in json_data.items():
        row = {'customer_id': cust_id}

        # Extract profile (01.pdf) data
        if 'profile' in data and data['profile']:
            profile = data['profile']

            # Customer info
            if 'customer_info' in profile:
                for key, value in profile['customer_info'].items():
                    row[f'customer_{key}'] = value

            # CIF info
            if 'cif_info' in profile:
                for key, value in profile['cif_info'].items():
                    row[f'cif_{key}'] = value

            # Total score
            if 'total_score' in profile:
                row['total_score'] = profile['total_score']

            # Assessment scores
            if 'assessment_scores' in profile:
                for score in profile['assessment_scores']:
                    field = score.get('field', '').replace(' ', '_').lower()
                    if field:
                        row[f'assessment_{field}_value'] = score.get('value', '')
                        row[f'assessment_{field}_score'] = score.get('score', 0)

        # Extract financials (02.pdf) data
        if 'financials' in data and data['financials']:
            for key, value in data['financials'].items():
                row[f'financials_{key.replace(" ", "_").lower()}'] = value

        # Extract personal info (09.pdf) data
        if 'personal_info' in data and data['personal_info']:
            for key, value in data['personal_info'].items():
                row[f'personal_{key.replace(" ", "_").lower()}'] = value

        rows.append(row)

    # Create DataFrame
    return pd.DataFrame(rows)

def save_df(df, output_path, format='csv'):
    """
    Save a DataFrame to a file in the specified format.

    Args:
        df (pandas.DataFrame): DataFrame to save
        output_path (str): Path to save the file
        format (str): Format to save ('csv', 'excel', 'parquet', etc.)

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        if format.lower() == 'csv':
            df.to_csv(output_path, index=False)
        elif format.lower() in ['excel', 'xlsx', 'xls']:
            df.to_excel(output_path, index=False)
        elif format.lower() == 'parquet':
            df.to_parquet(output_path, index=False)
        elif format.lower() == 'json':
            df.to_json(output_path, orient='records', lines=True)
        else:
            return False
        return True
    except Exception:
        return False
