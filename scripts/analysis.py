# analysis.py
"""
Perform statistical analysis on cleaned tech jobs salary data.

- Group by role, country, seniority
- Compare remote vs on-site salaries
- Compute descriptive statistics
- Prepare summary tables
"""

import pandas as pd
import logging
import os

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def analyze_data(input_path="data/cleaned/ds_salaries_cleaned.csv") -> dict:
    if not os.path.exists(input_path):
        logging.error(f"Input file {input_path} does not exist.")
        return {}
    
    df = pd.read_csv(input_path)
    logging.info(f"Analyzing dataset with {df.shape[0]} rows.")
    
    results = {}
    
    # Salary by role
    results['salary_by_role'] = df.groupby('job_title')['salary_in_usd'].agg(['mean','median','count']).sort_values('mean', ascending=False)
    
    # Salary by country
    results['salary_by_country'] = df.groupby('employee_residence')['salary_in_usd'].agg(['mean','median','count']).sort_values('mean', ascending=False)
    
    # Salary by seniority
    results['salary_by_seniority'] = df.groupby('seniority')['salary_in_usd'].agg(['mean','median','count']).sort_values('mean', ascending=False)
    
    # Remote vs on-site
    results['salary_by_remote'] = df.groupby('remote_ratio')['salary_in_usd'].agg(['mean','median','count']).sort_index()
    
    logging.info("Analysis complete. Summary tables prepared.")
    
    return results

if __name__ == "__main__":
    summary = analyze_data()
    for key, df in summary.items():
        print(f"\n--- {key} ---")
        print(df.head(10))
