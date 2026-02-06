"""
Build executive Excel dashboard from SalaryAnalysis.xlsx
- No recalculations
- Chart-ready sheets
- Designed for manual visual refinement
"""

import pandas as pd
import os

INPUT_EXCEL = "data/exports/SalaryAnalysis.xlsx"
OUTPUT_EXCEL = "excel/ChartsDashboard.xlsx"


def build_dashboard():
    if not os.path.exists(INPUT_EXCEL):
        raise FileNotFoundError(f"Input file not found: {INPUT_EXCEL}")

    os.makedirs(os.path.dirname(OUTPUT_EXCEL), exist_ok=True)

    # Sheets to extract from SalaryAnalysis
    sheets_mapping = {
        "salary_by_role": "Role_Comparison",
        "salary_by_country": "Country_Comparison",
        "salary_by_seniority": "Seniority_Analysis",
        "salary_by_remote": "Remote_Impact",
    }


    with pd.ExcelWriter(OUTPUT_EXCEL, engine="openpyxl") as writer:

        # README sheet
        readme = pd.DataFrame({
            "Dashboard Purpose": [
                "Executive-level salary insights for data-related roles.",
                "Built from cleaned and aggregated data.",
                "All calculations performed in Python.",
                "Charts and slicers intended to be added manually in Excel."
            ]
        })
        readme.to_excel(writer, sheet_name="README", index=False)

        # Copy analytical tables
        for source_sheet, target_sheet in sheets_mapping.items():
            try:
                df = pd.read_excel(INPUT_EXCEL, sheet_name=source_sheet)
                df.to_excel(writer, sheet_name=target_sheet, index=False)
            except ValueError:
                print(f"⚠ Sheet not found, skipped: {source_sheet}")

    print(f"✓ Charts dashboard base created at: {OUTPUT_EXCEL}")


if __name__ == "__main__":
    build_dashboard()
