"""
VISUALIZATION - 5 charts for the report
"""

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Load & calculate
df = pd.read_csv(Path(__file__).parent.parent.parent / "data/processed/master_sales_data.csv")
df['revenue'] = df['quantity'] * df['price']
df['profit'] = df['revenue'] - df['quantity'] * df['unit_cost']
out = Path("reports/figures")
out.mkdir(parents=True, exist_ok=True)

print(f"\n {len(df):,} rows | Revenue: ${df['revenue'].sum():,.0f} | Profit: ${df['profit'].sum():,.0f}")

# 1. Staffing
hourly = df.groupby('order_hour').size()
low = hourly.nsmallest(6).index
hourly.plot.bar(figsize=(10,4), color=['coral' if h in low else 'steelblue' for h in hourly.index])
plt.axhline(hourly.mean(), color='red', ls='--')
plt.title(f'Staffing: Save ${len(low)*25*365:,}/year')
plt.tight_layout()
plt.savefig(out/'1_staffing.png', dpi=300); plt.close()
print("   1_staffing.png")

# 2. Quarterly profit
df.groupby(['order_quarter', 'customer_segment'])['profit'].mean().unstack().plot.bar(figsize=(10,4))
plt.title('Profit by Quarter & Segment')
plt.tight_layout()
plt.savefig(out/'2_quarterly.png', dpi=300); plt.close()
print("   2_quarterly.png")

# 3. Black Friday
bf, norm = df[df['is_black_friday']]['revenue'].mean(), df[~df['is_black_friday']]['revenue'].mean()
plt.bar(['Normal', 'BF'], [norm, bf], color=['steelblue', 'coral'])
plt.title(f'BF: {((bf/norm)-1)*100:.0f}% Higher')
for i, v in enumerate([norm, bf]): plt.text(i, v+1, f'${v:.0f}', ha='center')
plt.tight_layout()
plt.savefig(out/'3_black_friday.png', dpi=300); plt.close()
print("   3_black_friday.png")

# 4. Top regions
df.groupby('region')['profit'].sum().sort_values(ascending=False).head(5).plot.bar(color='steelblue')
plt.title('Top 5 Regions by Profit')
plt.tight_layout()
plt.savefig(out/'4_top_regions.png', dpi=300); plt.close()
print("   4_top_regions.png")

# 5. Referral impact
ref, non = df[df['is_referred']==1]['revenue'].mean(), df[df['is_referred']==0]['revenue'].mean()
plt.bar(['Non-Referred', 'Referred'], [non, ref], color=['steelblue', 'green'])
plt.title(f'Referred: {((ref/non)-1)*100:.0f}% More')
for i, v in enumerate([non, ref]): plt.text(i, v+1, f'${v:.0f}', ha='center')
plt.tight_layout()
plt.savefig(out/'5_referral.png', dpi=300); plt.close()
print("   5_referral.png")

print(f"\n 5 charts saved to {out}")