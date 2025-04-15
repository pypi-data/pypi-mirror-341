import os
import json
import logging
import pdfplumber
import re
from glob import glob
from collections import defaultdict

# Configure logging
log_file = "pdf_processing.log"
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def group_pdfs_by_customer(folder_path):
    """Group PDFs by customer ID based on the naming pattern {custid_01.pdf}, {custid_02.pdf}, {custid_09.pdf}."""
    pdf_groups = defaultdict(list)
    pdf_pattern = os.path.join(folder_path, "*.pdf")

    for pdf_path in glob(pdf_pattern):
        filename = os.path.basename(pdf_path)
        # Match pattern like 2W00297489_NA_01.pdf
        match = re.match(r"(.+)_(\d{2})\.pdf$", filename)
        if match:
            cust_id = match.group(1)  # e.g., 2W00297489_NA
            suffix = match.group(2)   # e.g., 01, 02, 09
            if suffix in ['01', '02', '09']:
                pdf_groups[cust_id].append((suffix, pdf_path))

    # Validate groups
    valid_groups = {}
    for cust_id, files in pdf_groups.items():
        suffixes = set(suffix for suffix, _ in files)
        if suffixes == {'01', '02', '09'}:
            valid_groups[cust_id] = dict(files)
        else:
            logger.warning(f"Incomplete PDF set for customer {cust_id}: {suffixes}")

    return valid_groups

# Code from _01.pdf processing
def process_pdf_01(pdf_path):
    json_data = {
        "customer_info": {},
        "assessment_scores": [],
        "total_score": 0,
        "cif_info": {}
    }

    try:
        logger.debug(f"Processing _01 PDF: {pdf_path}")
        with pdfplumber.open(pdf_path) as pdf:
            page = pdf.pages[0]
            text = page.extract_text()
            tables = page.extract_tables()

            parse_text_01(text, json_data)
            if tables:
                parse_tables_01(tables, json_data)
            extract_all_assessment_scores_01(text, json_data)
            clean_json_data_01(json_data)

            if "branch" in json_data["cif_info"]:
                del json_data["cif_info"]["branch"]

        return json_data
    except Exception as e:
        logger.error(f"Error processing _01 PDF {pdf_path}: {e}")
        return None

def parse_text_01(text, json_data):
    lines = text.splitlines()
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue
        try:
            if line.startswith("1. Customer Name"):
                json_data["customer_info"]["name"] = line.replace("1. Customer Name", "").strip()
            elif line.startswith("2. Account Number"):
                json_data["customer_info"]["account_number"] = line.replace("2. Account Number", "").strip()
            elif line.startswith("3.Branch Name & Code"):
                json_data["customer_info"]["branch"] = line.replace("3.Branch Name & Code", "").strip()
            elif "CIF Code" in line and ":" in line:
                code_parts = line.split(":", 1)
                code = code_parts[1].strip()
                cif_match = re.search(r"\(CIF code-\s*([^\)]+)\)", code)
                code = cif_match.group(1).strip() if cif_match else re.sub(r"\s*\([^\)]*\)", "", code).strip()
                json_data["cif_info"]["code"] = code
            elif line.startswith("Name of CIF-") or line.startswith("CIF Name :"):
                json_data["cif_info"]["name"] = line.replace("Name of CIF-", "").replace("CIF Name :", "").strip()
            elif "Total score obtained" in line:
                match = re.search(r"Total score obtained.*?(\d+)(?=\s*$|\s+out)", line)
                if match:
                    json_data["total_score"] = int(match.group(1))
        except Exception as e:
            logger.error(f"Error parsing text line {i}: {line} - {e}")

