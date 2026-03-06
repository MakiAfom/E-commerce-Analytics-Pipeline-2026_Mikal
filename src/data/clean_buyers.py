"""
Buyer Data Cleaning
Creates cleaned data + Excel report with multiple sheets
"""

import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

# Import from config
from src.config import DATA_RAW, DATA_INTERIM, REPORTS_EXCEL, CONFIG

# Build paths
INPUT_FILE = DATA_RAW / "buyer.csv"
OUTPUT_FILE = DATA_INTERIM / "buyers_cleaned.csv"
EXCEL_REPORT = REPORTS_EXCEL / f"buyer_report_{datetime.now().strftime('%Y%m%d')}.xlsx"

print(f" Input: {INPUT_FILE}")
print(f" Output: {OUTPUT_FILE}")
print(f" Excel Report: {EXCEL_REPORT}")

# Text columns to clean
TEXT_COLS = [
    'customer_group', 'customer_segment', 'preferred_subcategory',
    'subcategory_pool', 'preferred_channel', 'preferred_payment',
    'region', 'state', 'timezone'
]

def parse_dates(date_str):
    
    if pd.isna(date_str): 
        return pd.NaT
    date_str = str(date_str).strip()
    
    # Unix timestamp
    if date_str.isdigit() and len(date_str) > 8:
        try: 
            return pd.to_datetime(int(date_str), unit='s')
        except: 
            return pd.NaT
    
    # Try common formats
    for fmt in ['%m/%d/%Y', '%Y-%m-%d', '%d-%b-%y', '%m/%d/%y']:
        try: 
            return pd.to_datetime(date_str, format=fmt)
        except: 
            continue
    
    
    try: 
        return pd.to_datetime(date_str)
    except: 
        return pd.NaT

def clean_buyer_data(df):
   
    original_rows = len(df)
    
    print("\n   Step 1: Cleaning buyer_id...")
    df['buyer_id'] = df['buyer_id'].astype(str).str.strip()
    df = df.dropna(subset=['buyer_id'])
    df = df.drop_duplicates(subset=['buyer_id'])
    
    print("   Step 2: Cleaning signup_date...")
    if 'signup_date' in df.columns:
        df['signup_date'] = df['signup_date'].apply(parse_dates)
        
        # Add date features
        df['signup_year'] = df['signup_date'].dt.year.astype('Int16')
        df['signup_month'] = df['signup_date'].dt.month.astype('Int8')
        df['signup_quarter'] = df['signup_date'].dt.quarter.astype('Int8')
        df['signup_dayofweek'] = df['signup_date'].dt.day_name()
        df['signup_weekend'] = df['signup_dayofweek'].isin(['Saturday', 'Sunday'])
    
    print("   Step 3: Cleaning text fields...")
    for col in TEXT_COLS:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
            df[col] = df[col].replace(['nan', 'NaN', 'None', ''], np.nan)
    
    print("   Step 4: Cleaning numeric fields...")
    if 'is_active_buyer' in df.columns:
        df['is_active_buyer'] = pd.to_numeric(df['is_active_buyer'], errors='coerce').fillna(0).astype('int8')
    
    if 'is_referred' in df.columns:
        df['is_referred'] = pd.to_numeric(df['is_referred'], errors='coerce').fillna(0).astype('int8')
    
    if 'wishlist_size' in df.columns:
        df['wishlist_size'] = pd.to_numeric(df['wishlist_size'], errors='coerce')
        median_wishlist = df['wishlist_size'].median()
        df['wishlist_size'] = df['wishlist_size'].fillna(median_wishlist).astype('Int32')
        
        # Create categories
        df['wishlist_category'] = pd.cut(
            df['wishlist_size'],
            bins=[0, 5, 15, 100],
            labels=['Low', 'Medium', 'High'],
            include_lowest=True
        )
    
    print("   Step 5: Removing duplicates...")
    df = df.drop_duplicates()
    
    return df

