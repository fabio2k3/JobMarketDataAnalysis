# export_excel.py
"""
Export analysis results to a professional Excel workbook.
- Each analysis table in its own sheet
- Auto-sized columns
- Ready for pivot tables and charts
"""

import pandas as pd
from analysis import analyze_data
import os

def export_to_excel(output_path="data/exports/SalaryAnalysis.xlsx",
                    input_path="data/cleaned/ds_salaries_cleaned.csv"):
    
    summary = analyze_data(input_path)
    if not summary:
        print("No data to export.")
        return
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        for sheet_name, df in summary.items():
            df.to_excel(writer, sheet_name=sheet_name[:31])  # Excel limit 31 chars
    
    print(f"Excel workbook exported successfully to {output_path}")

if __name__ == "__main__":
    export_to_excel()
