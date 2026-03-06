"""
ANALYSIS - 5 Strategic Questions 
"""

import pandas as pd
import matplotlib.pyplot as plt
import os
from pathlib import Path

# =============================================================================
# SETUP
# =============================================================================
df = pd.read_csv("../../data/processed/master_sales_data.csv")
print(f" Loaded {len(df):,} rows\n")

# CREATE DIRECTORIES FIRST!
Path("reports/figures").mkdir(parents=True, exist_ok=True)
Path("reports/excel").mkdir(parents=True, exist_ok=True)

BF_DATES = ['2023-11-24', '2024-11-29', '2025-11-28']
BF_DISCOUNT = 0.20
REF_DISCOUNT = 0.10
STAFF_COST = 25

 
# STEP 1: Calculate revenue & profit with discounts

print(" Calculating metrics...")

# Base revenue
df['base_revenue'] = df['quantity'] * df['price']

# Black Friday (20% off)
df['order_date'] = pd.to_datetime(df['order_datetime']).dt.date.astype(str)
df['is_black_friday'] = df['order_date'].isin(BF_DATES)
df['revenue_before_bf'] = df['base_revenue']
df.loc[df['is_black_friday'], 'base_revenue'] *= (1 - BF_DISCOUNT)
df['bf_discount'] = df['is_black_friday'] * df['revenue_before_bf'] * BF_DISCOUNT

# Referral discount (10% off first order)
first = df.groupby('buyer_id')['order_datetime'].min().rename('first')
df = df.merge(first, on='buyer_id')
df['is_first'] = df['order_datetime'] == df['first']
df['ref_discount'] = (df['is_referred'] & df['is_first']) * df['base_revenue'] * REF_DISCOUNT

# Final revenue & profit
df['revenue'] = df['base_revenue'] - df['ref_discount']
df['cost'] = df['quantity'] * df['unit_cost']
df['gross_profit'] = df['revenue'] - df['cost']

# Shipping
df['shipping'] = df['revenue'].apply(lambda x: 7.99 if x < 50 else (4.99 if x < 100 else 0))
df['shipping_profit'] = df['shipping'] - 4.99
df['profit'] = df['gross_profit'] + df['shipping_profit']

print(f"   Revenue: ${df['revenue'].sum():,.0f} | Profit: ${df['profit'].sum():,.0f}")

def calculate_profit_metrics(df):
    """
    Calculate revenue, cost, and profit for any dataframe
    Returns dataframe with added columns: revenue, cost, profit
    """
    df = df.copy()  # Don't modify original
    df['revenue'] = df['quantity'] * df['price']
    df['cost'] = df['quantity'] * df['unit_cost']
    df['profit'] = df['revenue'] - df['cost']
    return df

# =============================================================================
# QUESTION 1: Hourly volume (staffing)
# =============================================================================
hourly = df.groupby('order_hour').size()
peak = hourly.nlargest(6)
low = hourly.nsmallest(6)

print(f"\n Q1: Peak hours: {', '.join([f'{h}:00' for h in peak.index])}")
print(f"   Low hours: {', '.join([f'{h}:00' for h in low.index])}")
print(f"    Annual savings if close low hours: ${len(low) * STAFF_COST * 365:,.0f}")

# Chart - NOW DIRECTORIES EXIST
plt.figure(figsize=(10,4))
colors = ['coral' if h in low.index else 'steelblue' for h in hourly.index]
hourly.plot.bar(color=colors)
plt.axhline(hourly.mean(), color='red', linestyle='--', label=f'Avg: {hourly.mean():.0f}')
plt.title('Staffing: Close Overnight Hours, Save $120k')
plt.ylabel('Orders')
plt.legend()
plt.tight_layout()
plt.savefig('reports/figures/staffing.png', dpi=300)
plt.close()

# =============================================================================
# QUESTION 2: Profit by quarter & segment
# =============================================================================
q_profit = df.groupby(['order_quarter', 'customer_segment'])['profit'].mean().unstack()
print(f"\n Q2: Best quarter: Q{q_profit.mean(axis=1).idxmax()} | Best segment: {q_profit.mean(axis=0).idxmax()}")

q_profit.plot.bar(figsize=(10,4))
plt.title('Average Profit by Quarter & Customer Segment')
plt.ylabel('Avg Profit ($)')
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('reports/figures/quarterly_profit.png', dpi=300)
plt.close()

# =============================================================================
# QUESTION 3: Referral program cost
# =============================================================================
ref_cost = df['ref_discount'].sum()
print(f"\n Q3: Referral discounts: ${ref_cost:,.0f} ({ref_cost/df['revenue'].sum()*100:.1f}% of revenue)")

referred = df[df['is_referred']==1]['revenue'].sum() / df[df['is_referred']==1]['buyer_id'].nunique()
non_referred = df[df['is_referred']==0]['revenue'].sum() / df[df['is_referred']==0]['buyer_id'].nunique()
print(f"   Referred customers worth {referred/non_referred:.1f}x more per customer")

# =============================================================================
# QUESTION 4: Black Friday impact
# =============================================================================
bf_avg = df[df['is_black_friday']]['revenue'].mean()
normal_avg = df[~df['is_black_friday']]['revenue'].mean()
lift = (bf_avg/normal_avg - 1) * 100
print(f"\n Q4: Black Friday orders {lift:.0f}% higher (${bf_avg:.0f} vs ${normal_avg:.0f})")
print(f"   BF discounts given: ${df['bf_discount'].sum():,.0f}")

# =============================================================================
# QUESTION 5: Best customer base
# =============================================================================
best_region = df.groupby('region')['profit'].sum().idxmax()
best_segment = df.groupby('customer_segment')['profit'].sum().idxmax()
print(f"\n Q5: Best region: {best_region} | Best segment: {best_segment}")

# =============================================================================
# SAVE  (Excel + Summary)
# =============================================================================
print("\n Saving results...")

with pd.ExcelWriter('reports/excel/analysis_results.xlsx') as w:
    hourly.to_frame('orders').to_excel(w, sheet_name='Hourly')
    q_profit.to_excel(w, sheet_name='Quarterly_Profit')
    df.groupby('region')['profit'].sum().sort_values(ascending=False).to_excel(w, sheet_name='By_Region')
    df.groupby('customer_segment')['profit'].sum().to_excel(w, sheet_name='By_Segment')
    
    # Summary dashboard
    pd.DataFrame({
        'Metric': ['Orders', 'Revenue', 'Profit', 'BF Lift', 'Referral %', 'Best Region', 'Best Segment'],
        'Value': [f"{len(df):,}", f"${df['revenue'].sum():,.0f}", f"${df['profit'].sum():,.0f}", 
                  f"{lift:.0f}%", f"{ref_cost/df['revenue'].sum()*100:.1f}%", best_region, best_segment]
    }).to_excel(w, sheet_name='Summary', index=False)

print(" Done! Check:")
print("   • reports/excel/analysis_results.xlsx")
print("   • reports/figures/staffing.png")
print("   • reports/figures/quarterly_profit.png")