def parse_tables_01(tables, json_data):
    for table_idx, table in enumerate(tables):
        for row_idx, row in enumerate(table):
            try:
                row = [str(cell).strip() if cell else "" for cell in row]
                if not any(row):
                    continue
                if row[0] and "Customer Name" in row[0]:
                    json_data["customer_info"]["name"] = row[1] if len(row) > 1 else ""
                elif row[0] and "Account Number" in row[0]:
                    json_data["customer_info"]["account_number"] = row[1] if len(row) > 1 else ""
                elif row[0] and "Branch Name & Code" in row[0]:
                    json_data["customer_info"]["branch"] = row[1] if len(row) > 1 else ""
                extract_assessment_from_table_row_01(row, json_data)
            except Exception as e:
                logger.error(f"Error processing table {table_idx}, row {row_idx}: {row} - {e}")

def extract_assessment_from_table_row_01(row, json_data):
    if len(row) < 3:
        return
    field_name = None
    value = None
    score = None
    fields = {
        "I. Annual": "Annual Income (Rs. in Lacs)",
        "II. Occupation": "Occupation",
        "III.Age": "Age",
        "IV. Quali": "Qualification",
        "V. Residence": "Residence Population Group",
        "VI.Existing": "Existing Ownership/Investments"
    }
    for key, fname in fields.items():
        if row[0].startswith(key):
            field_name = fname
            value = row[1].strip()
            break
    if field_name:
        for i, cell in enumerate(row):
            if "Score" in cell and i < len(row) - 1 and row[i+1].isdigit():
                score = int(row[i+1])
                break
            elif "Score" in cell:
                score_match = re.search(r"Score\s+(\d+)", cell)
                if score_match:
                    score = int(score_match.group(1))
                    break
        if field_name and score is not None:
            add_assessment_score_01(json_data, field_name, value, score)

def add_assessment_score_01(json_data, field, value, score):
    value = re.sub(r'Score\s+\d+', '', value).strip()
    value = re.sub(r'\s+', ' ', value).strip()
    for entry in json_data["assessment_scores"]:
        if entry["field"] == field:
            entry.update({"value": value, "score": score})
            return
    json_data["assessment_scores"].append({"field": field, "value": value, "score": score})

def extract_all_assessment_scores_01(text, json_data):
    patterns = [
        (r"I\.\s*Annual\s*Income.*?(\d{1,2},\d{2},\d{3})\s*Score\s*(\d+)", "Annual Income (Rs. in Lacs)"),
        (r"III\.Age\s*(\d+)\s*Score\s*(\d+)", "Age"),
        (r"IV\.\s*Quali[fic]+ation\s*(\w+)\s*Score\s*(\d+)", "Qualification"),
        (r"V\.\s*Residence\s*Population\s*Group\s*(\w+)\s*Score\s*(\d+)", "Residence Population Group")
    ]
    for pattern, field in patterns:
        match = re.search(pattern, text, re.DOTALL)
        if match:
            add_assessment_score_01(json_data, field, match.group(1).strip(), int(match.group(2)))

    # Occupation
    lines = text.splitlines()
    occupation_start = -1
    occupation_text = []
    occupation_score = None
    for i, line in enumerate(lines):
        if "II. Occupation" in line:
            occupation_start = i
            score_match = re.search(r"Score\s+(\d+)", line)
            if score_match:
                occupation_score = int(score_match.group(1))
            line_text = re.sub(r"Score\s+\d+", "", line.replace("II. Occupation", "")).strip()
            if line_text:
                occupation_text.append(line_text)
            break
    if occupation_start >= 0:
        i = occupation_start + 1
        while i < len(lines) and not any(field in lines[i] for field in ["III.Age", "IV. Quali", "V. Residence"]):
            line = lines[i].strip()
            if re.match(r"^\s*Score\s+\d+\s*$", line):
                if not occupation_score:
                    score_match = re.search(r"Score\s+(\d+)", line)
                    if score_match:
                        occupation_score = int(score_match.group(1))
                i += 1
                continue
            line = re.sub(r"Score\s+\d+", "", line).strip()
            if line:
                occupation_text.append(line)
            i += 1
        if not occupation_score:
            score_context = "\n".join(lines[max(0, occupation_start-3):occupation_start+6])
            score_match = re.search(r"Score\s+(\d+)", score_context)
            occupation_score = int(score_match.group(1)) if score_match else 0
        if occupation_text:
            full_text = " ".join(occupation_text).strip()
            add_assessment_score_01(json_data, "Occupation", full_text, occupation_score)

    # Investments
    investment_patterns = [
        r"VI\.Existing\s*Ownership/?\s*Investments\s*([^S]+?)\s*Score\s*(\d+)",
        r"VI\.Existing\s*Ownership/?\s*([^S]+?)\s*Score\s*(\d+)",
        r"VI\.Existing\s*Ownership/?\s*Investments\s*(Insurance\s*/\s*MF\s*Product[^S]+?)\s*Score\s*(\d+)"
    ]
    for pattern in investment_patterns:
        match = re.search(pattern, text, re.DOTALL)
        if match:
            value = re.sub(r'\s+', ' ', match.group(1).strip())
            add_assessment_score_01(json_data, "Existing Ownership/Investments", value, int(match.group(2)))
            break
        else:
            lines = text.splitlines()
            for i, line in enumerate(lines):
                if "VI.Existing Ownership" in line:
                    area_text = "\n".join(lines[i:i+5])
                    investment_match = re.search(r"(Insurance\s*/\s*MF\s*Product[^S]+?)(?=Score|$)", area_text)
                    if investment_match:
                        value = re.sub(r'\s+', ' ', investment_match.group(1).strip())
                        score_match = re.search(r"Score\s+(\d+)", area_text)
                        if score_match:
                            add_assessment_score_01(json_data, "Existing Ownership/Investments", value, int(score_match.group(1)))
                            break

