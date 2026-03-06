"""
PRODUCT DATA CLEANING - 
This script reads all 12 product CSV files, cleans and standardizes the data, performs feature engineering, and saves a cleaned master CSV and an Excel report with key metrics and breakdowns.
"""

import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path
import sys
import glob

# Setup
root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(root))
from src.config import DATA_RAW, DATA_INTERIM, REPORTS_EXCEL

print("\n" + "="*60)
print(" PRODUCT DATA CLEANING")
print("="*60)

# ============================================================================
# LOAD ALL 12 CsV 
# ============================================================================
print("\n Loading files...")
files = list((DATA_RAW / "products").glob("*.csv"))
df = pd.concat([pd.read_csv(f).assign(source=f.name) for f in files], ignore_index=True)
print(f"    {len(df):,} rows from {len(files)} files")

# ============================================================================
# CLEAN EVERYTHING 
# ============================================================================
print("\n Cleaning...")

def clean_all(df):
    """One function to clean them all"""
    df = df.copy()
    original = len(df)
    
    # Text fields
    for col in ['category_name', 'subcategory_name', 'vendor']:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.upper().replace(['NAN', 'NULL', ''], 'UNKNOWN')
    
    # Booleans (handles TRUE/T/YES/1/ACTIVE)
    for col, new_col in [('currently_active_vendor', 'vendor_active'), ('active_product', 'product_active')]:
        if col in df.columns:
            df[new_col] = df[col].astype(str).str.upper().str.strip().isin(['TRUE', 'T', 'YES', '1', 'ACTIVE'])
    
    # Product numbers (fix scientific notation)
    df['product_num'] = df['product_num'].astype(str).str.replace(r'[\$,]', '', regex=True)
    sci_mask = df['product_num'].str.contains('E\+', na=False)
    df.loc[sci_mask, 'product_num'] = df.loc[sci_mask, 'product_num'].apply(lambda x: str(int(float(x))))
    
    # Price
    df['price'] = pd.to_numeric(df['price'].astype(str).str.replace(r'[\$,]', '', regex=True), errors='coerce')
    df['price'] = df['price'].clip(0).fillna(df.groupby('category_name')['price'].transform('median'))
    
    # Margin
    df['margin'] = pd.to_numeric(df['profit_margin'].astype(str).str.replace('%', ''), errors='coerce')
    if df['margin'].mean() > 1: df['margin'] /= 100
    df['margin'] = df['margin'].clip(-0.5, 0.9)
    
    # Stock
    df['stock'] = pd.to_numeric(df['current_stock'], errors='coerce').fillna(0).clip(0)
    df['stock_status'] = pd.cut(df['stock'], bins=[-1,0,20,50,np.inf], labels=['Out','Low','Medium','High'])
    
    # Remove duplicates (keep active)
    df = df.sort_values('product_active', ascending=False).drop_duplicates('product_num', keep='first')
    
    # New features
    df['unit_cost'] = df['price'] * (1 - df['margin'])
    df['unit_profit'] = df['price'] - df['unit_cost']
    df['inventory_value'] = df['price'] * df['stock']
    df['profit_potential'] = df['unit_profit'] * df['stock']
    
    df['price_tier'] = pd.cut(df['price'], bins=[0,10,25,50,100,np.inf], labels=['Budget','Economy','Standard','Premium','Luxury'])
    df['margin_tier'] = pd.cut(df['margin'], bins=[-1,0,0.2,0.4,0.6,1], labels=['Loss','Low','Medium','High','Very High'])
    
    print(f"    Kept {len(df):,} of {original:,} rows ({(len(df)/original*100):.1f}%)")
    return df

df_clean = clean_all(df)

# ============================================================================
# SAVE OUTPUTS 
# ============================================================================
print("\n" + "="*60)
print(" SAVING")
print("="*60)

# Create dirs
DATA_INTERIM.mkdir(parents=True, exist_ok=True)
REPORTS_EXCEL.mkdir(parents=True, exist_ok=True)

# Save CSV
csv_file = DATA_INTERIM / "products_cleaned.csv"
df_clean.to_csv(csv_file, index=False)
print(f" CSV: {csv_file}")

# Excel report
excel_file = REPORTS_EXCEL / f"products_{datetime.now():%Y%m%d}.xlsx"
with pd.ExcelWriter(excel_file, engine='openpyxl') as w:
    print("\n Excel sheets:")
    df_clean.head(1000).to_excel(w, sheet_name='Data', index=False); print("  • Data")
    
    pd.DataFrame({
        'Metric': ['Products','Active','Categories','Avg Price','Avg Margin','Inventory'],
        'Value': [f"{len(df_clean):,}", f"{df_clean['product_active'].sum():,}", 
                  f"{df_clean['category_name'].nunique()}", f"${df_clean['price'].mean():.2f}",
                  f"{df_clean['margin'].mean():.1%}", f"${df_clean['inventory_value'].sum():,.0f}"]
    }).to_excel(w, sheet_name='Summary', index=False); print("  • Summary")
    
    df_clean.groupby('category_name').agg(Products=('product_num','count'), 
        Avg_Price=('price','mean'), Avg_Margin=('margin','mean'), 
        Inventory=('inventory_value','sum')).round(2).to_excel(w, sheet_name='By_Category'); print("  • By Category")
    
    df_clean['stock_status'].value_counts().to_excel(w, sheet_name='Stock'); print("  • Stock")

print(f"\n Excel: {excel_file}")

# ============================================================================
# QUICK SUMMARY 
# ============================================================================
print("\n" + "="*60)
print(" SUMMARY")
print("="*60)
print(f"\n Products: {len(df_clean):,} total, {df_clean['product_active'].sum():,} active")
print(f" Categories: {df_clean['category_name'].nunique()}")
print(f"Avg price: ${df_clean['price'].mean():.2f} | Avg margin: {df_clean['margin'].mean():.1%}")
print(f" Inventory: ${df_clean['inventory_value'].sum():,.0f}")
print("\nStock:")
for s,c in df_clean['stock_status'].value_counts().items():
    print(f"   • {s}: {c:,} ({c/len(df_clean)*100:.1f}%)")

print("\n" + "="*60)
print("DONE!")
print("="*60)