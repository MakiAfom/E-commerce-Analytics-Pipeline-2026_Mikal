"""
SALES DATA CLEANING - FAST VERSION (No more getting stuck!)
This script reads the raw sales data, performs cleaning and feature engineering, and saves both a cleaned CSV and an Excel report with key metrics and breakdowns.
"""

import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path
import sys

# Setup
root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(root))
from src.config import DATA_RAW, DATA_INTERIM, REPORTS_EXCEL

in_file = DATA_RAW / "sales.csv"
out_file = DATA_INTERIM / "sales_cleaned.csv"
excel_file = REPORTS_EXCEL / f"sales_report_{datetime.now():%Y%m%d}.xlsx"

print(f"\n Looking for: {in_file}")
print("\n" + "="*60)
print(" SALES DATA CLEANING - LET'S GO!")
print("="*60)

# Load data
print(f"\n Reading file...")
df = pd.read_csv(in_file)
print(f"   Found {len(df):,} rows with columns: {', '.join(df.columns)}")

print("   Fixing dates...")

# FASTER APPROACH: Use pandas' built-in parser with multiple formats
df['order_datetime'] = pd.to_datetime(df['order_datetime'], errors='coerce')

# If that fails, try Unix timestamps (they're numbers)
if df['order_datetime'].isna().any():
    mask = df['order_datetime'].isna()
    # Check if these are Unix timestamps (all digits)
    unix_mask = df.loc[mask, 'order_datetime'].astype(str).str.isdigit()
    if unix_mask.any():
        df.loc[mask & unix_mask, 'order_datetime'] = pd.to_datetime(
            df.loc[mask & unix_mask, 'order_datetime'].astype(int), unit='s'
        )

print("   Adding date features...")
df['order_date'] = df['order_datetime'].dt.date
df['order_year'] = df['order_datetime'].dt.year.astype('Int16')
df['order_month'] = df['order_datetime'].dt.month.astype('Int8')
df['order_quarter'] = df['order_datetime'].dt.quarter.astype('Int8')
df['order_hour'] = df['order_datetime'].dt.hour.astype('Int8')
df['order_dayofweek'] = df['order_datetime'].dt.day_name()

print("    Fixing quantities...")
original = len(df)
df = df[df['quantity'] > 0].dropna(subset=['quantity', 'buyer_id'])
print(f"   Removed {original - len(df):,} bad rows")

print("    Removing duplicates...")
original = len(df)
df = df.drop_duplicates()
print(f"   Removed {original - len(df):,} duplicates")

print("    Fixing status typos...")
df['order_status'] = df['order_status'].replace({'Deliverred': 'Delivered'})

print("   Trimming text...")
for col in df.select_dtypes(include=['object']).columns:
    df[col] = df[col].astype(str).str.strip()

print(f"\n   Kept {len(df):,} of 376,004 rows ({(len(df)/376004*100):.1f}%)")

# Save
print("\n" + "="*60)
print(" SAVING EVERYTHING")
print("="*60)

out_file.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(out_file, index=False)
print(f" Cleaned data: {out_file}")

# Quick Excel report
print("\n Creating Excel report...")
with pd.ExcelWriter(excel_file, engine='openpyxl') as w:
    df.head(1000).to_excel(w, sheet_name='Clean_Data', index=False)
    
    # Summary
    pd.DataFrame({
        'Metric': ['Orders', 'Units', 'Buyers', 'Products', 'Delivered %'],
        'Value': [f"{len(df):,}", f"{df['quantity'].sum():,}", 
                  f"{df['buyer_id'].nunique():,}", f"{df['sku_id'].nunique():,}",
                  f"{(df['order_status']=='Delivered').mean()*100:.1f}%"]
    }).to_excel(w, sheet_name='Summary', index=False)

print(f" Excel report: {excel_file}")
print("\n" + "="*60)
print(" ALL DONE!")
print("="*60)