def clean_json_data_01(json_data):
    for section in ["customer_info", "cif_info"]:
        for key, value in json_data[section].items():
            if isinstance(value, str):
                json_data[section][key] = re.sub(r'\s+', ' ', value).strip()
    for score_entry in json_data["assessment_scores"]:
        if isinstance(score_entry["value"], str):
            score_entry["value"] = re.sub(r'Score\s+\d+', '', score_entry["value"]).strip()
    expected_fields = [
        "Annual Income (Rs. in Lacs)", "Occupation", "Age", "Qualification",
        "Residence Population Group", "Existing Ownership/Investments"
    ]
    existing_fields = {entry["field"]: entry for entry in json_data["assessment_scores"]}
    ordered_scores = []
    for field in expected_fields:
        if field in existing_fields:
            ordered_scores.append(existing_fields[field])
        else:
            ordered_scores.append({"field": field, "value": "", "score": 0})
            logger.warning(f"Added missing field: {field}")
    json_data["assessment_scores"] = ordered_scores

# Code from _02.pdf processing
def process_pdf_02(pdf_path):
    data = {
        "Customer Risk Score": "",
        "Customer Risk Appetite": "",
        "Eligible Products": "",
        "Gross Annual Income (A)": "",
        "Gross Annual Expenditure (Incldg EMI) (B)": "",
        "Surplus Income Available C=(A)-(B)": "",
        "Recommended Annual Premium/SIP": "",
        "SPCRPC": "",
        "Policyholder's Age at Present (A)": "",
        "Product's max entry age (B)": "",
        "Product's max exit age (C)": "",
        "Recommended Policy Term D = (C - A)": ""
    }

    try:
        logger.debug(f"Processing _02 PDF: {pdf_path}")
        with pdfplumber.open(pdf_path) as pdf:
            full_text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    full_text += page_text + "\n"

            patterns = [
                (r"Customer Risk Score\s*(\d+)", "Customer Risk Score"),
                (r"Customer Risk Appetite\s*(\w+)", "Customer Risk Appetite"),
                (r"Eligible Products\s*([^\n]+)", "Eligible Products"),
                (r"Gross Annual Income \(A\)\s*([\d,]+)", "Gross Annual Income (A)"),
                (r"Gross Annual Expenditure \(Incldg EMI\) \(B\)\s*([\d,]+)", "Gross Annual Expenditure (Incldg EMI) (B)"),
                (r"Surplus Income Available C=\(A\)-\(B\)\s*([\d,]+)", "Surplus Income Available C=(A)-(B)"),
                (r"Recommended Annual Premium/SIP\s*(?:.*?Upto 50% of Surplus.*?\s*)?(\d{6,})", "Recommended Annual Premium/SIP"),
                (r"Policyholder's Age at Present \(A\)\s*(\d+)", "Policyholder's Age at Present (A)"),
                (r"Product's max entry age \(B\)\s*(\d+)", "Product's max entry age (B)"),
                (r"Product's max exit age \(C\)\s*(\d+)", "Product's max exit age (C)"),
                (r"Recommended Policy Term D = \(C - A\)\s*(\d+)", "Recommended Policy Term D = (C - A)")
            ]
            for pattern, key in patterns:
                match = re.search(pattern, full_text, re.IGNORECASE | re.DOTALL)
                if match:
                    data[key] = match.group(1).strip()
            data["SPCRPC"] = ""
        return data
    except Exception as e:
        logger.error(f"Error processing _02 PDF {pdf_path}: {e}")
        return None