def create_excel_report(df, filename):
    
    
    print("\n Creating Excel report...")
    
  
    summary_data = {
        'Metric': [
            'Total Buyers',
            'Active Buyers',
            'Active %',
            'Referred Buyers',
            'Referred %',
            'Missing Signup Dates',
            'Unique Regions',
            'Unique States',
            'Avg Wishlist Size',
            'Median Wishlist Size'
        ],
        'Value': [
            f"{len(df):,}",
            f"{df['is_active_buyer'].sum():,}",
            f"{(df['is_active_buyer'].sum()/len(df)*100):.1f}%",
            f"{df['is_referred'].sum():,}",
            f"{(df['is_referred'].sum()/len(df)*100):.1f}%",
            f"{df['signup_date'].isna().sum():,}",
            f"{df['region'].nunique()}",
            f"{df['state'].nunique()}",
            f"{df['wishlist_size'].mean():.1f}",
            f"{df['wishlist_size'].median():.0f}"
        ]
    }
    summary_df = pd.DataFrame(summary_data)
    
   
    segment_df = df.groupby('customer_segment').agg({
        'buyer_id': 'count',
        'is_active_buyer': 'sum',
        'is_referred': 'sum',
        'wishlist_size': 'mean'
    }).round(1).reset_index()
    segment_df.columns = ['Segment', 'Buyers', 'Active', 'Referred', 'Avg Wishlist']
    segment_df['Active %'] = (segment_df['Active'] / segment_df['Buyers'] * 100).round(1)
    
    # This is  region breakdown
    region_df = df.groupby('region').agg({
        'buyer_id': 'count',
        'is_active_buyer': 'sum',
        'wishlist_size': 'mean'
    }).round(1).reset_index()
    region_df.columns = ['Region', 'Buyers', 'Active', 'Avg Wishlist']
    region_df['Active %'] = (region_df['Active'] / region_df['Buyers'] * 100).round(1)
    
    # This is the wishlist distribution
    wishlist_df = df['wishlist_category'].value_counts().reset_index()
    wishlist_df.columns = ['Category', 'Count']
    wishlist_df['Percentage'] = (wishlist_df['Count'] / len(df) * 100).round(1)
    
    # This code Is to Create Excel file
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        # Sheet 1: Cleaned Data (first 1000 rows for preview)
        print("  • Writing Cleaned Data sheet...")
        df.head(1000).to_excel(writer, sheet_name='Cleaned_Data', index=False)
        
        # Sheet 2: Summary Statistics
        print("  • Writing Summary sheet...")
        summary_df.to_excel(writer, sheet_name='Summary', index=False)
        
        # Sheet 3: Segment Breakdown
        print("  • Writing Segment Breakdown sheet...")
        segment_df.to_excel(writer, sheet_name='By_Segment', index=False)
        
        # Sheet 4: Region Breakdown
        print("  • Writing Region Breakdown sheet...")
        region_df.to_excel(writer, sheet_name='By_Region', index=False)
        
        # Sheet 5: Wishlist Distribution
        print("  • Writing Wishlist Distribution sheet...")
        wishlist_df.to_excel(writer, sheet_name='Wishlist_Distribution', index=False)
        
        # Auto-adjust column widths
        for sheet_name in writer.sheets:
            worksheet = writer.sheets[sheet_name]
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                worksheet.column_dimensions[column_letter].width = min(max_length + 2, 50)
    
    print(f"    Excel report saved to: {filename}")

def main():
    print("\n" + "="*80)
    print("BUYER DATA CLEANING & EXCEL REPORT")
    print("="*80)
    
    # Check if input file exists
    if not INPUT_FILE.exists():
        print(f" ERROR: Input file not found at {INPUT_FILE}")
        print("\nChecking data/raw folder:")
        if DATA_RAW.exists():
            files = list(DATA_RAW.glob("*.csv"))
            if files:
                print("Available CSV files:")
                for f in files:
                    print(f"   - {f.name}")
            else:
                print("   No CSV files found!")
        return
    
    # Load data
    print(f"\n Loading {INPUT_FILE}...")
    try:
        df = pd.read_csv(INPUT_FILE)
        print(f"    Loaded {len(df):,} rows")
        print(f"    Columns: {', '.join(df.columns)}")
    except Exception as e:
        print(f"    Error loading file: {e}")
        return
    
    # Clean
    print("\n Cleaning data...")
    df_clean = clean_buyer_data(df)
    print(f"\n    Kept {len(df_clean):,} of {len(df):,} rows ({(len(df_clean)/len(df)*100):.1f}% retained)")
    
    # Save cleaned data
    line = "=" * 80
    print(f"\n{line}\n SAVING OUTPUTS\n{line}")
    
    # Create directories
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    REPORTS_EXCEL.mkdir(parents=True, exist_ok=True)
    
    # Save cleaned data CSV
    df_clean.to_csv(OUTPUT_FILE, index=False)
    print(f"    CSV saved: {OUTPUT_FILE}")
    
    # Create Excel report
    create_excel_report(df_clean, EXCEL_REPORT)
    
    # Show summary
    print("\n QUICK SUMMARY:")
    print(f"   • Active buyers: {df_clean['is_active_buyer'].sum():,} ({(df_clean['is_active_buyer'].sum()/len(df_clean)*100):.1f}%)")
    print(f"   • Referred buyers: {df_clean['is_referred'].sum():,} ({(df_clean['is_referred'].sum()/len(df_clean)*100):.1f}%)")
    print(f"   • Avg wishlist size: {df_clean['wishlist_size'].mean():.1f}")
    print(f"   • Regions: {df_clean['region'].nunique()}")
    
    print("\n" + "="*80)
    print(" ALL DONE!")
    print("="*80)
    print(f"\n Files created:")
    print(f"    {OUTPUT_FILE}")
    print(f"    {EXCEL_REPORT}")

if __name__ == "__main__":
    main()