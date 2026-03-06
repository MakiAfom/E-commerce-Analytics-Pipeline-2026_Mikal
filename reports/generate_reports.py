"""
REPORT GENERATOR 
"""

from pathlib import Path
from datetime import datetime
import pandas as pd

# Load data
base = Path(__file__).parent.parent  # This goes to Ecommerce_Analysis_2025
df = pd.read_csv(base / "data/processed/master_sales_data.csv")

print(f"Looking for file at: {base / 'data/processed/master_sales_data.csv'}")
df['revenue'] = df['quantity'] * df['price']
df['profit'] = df['revenue'] - (df['quantity'] * df['unit_cost'])




ref = df[df['is_referred']==1]['revenue'].mean()
non = df[df['is_referred']==0]['revenue'].mean()
bf = df[df['is_black_friday']]['revenue'].mean()
norm = df[~df['is_black_friday']]['revenue'].mean()
hourly = df.groupby('order_hour').size()
low = list(hourly.nsmallest(6).index)
savings = len(low) * 25 * 365
top_region = df.groupby('region')['profit'].sum().idxmax()
region_profit = df.groupby('region')['profit'].sum().max()

# Data 
data = {
    "DATE": datetime.now().strftime("%Y-%m-%d"),
    "REVENUE": f"{df['revenue'].sum():,.0f}",
    "PROFIT": f"{df['profit'].sum():,.0f}",
    "ORDERS": f"{len(df):,}",
    "AVG_ORDER": f"{df['revenue'].mean():.0f}",
    "REF_AVG": f"{ref:.0f}", "NON_AVG": f"{non:.0f}", 
    "REF_LIFT": f"{((ref/non)-1)*100:.0f}",
    "BF_AVG": f"{bf:.0f}", "NORM_AVG": f"{norm:.0f}",
    "BF_LIFT": f"{((bf/norm)-1)*100:.0f}",
    "BEST_REGION": top_region, "REGION_PROFIT": f"{region_profit:,.0f}",
    "LOW_HOURS": str(low), "STAFF_SAVINGS": f"{savings:,.0f}",
    "YOUR_NAME": "Data Team"
}

#  reports
print("\n Generating reports...")
templates = Path("templates")
reports = Path("reports")
reports.mkdir(exist_ok=True)

for t in templates.glob("*.md"):
    content = open(t, encoding='utf-8').read()
    for k, v in data.items():
        content = content.replace(f"{{{{{k}}}}}", str(v))
    
    #  region rows
    if "stakeholder" in t.name:
        rows = ""
        for reg, row in df.groupby('region')['profit'].sum().sort_values(ascending=False).items():
            rows += f"| {reg} | ${row:,.0f} |\n"
        content = content.replace("{{REGION_ROWS}}", rows)
    
    out = reports / t.name.replace(".md", f"_{data['DATE']}.md")
    open(out, "w", encoding='utf-8').write(content)
    print(f"   {out.name}")

print(f"\n Done!")