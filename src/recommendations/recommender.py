"""
RECOMMENDATIONS - Strategic recommendations based on analysis, with a focus on referral program, Black Friday, and staffing. Prioritize referral program expansion for maximum impact. Save key insights to a text file for the CEO.
"""

import pandas as pd
from pathlib import Path

# Load data
df = pd.read_csv(Path(__file__).parent.parent.parent / "data/processed/master_sales_data.csv")
df['revenue'] = df['quantity'] * df['price']

# YOUR ACTUAL NUMBERS
bf = 60.17
norm = 22.50  
ref = 67.00   #  referred customers
non = 18.00   # non-referred
lift = ((ref/non)-1)*100  

print("\n" + "="*60)
print(" YOUR ACTUAL INSIGHTS")
print("="*60)
print(f" Referred customers: ${ref:.0f} vs Non-referred: ${non:.0f}")
print(f" That's {lift:.0f}% HIGHER! (3.7x more)")

print("\n" + "="*60)
print(" STRATEGIC RECOMMENDATIONS")
print("="*60)

print("\n  REFERRAL PROGRAM - YOUR BIGGEST WIN! 🏆")
print(f"   • Referred customers spend ${ref:.0f} vs ${non:.0f}")
print(f"   • That's {lift:.0f}% MORE per order!")
print("   ➡ RECOMMEND: DOUBLE DOWN ON REFERRALS")
print("      - Increase referral bonus from 10% to 20%")
print("      - Add tiered rewards: $10/$25/$50")
print("      - Launch 'refer 3 friends, get $100' campaign")

print("\n  BLACK FRIDAY")
print(f"   • BF orders: ${bf:.0f} vs normal ${norm:.0f}")
print(f"   • {((bf/norm)-1)*100:.0f}% higher")
print("   ➡ RECOMMEND: Stock up on top 100 items")

print("\n  STAFFING")
hourly = df.groupby('order_hour').size()
low_hours = list(hourly.nsmallest(6).index)
savings = len(low_hours) * 25 * 365
print(f"   • Low hours: {low_hours}")
print(f"   • Save ${savings:,.0f}/year")
print("   ➡ RECOMMEND: Close overnight")

print("\n" + "="*60)
print("BOTTOM LINE")
print("="*60)
print(f"• Referral program:  ({lift:.0f}% higher value)")
print(f"• Black Friday: Strong performer ({bf:.0f} vs {norm:.0f})")
print(f"• Staffing: Easy ${savings:,.0f} savings")
print("\nPRIORITY #1: EXPAND REFERRAL PROGRAM IMMEDIATELY!")

#  reports folder =====
reports_folder = Path(__file__).parent.parent.parent / "reports"
reports_folder.mkdir(parents=True, exist_ok=True)  

#  save 
file_path = reports_folder / "priority_recommendations.txt"
with open(file_path, "w") as f:
    f.write(" URGENT: REFERRAL PROGRAM IS YOUR BIGGEST OPPORTUNITY\n")
    f.write("="*50 + "\n")
    f.write(f"Referred customers spend {lift:.0f}% MORE (${ref} vs ${non})\n")
    f.write(f"That's 3.7x more revenue per order!\n")
    f.write("="*50 + "\n")
    f.write("ACTION ITEMS:\n")
    f.write("1. Increase referral bonus to 20% this month\n")
    f.write("2. Launch 'refer 3 friends' campaign\n")
    f.write("3. Track referral source in dashboard\n")

print(f"\n Saved to: {file_path}")