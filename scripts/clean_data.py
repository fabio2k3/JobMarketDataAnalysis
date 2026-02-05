# clean_data.py
"""
Clean and preprocess the tech jobs salary dataset.

Steps:
- Load raw CSV
- Standardize column names
- Clean text fields
- Handle missing values
- Convert salary to numeric
- Create derived columns
- Save cleaned dataset
"""

import pandas as pd
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def clean_data(input_path="data/raw/ds_salaries.csv",
               output_path="data/cleaned/ds_salaries_cleaned.csv") -> pd.DataFrame:
    if not os.path.exists(input_path):
        logging.error(f"Input file {input_path} does not exist.")
        return
    
    # Load dataset
    df = pd.read_csv(input_path)
    logging.info(f"Loaded dataset with {df.shape[0]} rows and {df.shape[1]} columns.")
    
    # Standardize column names
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    
    # Clean text fields
    text_cols = ['experience_level', 'employment_type', 'job_title', 'employee_residence', 'company_location']
    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.upper().str.strip()
    
    # Handle missing values
    missing = df.isnull().sum()
    logging.info(f"Missing values per column:\n{missing}")
    df.dropna(inplace=True)
    
    # Ensure salary is numeric
    df['salary_in_usd'] = pd.to_numeric(df['salary_in_usd'], errors='coerce')
    df = df.dropna(subset=['salary_in_usd'])
    
    # Derived columns
    # Example: create a simplified seniority column
    level_map = {"EN": "JUNIOR", "MI": "MID", "SE": "SENIOR", "EX": "EXECUTIVE"}
    df['seniority'] = df['experience_level'].map(level_map).fillna("UNKNOWN")
    
    # Save cleaned dataset
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    logging.info(f"Cleaned dataset saved to {output_path} with {df.shape[0]} rows.")
    
    return df

if __name__ == "__main__":
    clean_data()
