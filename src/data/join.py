"""
Master join + Summary Sheet - 
This script reads the cleaned sales, products, and buyers data, performs a master join to create a comprehensive dataset, and generates an Excel report with a summary sheet and key breakdowns. It also prints a quick summary to the console.
"""

import pandas as pd
from pathlib import Path
import sys

# Setup
root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(root))
from src.config import CLEANED_FILES, MASTER_DATA, REPORTS_EXCEL, CONFIG

print("\n" + "="*60)
print(" JOINING ")
print("="*60)

# Load & join
s,p,b = [pd.read_csv(f) for f in [CLEANED_FILES['sales'], CLEANED_FILES['products'], CLEANED_FILES['buyers']]]
s['product_num'] = s['sku_id'].str.split('-').str[-1]
df = s.merge(p, on='product_num').merge(b, on='buyer_id')

# Black Friday flag
df['order_date'] = pd.to_datetime(df['order_datetime']).dt.date.astype(str)
df['is_black_friday'] = df['order_date'].isin(CONFIG['black_friday_dates'])

print(f"\n Master: {len(df):,} rows, {df['is_black_friday'].sum():,} Black Friday orders")

# Save master CSV
MASTER_DATA.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(MASTER_DATA, index=False)
print(f" CSV: {MASTER_DATA}")

# ============================================================================
# EXCEL REPORT WITH SUMMARY SHEET
# ============================================================================
print("\n Building Excel report...")

with pd.ExcelWriter(REPORTS_EXCEL / "master_analysis.xlsx", engine='openpyxl') as w:
    
    # Sheet 1: SUMMARY - All key metrics in one place
    print("  • Summary sheet")
    summary_data = {
        'Metric': [
            'Total Orders',
            'Total Revenue',
            'Total Profit',
            'Avg Order Value',
            'Avg Profit per Order',
            'Unique Buyers',
            'Unique Products',
            'Black Friday Orders',
            'Black Friday Revenue',
            'Black Friday % of Revenue',
            'Best Selling Category',
            'Most Profitable Category',
            'Peak Shopping Hour',
            'Data Date Range'
        ],
        'Value': [
            f"{len(df):,}",
            f"${df['price'] .sum():,.0f}",
            f"${df['unit_profit'].sum():,.0f}",
            f"${df['price'].mean():.2f}",
            f"${df['unit_profit'].mean():.2f}",
            f"{df['buyer_id'].nunique():,}",
            f"{df['product_num'].nunique():,}",
            f"{df['is_black_friday'].sum():,}",
            f"${df[df['is_black_friday']]['price'].sum():,.0f}" if df['is_black_friday'].any() else "$0",
            f"{(df[df['is_black_friday']]['price'].sum()/df['price'].sum()*100):.1f}%" if df['is_black_friday'].any() else "0%",
            df.groupby('category_name')['order_id'].count().idxmax(),
            df.groupby('category_name')['unit_profit'].sum().idxmax(),
            f"{df.groupby('order_hour').size().idxmax()}:00",
            f"{df['order_datetime'].min()} to {df['order_datetime'].max()}"
        ]
    }
    pd.DataFrame(summary_data).to_excel(w, sheet_name='Summary', index=False)
    
    # Sheet 2: Hourly volume
    print("  • Hourly analysis")
    df.groupby('order_hour').size().rename('orders').to_excel(w, sheet_name='Hourly_Volume')
    
    # Sheet 3: Quarterly profit by segment
    print("  • Quarterly profit")
    df.groupby(['order_quarter', 'customer_segment'])['unit_profit'].mean().round(2).to_excel(w, sheet_name='Quarterly_Profit')
    
    # Sheet 4: Black Friday vs Regular
    print("  • Black Friday comparison")
    comparison = df.groupby('is_black_friday').agg({
        'order_id': 'count',
        'price': 'sum',
        'unit_profit': ['mean', 'sum']
    }).round(2)
    comparison.columns = ['Orders', 'Revenue', 'Avg Profit', 'Total Profit']
    comparison.to_excel(w, sheet_name='BF_vs_Regular')

print(f" Excel: {REPORTS_EXCEL / 'master_analysis.xlsx'}")

# Print quick summary to console
print("\n" + "="*60)
print(" QUICK NUMBERS")
print("="*60)
print(f" Total Revenue: ${df['price'].sum():,.0f}")
print(f" Total Profit: ${df['unit_profit'].sum():,.0f}")
print(f" Avg Order: ${df['price'].mean():.2f}")
print(f"  Top Category: {df.groupby('category_name')['order_id'].count().idxmax()}")
print("="*60)