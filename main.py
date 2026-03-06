"""
MAIN PIPELINE 
"""

import subprocess
from pathlib import Path

scripts = [
    "src.data.clean_buyers",
    "src.data.clean_sales", 
    "src.data.clean_products",
    "src.data.join",
    "src.analysis.analysis",
    "src.visualization.charts",
    "src.recommendations.recommender",
    "src.reports.generate_reports"
]

print("\n" + "="*60)
print(" RUNNING COMPLETE PIPELINE")
print("="*60)

for i, script in enumerate(scripts, 1):
    print(f"\n[{i}/8] Running {script}...")
    result = subprocess.run(f"python -m {script}", shell=True)
    
    if result.returncode != 0:
        print(f" Failed at {script}")
        break

print("\n" + "="*60)
print(" PIPELINE COMPLETE! Check reports/ folder")
print("="*60)