# Code from _09.pdf processing
def process_pdf_09(pdf_path):
    data = {}
    try:
        logger.debug(f"Processing _09 PDF: {pdf_path}")
        with pdfplumber.open(pdf_path) as pdf:
            text = pdf.pages[0].extract_text()
            patterns = [
                (r"Date of Birth\s*(\d{2}-\d{2}-\d{4})", "Date of Birth"),
                (r"Mobile No\.\s*:?\s*(\d{10})", "Mobile No.", re.IGNORECASE),
                (r"Email ID\s*:?\s*([\w\.]+@[\w\.]+)", "Email ID", re.IGNORECASE),
                (r"Date\s*:?\s*(\d{2}-\d{2}-\d{4})", "Date", re.IGNORECASE),
                (r"I express my willingness to buy the (SBI Life - Smart Annuity Plus)", "Product")
            ]
            for pattern, key, *flags in patterns:
                match = re.search(pattern, text, *flags)
                if match:
                    data[key] = match.group(1)
        return data
    except Exception as e:
        logger.error(f"Error processing _09 PDF {pdf_path}: {e}")
        return None

def combine_json_outputs(json_01, json_02, json_09, cust_id):
    """Combine the three JSON outputs into a single JSON."""
    combined = {
        "customer_id": cust_id,
        "profile": json_01 or {},
        "financials": json_02 or {},
        "personal_info": json_09 or {}
    }
    return combined

def main(folder_path):
    """Main function to process PDFs and generate combined JSON outputs."""
    if not os.path.exists(folder_path):
        logger.error(f"Folder not found: {folder_path}")
        return

    pdf_groups = group_pdfs_by_customer(folder_path)
    output_dir = os.path.join(folder_path, "output")
    os.makedirs(output_dir, exist_ok=True)

    for cust_id, pdfs in pdf_groups.items():
        logger.info(f"Processing customer: {cust_id}")
        json_01 = process_pdf_01(pdfs["01"]) if "01" in pdfs else None
        json_02 = process_pdf_02(pdfs["02"]) if "02" in pdfs else None
        json_09 = process_pdf_09(pdfs["09"]) if "09" in pdfs else None

        combined_json = combine_json_outputs(json_01, json_02, json_09, cust_id)
        output_path = os.path.join(output_dir, f"{cust_id}_combined.json")
        try:
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(combined_json, f, indent=2)
            logger.info(f"Saved combined JSON for {cust_id} to {output_path}")
        except Exception as e:
            logger.error(f"Error saving JSON for {cust_id}: {e}")

if __name__ == "__main__":
    folder_path = input("Enter the folder path containing PDFs: ")
    main(folder_path)
